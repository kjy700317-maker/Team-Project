-- 봉수 ERD v4 — 대기능 1 (긴장도 지수)  기준·데이터·보조 테이블 DDL
-- 설정 테이블(요소·기준값·단계)·결과 테이블은 팀 조율 후 별도 이슈에서 추가 (#7 범위 밖)
--
-- 적용 순서: 참조당하는 쪽(기준) → 데이터 → 보조.  SQLite는 연결마다 PRAGMA foreign_keys=ON 필요.
-- 실행: utils/build_erd.py 가 이 파일을 읽어 실행한 뒤 1단계 표(사건·수치·참여국·코드)에서 적재.

PRAGMA foreign_keys = ON;

-- ───────────────── ① 기준 테이블 (2개) ─────────────────
CREATE TABLE 국가 (
    국가코드   TEXT PRIMARY KEY,                       -- ISO3 + KOR_USA·UN·NATO·EU·MUL
    이름       TEXT NOT NULL,
    구분       TEXT,                                   -- 주요 국가 / 연합 / 국제기구 / 다자 / 국가 …
    관심국여부 TEXT NOT NULL DEFAULT 'N'
               CHECK (관심국여부 IN ('Y', 'N'))        -- Y = 한·북·미·중·일·러·대만
);

CREATE TABLE 날짜 (
    날짜 TEXT    PRIMARY KEY,                          -- 'YYYY-MM-DD', 1945-07-16 ~
    연도 INTEGER NOT NULL,
    연월 TEXT    NOT NULL,                             -- 'YYYY-MM'
    월   INTEGER NOT NULL,
    분기 INTEGER NOT NULL
);

-- ───────────────── ② 데이터 테이블 (3개) ─────────────────
-- 사건_일단위: 시작일이 있는 사건. 사용여부 Y · 주체국이 관심국(주요 국가·연합·다자·국제기구)인 행만.
CREATE TABLE 사건_일단위 (
    사건ID       TEXT PRIMARY KEY,                     -- A2-0001
    카테고리코드 TEXT NOT NULL,                        -- 사건ID 앞자리 (A2 등)
    시작일       TEXT NOT NULL REFERENCES 날짜(날짜),
    종료일       TEXT,
    연도         INTEGER NOT NULL,
    주체국       TEXT NOT NULL REFERENCES 국가(국가코드),
    대상국       TEXT          REFERENCES 국가(국가코드),  -- NULL 허용
    사건명       TEXT,
    요약         TEXT,
    비고         TEXT,
    사용여부     TEXT NOT NULL CHECK (사용여부 = 'Y'),  -- N 행은 DB가 거부
    제외사유     TEXT
);

-- 사건_연단위: 시작일이 없고 연도만 있는 사건 (A4 일부·A5·B2).
CREATE TABLE 사건_연단위 (
    사건ID       TEXT PRIMARY KEY,
    카테고리코드 TEXT NOT NULL,
    시작일       TEXT,                                 -- 항상 NULL
    종료일       TEXT,
    연도         INTEGER NOT NULL,
    주체국       TEXT NOT NULL REFERENCES 국가(국가코드),
    대상국       TEXT          REFERENCES 국가(국가코드),
    사건명       TEXT,
    요약         TEXT,
    비고         TEXT,
    사용여부     TEXT NOT NULL CHECK (사용여부 = 'Y'),
    제외사유     TEXT
);

-- 지표값: D·F 지표형 데이터. 값은 표준 단위(공통_단위.표준_단위) 기준.
CREATE TABLE 지표값 (
    국가코드 TEXT    NOT NULL REFERENCES 국가(국가코드),
    지표명   TEXT    NOT NULL,                         -- 국민총소득 등
    세부항목 TEXT    NOT NULL DEFAULT '합계',
    연도     INTEGER NOT NULL CHECK (연도 <= 2025),
    값       REAL,                                     -- NULL = 원자료 없음
    단위     TEXT,
    출처파트 TEXT,                                     -- D1 / D3 / F1 / F4
    PRIMARY KEY (국가코드, 지표명, 세부항목, 연도)
);

-- ───────────────── ③ 보조 테이블 ─────────────────
-- 사건_목록: 사건ID가 일단위·연단위 어느 표에 들어갔는지. (SQLite FK는 표 하나만 가리킬 수 있어
--            사건_참여국이 두 사건 표의 사건을 함께 참조하도록 두는 작은 색인)
CREATE TABLE 사건_목록 (
    사건ID TEXT PRIMARY KEY,
    적재표 TEXT NOT NULL CHECK (적재표 IN ('사건_일단위', '사건_연단위'))
);

-- 사건_참여국: 주체국 MUL(다자·양자) 사건의 참여국. 공통_참여국.csv
CREATE TABLE 사건_참여국 (
    사건ID TEXT NOT NULL REFERENCES 사건_목록(사건ID),
    참여국 TEXT NOT NULL REFERENCES 국가(국가코드),
    PRIMARY KEY (사건ID, 참여국)
);


-- 사건 상세 13개 (ERD v4 사건 상세 그림 기준) — 파일마다 열이 달라 build_erd.py가 동적으로 만든다.
--   열 = 전처리 CSV 열 그대로 (공통 11열만 제외, 열 이름에 단위 없음, 단위는 공통_단위.csv)
--   사건ID TEXT PRIMARY KEY REFERENCES 사건_일단위(사건ID)   ← A2·A6·A7·B1·B3·B4_핵태세·B4_공약문구·C1~C5
--   사건ID TEXT PRIMARY KEY REFERENCES 사건_연단위(사건ID)   ← B2_무기이전
--   공통_단위에 등록된 수치 열은 REAL, 나머지는 TEXT
--   A1·A3·A4·A5 는 상세 표 없음

-- 인덱스
CREATE INDEX ix_사건일_시작일 ON 사건_일단위(시작일);
CREATE INDEX ix_사건일_주체국 ON 사건_일단위(주체국, 시작일);
CREATE INDEX ix_사건일_카테고리 ON 사건_일단위(카테고리코드);
CREATE INDEX ix_사건연_연도   ON 사건_연단위(연도, 주체국);
CREATE INDEX ix_지표값_지표   ON 지표값(지표명, 국가코드, 연도);
