"""F6 테스트 — 비교선 T_basic(⑮′) · GPR 읽기·비교 · 반감기 민감도 · 유사 시기 주요 사건 · 그림.

합성 자료 테스트는 사건표 없이 돈다. 화면 통로 테스트는 커밋된 결과(data/tension)를 읽는다(test_screen.py와 같음).
run_tension 출력 테스트는 사건표가 필요해 regression 표시.
"""
import subprocess
import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

import config
from tests.test_core import base_events, ev
from utils.tension import charts, core, io as tio, screen, summary as sm

ROOT = screen.ROOT
DATA = ROOT / config.TENSION_DATA_DIR
DAYS = core.calc_days("2010-01-01", "2020-12-31")
MASK = core.base_mask(DAYS)


# ⑮′ 비교선
def test_basic_index_equals_T_when_baselines_equal():
    """묶음 평소값이 모두 같으면 정규화 효과가 없다 → T_basic = T(정의 확인)."""
    rows = []
    for y in range(2010, 2021):
        for m in range(1, 13):
            d = f"{y}-{m:02d}-01"
            for i, (b, e) in enumerate([("핵·미사일", "A2"), ("군사 과시", "A4"), ("위협 언어·교리", "C1")]):
                rows.append((f"{e}-{y}{m:02d}", d, e, b, 2.0 + (m % 3), "합성"))
            rows.append((f"F2-{y}{m:02d}", d, "F2", "완화", 1.0, "합성"))
    comp, B = core.tension_components(ev(rows), DAYS, config.BUNDLES_BASE)
    assert B[list(config.BUNDLES_BASE)].nunique() == 1
    tb = core.basic_index(comp, config.BUNDLES_BASE, MASK)
    assert float((tb - comp["T"]).abs().max()) < 1e-9


def test_basic_index_formula_and_relief():
    comp, _ = core.tension_components(base_events(), DAYS, config.BUNDLES_BASE)
    R = sum(comp[f"R_{b}"] for b in config.BUNDLES_BASE)
    expect = 100 * R / R[MASK].mean() * (1 - comp["delta"])
    tb = core.basic_index(comp, config.BUNDLES_BASE, MASK)
    assert float((tb - expect).abs().max()) < 1e-12
    assert abs(float((100 * R / R[MASK].mean())[MASK].mean()) - 100) < 1e-9   # 할인 전 기준기간 평균 = 100
    assert (tb >= 0).all()


def test_basic_index_stops_when_base_zero():
    comp, _ = core.tension_components(base_events(), DAYS, config.BUNDLES_BASE)
    zero = comp.copy()
    for b in config.BUNDLES_BASE:
        zero[f"R_{b}"] = 0.0
    with pytest.raises(ValueError, match="0 이하"):
        core.basic_index(zero, config.BUNDLES_BASE, MASK)


# 반감기 민감도(집계)
def test_half_life_table_rows_and_ref():
    events = base_events()
    runs = {h: core.daily_table(events, DAYS, config.BUNDLES_BASE, frozenset(), {"half_life": h, "kill_ids": ()}) for h in (7, 14, 30)}
    crises = config.CRISIS_LIST[:6]                                  # 합성 기간(~2020) 안의 위기만
    t = sm.half_life_table(runs, 14, crises)
    assert list(t.columns[:len(sm.HALF_LIFE_COLUMNS)]) == list(sm.HALF_LIFE_COLUMNS)
    assert list(t.columns[len(sm.HALF_LIFE_COLUMNS):]) == [n for n, _, _ in crises] + ["현재"]
    assert t["반감기"].tolist() == [7, 14, 30]
    ref = t.set_index("반감기").loc[14]
    assert ref["기준 반감기와 단계 같은 날%"] == 100.0 and ref["한 단계 안%"] == 100.0
    assert t[[f"{k}거%" for k in range(1, 6)]].sum(axis=1).between(99.8, 100.2).all()
    with pytest.raises(ValueError, match="기준 반감기"):
        sm.half_life_table({7: runs[7]}, 14, crises)


# GPR 읽기
def _gpr_file(tmp_path, lines, header="month,GPRC_KOR,GPRHC_KOR"):
    p = tmp_path / "gpr.csv"
    p.write_text("\n".join([header, *lines]) + "\n", encoding="utf-8-sig")
    return p


def test_load_gpr_monthly_ok(tmp_path):
    g = tio.load_gpr_monthly(_gpr_file(tmp_path, ["2010-02,0.2,0.3", "2010-01,0.1,0.2"]))
    assert list(g.columns) == ["연월", "GPR"] and g["연월"].tolist() == ["2010-01", "2010-02"]
    assert g["GPR"].tolist() == [0.1, 0.2]


@pytest.mark.parametrize("lines, header, msg", [
    (["2010-1,0.1,0.2"], "month,GPRC_KOR,GPRHC_KOR", "형식"),
    (["2010-01,0.1,0.2", "2010-01,0.2,0.2"], "month,GPRC_KOR,GPRHC_KOR", "중복"),
    (["2010-01,,0.2"], "month,GPRC_KOR,GPRHC_KOR", "빈 값"),
    (["2010-01,0.1"], "month,GPRC_KOR", "열 이름"),
])
def test_load_gpr_monthly_stops(tmp_path, lines, header, msg):
    with pytest.raises(ValueError, match=msg):
        tio.load_gpr_monthly(_gpr_file(tmp_path, lines, header))


def test_gpr_file_is_committed_copy():
    """data/tension/GPR_한국_월별.csv = 채점 v0 입력 그대로(2010-01~2026-09, 201달)."""
    g = screen.gpr_monthly()
    assert g["연월"].iloc[0] == "2010-01" and len(g) >= 201
    assert g.set_index("연월").loc["2026-09", "GPR"] == pytest.approx(0.2808381915092468, abs=1e-15)


# 화면 통로(커밋된 결과)
@pytest.mark.parametrize("scenario", ["기본", "확장"])
def test_basic_line_matches_daily(scenario):
    b = screen.basic_line(scenario)
    d = screen.daily_raw(scenario)
    assert len(b) == len(d) and b["날짜"].tolist() == list(d.index)
    assert list(b.columns) == ["날짜", "T_원값", "T_표시7일", "T_basic", "T_basic_표시7일", "차이_표시7일"]
    assert (b["T_basic"] >= 0).all()
    st = screen.basic_stats(scenario).set_index("항목")["값"]
    assert float(st["주 지수(T)와 상관"]) > 0.99            # 10-29: 상승 묶음 평소값이 비슷해 정규화 효과가 작음


@pytest.mark.parametrize("scenario", ["기본", "확장"])
def test_gpr_compare(scenario):
    t = screen.gpr_compare(scenario)
    assert list(t.columns) == ["연월", "봉수_T평균", "GPR", "봉수_순위%", "GPR_순위%", "순위차"]
    assert t["연월"].is_monotonic_increasing and t["연월"].iloc[0] == "2010-01"
    assert t["연월"].iloc[-1] == screen.gpr_monthly()["연월"].iloc[-1]
    for c in ("봉수_순위%", "GPR_순위%"):
        assert t[c].between(0, 100).all()
    m = screen.monthly(scenario).set_index("연월")["T_평균"]
    assert (t.set_index("연월")["봉수_T평균"] == m.loc[t["연월"]]).all()
    st = screen.gpr_stats(scenario).set_index("항목")["값"]
    assert st["달 수"] == str(len(t)) and -1 <= float(st["피어슨 상관"]) <= 1


def test_gpr_2018_note_direction():
    """판독문 셋째 줄(2018 정상회담기 GPR 높음·봉수 낮음)이 지금 결과와 맞는지."""
    t = screen.gpr_compare("기본").set_index("연월")
    y2018 = t.loc["2018-03":"2018-10"]
    assert (y2018["순위차"] < 0).all()
    assert len(screen.GPR_NOTES) == 3 and screen.GPR_NOTES[:2] == screen.READING_NOTES[2:4]


@pytest.mark.parametrize("scenario", ["기본", "확장"])
def test_half_life_screen_table(scenario):
    t = screen.half_life_table(scenario)
    assert t["반감기"].tolist() == list(config.HALF_LIFE_SENSITIVITY)
    ref = t.set_index("반감기").loc[config.HALF_LIFE_DAYS]
    s = screen.summary()[screen.SUMMARY_COLUMN[scenario]]
    assert ref["T구간(2·3·4·5거 시작)"] == s["T구간(2·3·4·5거 시작)"]
    for k in range(1, 6):
        assert float(ref[f"{k}거%"]) == float(s[f"{k}거%"])
    for name, _, _ in config.CRISIS_LIST:
        assert int(ref[name]) == int(s[name])
    assert "7·21·30일" in screen.HALF_LIFE_NOTE[-1]


def test_month_events():
    e = screen.month_events("2017-09")
    assert list(e.columns) == ["날짜", "사건ID", "요소", "묶음", "구분", "S", "주체국", "사건명"]
    assert len(e) == 3 and e["S"].is_monotonic_decreasing
    assert e["사건ID"].iloc[0] == "A1-2058"                          # 6차 핵실험
    assert (e["날짜"].dt.strftime("%Y-%m") == "2017-09").all()
    assert set(screen.month_events("2010-03", top=10)["구분"]) <= {"상승", "완화(할인)", "하한 대상", "표시만"}
    assert screen.month_events("2009-01").empty


# 그림
def test_figures(tmp_path):
    f1 = screen.normalization_figure("기본")
    f2 = screen.gpr_figure("기본")
    assert isinstance(f1, go.Figure) and isinstance(f2, go.Figure)
    assert [t.name for t in f1.data] == ["주 지수(묶음별 평소 대비) 7일 평균", "비교선 T_basic(단순 합) 7일 평균",
                                         "차이(T_basic − 주 지수)"]
    assert [t.name for t in f2.data] == ["봉수 월평균 T 순위%", "GPR 한국 순위%"]
    assert list(f2.layout.yaxis.range) == [0, 100]
    for name, fig in (("norm", f1), ("gpr", f2)):
        assert charts.save_html(fig, tmp_path / f"{name}.html").stat().st_size > 1000


# run_tension 출력(사건표 필요)
@pytest.mark.regression
def test_run_tension_writes_f6_files(tmp_path):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", "2026-10-27", "--out", str(tmp_path)],
                       cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    b = tio.read_csv_kr(tmp_path / "비교선_일별.csv")
    assert list(b.columns) == ["시나리오", "날짜", "T_basic", "T_basic_표시7일"]
    assert b.groupby("시나리오").size().to_dict() == {"기본": 6144, "확장": 6144}
    raw = (tmp_path / "비교선_일별.csv").read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
    h = tio.read_csv_kr(tmp_path / "반감기_민감도.csv")
    assert list(h.columns[:2]) == ["시나리오", "반감기"] and len(h) == 2 * len(config.HALF_LIFE_SENSITIVITY)
    # 반감기 14일 행 = v0.1.4 요약(회귀 기준)과 같은 1~5거%·위기 단계
    ref = tio.read_csv_kr(ROOT / "tests" / "fixtures" / "v014_요약.csv", index_col=0, dtype=str, keep_default_na=False)
    for scenario, col in screen.SUMMARY_COLUMN.items():
        r = h[(h["시나리오"] == scenario) & (h["반감기"] == config.HALF_LIFE_DAYS)].iloc[0]
        assert r["T구간(2·3·4·5거 시작)"] == ref.loc["T구간(2·3·4·5거 시작)", col]
        assert all(float(r[f"{k}거%"]) == float(ref.loc[f"{k}거%", col]) for k in range(1, 6))
        assert all(int(r[n]) == int(ref.loc[n, col]) for n, _, _ in config.CRISIS_LIST)
    # 비교선 = 사건표로 다시 계산한 ⑮′(기본, 3자리 반올림 안)
    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
    days = core.calc_days(config.CALC_START_DATE, "2026-10-27")
    events, _ = tio.load_events(DATA / "events_기본.csv")
    _, info = core.daily_table(events, days, config.BUNDLES_BASE, type4)
    tb = core.basic_index(info["components"], config.BUNDLES_BASE, core.base_mask(days))
    got = b[b["시나리오"] == "기본"]["T_basic"].to_numpy()
    assert float(np.abs(got - tb.to_numpy()).max()) <= 0.0005 + 1e-9
