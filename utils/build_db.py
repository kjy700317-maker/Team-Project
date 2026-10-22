"""
봉수 통합 DB 만들기 (SQLite)  — v1.2 (2026-10-20)

data/processed/ 아래의 전처리 CSV를 모두 읽어서 SQLite DB 하나로 합칩니다.

사용법 (Team-Project 폴더에서):
    python utils/build_db.py
    python utils/build_db.py --src data/processed --out data/bongsu.db

만들어지는 테이블
    사건          사건 파일의 공통 열을 세로로 합친 표 (1행 = 사건 1건)
    수치          수치 파일을 세로로 합친 표 (1행 = 국가 × 지표 × 연도)
                  - 사건표 모양으로 된 연 단위 수치(F1 등: 주체국·항목·연도·값)도 자동으로 들어감
    참여국        공통_참여국.csv
    단위          공통_단위.csv  (키: 파일명 + 컬럼명 + 지표). 값은 표준_단위 기준
    코드          공통_국가코드.csv (주요국·연합·기구·MUL + ISO3 전체) = 허용 코드 목록
    파일_<파일명>  각 파일 전체 (파일마다 다른 고유 열 보존)
    파일목록      어떤 파일이 어떤 표로 들어갔는지
만들어지는 뷰
    수치_단위     수치 × 단위 join → 원본단위값 = 값 ÷ 환산_배수 (값 자체가 표준 단위)

DB는 실행할 때마다 새로 만듭니다 (기존 파일 덮어씀).
"""

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

# ── 규칙 (전처리README v1.2 기준) ─────────────────────────
사건_공통열 = [
    "사건ID", "시작일", "종료일", "연도", "종료연도",
    "주체국", "대상국", "사건명", "요약", "비고", "사용여부", "제외사유",
]
수치_공통열 = ["국가", "지표", "연도", "값"]
기본코드 = {"KOR", "PRK", "USA", "CHN", "JPN", "RUS", "TWN",
            "KOR_USA", "UN", "NATO", "EU", "MUL"}
공통파일 = {"공통_참여국": "참여국", "공통_단위": "단위", "공통_국가코드": "국가코드"}
# 통합 사건표에 넣지 않는 파일. 파일_<이름> 표로는 저장되므로 사건ID로 join해서 씀.
#   집계·파생: 원천 파일에서 다시 만들 수 있는 것
#   부속표  : 원천 사건과 같은 사건ID를 쓰는 상세·출처·대응 표 (통합하면 사건ID가 겹침)
제외파일 = {
    "A1_핵실험_CSV",                 # 주체국×연도 집계 (결정 5: 일단위 파일을 원천으로)
    "A5_미_전력자산_전개_일단위_CSV",  # A5_미_전력자산_전개_CSV 의 일별 전개
    "B4_확장억제_공약문구",           # B4_핵태세확장억제_사건 의 상세
    "E1_UN표결_대응표",              # E1_UN표결_사건 의 문서 링크 대응
    "C3_출처",                       # C3_동맹협의_사건 의 출처 목록
}


def read_csv(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "cp949"):
        try:
            df = pd.read_csv(path, dtype=str, encoding=enc, keep_default_na=False)
            df.columns = [c.strip() for c in df.columns]
            return df.replace({"": None})
        except UnicodeDecodeError:
            continue
    raise ValueError(f"인코딩을 알 수 없음: {path}")


def 파일종류(df: pd.DataFrame) -> str:
    cols = set(df.columns)
    if set(수치_공통열) <= cols:
        return "수치"
    if "사건ID" in cols and "시작일" in cols:
        return "사건"
    if {"주체국", "항목", "연도", "값"} <= cols:       # F1처럼 사건표 모양의 연 단위 수치
        return "수치(변환)"
    return "기타"


def to_int(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").astype("Int64")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/processed")
    ap.add_argument("--out", default="data/bongsu.db")
    args = ap.parse_args()

    src, out = Path(args.src), Path(args.out)
    if not src.exists():
        raise SystemExit(f"폴더가 없습니다: {src.resolve()}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    con = sqlite3.connect(out)

    사건들, 수치들, 목록, 파일단위 = [], [], [], []
    공통 = {}

    # 공통 파일은 어느 폴더에 있어도 찾음 (단, 'C2_공통_참여국' 같은 카테고리별 사본은 무시)
    for path in sorted(src.rglob("*.csv")):
        이름 = path.stem
        if 이름 in 공통파일:
            공통[공통파일[이름]] = read_csv(path)
            목록.append((이름, "", 공통파일[이름], len(공통[공통파일[이름]])))

    for path in sorted(src.rglob("*.csv")):
        이름 = path.stem
        if 이름 in 공통파일 or 이름.endswith("_공통_참여국"):
            continue
        df = read_csv(path)
        카테고리 = 이름.split("_")[0]
        종류 = 파일종류(df)
        df.to_sql(f"파일_{이름}", con, index=False)

        # 파일 안 단위 열 수집 (결정 3: 허용, 단 단위표와 대조)
        for c in [c for c in df.columns if c == "단위" or c.startswith("단위_")]:
            vals = df[c].dropna().unique()
            for v in vals:
                파일단위.append((이름, c, v))

        if 이름 in 제외파일:
            종류 = "제외"
        elif 종류 == "사건":
            t = df.reindex(columns=사건_공통열)
            t.insert(1, "카테고리", 카테고리)
            t.insert(2, "파일명", 이름)
            사건들.append(t)
        elif 종류 == "수치":
            t = df[수치_공통열].copy()
            t.insert(0, "카테고리", 카테고리); t.insert(1, "파일명", 이름)
            수치들.append(t)
        elif 종류 == "수치(변환)":
            t = pd.DataFrame({
                "카테고리": 카테고리, "파일명": 이름,
                "국가": df["주체국"],
                "지표": df["항목"] if "세부항목" not in df else
                        df["항목"].fillna("") + df["세부항목"].map(lambda v: f"_{v}" if v else ""),
                "연도": df["연도"], "값": df["값"],
            })
            if "사용여부" in df:
                t = t[df["사용여부"].fillna("Y") != "N"]
            수치들.append(t)
        목록.append((이름, 카테고리, 종류, len(df)))

    # ── 통합 테이블 ──────────────────────────────────────
    사건 = pd.concat(사건들, ignore_index=True)
    for c in ("연도", "종료연도"):
        사건[c] = to_int(사건[c])
    사건.to_sql("사건", con, index=False)

    수치 = pd.concat(수치들, ignore_index=True)
    수치["연도"] = to_int(수치["연도"])
    원값 = 수치["값"]
    수치["값"] = pd.to_numeric(원값, errors="coerce")
    값_문자 = int((원값.notna() & 수치["값"].isna()).sum())   # 숫자로 못 바꾼 문자열
    값_빈칸 = int(원값.isna().sum())                            # Null (허용)
    수치.to_sql("수치", con, index=False)

    참여국 = 공통.get("참여국", pd.DataFrame(columns=["사건ID", "참여국"]))
    참여국.to_sql("참여국", con, index=False)

    단위 = 공통.get("단위", pd.DataFrame(columns=["파일명", "컬럼명", "지표", "원본_단위", "표준_단위", "환산_배수"]))
    if "지표" not in 단위:
        단위["지표"] = None
    단위["지표"] = 단위["지표"].fillna("")
    단위["환산_배수"] = pd.to_numeric(단위["환산_배수"], errors="coerce")
    단위.to_sql("단위", con, index=False)

    # 코드 목록 = 공통_국가코드.csv (없으면 기본 12개만)
    if "국가코드" in 공통:
        국가코드 = 공통["국가코드"]
    else:
        print("  !! 공통_국가코드.csv 없음 — 기본 코드 12개로만 검사")
        국가코드 = pd.DataFrame({"코드": sorted(기본코드), "이름": None, "구분": None})
    국가코드["코드"] = 국가코드["코드"].str.strip()
    코드 = set(국가코드["코드"].dropna()) | 기본코드
    국가코드.to_sql("코드", con, index=False)
    pd.DataFrame(파일단위, columns=["파일명", "컬럼", "단위"]).to_sql("_파일단위", con, index=False)
    pd.DataFrame(목록, columns=["파일명", "카테고리", "종류", "행수"]).to_sql("파일목록", con, index=False)

    # ── 인덱스·뷰 ─────────────────────────────────────────
    con.executescript("""
        CREATE INDEX ix_사건_ID     ON 사건(사건ID);
        CREATE INDEX ix_사건_시작일 ON 사건(시작일);
        CREATE INDEX ix_수치_키     ON 수치(파일명, 국가, 지표, 연도);
        CREATE INDEX ix_참여국_ID   ON 참여국(사건ID);
        CREATE INDEX ix_단위_키     ON 단위(파일명, 컬럼명, 지표);
        CREATE VIEW 수치_단위 AS
        SELECT s.*, u.표준_단위, u.원본_단위, u.환산_배수,
               s.값 / u.환산_배수 AS 원본단위값
        FROM 수치 s
        LEFT JOIN 단위 u
          ON u.파일명 = s.파일명 AND u.컬럼명 = '값'
         AND (u.지표 = s.지표 OR u.지표 = '');
    """)
    con.commit()

    # ── 검증 (README 11번) ───────────────────────────────
    문제 = []

    def check(이름, sql, 경고=False):
        n = con.execute(sql).fetchone()[0]
        tag = "OK " if n == 0 else ("!! " if 경고 else "XX ")
        print(f"  {tag} {이름}: {n}")
        if n and not 경고:
            문제.append(이름)

    print(f"\nDB: {out.resolve()}")
    for t, n in con.execute("SELECT 종류, COUNT(*) FROM 파일목록 GROUP BY 종류"):
        print(f"  {t} 파일 {n}개")
    print(f"  사건 {len(사건)}행 · 수치 {len(수치)}행 · 참여국 {len(참여국)}행 · 단위 {len(단위)}행 · 코드 {len(코드)}개\n")

    check("사건ID 중복", "SELECT COUNT(*) FROM (SELECT 사건ID FROM 사건 GROUP BY 사건ID HAVING COUNT(*)>1)")
    check("사건ID 빈칸", "SELECT COUNT(*) FROM 사건 WHERE 사건ID IS NULL")
    check("사건ID 형식 (XX-nnnn 또는 XX-nnnnn)",
          "SELECT COUNT(*) FROM 사건 WHERE 사건ID NOT GLOB '[A-F][0-9]-[0-9][0-9][0-9][0-9]' "
          "AND 사건ID NOT GLOB '[A-F][0-9]-[0-9][0-9][0-9][0-9][0-9]'")
    check("종료일 < 시작일", "SELECT COUNT(*) FROM 사건 WHERE 종료일 < 시작일")
    check("연도 ≠ 시작일의 연도",
          "SELECT COUNT(*) FROM 사건 WHERE 시작일 IS NOT NULL AND 연도 != CAST(substr(시작일,1,4) AS INTEGER)")
    check("연도 빈칸 (사건)", "SELECT COUNT(*) FROM 사건 WHERE 연도 IS NULL")
    check("목록 밖 주체국", "SELECT COUNT(*) FROM 사건 WHERE 주체국 IS NOT NULL AND 주체국 NOT IN (SELECT 코드 FROM 코드)")
    check("목록 밖 대상국", "SELECT COUNT(*) FROM 사건 WHERE 대상국 IS NOT NULL AND 대상국 NOT IN (SELECT 코드 FROM 코드)")
    check("목록 밖 참여국", "SELECT COUNT(*) FROM 참여국 WHERE 참여국 NOT IN (SELECT 코드 FROM 코드)")
    check("목록 밖 국가 (수치)", "SELECT COUNT(*) FROM 수치 WHERE 국가 NOT IN (SELECT 코드 FROM 코드)")
    check("MUL + 사용여부 Y 인데 참여국 2행 미만", """
        SELECT COUNT(*) FROM 사건 e WHERE 주체국='MUL' AND COALESCE(사용여부,'Y')='Y'
        AND (SELECT COUNT(*) FROM 참여국 p WHERE p.사건ID=e.사건ID) < 2""")
    check("참여국 표에만 있는 사건ID", "SELECT COUNT(*) FROM 참여국 WHERE 사건ID NOT IN (SELECT 사건ID FROM 사건)")
    check("참여국 (사건ID+참여국) 중복",
          "SELECT COUNT(*) FROM (SELECT 1 FROM 참여국 GROUP BY 사건ID, 참여국 HAVING COUNT(*)>1)")
    check("수치 (파일+국가+지표+연도) 중복",
          "SELECT COUNT(*) FROM (SELECT 1 FROM 수치 GROUP BY 파일명, 국가, 지표, 연도 HAVING COUNT(*)>1)")
    print(f"  {'OK ' if 값_문자 == 0 else 'XX '} 수치 값에 숫자 아닌 문자열: {값_문자}   (빈칸 Null은 {값_빈칸}건, 허용)")
    if 값_문자:
        문제.append("수치 값 문자열")
    check("같은 사건ID가 두 파일에 있음 (부속표면 제외파일에 추가)",
          "SELECT COUNT(*) FROM (SELECT 사건ID FROM 사건 GROUP BY 사건ID HAVING COUNT(DISTINCT 파일명)>1)")
    check("단위 (파일명+컬럼명+지표) 중복",
          "SELECT COUNT(*) FROM (SELECT 1 FROM 단위 GROUP BY 파일명, 컬럼명, 지표 HAVING COUNT(*)>1)")
    check("단위 빈칸 (원본_단위·표준_단위·환산_배수)",
          "SELECT COUNT(*) FROM 단위 WHERE 원본_단위 IS NULL OR 표준_단위 IS NULL OR 환산_배수 IS NULL")
    check("단위 표에 없는 수치 (파일명+지표)",
          "SELECT COUNT(*) FROM (SELECT DISTINCT 파일명, 지표 FROM 수치 s WHERE NOT EXISTS "
          "(SELECT 1 FROM 단위 u WHERE u.파일명=s.파일명 AND u.컬럼명='값' AND (u.지표=s.지표 OR u.지표='')))")
    check("단위 표 파일명이 실제 파일에 없음",
          "SELECT COUNT(DISTINCT 파일명) FROM 단위 WHERE 파일명 NOT IN (SELECT 파일명 FROM 파일목록)")
    # 결정 1·3: 값은 표준 단위. 파일 안 `단위` 열은 단위표 표준_단위와 같아야 함
    check("파일 안 `단위` 값이 단위표 표준_단위와 다름 (값이 원본 단위로 들어간 것?)", """
        SELECT COUNT(*) FROM _파일단위 f WHERE NOT EXISTS
        (SELECT 1 FROM 단위 u WHERE u.파일명=f.파일명 AND u.표준_단위=f.단위)""")

    기타 = [r[0] for r in con.execute("SELECT 파일명 FROM 파일목록 WHERE 종류 IN ('기타','제외')")]
    if 기타:
        print("\n  참고: 통합 표에 안 들어간 파일 (파일_<이름> 표로만 저장):")
        for n in 기타:
            print(f"    - {n}")

    print("\n결과:", "문제 없음" if not 문제 else f"확인 필요 {len(문제)}건 → {', '.join(문제)}")
    con.close()


if __name__ == "__main__":
    main()
