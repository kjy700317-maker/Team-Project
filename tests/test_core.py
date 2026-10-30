"""core.py 단위 테스트(F3) — 작은 합성 자료로 식 ②~⑰과 멈춤 규칙을 고정한다. 사건표·원자료 없이 돈다."""
import numpy as np
import pandas as pd
import pytest

import config
from utils.tension import core

DOT = "·"


def ev(rows):
    """(사건ID, date, 요소, 묶음, S, 사건명) 목록 → io.load_events와 같은 모양의 사건표."""
    df = pd.DataFrame(rows, columns=["사건ID", "date", "요소", "묶음", "S", "사건명"])
    df["date"] = pd.to_datetime(df["date"])
    df["S"] = df["S"].astype(float)
    return df


def s(values, start="2020-01-01"):
    return pd.Series(values, index=pd.date_range(start, periods=len(values), freq="D"), dtype=float)


def base_events(first_year=2010, last_year=2020):
    """기준기간을 채우는 합성 사건표 — 상승 3묶음·완화를 매달 1일에 한 건씩."""
    rows = []
    for y in range(first_year, last_year + 1):
        for m in range(1, 13):
            d = f"{y}-{m:02d}-01"
            for i, (b, e, sc) in enumerate([("핵·미사일", "A2", 5.0), ("군사 과시", "B2", 3.0),
                                            ("위협 언어·교리", "C1", 4.0), ("완화", "F2", 1.0)]):
                rows.append((f"{e}-{y}{m:02d}{i}", d, e, b, sc + (m % 3), "합성"))
    return ev(rows)


# ③ 감쇠
def test_decay_half_life():
    r = core.decay_cumulative(s([1.0] + [0.0] * 14))
    assert r.iloc[0] == 1.0
    assert abs(r.iloc[14] - 0.5) < 1e-12


def test_decay_accumulates_from_zero():
    lam = 2 ** (-1 / 14)
    r = core.decay_cumulative(s([1.0, 1.0]))
    assert r.tolist() == pytest.approx([1.0, 1.0 + lam], abs=1e-15)


# ⑩ 반가우스 창
def test_half_gauss_window_weights():
    r = core.half_gauss_window(s([1.0] + [0.0] * 30))
    assert r.iloc[0] == 1.0
    assert abs(r.iloc[10] - np.exp(-0.5)) < 1e-12
    assert abs(r.iloc[29] - np.exp(-841 / 200)) < 1e-15
    assert r.iloc[30] == 0.0


# ④~⑧
def test_relative_rising_relief_tension():
    idx = pd.date_range("2020-01-01", periods=1)
    R = pd.DataFrame({"a": [2.0], "b": [4.0]}, index=idx)
    Tg = core.relative_index(R, pd.Series({"a": 1.0, "b": 2.0}))
    assert Tg.iloc[0].tolist() == [200.0, 200.0]
    T_plus = core.rising_index(Tg)
    delta = core.relief_discount(pd.Series([10.0], index=idx), 1.0)
    assert (T_plus.iloc[0], delta.iloc[0]) == (200.0, 0.5)       # c·R/B = 1.0 → 상한 0.5
    assert core.tension_index(T_plus, delta).iloc[0] == 100.0


# ⑨ 구간
@pytest.mark.parametrize("values, cut, warn", [([114, 115], 114, True), ([115, 116], 116, True), ([115, 115.4], 115, False)])
def test_stage_cuts_round_half_even(values, cut, warn):
    T = pd.Series(values, dtype=float)
    cuts, q = core.stage_cuts(T, np.array([True] * len(values)), quantiles=(0.5, 0.5, 0.5, 0.5))
    assert cuts[0] == cut
    assert core.cuts_half_warning(q) is warn


def test_cuts_half_warning_float_tolerance():
    assert core.cuts_half_warning([256.49999999999997]) is True
    assert core.cuts_half_warning([256.4, 115.27]) is False


def test_stage_from_index_boundaries():
    T = pd.Series([114.999999999, 115, 255.99, 256, 315, 378, 1000, 0])
    assert core.stage_from_index(T, (115, 256, 315, 378)).tolist() == [1, 2, 2, 3, 4, 5, 5, 1]


# ⑪⑫
def test_judge_is_max():
    a, b, c, d = (pd.Series(x) for x in ([1, 3], [2, 1], [1, 1], [4, 1]))
    out = core.judge(a, b, c, d)
    assert out.tolist() == [4, 3] and out.dtype == "int64"


def test_step_down_one_stage_per_seven_days():
    L = core.step_down(pd.Series([5] + [1] * 30))
    assert L.tolist() == [5] * 7 + [4] * 7 + [3] * 7 + [2] * 7 + [1] * 3


def test_step_down_wait_continues_through_lower_judgement():
    J = pd.Series([3, 5, 1, 1, 1, 1, 1, 1, 4, 1])
    assert core.step_down(J).tolist() == [3, 5, 5, 5, 5, 5, 5, 5, 4, 4]


def test_step_down_rises_immediately_and_n_param():
    assert core.step_down(pd.Series([1, 3, 1, 1, 1, 1]), n=3).tolist() == [1, 3, 3, 3, 2, 2]


# ⑬⑭⑯⑰
def test_display_ma_first_days_partial():
    assert core.display_ma(s([7, 0, 0, 0, 0, 0, 0, 0])).tolist() == pytest.approx([7, 3.5, 7 / 3, 1.75, 1.4, 7 / 6, 1.0, 0.0])


def test_cumulative_top_pct_ties_are_le():
    assert core.cumulative_top_pct(s([0, 0, 0, 5, 5, 1])).tolist() == pytest.approx([0, 0, 0, 0, 0, 100 / 3])


@pytest.mark.parametrize("prev, pct_nan", [(50.0, False), (49.999, True)])
def test_trend_pct_min(prev, pct_nan):
    tr = core.trend(s([prev] + [0.0] * 13 + [60.0]))
    assert list(tr.columns) == ["변화14_표시", "변화율14_표시"]
    assert tr["변화14_표시"].iloc[14] == pytest.approx(60.0 - prev)
    assert bool(np.isnan(tr["변화율14_표시"].iloc[14])) is pct_nan
    if not pct_nan:
        assert tr["변화율14_표시"].iloc[14] == pytest.approx(20.0)


def test_stage_label_wording():
    out = core.stage_label(pd.Series([2, 3]), pd.Series([1, 3])).tolist()
    assert out == [f"2거 {DOT} 하강 중(판정 1거)", "3거"]


# 보조 열
def test_provisional_last_six_days():
    days = pd.date_range("2020-01-01", periods=10)
    assert core.provisional(days).tolist() == [False] * 4 + [True] * 6


def test_a2_note_after_end():
    out = core.a2_note(pd.DatetimeIndex(["2024-11-05", "2024-11-06"])).tolist()
    assert out == ["", "A2 자료 없음(2024-11-05까지)"]


def test_relief_display_zero_when_rising_zero():
    T = pd.Series([0.0, 50.0])
    Tg = pd.DataFrame({"a": [0.0, 100.0], "b": [0.0, 100.0]})
    assert core.relief_display(T, Tg).tolist() == [0.0, 0.5]


def test_raw_gauge_and_crisis_window():
    idx = pd.date_range("2020-01-01", periods=10)
    comp = pd.DataFrame({"R_a": np.arange(10.0), "R_b": np.ones(10)}, index=idx)
    g = core.raw_gauge(comp, ["a", "b"])
    assert g.tolist() == list(np.arange(10.0) + 1)
    m = core.crisis_window_max(g, crises=[("x", "2020-01-02", "")], window_days=3)
    assert m["x"] == 5.0                                            # 01-02~01-05 양 끝 포함


# ⑩ 하한
PHYS = "물리 충돌"


def test_floor_physical_rules():
    days = pd.date_range("2020-01-01", "2020-03-31")
    e = ev([("A3-1", "2020-01-05", "A3", PHYS, 3.0, "Trash balloon"), ("A3-2", "2020-01-05", "A3", PHYS, 3.2, "BALLOON"),
            ("A3-3", "2020-02-01", "A3", PHYS, 3.4, "Balloon launch"),
            ("A7-1", "2020-03-01", "A7", PHYS, 7.2, "포격")])
    fp = core.floor_physical(e, days, set(), kill_ids=())
    assert fp["2020-01-05"] == 3                                    # 풍선 같은 날 6.2 ≥ 6
    assert fp["2020-02-01"] == 1                                    # 풍선 1건 3.4
    assert (fp["2020-03-01":"2020-03-03"] == 4).all() and fp["2020-03-04"] == 3
    assert (fp["2020-03-04":"2020-03-14"] == 3).all() and fp["2020-03-15"] == 1


def test_floor_physical_type4_and_kill():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("A3-9", "2020-01-10", "A3", PHYS, 3.88, "침범"), ("A7-9", "2020-01-20", "A7", PHYS, 7.2, "침몰")])
    fp = core.floor_physical(e, days, {"A3-9", "A7-9"}, kill_ids=("A7-9",))
    assert fp["2020-01-10"] == 4 and fp["2020-01-11"] == 3        # 4거 유형일은 그날만 ≥ 4
    assert fp["2020-01-20"] == 5 and fp["2020-01-21"] == 4        # 사망·침몰일 5가 4거 유형보다 먼저
    assert core.type4_days(e, days, {"A3-9"}).sum() == 1


def test_floor_e5_and_event():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("E5-1", "2020-01-02", "E5", "북러 밀착", 4.0, "a"), ("E5-2", "2020-01-20", "E5", "북러 밀착", 10.0, "b"),
            ("A2-1", "2020-01-05", "A2", "핵·미사일", 7.5, "ICBM"), ("A2-2", "2020-01-06", "A2", "핵·미사일", 7.4999, "IRBM"),
            ("A1-1", "2020-01-07", "A1", "핵·미사일", 0.0, "핵실험")])
    fe = core.floor_e5(e, days)
    assert (fe["2020-01-02"], fe["2020-01-20"]) == (3, 4)
    fs = core.floor_event(e, days)
    assert (fs["2020-01-05"], fs["2020-01-06"], fs["2020-01-07"]) == (3, 1, 3)


def test_id_arguments_checked():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("A3-9", "2020-01-10", "A3", PHYS, 3.88, "침범")])
    with pytest.raises(TypeError):
        core.type4_days(e, days, "A3-9")
    with pytest.raises(TypeError):
        core.floor_physical(e, days, set(), kill_ids="A3-9")
    with pytest.raises(ValueError, match="A3-0"):
        core.type4_days(e, days, {"A3-0"})
    with pytest.raises(ValueError, match="사망"):
        core.floor_physical(e, days, set(), kill_ids=("A7-0",))


# 조립·멈춤 규칙 (F2-3)
B3 = config.BUNDLES_BASE
NOKILL = {"kill_ids": ()}


def test_daily_table_shape_and_purity():
    e = base_events()
    before = e.copy()
    days = core.calc_days("2010-01-01", "2020-12-31")
    d, info = core.daily_table(e, days, B3, set(), NOKILL)
    assert list(d.columns) == core.daily_columns(B3) and len(d.columns) == 20 and d.index.name == "날짜"
    assert all(d[c].dtype == "int64" for c in ["단계_T", "하한_물리", "하한_E5", "하한_사건", "단계_판정", "단계_최종"])
    assert d["잠정"].dtype == bool and d["물리_4거유형일"].dtype == bool
    assert e.equals(before)
    assert set(info) == {"B", "cuts", "quantiles_raw", "half_warning", "components", "params"}


@pytest.mark.parametrize("end", ["2019-12-30", "2015-06-30"])
def test_end_before_base_end_stops(end):
    with pytest.raises(ValueError, match="기준기간"):
        core.daily_table(base_events(), core.calc_days("2010-01-01", end), B3, set(), NOKILL)


def test_missing_relief_stops():
    e = base_events()
    with pytest.raises(ValueError, match="완화"):
        core.daily_table(e[e["묶음"] != "완화"], core.calc_days("2010-01-01", "2020-12-31"), B3, set(), NOKILL)


def test_first_cut_nonpositive_stops():
    with pytest.raises(ValueError, match="첫 문턱"):
        core.daily_table(base_events(2018, 2020), core.calc_days("2010-01-01", "2020-12-31"), B3, set(), NOKILL)


def test_params_none_empty_and_unknown():
    e, days = base_events(), core.calc_days("2010-01-01", "2020-12-31")
    d0, _ = core.daily_table(e, days, B3, set(), NOKILL)
    d1, _ = core.daily_table(e, days, B3, set(), {"kill_ids": (), "half_life": config.HALF_LIFE_DAYS})
    assert d0.equals(d1)
    d2, _ = core.daily_table(e, days, B3, set(), {"kill_ids": (), "half_life": 7})
    assert not d2["T_원값"].equals(d0["T_원값"])
    with pytest.raises(ValueError, match="halflife"):
        core.daily_table(e, days, B3, set(), {"halflife": 7})


def test_calc_days_end_none_is_today():
    assert core.calc_days("2026-01-01", None)[-1] == pd.Timestamp.today().normalize()


# F7(F2 검토 발견 10) — 오물풍선 단어·A2 문구는 config, T 구간 문턱은 4개
@pytest.mark.parametrize("n", [0, 3, 5])
def test_stage_from_index_needs_four_cuts(n):
    with pytest.raises(ValueError, match="4개"):
        core.stage_from_index(pd.Series([1.0, 2.0]), tuple(range(1, n + 1)))


@pytest.mark.parametrize("n", [3, 5])
def test_stage_cuts_needs_four_quantiles(n):
    with pytest.raises(ValueError, match="4개"):
        core.stage_cuts(pd.Series([1.0, 2.0, 3.0]), np.array([True] * 3), quantiles=tuple(np.linspace(0.1, 0.9, n)))


def test_daily_table_three_quantiles_stops():
    e, days = base_events(), core.calc_days("2010-01-01", "2020-12-31")
    with pytest.raises(ValueError, match="4개"):
        core.daily_table(e, days, B3, set(), {**NOKILL, "quantiles": (0.7, 0.9, 0.95)})


def test_balloon_keyword_and_a2_note_come_from_config(monkeypatch):
    days = pd.date_range("2020-01-25", "2020-02-10")
    e = ev([("A3-3", "2020-02-01", "A3", PHYS, 3.4, "Balloon launch")])
    assert core.floor_physical(e, days, set(), kill_ids=())["2020-02-01"] == 1       # 풍선 1건 3.4 < 6
    monkeypatch.setattr(config, "BALLOON_KEYWORD", "Kite")
    assert core.floor_physical(e, days, set(), kill_ids=())["2020-02-01"] == 3       # 풍선으로 안 보면 일반 물리 ρ 3.4 ≥ 3
    monkeypatch.setattr(config, "A2_NOTE", "자료 끝({end})")
    assert core.a2_note(pd.DatetimeIndex(["2024-11-06"])).tolist() == ["자료 끝(2024-11-05)"]
