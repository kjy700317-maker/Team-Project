"""로컬 원자료 → 사건표 기본·확장·제외기록·입력 파일 기록 (F1).

v0.1.4 사건표를 만든 세 단계의 규칙을 하나로 합쳐 원자료에서 한 번에 만든다(규칙은 바꾸지 않음).
  - v0.1_시험/S2/s2lib.py build_x() — 요소별 시트·열·거르기(확정 옵션 S2/e5v2.py FIN)
  - v0.1_시험/S2/team.py sheet() — 엑셀 읽기
  - v0.1_시험/v0.1.3/build_v013_input.py — ① A3-0059 · ③ A2 같은 날 1회 · ④ C5, 제외기록 문구
  - v0.1_시험/v0.1.4/build_v014_input.py — A4·A6 보완(팀 파일에 들어 있어 표대로 반영됨)
적용 순서: (가) 날짜가 읽히고 start ≤ date ≤ end인 행만 — 날짜 없음은 ⑤(사용여부 N 행은 기록 안 함), 기간 밖은 기록 안 함
          (나) 사용여부 N → ③·④·⑦  (다) 추가 제외 → ①·⑥  (라) 남은 행 = 사건표

사용: python scripts/build_events.py [--raw-dir …] [--out-dir …] [--start YYYY-MM-DD] [--end YYYY-MM-DD]
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import openpyxl  # noqa: E402
import pandas as pd  # noqa: E402

import config  # noqa: E402
from utils.tension.io import EVENT_COLUMNS, read_csv_kr, write_csv  # noqa: E402

DEFAULT_RAW_DIR = ROOT / "data" / "raw" / "긴장도_산출식_세부_기준"
EXCLUDED_LOG_COLUMNS = ("사건ID", "date", "요소", "S", "대표ID", "사유")
INPUT_LOG_COLUMNS = ("요소", "파일", "크기", "SHA256")

# 엑셀 요소 — (요소, 파일 패턴, 시트, 사용여부 처리, 날짜 열, 점수 열, 묶음)
#   사용여부: None = 열 없음(생기면 멈춤) / "③"·"⑦" = Y만, N은 그 코드로 기록 / "④" = Y이고 점수 있음(C5)
EXCEL_ELEMENTS = (
    ("A1", "*A1_*", "02_PRK6건_시험점수", None, "시작일", "위력반영점수", "핵·미사일"),
    ("A2", "*A2_*", "01_294건_적용본", "③", "시작일", "시험 점수", "핵·미사일"),
    ("B1", "*B1_*", "B1_사건별시험", "⑦", "시작일", "시험점수", "핵·미사일"),
    ("A3", "*A3_*", "01_Y62_사건판정", None, "시작일", "사건시험점수", "물리 충돌"),
    ("A7", "*A7_*", "A7_사건별_맥락검토", None, "시작일", "기존 점수", "물리 충돌"),
    ("A4", "*A4_*", "01_39건_점수시험", None, "시작일", "사건시험점수", "군사 과시"),
    ("A5", "*A5_*", "01_사건별117건", "⑦", "시작일", "사건 시험점수", "군사 과시"),
    ("A6", "*A6_*", "01_A6_17건_점수", "⑦", "시작일", "시험점수", "군사 과시"),
    ("B4", "*B4_*", "B4_41건_점수시험", "⑦", "시작일", "시험점수", "위협 언어·교리"),
    ("C1", "*C1_*", "C1_전건_재검토", "⑦", "날짜", "v0.2 점수", "위협 언어·교리"),
    ("C2", "*C2_*", "C2_사건별_v03비교", "⑦", "시작일", "v0.2 점수", "위협 언어·교리"),
    ("C3", "*C3_v0.7*", "사건별_66건_시험", "⑦", "시작일", "시험점수", "위협 언어·교리"),
    ("C5", "*C5_*", "C5_282건_사건별시험", "④", "시작일", "시험점수", "제재·압박"),
)
E5_SCORES = "E/E5_점수표_v2_2026-10-27.csv"
F2_SCORES = "F/F2_점수표_v4_2026-10-27.csv"
F2_LIST = "F/F2_연도별회담_정제.csv"
EXT_ONLY = ("C5",)

A3_A7_SAME = "A3-0059"
C3_SAME_TALKS = ("C3-0050", "C3-0019", "C3-0046", "C3-0063")


def _rules(el, f2_ids):
    """(다) 추가 제외 — [(조건, 사유, 대표ID)]. 조건은 행(Series) → bool."""
    if el == "B1":
        return [(lambda r: r["중복연계_표시"] == "A2 동일 사건 명시", "⑥ 기존 규칙: A2 동일 사건 명시", "")]
    if el == "A3":
        return [(lambda r: r["사건ID"] == A3_A7_SAME,
                 "① A3–A7 같은 사건(2024-10-15 도로 폭파) — A7 대표, 계산 제외(0점 아님)", "A7-0120")]
    if el == "B4":
        return [(lambda r: r["태세방향"] == "완화", "⑥ 기존 규칙: 태세방향 완화", "")]
    if el == "C2":
        return [(lambda r: r["사건ID"] == "C2-0035", "⑥ 기존 규칙: 9·19 군사합의 체결, 완화", "")]
    if el == "C3":
        return [(lambda r: r["사건ID"] in C3_SAME_TALKS, "⑥ 기존 규칙: 같은 회담", ""),
                (lambda r: r["협의축"] == "북러", "⑥ 기존 규칙: E5가 대표", "")]
    if el == "F2":
        return [(lambda r: r["사건ID"] not in f2_ids, f"⑥ 기존 규칙: {Path(F2_LIST).name}에 없음", "")]
    return []


def _blank(v):
    return v is None or (isinstance(v, float) and pd.isna(v)) or (isinstance(v, str) and v.strip() == "")


def _text(v):
    return "" if _blank(v) else str(v)


def _float_or_none(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def find_workbook(raw_dir, pattern, sheet):
    """`<raw_dir>/*/<pattern>`의 .xlsx 중 그 시트가 있는 파일 — 정확히 1개여야 한다."""
    hits = []
    for f in sorted(p for p in Path(raw_dir).glob(f"*/{pattern}") if p.suffix == ".xlsx"):
        wb = openpyxl.load_workbook(f, read_only=True)
        if sheet in wb.sheetnames:
            hits.append(f)
        wb.close()
    if len(hits) != 1:
        raise SystemExit(f"엑셀 찾기 실패: 패턴 {pattern} · 시트 {sheet} → {len(hits)}개 {[str(h) for h in hits]}")
    return hits[0]


def read_sheet(path, sheet):
    """첫 행 = 열 이름(str), 첫 열이 비어 있는 행은 버린다."""
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    df = pd.DataFrame(rows[1:], columns=[str(c) for c in rows[0]], dtype=object)
    return df[df.iloc[:, 0].notna()].reset_index(drop=True)


def find_input_files(raw_dir):
    """이번 실행에서 읽을 파일 — [(요소, 경로, 시트 또는 None)] 16개. 쓴 파일 이름을 출력한다."""
    raw_dir = Path(raw_dir)
    files = []
    for el, pattern, sheet, *_ in EXCEL_ELEMENTS:
        f = find_workbook(raw_dir, pattern, sheet)
        print(f"  {el}: {f.name} [{sheet}]")
        files.append((el, f, sheet))
    for el, rel in (("E5", E5_SCORES), ("F2", F2_SCORES), ("F2", F2_LIST)):
        f = raw_dir / rel
        if not f.is_file():
            raise SystemExit(f"파일 없음: {f}")
        print(f"  {el}: {f.name}")
        files.append((el, f, None))
    return files


def check_f2_factor(f2):
    """φ 대조(결과는 바꾸지 않음): 분야보정 == config.F2_FIELD_FACTOR[분야군], |S × 분야보정 − S_보정| < 1e-9."""
    bad = []
    for _, r in f2.iterrows():
        factor = config.F2_FIELD_FACTOR.get(r["분야군"])
        phi, s, s_adj = (_float_or_none(r[c]) for c in ("분야보정", "S", "S_보정"))
        if factor is None or phi is None or s is None or s_adj is None or phi != factor or abs(s * phi - s_adj) >= 1e-9:
            bad.append(r["사건ID"])
    if bad:
        raise SystemExit(f"φ 대조 실패 {len(bad)}행: {bad[:20]}")
    print(f"φ 대조 통과 {len(f2)}")


def _collect(df, el, use, date_col, score_col, bundle, rules, start, end, rows, log):
    """한 요소의 행을 (가)~(라) 순서로 사건표 행(rows)과 제외기록(log)으로 나눈다."""
    if use is None and "사용여부" in df.columns:
        raise SystemExit(f"{el}: 사용여부 열이 생겼음 — 새 규칙이 필요함")
    if use is not None and "사용여부" not in df.columns:
        raise SystemExit(f"{el}: 사용여부 열이 없음")
    for _, r in df.iterrows():
        eid = str(r["사건ID"])
        score = r[score_col]
        if use is None:
            is_n = False
        elif use == "④":
            is_n = not (r["사용여부"] == "Y" and not _blank(score))
        else:
            is_n = r["사용여부"] != "Y"
        dt = pd.to_datetime(str(r[date_col])[:10], errors="coerce")
        if pd.isna(dt):
            if not is_n:
                log.append(dict(사건ID=eid, date="", 요소=el, S=_float_or_none(score), 대표ID="", 사유="⑤ 날짜 없음(일별 반영 보류)"))
            continue
        if not (start <= dt <= end):
            continue
        day = dt.strftime("%Y-%m-%d")
        if is_n:
            why = _text(r["제외사유"]) if "제외사유" in df.columns else ""
            if use == "③":
                m = re.search(r"(A2-\d{4}) 유지", why)
                log.append(dict(사건ID=eid, date=day, 요소=el, S=_float_or_none(score), 대표ID=m.group(1) if m else "",
                                사유="③ 같은 날 1회(팀 사용여부 N): " + why))
            elif use == "④":
                log.append(dict(사건ID=eid, date=day, 요소=el, S=None, 대표ID="", 사유="④ 팀 사용여부 N: " + why))
            else:
                log.append(dict(사건ID=eid, date=day, 요소=el, S=_float_or_none(score), 대표ID="",
                                사유=("⑦ 팀 사용여부 N: " + why).rstrip(": ")))
            continue
        hit = next(((why, rep) for cond, why, rep in rules if cond(r)), None)
        if hit is not None:
            log.append(dict(사건ID=eid, date=day, 요소=el, S=_float_or_none(score), 대표ID=hit[1], 사유=hit[0]))
            continue
        s = _float_or_none(score)
        if s is None:
            raise SystemExit(f"{el} {eid}: 점수 열 {score_col!r} 값이 비었거나 숫자가 아님 ({score!r})")
        b = bundle(r) if callable(bundle) else bundle
        rows.append(dict(사건ID=eid, date=dt, 요소=el, 묶음=b, S=s, 사건명=str(r["사건명"])[:60]))


def _sort_events(rows):
    ev = pd.DataFrame(rows, columns=list(EVENT_COLUMNS))
    return ev.sort_values(["date", "사건ID"], kind="mergesort").reset_index(drop=True)


def build_events(raw_dir, start, end, files=None):
    """원자료 → (사건표 기본, 사건표 확장, 제외기록). 기본 = C5를 뺀 전부, 확장 = 기본 + C5."""
    raw_dir = Path(raw_dir)
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if files is None:
        files = find_input_files(raw_dir)
    path_of = {(el, f.name if sheet is None else sheet): f for el, f, sheet in files}

    f2_ids = set(read_csv_kr(path_of[("F2", Path(F2_LIST).name)], dtype=str)["사건ID"])
    rows, ext_rows, log = [], [], []
    for el, _pattern, sheet, use, date_col, score_col, bundle in EXCEL_ELEMENTS:
        df = read_sheet(path_of[(el, sheet)], sheet)
        target = ext_rows if el in EXT_ONLY else rows
        _collect(df, el, use, date_col, score_col, bundle, _rules(el, f2_ids), start, end, target, log)

    e5 = read_csv_kr(path_of[("E5", Path(E5_SCORES).name)], dtype=str)
    e5_bundle = lambda r: config.BUNDLE_E5 if r["기준선대상"] == "Y" else "북러(표시만)"  # noqa: E731
    _collect(e5, "E5", None, "시작일", "S", e5_bundle, [], start, end, rows, log)

    f2 = read_csv_kr(path_of[("F2", Path(F2_SCORES).name)], dtype=str)
    check_f2_factor(f2)
    _collect(f2, "F2", "⑦", "시작일", "S_보정", config.BUNDLE_RELIEF, _rules("F2", f2_ids), start, end, rows, log)

    base = _sort_events(rows)
    ext = _sort_events(rows + ext_rows)
    excluded = pd.DataFrame(log, columns=list(EXCLUDED_LOG_COLUMNS))
    excluded = excluded.assign(_code=excluded["사유"].str[:1]).sort_values(
        ["_code", "date", "사건ID"], kind="mergesort").drop(columns="_code").reset_index(drop=True)
    return base, ext, excluded


def input_file_table(raw_dir, files):
    """읽은 파일마다 한 행(요소, --raw-dir 기준 상대 경로, 바이트, SHA256). 실행 시각은 넣지 않는다."""
    out = []
    for el, f, _sheet in files:
        out.append(dict(요소=el, 파일=f.relative_to(raw_dir).as_posix(), 크기=f.stat().st_size,
                        SHA256=hashlib.sha256(f.read_bytes()).hexdigest()))
    return pd.DataFrame(out, columns=list(INPUT_LOG_COLUMNS)).sort_values(["요소", "파일"], kind="mergesort").reset_index(drop=True)


def main(argv=None):
    p = argparse.ArgumentParser(description="원자료 → 사건표 기본·확장·제외기록")
    p.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR))
    p.add_argument("--out-dir", default=str(ROOT / config.TENSION_DATA_DIR))
    p.add_argument("--start", default=config.CALC_START_DATE)
    p.add_argument("--end", default=config.END_DATE)
    a = p.parse_args(argv)
    raw_dir = Path(a.raw_dir).resolve()
    out_dir = Path(a.out_dir)
    end = pd.Timestamp(a.end) if a.end else pd.Timestamp.today().normalize()
    print(f"원자료 {raw_dir} · 기간 {a.start} ~ {end:%Y-%m-%d}")

    print("읽은 파일:")
    files = find_input_files(raw_dir)
    base, ext, excluded = build_events(raw_dir, a.start, end, files=files)

    fmt = lambda d: d.assign(date=d["date"].dt.strftime("%Y-%m-%d"))  # noqa: E731
    write_csv(fmt(base), out_dir / "events_기본.csv")
    write_csv(fmt(ext), out_dir / "events_확장.csv")
    write_csv(excluded, out_dir / "events_제외기록.csv")
    write_csv(input_file_table(raw_dir, files), out_dir / "events_입력파일.csv")

    pd.set_option("display.width", 200)
    print(ext.groupby(["요소", "묶음"], sort=True).agg(n=("S", "size"), S합=("S", "sum")).round(3).to_string())
    print(f"기본 {len(base)}행 / 확장 {len(ext)}행 / 제외기록 {len(excluded)}행")
    print("사유 코드별:", excluded["사유"].str[:1].value_counts().sort_index().to_dict())
    print(f"쓴 파일: {out_dir}/events_기본.csv · events_확장.csv · events_제외기록.csv · events_입력파일.csv")


if __name__ == "__main__":
    main()
