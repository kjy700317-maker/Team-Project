"""
봉수 ERD v4 테이블 만들기 — 2단계 (이슈 #7)

build_db.py(1단계)가 만든 표(사건·수치·참여국·단위·코드·파일_<이름>)를 읽어서
ERD v4의 기준·데이터·보조 테이블을 같은 DB 안에 만듭니다.

사용법 (Team-Project 폴더에서):
    python utils/build_db.py            # 1단계 끝에 자동으로 이 파일을 호출
    python utils/build_erd.py           # 1단계 DB가 이미 있을 때 2단계만 다시 실행
    python utils/build_erd.py --db data/bongsu.db --schema db/schema.sql

적재 규칙 (ERD v4, 2026-10-22 결정)
    기준   국가   = 코드 표. 관심국여부 Y = 한·북·미·중·일·러·대만
           날짜   = 1945-07-16 ~ 올해 12-31 하루 1행
    데이터 사건_일단위 / 사건_연단위
             - A·B·C 파트 사건만 (E1·E5·F2 사건은 1단계 사건 표에만 두고, 산출식 확정 후 통합 방식 재검토)
             - 사용여부 Y · 주체국 있음 · 주체국이 사용 가능 구분(주요 국가·연합·다자·국제기구)인 행만
               → 빠지는 건 '그 밖의 국가'(IRN·SYR 등)가 주체국인 행뿐
             - 시작일 있으면 일단위, 없으면 연단위
           지표값 = 수치 표 중 관심국·연도 2025 이하. 같은 지표가 D·F 두 파일에 있으면 연도 범위가 긴 파일, 같으면 F
                    증감률 지표는 넣지 않음 (원 지표에서 계산하는 파생값)
    보조   사건_목록(사건ID → 어느 사건 표), 사건_참여국
           사건 상세 13개 = 전처리 CSV 열 그대로(공통 11열 제외), 값도 그대로(단위 환산은 공통_단위로 쓸 때)

1단계 표는 그대로 두고 ERD 표만 추가/재생성합니다.
"""

import argparse
import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd

관심국 = ["KOR", "PRK", "USA", "CHN", "JPN", "RUS", "TWN"]
사용구분 = {"주요 국가", "연합", "다자", "국제기구"}          # 공통_국가코드.csv 의 구분 값
대기능1_파트 = {"A", "B", "C"}                                 # 사건 표에 넣는 파트. E·F 사건은 산출식 확정 후 재검토
사건_공통열 = ["사건ID", "카테고리코드", "시작일", "종료일", "연도", "주체국", "대상국",
             "사건명", "요약", "비고", "사용여부", "제외사유"]
상세제외열 = set(사건_공통열) | {"카테고리", "파일명", "종료연도"}   # 1단계가 붙인 열 포함

# 사건 상세 13개: 상세표 이름 → (파일_ 표의 원본 파일명, FK가 가리키는 사건 표)
상세표 = {
    "B2_무기이전":   ("B2_SIPRI_무기이전_전처리", "사건_연단위"),
    "A2_미사일발사": ("A2_미사일_발사_CSV",       "사건_일단위"),
    "A6_열병식":     ("A6_열병식_CSV",            "사건_일단위"),
    "A7_포격충돌":   ("A7_포격_총격_물리_충돌_CSV", "사건_일단위"),
    "B1_신형무기시험": ("B1_신형무기개발시험_전처리", "사건_일단위"),
    "B3_국방비":     ("B3_군비이벤트_전처리",      "사건_일단위"),
    "B4_핵태세":     ("B4_핵태세확장억제_사건",    "사건_일단위"),
    "B4_공약문구":   ("B4_확장억제_공약문구",      "사건_일단위"),
    "C1_위협성명":   ("C1_위협성명담화_전처리",    "사건_일단위"),
    "C2_교리법제":   ("C2_교리법제_전처리",        "사건_일단위"),
    "C3_동맹협의":   ("C3_동맹협의_사건",          "사건_일단위"),
    "C4_대화협상":   ("C4_대화협상합의_전처리",    "사건_일단위"),
    "C5_제재":       ("C5_제재_결의_수출통제",      "사건_일단위"),
}
ERD_테이블 = list(상세표) + ["사건_참여국", "사건_목록", "지표값", "사건_연단위", "사건_일단위", "날짜", "국가"]


def 기존_ERD표_삭제(con: sqlite3.Connection) -> None:
    """다시 실행해도 되도록 ERD 표만 지운다 (1단계 표는 보존)."""
    con.execute("PRAGMA foreign_keys = OFF")
    for name in ERD_테이블:
        con.execute(f'DROP TABLE IF EXISTS "{name}"')
    con.commit()


def build_erd(con: sqlite3.Connection, schema: Path) -> list[str]:
    """ERD 표를 만들고 채운다. 반환: 검증에서 걸린 항목 이름 목록."""
    기존_ERD표_삭제(con)
    con.executescript(schema.read_text(encoding="utf-8"))
    con.execute("PRAGMA foreign_keys = ON")

    # ── ① 기준: 국가 ───────────────────────────────────
    코드 = pd.read_sql("SELECT 코드 AS 국가코드, 이름, 구분 FROM 코드", con)
    코드["이름"] = 코드["이름"].fillna(코드["국가코드"])
    코드["관심국여부"] = 코드["국가코드"].isin(관심국).map({True: "Y", False: "N"})
    코드.to_sql("국가", con, if_exists="append", index=False)
    사용코드 = set(코드[코드["구분"].isin(사용구분)]["국가코드"])

    # ── ① 기준: 날짜 ───────────────────────────────────
    d = pd.date_range("1945-07-16", f"{date.today().year}-12-31")
    pd.DataFrame({"날짜": d.strftime("%Y-%m-%d"), "연도": d.year, "연월": d.strftime("%Y-%m"),
                  "월": d.month, "분기": d.quarter}).to_sql("날짜", con, if_exists="append", index=False)

    # ── ② 데이터: 사건 ─────────────────────────────────
    사건 = pd.read_sql("SELECT * FROM 사건", con)
    사건["카테고리코드"] = 사건["사건ID"].str.split("-").str[0]
    # 대기능 1 = A·B·C 사건만. E(UN표결·남북관계연표)·F2(회담)는 산출식 확정 후 통합 방식 재검토 (2026-10-22)
    대기능1 = 사건["카테고리코드"].str[0].isin(대기능1_파트)
    제외_파트 = int(((사건["사용여부"] == "Y") & ~대기능1).sum())
    사건 = 사건[대기능1]
    쓸사건 = 사건[(사건["사용여부"] == "Y") & 사건["주체국"].isin(사용코드)]
    제외_N = int((사건["사용여부"] != "Y").sum())
    제외_주체 = int(((사건["사용여부"] == "Y") & ~사건["주체국"].isin(사용코드)).sum())

    쓸사건 = 쓸사건[사건_공통열].copy()
    쓸사건["연도"] = 쓸사건["연도"].astype("Int64")
    일단위 = 쓸사건[쓸사건["시작일"].notna()]
    연단위 = 쓸사건[쓸사건["시작일"].isna()]
    일단위.to_sql("사건_일단위", con, if_exists="append", index=False)
    연단위.to_sql("사건_연단위", con, if_exists="append", index=False)

    목록 = pd.concat([pd.DataFrame({"사건ID": 일단위["사건ID"], "적재표": "사건_일단위"}),
                    pd.DataFrame({"사건ID": 연단위["사건ID"], "적재표": "사건_연단위"})])
    목록.to_sql("사건_목록", con, if_exists="append", index=False)
    적재ID = {"사건_일단위": set(일단위["사건ID"]), "사건_연단위": set(연단위["사건ID"])}

    # ── ② 데이터: 지표값 ───────────────────────────────
    수치 = pd.read_sql("""
        SELECT s.카테고리 AS 출처파트, s.파일명, s.국가 AS 국가코드, s.지표 AS 지표명,
               s.연도, s.값, u.표준_단위 AS 단위
        FROM 수치 s
        LEFT JOIN 단위 u ON u.파일명 = s.파일명 AND u.컬럼명 = '값' AND (u.지표 = s.지표 OR u.지표 = '')
    """, con)
    수치 = 수치[수치["국가코드"].isin(관심국) & (수치["연도"] <= 2025)].copy()
    수치["세부항목"] = "합계"
    # 증감률은 원 지표에서 계산 가능한 파생값이라 지표값에 넣지 않음 (2026-10-22 검수)
    #   원본 증감률은 산출 당시의 전년 값(잠정치) 기준이라 현재 원 지표와 최대 0.16%p 어긋남.
    #   대시보드 안에서 생산량과 증감률이 모순되지 않도록 원 지표 하나만 두고 계산 시점에 산출.
    #   경제성장률·산업별성장률은 성장률 자체가 지표(원 금액 시리즈 없음)라 유지.
    증감률 = 수치["지표명"].str.contains("증감률")
    제외_증감률 = int(증감률.sum())
    수치 = 수치[~증감률]
    # 같은 지표가 두 파일에 있을 때 (2026-10-22 결정): 연도 범위(커버리지)가 긴 파일을 쓰고, 같으면 F.
    # 띄어쓰기·밑줄만 다른 이름('1인당 국민총소득' ↔ '1인당_국민총소득')은 같은 지표로 본다.
    수치["_키"] = 수치["지표명"].str.replace(r"[\s_]+", "_", regex=True)
    범위 = (수치.groupby(["_키", "파일명"])["연도"]
            .agg(lambda s: s.max() - s.min() + 1).rename("_범위").reset_index())
    범위["_F"] = 범위["파일명"].str.startswith("F").astype(int)
    범위 = 범위.sort_values(["_키", "_범위", "_F"], ascending=[True, False, False])
    범위["_순위"] = 범위.groupby("_키").cumcount()
    수치 = 수치.merge(범위[["_키", "파일명", "_순위"]], on=["_키", "파일명"]).sort_values("_순위", kind="stable")
    승자 = 범위[범위["_순위"] == 0].set_index("_키")["파일명"]
    키 = ["국가코드", "지표명", "세부항목", "연도"]
    진파일 = 수치[수치["_순위"] > 0]
    # 진 파일에만 있고 값이 실제로 있는 행 (이긴 파일만 쓰므로 버려짐 — 0건이어야 손실 없음)
    이긴키 = set(map(tuple, 수치[수치["_순위"] == 0][["_키", "국가코드", "연도"]].itertuples(index=False)))
    버린값 = 진파일[진파일["값"].notna()
                 & ~진파일[["_키", "국가코드", "연도"]].apply(tuple, axis=1).isin(이긴키)]
    중복쌍 = 범위[범위["_키"].isin(범위[범위["_순위"] > 0]["_키"])]
    수치 = 수치[수치["_순위"] == 0].drop(columns=["_순위", "_키", "파일명"])
    수치[키 + ["값", "단위", "출처파트"]].to_sql("지표값", con, if_exists="append", index=False)

    # ── ③ 보조: 참여국 ─────────────────────────────────
    참여국 = pd.read_sql("SELECT 사건ID, 참여국 FROM 참여국", con)
    모든ID = 적재ID["사건_일단위"] | 적재ID["사건_연단위"]
    참여국[참여국["사건ID"].isin(모든ID)].drop_duplicates().to_sql(
        "사건_참여국", con, if_exists="append", index=False)

    # ── ③ 보조: 사건 상세 13개 (CSV 열 그대로) ───────────
    수치열 = {(r[0], r[1]) for r in con.execute("SELECT 파일명, 컬럼명 FROM 단위")}
    상세결과 = []
    for 표, (파일명, FK표) in 상세표.items():
        if not con.execute("SELECT 1 FROM sqlite_master WHERE name=?", (f"파일_{파일명}",)).fetchone():
            print(f"  !! 파일_{파일명} 없음 → {표} 생략")
            continue
        df = pd.read_sql(f'SELECT * FROM "파일_{파일명}"', con)
        고유열 = [c for c in df.columns if c not in 상세제외열]
        df = df[df["사건ID"].isin(적재ID[FK표])][["사건ID"] + 고유열].copy()
        defs = []
        for c in 고유열:
            if (파일명, c) in 수치열:
                df[c] = pd.to_numeric(df[c], errors="coerce")
                defs.append(f'"{c}" REAL')
            else:
                defs.append(f'"{c}" TEXT')
        con.execute(f'CREATE TABLE "{표}" ("사건ID" TEXT PRIMARY KEY REFERENCES {FK표}(사건ID), '
                    + ", ".join(defs) + ")")
        df.to_sql(표, con, if_exists="append", index=False)
        상세결과.append((표, len(df), len(고유열)))
    con.commit()

    # ── 보고 ──────────────────────────────────────────
    print("\n[ERD v4 테이블]")
    for t in ("국가", "날짜", "사건_일단위", "사건_연단위", "지표값", "사건_참여국"):
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:12s} {n:>8,}행")
    print("  상세 13개:  " + ", ".join(f"{t}({n}행·{k}열)" for t, n, k in 상세결과))
    print(f"\n  사건 표 {len(사건) + 제외_파트:,}행 → {len(쓸사건):,}행 적재 "
          f"(E·F 사건 {제외_파트}행, 사용여부 N {제외_N}행, 주체국이 사용 구분 밖 {제외_주체}행 제외)")
    print(f"  지표값: 증감률 지표 {제외_증감률}행 제외 (원 지표에서 계산)")
    if len(중복쌍):
        print("  지표값: 같은 지표가 두 파일에 있어 연도 범위가 긴 파일(같으면 F)만 사용")
        for k, g in 중복쌍.groupby("_키", sort=False):
            설명 = " / ".join(f"{f}({n}년)" for f, n in zip(g["파일명"], g["_범위"]))
            print(f"      {k}: {설명} → {g['파일명'].iloc[0]}")
        print(f"  {'OK ' if len(버린값) == 0 else '!! '} 진 파일에만 있던 실제 값 (버려짐): {len(버린값)}건")

    # ── 검증 ──────────────────────────────────────────
    문제 = []

    def check(이름, sql):
        n = con.execute(sql).fetchone()[0]
        print(f"  {'OK ' if n == 0 else 'XX '} {이름}: {n}")
        if n:
            문제.append(이름)

    print()
    check("FK 위반 (PRAGMA foreign_key_check)", "SELECT COUNT(*) FROM pragma_foreign_key_check")
    check("사용여부 N 또는 주체국 Null (일단위)", "SELECT COUNT(*) FROM 사건_일단위 WHERE 사용여부!='Y' OR 주체국 IS NULL")
    check("사용여부 N 또는 주체국 Null (연단위)", "SELECT COUNT(*) FROM 사건_연단위 WHERE 사용여부!='Y' OR 주체국 IS NULL")
    check("같은 사건ID가 일단위·연단위 양쪽에", "SELECT COUNT(*) FROM 사건_일단위 WHERE 사건ID IN (SELECT 사건ID FROM 사건_연단위)")
    check("관심국 아닌 국가 (지표값)", "SELECT COUNT(*) FROM 지표값 WHERE 국가코드 NOT IN (SELECT 국가코드 FROM 국가 WHERE 관심국여부='Y')")
    for 표, (_, FK표) in 상세표.items():
        코드명 = 표.split("_")[0]
        if 표 == "B4_공약문구":
            continue                                  # 사건이 아니라 부속표라 1:1 아님
        check(f"{FK표} {코드명} 사건 중 {표} 상세 없음",
              f"SELECT COUNT(*) FROM {FK표} WHERE 카테고리코드='{코드명}' AND 사건ID NOT IN (SELECT 사건ID FROM \"{표}\")")
    check("MUL 사건인데 참여국 없음",
          "SELECT COUNT(*) FROM 사건_목록 m WHERE m.사건ID IN (SELECT 사건ID FROM 사건_일단위 WHERE 주체국='MUL' "
          "UNION SELECT 사건ID FROM 사건_연단위 WHERE 주체국='MUL') AND NOT EXISTS (SELECT 1 FROM 사건_참여국 p WHERE p.사건ID=m.사건ID)")
    print("\nERD 결과:", "문제 없음" if not 문제 else f"확인 필요 {len(문제)}건 → {', '.join(문제)}")
    return 문제


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/bongsu.db")
    ap.add_argument("--schema", default="db/schema.sql")
    args = ap.parse_args()
    db, schema = Path(args.db), Path(args.schema)
    if not db.exists():
        raise SystemExit(f"1단계 DB가 없습니다. 먼저 python utils/build_db.py 를 실행하세요: {db.resolve()}")
    if not schema.exists():
        raise SystemExit(f"스키마 파일이 없습니다: {schema.resolve()}")
    con = sqlite3.connect(db)
    try:
        build_erd(con, schema)
    finally:
        con.close()


if __name__ == "__main__":
    main()
