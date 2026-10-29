"""v0.1.4 회귀(F3·F4) — 사건표로 계산한 일별·요약·연도별이 tests/fixtures의 v0.1.4 기준과 같은지.

사건표(data/tension/events_기본·확장.csv)는 F4부터 커밋한다(사용자 10-29). 그래도 없으면 **실패**한다 — 실패 메시지에 만드는 법을 적는다.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import config
from utils.tension import core, io as tio, summary as sm

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
            f"  사건표는 커밋된다(F4) — git pull로 받거나 원자료로 만든다. 원자료 {RAW_DIR.relative_to(ROOT).as_posix()}/ : {raw}\n"
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


def _summary_csv(computed, tmp_path, input_names=None):
    """summary.py로 만든 요약을 CSV로 쓰고 문자열로 다시 읽는다(기준 파일과 글자 그대로 비교)."""
    cols = {}
    for name, (label, bundles) in SCEN.items():
        r = computed["res"][name]
        inp = (input_names or {}).get(name, f"events_{name}.csv")
        cols[label] = sm.summary_values(r["daily"], r["info"], computed["days"], bundles, input_name=inp,
                                        n_type4=len(computed["type4"]))
    out = tmp_path / "요약.csv"
    tio.write_csv(sm.summary_table(cols), out, index=True)
    return out


def _read_str(path):
    return tio.read_csv_kr(path, index_col=0, dtype=str, keep_default_na=False)


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


def test_summary_matches_v014(computed, tmp_path):
    """요약 = v0.1.4 요약과 행 이름·순서·값이 글자 그대로 같다(입력 행만 파일 이름이 다름)."""
    got = _read_str(_summary_csv(computed, tmp_path))
    ref = _read_str(FIX / "v014_요약.csv")
    assert list(got.index) == list(ref.index) and list(got.columns) == list(ref.columns)
    diff = got.drop(index="입력").compare(ref.drop(index="입력"))
    assert diff.empty, f"요약이 다름:\n{diff}"
    assert list(got.loc["입력"]) == ["events_기본.csv", "events_확장.csv"]


def test_summary_bytes_match_v014(computed, tmp_path):
    """입력 이름을 v0.1.4와 같게 주면 요약 CSV가 바이트까지 같다(인코딩·줄바꿈·숫자 표기)."""
    out = _summary_csv(computed, tmp_path, {"기본": "사건표_v014_기본.csv", "확장": "사건표_v014_확장.csv"})
    assert out.read_bytes() == (FIX / "v014_요약.csv").read_bytes()


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_yearly_matches_v014(computed, name):
    """연도별 = v0.1.4 연도별_v014(T원값_평균·평균단계·사거이상일·오거일)."""
    y = sm.period_table(computed["res"][name]["daily"], "연")
    ref = tio.read_csv_kr(FIX / f"v014_연도별_{name}.csv")
    assert y["연도"].tolist() == ref["연도"].tolist()
    assert float((y["T_평균"] - ref["T원값_평균"]).abs().max()) <= 0.0051   # 기준은 2자리, 새 값은 3자리
    assert y["단계_평균"].tolist() == ref["평균단계"].tolist()
    assert (y["4거일"] + y["5거일"]).tolist() == ref["사거이상일"].tolist()
    assert y["5거일"].tolist() == ref["오거일"].tolist()


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_end_extension_keeps_past(computed, name):
    r, days = computed["res"][name], computed["days"]
    longer, _ = core.daily_table(r["events"], core.calc_days(config.CALC_START_DATE, "2026-11-10"), SCEN[name][1], computed["type4"])
    assert longer.loc[days].drop(columns="잠정").equals(r["daily"].drop(columns="잠정"))
    assert int((longer.loc[days, "잠정"] != r["daily"]["잠정"]).sum()) == config.PROVISIONAL_DAYS


def test_run_tension_output_matches_v014(computed, tmp_path):
    """run_tension.py --end 2026-10-27 --out <임시> → 일별 2개·요약·월별·연도별이 v0.1.4와 맞는다."""
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", END, "--out", str(tmp_path)],
                       cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    for name in SCEN:
        out = tmp_path / f"일별_{name}.csv"
        raw = out.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
        assert raw == (FIX / f"v014_일별_{name}.csv").read_bytes()
    got, ref = _read_str(tmp_path / "요약.csv"), _read_str(FIX / "v014_요약.csv")
    assert got.drop(index="입력").equals(ref.drop(index="입력"))
    for fname, n in (("월별.csv", 2 * 202), ("연도별.csv", 2 * 17)):
        t = tio.read_csv_kr(tmp_path / fname)
        assert list(t.columns) == ["시나리오", "연월" if fname == "월별.csv" else "연도", *sm.PERIOD_COLUMNS]
        assert len(t) == n and t.groupby("시나리오")["일수"].sum().to_dict() == {"기본": 6144, "확장": 6144}
