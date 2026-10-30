"""가정 바꿔 보기(F8, ADR-019) 테스트 — 반감기·완화 c·κ·묶음 비중을 바꾼 재계산. 모두 기본값이면 공식 결과와 같아야 한다."""
import numpy as np
import pandas as pd
import pytest

import config
from utils.tension import core, screen

B3 = list(config.BUNDLES_BASE)


@pytest.fixture(scope="module")
def official():
    return screen.daily("기본")


@pytest.mark.parametrize("scenario", ["기본", "확장"])
def test_default_equals_official(scenario):
    view, table, meta = screen.recompute(scenario=scenario)
    assert view.equals(screen.daily(scenario))                       # 열·값·자료형까지 공식 결과와 같음
    assert meta["공식과_같음"] and meta["같은날%"] == 100.0 and meta["구간"] == screen.cuts(scenario)
    assert (table["공식"] == table["내 설정"]).all()


def test_equal_multipliers_are_default(official):
    view, _, meta = screen.recompute(weights={b: 2 for b in B3})
    assert view.equals(official) and meta["공식과_같음"]
    assert meta["비중%"] == {b: 33.3 for b in B3}


def test_core_equal_weights_take_current_path():
    raw = screen.daily_raw("기본")
    events, type4 = screen._recompute_inputs("기본", screen.DATA_DIR)
    days = pd.DatetimeIndex(raw.index)
    a, _ = core.daily_table(events, days, B3, type4)
    b, _ = core.daily_table(events, days, B3, type4, {"bundle_weights": {x: 1.5 for x in B3}})
    assert a.equals(b)                                                # 같은 배수 = 지금 경로(합 ÷ 개수) 그대로
    assert "bundle_weights" in core.PARAM_KEYS


def test_slider_values_recut_stages():
    _, table, meta = screen.recompute(21, 0.2, 0.3)
    assert meta["구간"] == (111, 251, 302, 342) and not meta["공식과_같음"]   # 10-30 측정값(ADR-018 규칙으로 다시 뽑음)
    assert table.set_index("항목").loc["단계 구간(2·3·4·5거 시작)", "공식"] == "115/256/315/378"


def test_weights_change_t_plus(official):
    view, _, meta = screen.recompute(weights={"핵·미사일": 2})
    assert meta["비중%"] == {"핵·미사일": 50.0, "군사 과시": 25.0, "위협 언어·교리": 25.0}
    assert not meta["공식과_같음"] and meta["구간"] != screen.cuts("기본")
    tg = view[[f"Tg_{b}" for b in B3]].to_numpy()
    t_plus = (2 * tg[:, 0] + tg[:, 1] + tg[:, 2]) / 4                    # T⁺ = Σ(배수·T_g) ÷ Σ배수
    T = t_plus * (1 - view["완화할인_δ"].to_numpy())
    assert (np.abs(T - view["T_원값"].to_numpy()) <= 0.0006 * t_plus + 0.002).all()   # 반올림(3자리, δ×T⁺) 차이만
    on = t_plus > 0                                                     # 완화할인 표시 열도 가중 T⁺ 기준
    assert np.abs(view.loc[on, "완화할인"].to_numpy() - view.loc[on, "완화할인_δ"].to_numpy()).max() < 0.0011   # T⁺ > 0이면 δ와 같음
    assert view["원점수_게이지"].equals(official["원점수_게이지"])          # 원점수 게이지(R 합)는 ω와 무관
    assert view["하한_물리"].equals(official["하한_물리"])                  # 하한은 그대로


def test_extended_scenario_weights():
    _, _, meta = screen.recompute(weights={"제재·압박": 0.5}, scenario="확장")
    assert meta["비중%"]["제재·압박"] == round(0.5 / 3.5 * 100, 1) and not meta["공식과_같음"]


@pytest.mark.parametrize("kwargs", [
    {"half_life": 6}, {"half_life": 31}, {"relief_c": -0.1}, {"relief_c": 0.31}, {"relief_cap": 0.81},
    {"weights": {"핵·미사일": 0.4}}, {"weights": {"핵·미사일": 2.1}}, {"weights": {"제재·압박": 1}},
    {"weights": {"없는 묶음": 1}}, {"scenario": "없음"}, {"half_life": float("nan")},
])
def test_out_of_range_stops(kwargs):
    with pytest.raises(ValueError):
        screen.recompute(**kwargs)


def test_core_bundle_weights_checks():
    assert core.bundle_weight_map(None, B3) is None and core.bundle_weight_map({"핵·미사일": 1}, B3) is None
    assert core.bundle_weight_map({"핵·미사일": 2}, B3) == {"핵·미사일": 2.0, "군사 과시": 1.0, "위협 언어·교리": 1.0}
    for bad in ({"없는 묶음": 1}, {"핵·미사일": 0}, {"핵·미사일": -1}, {"핵·미사일": float("inf")}):
        with pytest.raises(ValueError):
            core.bundle_weight_map(bad, B3)


def test_loader_recompute_matches_screen():
    from utils import loader
    a = loader.load_tension_recompute(weights={"핵·미사일": 2})
    b = screen.recompute(weights={"핵·미사일": 2})
    assert a[0].equals(b[0]) and a[1].equals(b[1]) and a[2] == b[2]
