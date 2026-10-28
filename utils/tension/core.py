"""긴장도 계산 코어 — 산출식 ①~⑰(docs/tension/산출식_정리.md 1A.2절). 순수 함수: DataFrame·Series → DataFrame·Series.

F2-1 = ②~⑧·⑩, F2-2 = ⑨·⑪~⑰. 입력 사건표는 io.load_events()가 돌려준 표(date datetime64·S float64),
반환 Series·DataFrame의 인덱스는 calc_days()의 날짜. config 값은 인자 기본값으로만 쓴다.
"""
import numpy as np
import pandas as pd

import config


def calc_days(start=config.CALC_START_DATE, end=config.END_DATE) -> pd.DatetimeIndex:
    """(보조) 𝒯 계산 기간 — start~end 하루 간격, end가 None이면 오늘."""
    if end is None:
        end = pd.Timestamp.today().normalize()
    return pd.date_range(start, end, freq="D")


def base_mask(days, base_period=config.BASE_PERIOD) -> np.ndarray:
    """(보조) 𝒯₀ 기준기간 — 연도가 base_period 안인 날 True."""
    a, b = base_period
    return (days.year >= a) & (days.year <= b)


def _day_sum(rows, days) -> pd.Series:
    """(보조) 행들의 그날 S 합, 사건 없는 날 0 — 기간 밖 날짜는 버린다(s3_core.load)."""
    return rows.groupby("date")["S"].sum().reindex(days, fill_value=0.0)


def daily_sums(events, days, bundles) -> pd.DataFrame:
    """② 묶음별 일 합 — 묶음 g의 그날 사건 점수 합, 사건 없는 날 0."""
    return pd.DataFrame({b: _day_sum(events[events["묶음"] == b], days) for b in bundles}, index=days)


def decay_cumulative(d, half_life=config.HALF_LIFE_DAYS) -> pd.Series:
    """③ 감쇠 누적 — R_t = λ·R_t−1 + d_t, λ = 2^(−1/반감기), 시작값 0."""
    # 기준 구현(s3_core.decay)과 같은 파이썬 루프 — ewm·lfilter로 바꾸지 않는다(대응표 ③)
    a = 2 ** (-1 / half_life)
    r = np.zeros(len(d))
    acc = 0.0
    for i, v in enumerate(d.to_numpy(float)):
        acc = acc * a + v
        r[i] = acc
    return pd.Series(r, index=d.index, name=d.name)


def baseline_means(R, mask) -> pd.Series:
    """④ 평소값 — 기준기간 R의 평균(열마다)."""
    return pd.Series({c: R[c][mask].mean() for c in R.columns}, dtype="float64")


def relative_index(R, B) -> pd.DataFrame:
    """⑤ 평소 대비 — T_g = 100 · R_g / B_g."""
    return pd.DataFrame({c: R[c] / B[c] * 100 for c in R.columns}, index=R.index)


def rising_index(Tg) -> pd.Series:
    """⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중)."""
    # 기준 구현 sum(Tg.values()) / len(bundles) — 열 순서대로 더한 뒤 나눈다(mean(axis=1) 아님)
    return sum(Tg[c] for c in Tg.columns) / len(Tg.columns)


def relief_discount(R_relief, B_relief, c=config.RELIEF_C, cap=config.RELIEF_CAP) -> pd.Series:
    """⑦ 완화 할인 — δ = min(c · R완 / B완, κ)."""
    return pd.Series(np.minimum(c * R_relief / B_relief, cap), index=R_relief.index)


def tension_index(T_plus, delta) -> pd.Series:
    """⑧ 긴장도 — T = T⁺ · (1 − δ)."""
    return T_plus * (1 - delta)


def tension_components(events, days, bundles, base_period=config.BASE_PERIOD, half_life=config.HALF_LIFE_DAYS,
                       relief_c=config.RELIEF_C, relief_cap=config.RELIEF_CAP,
                       relief_bundle=config.BUNDLE_RELIEF) -> tuple[pd.DataFrame, pd.Series]:
    """②~⑧ 묶음 — 사건표에서 R·B·T_g·T⁺·δ·T를 한 번에.

    반환 = (열 R_<대상>·Tg_<묶음>·T_plus·delta·T 인 DataFrame, 평소값 B Series). 대상 = bundles + relief_bundle.
    기준 구현은 run을 두 번 부르지만 T는 단계 구간과 무관하므로 한 번만 계산한다.
    """
    bundles = list(bundles)
    targets = bundles + [relief_bundle]
    D = daily_sums(events, days, targets)
    R = pd.DataFrame({b: decay_cumulative(D[b], half_life) for b in targets}, index=days)
    B = baseline_means(R, base_mask(days, base_period))
    Tg = relative_index(R[bundles], B[bundles])
    T_plus = rising_index(Tg)
    delta = relief_discount(R[relief_bundle], B[relief_bundle], relief_c, relief_cap)
    T = tension_index(T_plus, delta)
    comp = pd.concat([R.add_prefix("R_"), Tg.add_prefix("Tg_")], axis=1)
    comp["T_plus"] = T_plus
    comp["delta"] = delta
    comp["T"] = T
    return comp, B
