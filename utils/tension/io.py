"""사건표·유형판정표 읽기·검증과 CSV 쓰기 (F1). 파일 경로만 받고 Streamlit을 모른다.

결측·형식 오류·중복 행은 0점으로 두지 않고 빼서 제외기록에 남긴다(ADR-004).
열 이름·순서가 다른 파일, 같은 사건ID에 내용이 다른 행은 구조 오류로 ValueError.
"""
from pathlib import Path

import pandas as pd

EVENT_COLUMNS = ("사건ID", "date", "요소", "묶음", "S", "사건명")
KNOWN_BUNDLES = ("핵·미사일", "군사 과시", "위협 언어·교리", "제재·압박", "물리 충돌", "북러 밀착", "북러(표시만)", "완화")
EXCLUDED_COLUMNS = EVENT_COLUMNS + ("사유",)
TYPE4_COLUMNS = ("사건ID", "date", "요소", "S", "사건명", "판정유형", "4거유형", "봉수원뜻", "판정근거(팀 요약 원문 문구)", "비고")

DATE_FORMAT = "%Y-%m-%d"
TYPE4_ELEMENTS = ("A3", "A7")


def read_csv_kr(path, **kwargs) -> pd.DataFrame:
    """CSV 읽기(utf-8-sig — BOM이 있든 없든 읽힌다)."""
    return pd.read_csv(path, encoding="utf-8-sig", **kwargs)


def write_csv(df, path, index=False) -> None:
    """CSV 쓰기(utf-8-sig, 줄바꿈 LF). 상위 폴더가 없으면 만든다."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index, encoding="utf-8-sig", lineterminator="\n")


def _check_columns(df, expected, path):
    if tuple(df.columns) != tuple(expected):
        raise ValueError(f"{path}: 열 이름·순서가 다름 — 기대 {list(expected)}, 실제 {list(df.columns)}")


def load_events(path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """사건표를 읽고 검증한다. 반환 = (사건표, 제외기록).

    빈칸·날짜 형식·S 숫자 아님·모르는 묶음·중복 행은 빼서 제외기록(EXCLUDED_COLUMNS, 원래 문자열 + 사유)에 남긴다.
    S = 0은 정상 행이다. 날짜 범위로 거르지 않는다.
    """
    raw = read_csv_kr(path, dtype=str, keep_default_na=False)
    _check_columns(raw, EVENT_COLUMNS, path)
    raw = raw.reset_index(drop=True)

    dates = pd.to_datetime(raw["date"], format=DATE_FORMAT, errors="coerce")
    scores = pd.to_numeric(raw["S"].str.strip(), errors="coerce")

    reason = pd.Series("", index=raw.index, dtype=object)
    checks = [(raw[c].str.strip() == "", f"빈칸: {c}") for c in ("사건ID", "요소", "묶음")]
    checks.append((dates.isna(), "날짜 형식"))
    checks.append((scores.isna(), "S 숫자 아님"))
    for mask, text in checks:
        reason[(reason == "") & mask.to_numpy()] = text
    unknown = (reason == "") & ~raw["묶음"].isin(KNOWN_BUNDLES).to_numpy()
    reason[unknown] = "묶음 모름: " + raw.loc[unknown, "묶음"].astype(object)

    valid = reason == ""
    dup = valid & raw.duplicated(subset=list(EVENT_COLUMNS), keep="first").to_numpy()
    # 6개 열이 같은 행은 유효·무효가 같으므로, 유효한 행 중 두 번째부터가 중복
    reason[dup] = "중복 행"
    valid = reason == ""

    kept = raw[valid.to_numpy()]
    clash = kept.groupby("사건ID", sort=False).size()
    clash = clash[clash > 1]
    if len(clash):
        raise ValueError(f"{path}: 같은 사건ID에 내용이 다른 행 — {list(clash.index[:10])}")

    excluded = raw[~valid.to_numpy()].copy()
    excluded["사유"] = reason[~valid].astype(str).to_numpy()
    excluded = excluded[list(EXCLUDED_COLUMNS)].reset_index(drop=True)

    events = kept.copy()
    events["date"] = dates[valid.to_numpy()].dt.normalize()
    events["S"] = scores[valid.to_numpy()].astype("float64")
    events = events.sort_values(["date", "사건ID"], kind="mergesort").reset_index(drop=True)
    return events[list(EVENT_COLUMNS)], excluded


def load_type4_table(path) -> pd.DataFrame:
    """물리사건 유형판정표를 읽고 검증한다. `4거유형`은 공백 제거·대문자(Y/N), `date`는 datetime64."""
    table = read_csv_kr(path, dtype=str, keep_default_na=False)
    _check_columns(table, TYPE4_COLUMNS, path)
    flag = table["4거유형"].str.strip().str.upper()
    bad = ~flag.isin(("Y", "N"))
    if bad.any():
        raise ValueError(f"{path}: 4거유형이 Y/N 밖 — {list(table.loc[bad, '사건ID'][:10])}")
    dup = table["사건ID"].duplicated(keep=False)
    if dup.any():
        raise ValueError(f"{path}: 사건ID 중복 — {sorted(set(table.loc[dup, '사건ID']))[:10]}")
    dates = pd.to_datetime(table["date"], format=DATE_FORMAT, errors="coerce")
    if dates.isna().any():
        raise ValueError(f"{path}: 날짜 형식 — {list(table.loc[dates.isna(), '사건ID'][:10])}")
    table = table.copy()
    table["4거유형"] = flag
    table["date"] = dates.dt.normalize()
    return table.reset_index(drop=True)


def type4_event_ids(table) -> frozenset[str]:
    """판정표에서 4거 유형(`4거유형` == "Y") 사건ID 집합."""
    flag = table["4거유형"].astype(str).str.strip().str.upper()
    return frozenset(table.loc[flag == "Y", "사건ID"].astype(str))


def check_type4_against_events(table, events) -> pd.DataFrame:
    """판정표를 사건표와 대조해 문제 행(열 `사건ID, 문제`)을 돌려준다. 빈 표면 문제 없음."""
    ev_dates = events.drop_duplicates("사건ID").set_index("사건ID")["date"]
    problems = []
    for _, r in table.iterrows():
        eid = r["사건ID"]
        if eid not in ev_dates.index:
            problems.append((eid, "사건표에 없음"))
        elif pd.Timestamp(r["date"]) != pd.Timestamp(ev_dates[eid]):
            problems.append((eid, f"날짜 다름(판정표 {pd.Timestamp(r['date']):%Y-%m-%d}, 사건표 {pd.Timestamp(ev_dates[eid]):%Y-%m-%d})"))
        if r["요소"] not in TYPE4_ELEMENTS:
            problems.append((eid, "요소가 A3·A7 아님"))
    return pd.DataFrame(problems, columns=["사건ID", "문제"])
