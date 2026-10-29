"""screen.py·loader 새 함수 테스트(F5) — 커밋된 결과 CSV(data/tension)를 화면 모양으로 읽는지. Streamlit 화면은 test_app_smoke.py."""
import numpy as np
import pandas as pd
import pytest

import config
from utils.tension import core, io as tio, screen

ROOT = screen.ROOT


@pytest.fixture(scope="module")
def d():
    return screen.daily("기본")


def test_daily_screen_columns(d):
    raw = screen.daily_raw("기본")
    assert len(d) == len(raw) and d["날짜"].tolist() == list(raw.index)
    assert list(d.columns[:len(raw.columns) + 1]) == ["날짜", *raw.columns]          # 결과 열은 그대로 앞에
    assert d["평소대비"].equals(d["T_표시7일"]) and d["평소대비_원값"].equals(d["T_원값"])
    assert d["원점수"].equals(d["원점수_게이지"]) and (d["최종단계"] == d["단계_최종"]).all()
    assert set(d["단계이름"]) <= set(config.STAGE_NAMES.values())


def test_streak_and_top_pct(d):
    on = (d["최종단계"] >= 4).to_numpy()
    assert ((d["지속일수"] > 0).to_numpy() == on).all()
    i = int(np.argmax(on))                                                            # 처음 4거 이상인 날
    assert d["지속일수"].iloc[i] == 1
    assert d["상위%_표시"].iloc[:365].isna().all() and d["상위%_표시"].iloc[365:].notna().all()
    assert d["상위%_표시"].iloc[365:].equals(d["그날까지_상위%"].iloc[365:].astype(float))


def test_relief_delta_matches_core(d):
    tg = d[[f"Tg_{b}" for b in config.BUNDLES_BASE]].mean(axis=1)
    on = tg > 0
    assert float((d.loc[on, "완화할인_δ"] - d.loc[on, "완화할인"]).abs().max()) < 0.0011   # T⁺ > 0이면 CSV 열과 같음
    assert int(((tg == 0) & (d["완화할인_δ"] > 0)).sum()) > 0                               # T⁺ = 0이어도 δ가 나옴
    assert d["완화할인_δ"].between(0, config.RELIEF_CAP).all()


def test_periods_and_cuts():
    m, y = screen.monthly("기본"), screen.yearly("확장")
    assert "시나리오" not in m.columns and m["평소대비"].equals(m["T_평균"]) and m["최종단계"].equals(m["단계_최고"])
    assert y["연도"].iloc[0] == 2010 and y["원점수"].equals(y["원점수_평균"])
    assert screen.cuts("기본") == (115, 256, 315, 378) and screen.cuts("확장") == (110, 237, 314, 374)
    with pytest.raises(ValueError):
        screen.cuts("다른것")


def test_stage_table_and_crisis():
    t = screen.stage_table("기본")
    assert t["T 구간(이상)"].tolist() == [0, 115, 256, 315, 378]
    assert t["이름"].tolist()[0] == f"1거 · {config.STAGE_NAMES[1]}" and len(t) == 5
    c = screen.crisis_marks("기본")
    assert len(c) == len(config.CRISIS_LIST) and c.loc[c["위기"] == "6차 핵", "게이지 눈금"].item() == 33.8


def test_contributions(d):
    table, ev = screen.contributions("2026-10-29", "기본", top=10)
    row = d.iloc[-1]
    assert table["값"].iloc[-1] == row["T_원값"] and len(table) == len(config.BUNDLES_BASE) + 3
    assert len(ev) == 10 and ev["남은점수"].is_monotonic_decreasing
    first = ev.iloc[0]
    k = (pd.Timestamp("2026-10-29") - first["날짜"]).days
    assert first["남은점수"] == round(first["S"] * 2 ** (-k / config.HALF_LIFE_DAYS), 3)
    assert set(ev["구분"]) <= {"상승", "완화(할인)", "하한 대상", "표시만", "그 밖"}
    _, before = screen.contributions("2026-09-25", "기본")                             # 기준일 뒤 사건은 빠짐
    assert (before["날짜"] <= "2026-09-25").all()


def test_unknown_actor():
    actors = screen._actor_map()
    for k in ("F2-0668", "E5-8978", "E5-8981", "E5-8983", "E5-8986"):
        assert k not in actors
    ev, _ = tio.load_events(ROOT / "data" / "tension" / "events_확장.csv")
    hit = ev["사건ID"].map(lambda k: k in actors)
    assert int((~hit).sum()) == 5


def test_figure_uses_config_colors():
    f = screen.figure("기본")
    assert [t.name for t in f.data][-2:] == ["확장(C5 포함) 7일 평균", "최종 단계"]
    scale = [c for _, c in f.data[-1].colorscale]
    assert [scale[2 * (k - 1)] for k in range(1, 6)] == [config.STAGE_COLORS[k] for k in range(1, 6)]


def test_loader_functions_match_screen():
    from utils import loader
    assert loader.load_tension_daily("기본").equals(screen.daily("기본"))
    assert loader.load_tension_stage_table().equals(screen.stage_table())
    t1, e1 = loader.load_tension_contrib("2026-10-29")
    t2, e2 = screen.contributions("2026-10-29")
    assert t1.equals(t2) and e1.equals(e2)
    assert callable(loader.load_daily) and callable(loader.load_monthly)                # 기존 함수 그대로
