"""summary.py 단위 테스트(F4) — 작은 합성 일별 표로 집계 규칙 확인(사건표 없이 돈다)."""
import numpy as np
import pandas as pd
import pytest

from utils.tension import summary as sm


def _daily(stages, start="2024-12-30"):
    days = pd.date_range(start, periods=len(stages), name="날짜")
    n = len(stages)
    return pd.DataFrame({"T_원값": np.arange(n, dtype=float), "T_표시7일": np.arange(n, dtype=float) * 2,
                         "원점수_게이지": np.full(n, 1.5), "단계_최종": stages}, index=days)


def test_stage_streak_counts_and_resets():
    s = sm.stage_streak(pd.Series([1, 4, 5, 4, 3, 4, 4]))
    assert s.tolist() == [0, 1, 2, 3, 0, 1, 2]
    assert sm.stage_streak(pd.Series([3, 3, 2]), min_stage=3).tolist() == [1, 2, 0]


def test_period_table_month_and_year():
    d = _daily([1, 2, 3, 4, 5])                     # 2024-12-30 ~ 2025-01-03
    m = sm.period_table(d, "월")
    assert list(m.columns) == ["연월", *sm.PERIOD_COLUMNS]
    assert m["연월"].tolist() == ["2024-12", "2025-01"] and m["일수"].tolist() == [2, 3]
    assert m["T_평균"].tolist() == [0.5, 3.0] and m["T표시_최고"].tolist() == [2.0, 8.0]
    assert m["단계_최고"].tolist() == [2, 5] and m["단계_평균"].tolist() == [1.5, 4.0]
    assert m[["1거일", "2거일", "3거일", "4거일", "5거일"]].sum(axis=1).tolist() == [2, 3]
    y = sm.period_table(d, "연")
    assert y["연도"].tolist() == [2024, 2025] and y["원점수_평균"].tolist() == [1.5, 1.5]


def test_period_table_rounding():
    d = _daily([1, 2, 2], start="2025-01-01")
    d["T_원값"] = [1.00049, 1.0, 1.0]
    assert sm.period_table(d, "연")["T_평균"].iloc[0] == round(np.mean([1.00049, 1.0, 1.0]), 3)
    assert sm.period_table(d, "연")["단계_평균"].iloc[0] == 1.67


def test_period_table_bad_freq():
    with pytest.raises(ValueError):
        sm.period_table(_daily([1]), "주")


def test_period_tables_scenario_column():
    t = sm.period_tables({"기본": _daily([1, 2, 3]), "확장": _daily([3, 4, 5])}, "월")   # 2024-12·2025-01 걸침
    assert t.columns[0] == "시나리오" and t["시나리오"].tolist() == ["기본", "기본", "확장", "확장"]


def test_summary_table_row_union_order():
    t = sm.summary_table({"기본": {"a": 1, "b": 2}, "확장": {"a": 3, "b": 4, "c": 5}})
    assert list(t.index) == ["a", "b", "c"] and list(t.columns) == ["기본", "확장"]
    assert pd.isna(t.loc["c", "기본"])
