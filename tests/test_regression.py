"""v0.1.4 회귀(F3) — 로컬 사건표로 계산한 일별·요약이 tests/fixtures의 v0.1.4 기준과 같은지.

사건표(data/tension/events_*.csv)는 깃에 올리지 않으므로 없는 PC에서는 **실패**한다(사용자 10-29) — 실패 메시지에 만드는 법을 적는다.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import config
from utils.tension import core, io as tio

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
END = "2026-10-27"
SCEN = {"기본": ("기본", config.BUNDLES_BASE), "확장": ("확장(C5 포함)", config.BUNDLES_EXT)}
ROWS = {"기본": 720, "확장": 941}
INT_COLS = ["단계_T", "하한_물리", "하한_E5", "하한_사건", "단계_판정", "단계_최종"]
BOOL_COLS = ["잠정", "물리_4거유형일"]
STR_COLS = ["A2자료", "화면_단계문구"]
RAW_DIR = ROOT / "data" / "raw" / "긴장도_산출식_세부_기준"


def _events_path(name):
    return ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv"


def _missing():
    return [_events_path(n).relative_to(ROOT).as_posix() for n in SCEN if not _events_path(n).exists()]


def _missing_message(missing):
    raw = "있음" if RAW_DIR.exists() else "없음 — 팀 드라이브에서 받아 이 위치에 둔다"
    return (f"회귀 테스트 입력 사건표가 없다: {missing}\n"
            f"  사건표는 깃에 올리지 않는다(D1). 원자료 {RAW_DIR.relative_to(ROOT).as_posix()}/ : {raw}\n"
            f"  만들기: python scripts/build_events.py --end {END}  → 그다음 pytest 다시\n"
            f"  회귀만 빼고 돌리기: python -m pytest -m \"not regression\"")


def test_events_present():
    """사건표가 있어야 회귀가 돈다 — 없으면 이 테스트 하나가 원인과 만드는 법을 알리며 실패하고 나머지는 건너뛴다."""
    missing = _missing()
    if missing:
        pytest.fail(_missing_message(missing), pytrace=False)


@pytest.fixture(scope="module")
def computed():
    if _missing():
        pytest.skip("사건표 없음 — test_events_present의 실패 메시지 참고")
    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
    days = core.calc_days(config.CALC_START_DATE, END)
    out = {}
    for name, (_, bundles) in SCEN.items():
        events, excluded = tio.load_events(_events_path(name))
        daily, info = core.daily_table(events, days, bundles, type4)
        out[name] = {"events": events, "excluded": excluded, "daily": daily, "info": info}
    return {"days": days, "type4": type4, "res": out}


@pytest.fixture(scope="module")
def summary():
    return tio.read_csv_kr(FIX / "v014_요약.csv", index_col=0)


def _ref_daily(name):
    return tio.read_csv_kr(FIX / f"v014_일별_{name}.csv", index_col=0, parse_dates=True)


def _diff_cells(new, ref, tol=0.001):
    """열마다 (다른 칸 수, 처음 다른 날짜 5개). 실수 = |차| ≥ tol 또는 NaN 위치 다름 · 그 밖 = 값 다름(문자열 빈칸 = '')."""
    bad = {}
    for c in ref.columns:
        a, b = new[c], ref[c]
        if c in INT_COLS:
            m = a.to_numpy("int64") != b.to_numpy("int64")
        elif c in BOOL_COLS:
            m = a.to_numpy(bool) != b.to_numpy(bool)
        elif c in STR_COLS:
            m = a.fillna("").astype(str).to_numpy() != b.fillna("").astype(str).to_numpy()
        else:
            av, bv = a.to_numpy(float), b.to_numpy(float)
            m = (np.isnan(av) != np.isnan(bv)) | (np.abs(np.nan_to_num(av) - np.nan_to_num(bv)) >= tol)
        if m.any():
            bad[c] = (int(m.sum()), [f"{d:%Y-%m-%d}" for d in ref.index[m][:5]])
    return bad


def _summary_values(daily, info, days):
    """요약_v014.csv와 같은 이름의 값(F4 요약 함수가 생기기 전까지 테스트 안에서 계산)."""
    L = daily["단계_최종"]
    bm = core.base_mask(days)
    last = daily.iloc[-1]
    v = {"T구간(2·3·4·5거 시작)": "/".join(f"{x:g}" for x in info["cuts"]),
         "T구간_반올림전": "/".join(f"{x:.2f}" for x in info["quantiles_raw"]),
         "경계_x.5_주의": str(info["half_warning"]),
         **{f"B_{b}": round(float(x), 3) for b, x in info["B"].items()},
         **{f"{k}거%": round((L == k).mean() * 100, 1) for k in range(1, 6)},
         "바뀜/년": round((L.diff().fillna(0) != 0).sum() / (len(days) / 365.25), 1),
         "2018 평균단계": round(L.loc["2018"].mean(), 2), "2018 3거이상일": int((L.loc["2018"] >= 3).sum()),
         "2021 평균단계": round(L.loc["2021"].mean(), 2), "2023 4거이상%": round((L.loc["2023"] >= 4).mean() * 100, 0),
         "2023 5거%": round((L.loc["2023"] == 5).mean() * 100, 0), "현재(10-27)": int(L.iloc[-1]),
         "사건하한 날 수": int((daily["하한_사건"] == 3).sum()), "물리 4거유형 사건일 수": int(daily["물리_4거유형일"].sum()),
         "E5하한 3거↑ 날": int((daily["하한_E5"] >= 3).sum()),
         "E5가 판정을 올린 날": int((daily["하한_E5"] > daily[["단계_T", "하한_물리", "하한_사건"]].max(axis=1)).sum()),
         "물리하한 3거↑ 날": int((daily["하한_물리"] >= 3).sum()), "물리하한 4거↑ 날": int((daily["하한_물리"] >= 4).sum()),
         "물리하한 5거 날": int((daily["하한_물리"] == 5).sum()),
         "완화 상한에 붙은 날": int((info["components"]["delta"] >= config.RELIEF_CAP - 1e-12).sum()),
         "원점수 기준기간 평균": round(daily["원점수_게이지"][bm].mean(), 2),
         "T원값 최대": round(daily["T_원값"].max()), "표시선 최대": round(daily["T_표시7일"].max()),
         "현재 표시(잠정)": round(last["T_표시7일"], 1), "현재 그날까지 상위%": round(last["그날까지_상위%"], 1),
         "현재 원점수": round(last["원점수_게이지"], 1), "현재 14일 변화": round(last["변화14_표시"], 1),
         "현재 화면 단계": last["화면_단계문구"]}
    stages = core.crisis_window_max(L)
    marks = core.crisis_window_max(daily["원점수_게이지"])
    for name, _, _ in config.CRISIS_LIST:
        v[name] = int(stages[name])
        v[f"게이지_{name}"] = round(float(marks[name]), 1)
    return v


def _same(new, ref):
    return new == ref if isinstance(new, str) else float(new) == float(ref)


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_events_loaded(computed, name):
    r = computed["res"][name]
    assert len(r["excluded"]) == 0, r["excluded"].head()
    assert len(r["events"]) == ROWS[name]


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_daily_shape(computed, name):
    daily, ref = computed["res"][name]["daily"], _ref_daily(name)
    assert list(daily.columns) == list(ref.columns)
    assert daily.index.name == "날짜" and len(daily) == 6144
    assert np.array_equal(daily.index.to_numpy(), ref.index.to_numpy())


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_daily_all_columns_match_v014(computed, name):
    bad = _diff_cells(computed["res"][name]["daily"], _ref_daily(name))
    assert not bad, f"v0.1.4와 다른 열(칸 수, 처음 날짜): {bad}"


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_completion_criteria(computed, name):
    """지시서 0절 완료 기준 — 단계_최종 다른 날 0, T_원값 최대 절대차 < 0.001."""
    daily, ref = computed["res"][name]["daily"], _ref_daily(name)
    assert int((daily["단계_최종"].to_numpy() != ref["단계_최종"].to_numpy()).sum()) == 0
    assert float((daily["T_원값"] - ref["T_원값"]).abs().max()) < 0.001


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_summary_matches_v014(computed, summary, name):
    r = computed["res"][name]
    got = _summary_values(r["daily"], r["info"], computed["days"])
    ref = summary[SCEN[name][0]]
    wrong = {k: (v, ref[k]) for k, v in got.items() if not _same(v, ref[k])}
    assert not wrong, f"요약 값이 다름(새 값, 기준): {wrong}"


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_end_extension_keeps_past(computed, name):
    r, days = computed["res"][name], computed["days"]
    longer, _ = core.daily_table(r["events"], core.calc_days(config.CALC_START_DATE, "2026-11-10"), SCEN[name][1], computed["type4"])
    assert longer.loc[days].drop(columns="잠정").equals(r["daily"].drop(columns="잠정"))
    assert int((longer.loc[days, "잠정"] != r["daily"]["잠정"]).sum()) == config.PROVISIONAL_DAYS


def test_run_tension_output_matches_v014(computed):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", END], cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    for name in SCEN:
        out = ROOT / config.TENSION_DATA_DIR / "_check" / f"일별_{name}.csv"
        raw = out.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
        got = tio.read_csv_kr(out, index_col=0, parse_dates=True)
        assert list(got.columns) == list(_ref_daily(name).columns)
        assert not _diff_cells(got, _ref_daily(name), tol=0.001 + 1e-9)
