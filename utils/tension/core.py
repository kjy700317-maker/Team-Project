"""긴장도 계산 코어 — 산출식 ①~⑰(docs/tension/산출식_정리.md 1A.2절). 순수 함수: DataFrame·Series → DataFrame·Series.

F2-1 = ②~⑧·⑩, F2-2 = ⑨·⑪~⑰, F6 = ⑮′(비교선 T_basic). 입력 사건표는 io.load_events()가 돌려준 표(date datetime64·S float64),
반환 Series·DataFrame의 인덱스는 calc_days()의 날짜. config 값은 인자 기본값으로만 쓴다.
"""
import bisect

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


def _require_full_base(days, base_period) -> None:
    """(보조) 계산 기간이 기준기간 전체를 담는지 — 아니면 ValueError(사용자 10-29: 이른 END는 막는다)."""
    a, b = base_period
    first, last = pd.Timestamp(f"{a}-01-01"), pd.Timestamp(f"{b}-12-31")
    if len(days) == 0 or days[0] > first or days[-1] < last:
        span = f"{days[0]:%Y-%m-%d}~{days[-1]:%Y-%m-%d}" if len(days) else "빈 기간"
        raise ValueError(f"계산 기간 {span}이 기준기간 {first:%Y-%m-%d}~{last:%Y-%m-%d}을 다 담지 않음 - 끝날짜는 {last:%Y-%m-%d} 이후로")


def _require_ids(events, ids, what) -> list:
    """(보조) ids가 사건ID 모음이고 모두 사건표에 있는지 — 아니면 TypeError·ValueError(사용자 10-29: 자료 이상은 멈춤)."""
    if isinstance(ids, str):
        raise TypeError(f"{what}: 문자열 하나가 아니라 사건ID 모음(set·tuple·list)으로 넘긴다")
    ids = list(ids)
    missing = sorted(set(ids) - set(events["사건ID"]))
    if missing:
        raise ValueError(f"{what}: 사건표에 없는 사건ID {missing[:10]}")
    return ids


def _day_sum(rows, days) -> pd.Series:
    """(보조) 행들의 그날 S 합, 사건 없는 날 0 — 기간 밖 날짜는 버린다(s3_core.load)."""
    return rows.groupby("date")["S"].sum().reindex(days, fill_value=0.0)


def daily_sums(events, days, bundles) -> pd.DataFrame:
    """② 묶음별 일 합 — 묶음 g의 그날 사건 점수 합, 사건 없는 날 0."""
    return pd.DataFrame({b: _day_sum(events[events["묶음"] == b], days) for b in bundles}, index=days)


def decay_cumulative(d, half_life=config.HALF_LIFE_DAYS) -> pd.Series:
    """③ 감쇠 누적 — R_t = λ·R_t−1 + d_t, λ = 2^(−1/반감기), 시작값 0."""
    # 기준 구현(s3_core.decay)과 같은 파이썬 루프 — 벡터화하지 않는다(대응표 ③)
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
    """⑦ 완화 할인 — δ = min(c · R완 / B완, κ).

    완화 사건의 S에는 분야 보정 φ(ADR-015)가 사건표를 만들 때 이미 곱해져 있다(build_events) — core는 φ를 모른다.
    """
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
    _require_full_base(days, base_period)
    D = daily_sums(events, days, targets)
    R = pd.DataFrame({b: decay_cumulative(D[b], half_life) for b in targets}, index=days)
    B = baseline_means(R, base_mask(days, base_period))
    bad = [b for b in targets if not B[b] > 0]
    if bad:
        raise ValueError(f"기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): {bad}")
    Tg = relative_index(R[bundles], B[bundles])
    T_plus = rising_index(Tg)
    delta = relief_discount(R[relief_bundle], B[relief_bundle], relief_c, relief_cap)
    T = tension_index(T_plus, delta)
    comp = pd.concat([R.add_prefix("R_"), Tg.add_prefix("Tg_")], axis=1)
    comp["T_plus"] = T_plus
    comp["delta"] = delta
    comp["T"] = T
    return comp, B


def half_gauss_window(d, sigma=config.HALF_GAUSS_SIGMA, window=config.FLOOR_WINDOW) -> pd.Series:
    """⑩ 하한 원점수 — ρ_t = Σ_{k<창} exp(−k²/(2σ²)) · d_t−k (반가우스 σ10·30일)."""
    w = np.exp(-np.arange(window) ** 2 / (2 * sigma ** 2))
    return pd.Series(np.convolve(d.to_numpy(float), w)[:len(d)], index=d.index)


def type4_days(events, days, type4_ids) -> pd.Series:
    """⑩ 물리 4거 유형 사건일 — 판정표 Y 사건의 사건표 날짜면 True."""
    # 날짜는 사건표에서 가져온다(판정표 date 아님 — 대응표 ⑩-b)
    ids = _require_ids(events, type4_ids, "4거 유형 사건(판정표 Y)")
    t4 = events.loc[events["사건ID"].isin(ids), "date"].unique()
    return pd.Series(days.isin(t4), index=days)


def floor_physical(events, days, type4_ids, kill_ids=config.KILL_EVENTS, thresholds=config.PHYS_FLOOR,
                   type4_stage=config.TYPE4_FLOOR_STAGE, kill_stage=config.KILL_FLOOR_STAGE,
                   bundle=config.BUNDLE_PHYS, sigma=config.HALF_GAUSS_SIGMA, window=config.FLOOR_WINDOW) -> pd.Series:
    """⑩ 물리 하한 F^물 — 풍선 뺀 A3·A7 ρ≥3→3·≥7→4, 풍선 ρ≥6→3, 4거 유형일 ≥4, 사망·침몰일 5.

    순서 그대로(s3_core.floors_s1 + compute_v014.floors_v014): ① 반가우스 판정 → ② 4거 유형일 max → ③ 사망·침몰일 덮어씀.
    """
    ph = events[events["묶음"] == bundle]
    balloon = ph["요소"].eq("A3") & ph["사건명"].astype(str).str.contains(config.BALLOON_KEYWORD, case=False, na=False)
    rho_o = half_gauss_window(_day_sum(ph[~balloon], days), sigma, window).to_numpy()
    rho_b = half_gauss_window(_day_sum(ph[balloon], days), sigma, window).to_numpy()
    th = thresholds
    fp = np.select([rho_o >= th["4거"], rho_o >= th["3거"], rho_b >= th["풍선3거"]], [4, 3, 3], 1)
    t4 = type4_days(events, days, type4_ids).to_numpy()
    fp[t4] = np.maximum(fp[t4], type4_stage)
    kill_ids = _require_ids(events, kill_ids, "사망·침몰 사건(KILL_EVENTS)")
    kill = events.loc[events["사건ID"].isin(kill_ids), "date"]
    fp[days.isin(kill)] = kill_stage
    return pd.Series(fp.astype("int64"), index=days)


def floor_e5(events, days, thresholds=config.E5_FLOOR, bundle=config.BUNDLE_E5, sigma=config.HALF_GAUSS_SIGMA,
             window=config.FLOOR_WINDOW) -> pd.Series:
    """⑩ E5 하한 F^E5 — 북러 밀착 ρ≥4→3, ≥10→4."""
    rho = half_gauss_window(_day_sum(events[events["묶음"] == bundle], days), sigma, window).to_numpy()
    th = thresholds
    fe = np.select([rho >= th["4거"], rho >= th["3거"]], [4, 3], 1)
    return pd.Series(fe.astype("int64"), index=days)


def floor_event(events, days, icbm_s=config.EVENT_FLOOR_ICBM_S, stage=config.EVENT_FLOOR_STAGE) -> pd.Series:
    """⑩ 사건 하한 F^사 — 핵실험(A1) 또는 ICBM(A2, S ≥ 7.5) 당일 3거."""
    el = events["요소"]
    key = events.loc[(el == "A1") | ((el == "A2") & (events["S"] >= icbm_s)), "date"].unique()
    fs = np.where(days.isin(key), stage, 1)
    return pd.Series(fs.astype("int64"), index=days)


# ---- F2-2: ⑨·⑪~⑰ · 일별 결과 조립 ----

DAILY_HEAD = ("T_원값", "T_표시7일", "잠정")
DAILY_TAIL = ("완화할인", "원점수_게이지", "단계_T", "하한_물리", "물리_4거유형일", "하한_E5", "하한_사건", "단계_판정",
              "단계_최종", "그날까지_상위%", "A2자료", "화면_단계문구", "변화14_표시", "변화율14_표시")

def _require_four_cuts(values, what) -> None:
    """(보조) T 구간 문턱·분위는 정확히 4개(2·3·4·5거 시작) — 아니면 ValueError(F2 검토 발견 10, 자료 이상은 멈춤)."""
    if len(values) != 4:
        raise ValueError(f"{what}은 2·3·4·5거 시작 4개여야 함: {len(values)}개")


def stage_cuts(T, mask, quantiles=config.STAGE_QUANTILES) -> tuple[np.ndarray, np.ndarray]:
    """⑨ T 구간 — 기준기간 T의 70·90·95·98분위를 반올림한 정수 문턱 θ와 반올림 전 분위."""
    # np.quantile 기본(linear) · np.round 짝수 반올림 그대로(compute_v014.compute — 대응표 ⑨)
    _require_four_cuts(quantiles, "T 구간 분위")
    q = np.quantile(T[mask], quantiles)
    return np.round(q, 0), q


def cuts_half_warning(q) -> bool:
    """⑨ 반올림 경계 — 반올림 전 분위 중 하나라도 정확히 x.5면 True(짝수 반올림 주의, 1A.5)."""
    return bool(any(abs(v - np.floor(v) - 0.5) < 1e-9 for v in q))


def stage_from_index(T, cuts) -> pd.Series:
    """⑨ T 구간 단계 L^T — 1 + #{j : T ≥ θ_j} (1~5거)."""
    _require_four_cuts(cuts, "T 구간 문턱")
    c1, c2, c3, c4 = cuts
    return pd.Series(np.select([T >= c4, T >= c3, T >= c2, T >= c1], [5, 4, 3, 2], 1).astype("int64"), index=T.index)


def judge(*levels) -> pd.Series:
    """⑪ 판정 J — 단계_T와 하한들 중 가장 높은 단계."""
    return pd.concat(levels, axis=1).max(axis=1).astype("int64")


def step_down(J, n=config.STEP_DOWN_DAYS) -> pd.Series:
    """⑫ 최종 단계 L — 판정이 같거나 높으면 즉시 따라가고, 낮은 날이 n일 쌓이면 한 단계 내림(첫날 L = J)."""
    # 기준 구현(s3_core.step_down)과 같은 파이썬 루프 — 벡터화하지 않는다(대응표 ⑫)
    out = np.empty(len(J), dtype="int64")
    cur = J.iloc[0]
    below = 0
    for i, r in enumerate(J.to_numpy()):
        if r >= cur:
            cur, below = r, 0
        else:
            below += 1
            if below >= n:
                cur, below = cur - 1, 0
        out[i] = cur
    return pd.Series(out, index=J.index)


def display_ma(T, window=config.DISPLAY_MA_DAYS) -> pd.Series:
    """⑬ 표시선 T̄ — 7일 후행 이동평균(처음 6일은 있는 날만 평균)."""
    return T.rolling(window, min_periods=1).mean()


def cumulative_top_pct(T_bar) -> pd.Series:
    """⑭ 그날까지 상위% — 100 − 100 · #{s ≤ t : T̄_s ≤ T̄_t} / #{s ≤ t}."""
    # 기준 구현(compute_v014.compute)과 같은 bisect 누적 — 벡터화 rank로 바꾸지 않는다(동점 처리, 대응표 ⑭)
    srt, pe = [], []
    for v in T_bar.to_numpy(float):
        bisect.insort(srt, v)
        pe.append(bisect.bisect_right(srt, v) / len(srt) * 100)
    return pd.Series(100 - np.array(pe), index=T_bar.index)


def raw_gauge(comp, bundles) -> pd.Series:
    """⑮ 원점수 게이지 R^합 — 상승 묶음 R_g의 합(확장이면 제재·압박 포함)."""
    return sum(comp[f"R_{b}"] for b in bundles)


def basic_index(comp, bundles, mask) -> pd.Series:
    """⑮′ 비교선 T_basic — 상승 묶음 R의 합 ÷ 기준기간 평균 × 100 × (1 − δ). 묶음별 ÷B_g(정규화)만 뺀 T(사용자 10-29).

    comp = tension_components()의 표(R_<묶음>·delta), mask = base_mask(days). 완화 할인 δ와 묶음 구성은 주 지수와 같다.
    기준기간 평균이 0 이하이면 멈춘다(ValueError — 자료 이상, F2-3과 같은 규칙).
    """
    R = raw_gauge(comp, bundles)
    base = float(R[mask].mean())
    if not base > 0:
        raise ValueError(f"비교선 T_basic: 기준기간 상승 묶음 R 합의 평균이 {base:g} - 0 이하(기준기간 사건 없음)")
    return 100 * R / base * (1 - comp["delta"])


def crisis_window_max(x, crises=config.CRISIS_LIST, window_days=config.CRISIS_WINDOW_DAYS) -> pd.Series:
    """⑮ 위기 눈금 — 위기일 t_c부터 t_c + 14일까지 x의 최댓값(x = 원점수_게이지면 게이지 눈금, 단계_최종이면 위기 단계)."""
    out = {}
    for name, date, _ in crises:
        t = pd.Timestamp(date)
        out[name] = x.loc[t:t + pd.Timedelta(days=window_days)].max()
    return pd.Series(out)


def trend(T_bar, days=config.TREND_DAYS, pct_min=config.TREND_PCT_MIN) -> pd.DataFrame:
    """⑯ 추세 — Δ = T̄_t − T̄_t−14, 변화율 = 100 · Δ / T̄_t−14 (T̄_t−14 ≥ 50일 때만, 그 밖 NaN)."""
    prev = T_bar.shift(days)
    chg = T_bar - prev
    pct = np.where(prev >= pct_min, chg / prev * 100, np.nan)
    return pd.DataFrame({"변화14_표시": chg, "변화율14_표시": pct}, index=T_bar.index)


def stage_label(L, J) -> pd.Series:
    """⑰ 단계 카드 문구 — L > J면 "L거 · 하강 중(판정 J거)", 그 밖 "L거"."""
    return pd.Series([f"{l}거 · 하강 중(판정 {j}거)" if j < l else f"{l}거" for l, j in zip(L, J)], index=L.index)


def provisional(days, n=config.PROVISIONAL_DAYS) -> pd.Series:
    """(보조) 잠정 — 마지막 날 − n일보다 뒤인 날(최근 6일) True."""
    return pd.Series(days > days[-1] - pd.Timedelta(days=n), index=days)


def a2_note(days, a2_end=config.A2_DATA_END) -> pd.Series:
    """(보조) A2자료 — a2_end보다 뒤인 날 "A2 자료 없음(a2_end까지)", 그 밖 빈 문자열."""
    return pd.Series(np.where(days > pd.Timestamp(a2_end), config.A2_NOTE.format(end=a2_end), ""), index=days)


def relief_display(T, Tg) -> pd.Series:
    """(보조) 완화할인 열 — 1 − T / mean(T_g), mean = 0인 날 0 (δ와 다름 — 대응표 2절)."""
    # 기준 구현 정의 그대로: T⁺ = 0인 날은 δ > 0이어도 0(회귀 일치를 위해 이식 — 대응표 2절 완화할인)
    return (1 - T / Tg.mean(axis=1).replace(0, np.nan)).fillna(0)


def daily_columns(bundles) -> list[str]:
    """(보조) 일별 CSV 열 순서 — 인덱스(날짜) 빼고 기본 20열·확장 21열."""
    return [*DAILY_HEAD, *[f"Tg_{b}" for b in bundles], *DAILY_TAIL]


# daily_table params 키 — 값을 바꾼 계산(민감도·비교선)은 config를 고치지 말고 이 키로 넘긴다(사용자 10-29)
PARAM_KEYS = ("base_period", "half_life", "relief_c", "relief_cap", "quantiles", "sigma", "window",
              "phys_thresholds", "type4_stage", "kill_ids", "kill_stage", "e5_thresholds", "icbm_s", "event_stage",
              "step_days", "ma_days", "provisional_days", "trend_days", "trend_pct_min", "a2_end")


def _pick(params, **argmap) -> dict:
    """(보조) params에서 이 함수 인자에 해당하는 키만 골라 {인자: 값}."""
    return {arg: params[key] for arg, key in argmap.items() if key in params}


def daily_table(events, days, bundles, type4_ids, params=None) -> tuple[pd.DataFrame, dict]:
    """②~⑰ 일별 결과 — 사건표에서 일별 CSV의 모든 열(반올림 전)과 계산 정보를 한 번에.

    params = PARAM_KEYS 중 바꿀 것만 담은 dict. 없는 키는 각 함수의 기본값(config). config 값은 import 때
    함수 기본값으로 묶이므로 실행 중 config를 바꿔도 반영되지 않는다 — 바꾼 계산은 params로 넘긴다.
    열 이름은 고정(trend_days를 바꿔도 `변화14_표시` 그대로). 반올림하지 않는다(쓸 때 round(3)).
    기준기간이 다 들어 있지 않거나, 평소값 B ≤ 0, 첫 문턱 θ₁ ≤ 0, 판정표·사망 사건ID가 사건표에 없으면 멈춘다(ValueError).
    info = {"B", "cuts", "quantiles_raw", "half_warning", "components", "params"(넘긴 params)}.
    """
    p = dict(params or {})
    unknown = sorted(set(p) - set(PARAM_KEYS))
    if unknown:
        raise ValueError(f"params에 모르는 키 {unknown} — 쓸 수 있는 키: {list(PARAM_KEYS)}")
    bundles = list(bundles)
    comp, B = tension_components(events, days, bundles, **_pick(p, base_period="base_period", half_life="half_life",
                                                                 relief_c="relief_c", relief_cap="relief_cap"))
    T = comp["T"]
    Tg = comp[[f"Tg_{b}" for b in bundles]]
    # T는 한 번만 계산 — 구간과 무관(대응표 ⑨)
    cuts, q = stage_cuts(T, base_mask(days, **_pick(p, base_period="base_period")), **_pick(p, quantiles="quantiles"))
    if not cuts[0] > 0:
        raise ValueError(f"T 구간 첫 문턱(2거 시작)이 {cuts[0]:g} - 0 이하(기준기간 T가 대부분 0, 자료 부족)")
    LT = stage_from_index(T, cuts)
    gauss = _pick(p, sigma="sigma", window="window")
    fp = floor_physical(events, days, type4_ids, **_pick(p, kill_ids="kill_ids", thresholds="phys_thresholds",
                                                         type4_stage="type4_stage", kill_stage="kill_stage"), **gauss)
    fe = floor_e5(events, days, **_pick(p, thresholds="e5_thresholds"), **gauss)
    fs = floor_event(events, days, **_pick(p, icbm_s="icbm_s", stage="event_stage"))
    J = judge(LT, fp, fe, fs)
    L = step_down(J, **_pick(p, n="step_days"))
    T_bar = display_ma(T, **_pick(p, window="ma_days"))
    tr = trend(T_bar, **_pick(p, days="trend_days", pct_min="trend_pct_min"))
    cols = {"T_원값": T, "T_표시7일": T_bar, "잠정": provisional(days, **_pick(p, n="provisional_days")),
            **{f"Tg_{b}": Tg[f"Tg_{b}"] for b in bundles},
            "완화할인": relief_display(T, Tg), "원점수_게이지": raw_gauge(comp, bundles), "단계_T": LT,
            "하한_물리": fp, "물리_4거유형일": type4_days(events, days, type4_ids), "하한_E5": fe, "하한_사건": fs,
            "단계_판정": J, "단계_최종": L, "그날까지_상위%": cumulative_top_pct(T_bar),
            "A2자료": a2_note(days, **_pick(p, a2_end="a2_end")),
            "화면_단계문구": stage_label(L, J), "변화14_표시": tr["변화14_표시"], "변화율14_표시": tr["변화율14_표시"]}
    daily = pd.DataFrame(cols, index=days)[daily_columns(bundles)]
    daily.index.name = "날짜"
    info = {"B": B, "cuts": cuts, "quantiles_raw": q, "half_warning": cuts_half_warning(q), "components": comp,
            "params": p}
    return daily, info
