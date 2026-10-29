"""요약·월별·연도별·지속일수 (F4) — 일별 결과(core.daily_table 출력)를 모으는 집계 함수.

식 ①~⑰은 core.py. 여기는 일별 표를 세고 평균 내는 일만 한다(규칙 없음). Streamlit·파일 경로를 모른다.
요약 행 이름·순서는 v0.1.4 `요약_v014.csv`(tests/fixtures/v014_요약.csv)와 같다.
"""
import numpy as np
import pandas as pd

import config
from utils.tension import core

PERIOD_COLUMNS = ("일수", "T_평균", "T표시_최고", "원점수_평균", "단계_최고", "단계_평균",
                  "1거일", "2거일", "3거일", "4거일", "5거일")
SUMMARY_NOTE = "A2 자료 {end}까지 — 그 뒤 미사일·ICBM 사건 하한 없음"


def stage_streak(L, min_stage=4) -> pd.Series:
    """(집계) 지속일수 — 단계_최종이 min_stage 이상인 날이 오늘까지 며칠째 이어지는지(아니면 0)."""
    on = (L >= min_stage).to_numpy()
    out = np.zeros(len(on), dtype="int64")
    run = 0
    for i, v in enumerate(on):
        run = run + 1 if v else 0
        out[i] = run
    return pd.Series(out, index=L.index, name="지속일수")


def period_table(daily, freq) -> pd.DataFrame:
    """(집계) 월별(freq="월") 또는 연도별(freq="연") — PERIOD_COLUMNS. T·원점수 3자리, 단계_평균 2자리."""
    if freq == "월":
        key, label = daily.index.strftime("%Y-%m"), "연월"
    elif freq == "연":
        key, label = daily.index.year, "연도"
    else:
        raise ValueError(f"freq는 '월' 또는 '연': {freq}")
    L = daily["단계_최종"].astype("int64")
    g = pd.DataFrame({"T": daily["T_원값"], "Tb": daily["T_표시7일"], "R": daily["원점수_게이지"], "L": L}).groupby(key)
    out = pd.DataFrame({
        "일수": g.size().astype("int64"),
        "T_평균": g["T"].mean().round(3),
        "T표시_최고": g["Tb"].max().round(3),
        "원점수_평균": g["R"].mean().round(3),
        "단계_최고": g["L"].max().astype("int64"),
        "단계_평균": g["L"].mean().round(2),
        **{f"{k}거일": g["L"].apply(lambda s, k=k: int((s == k).sum())).astype("int64") for k in range(1, 6)},
    })
    out.index.name = label
    return out.reset_index()


def period_tables(dailies, freq) -> pd.DataFrame:
    """(집계) 시나리오 여러 개를 한 표로 — 첫 열 `시나리오`. dailies = {시나리오 이름: 일별 표}(순서 유지)."""
    parts = [period_table(d, freq).assign(시나리오=name) for name, d in dailies.items()]
    out = pd.concat(parts, ignore_index=True)
    return out[["시나리오", *[c for c in out.columns if c != "시나리오"]]]


def summary_values(daily, info, days, bundles, *, input_name, n_type4, base_period=config.BASE_PERIOD,
                   crises=config.CRISIS_LIST, relief_cap=config.RELIEF_CAP, a2_end=config.A2_DATA_END) -> dict:
    """(집계) 요약 한 열 — v0.1.4 `요약_v014.csv`와 같은 행 이름·순서·반올림. 현재 행 이름은 끝날(`현재(MM-DD)`)."""
    L = daily["단계_최종"]
    bm = core.base_mask(days, base_period)
    last = daily.iloc[-1]
    stages = core.crisis_window_max(L, crises)
    marks = core.crisis_window_max(daily["원점수_게이지"], crises)
    other = daily[["단계_T", "하한_물리", "하한_사건"]].max(axis=1)
    v = {"입력": input_name, "묶음": " · ".join(bundles), "기준기간": f"{base_period[0]}~{base_period[1]}",
         **{f"B_{b}": round(float(x), 3) for b, x in info["B"].items()},
         "T구간(2·3·4·5거 시작)": "/".join(f"{x:g}" for x in info["cuts"]),
         "T구간_반올림전": "/".join(f"{x:.2f}" for x in info["quantiles_raw"]),
         "경계_x.5_주의": bool(info["half_warning"]),
         **{f"{k}거%": round((L == k).mean() * 100, 1) for k in range(1, 6)},
         "바뀜/년": round((L.diff().fillna(0) != 0).sum() / (len(days) / 365.25), 1),
         **{name: int(stages[name]) for name, _, _ in crises},
         "2018 평균단계": round(L.loc["2018"].mean(), 2), "2018 3거이상일": int((L.loc["2018"] >= 3).sum()),
         "2021 평균단계": round(L.loc["2021"].mean(), 2),
         "2023 4거이상%": round((L.loc["2023"] >= 4).mean() * 100, 0), "2023 5거%": round((L.loc["2023"] == 5).mean() * 100, 0),
         f"현재({days[-1]:%m-%d})": int(L.iloc[-1]),
         "사건하한 날 수": int((daily["하한_사건"] > 1).sum()), "물리 4거유형 사건일 수": int(daily["물리_4거유형일"].sum()),
         "E5하한 3거↑ 날": int((daily["하한_E5"] >= 3).sum()), "E5가 판정을 올린 날": int((daily["하한_E5"] > other).sum()),
         "물리하한 3거↑ 날": int((daily["하한_물리"] >= 3).sum()), "물리하한 4거↑ 날": int((daily["하한_물리"] >= 4).sum()),
         "물리하한 5거 날": int((daily["하한_물리"] == 5).sum()),
         "완화 상한에 붙은 날": int((info["components"]["delta"] >= relief_cap - 1e-12).sum()),
         "원점수 기준기간 평균": round(float(daily["원점수_게이지"][bm].mean()), 2),
         **{f"게이지_{name}": round(float(marks[name]), 1) for name, _, _ in crises},
         "T원값 최대": round(daily["T_원값"].max()), "표시선 최대": round(daily["T_표시7일"].max()),
         "현재 표시(잠정)": round(last["T_표시7일"], 1), "현재 그날까지 상위%": round(last["그날까지_상위%"], 1),
         "현재 원점수": round(last["원점수_게이지"], 1), "현재 14일 변화": round(last["변화14_표시"], 1),
         "현재 화면 단계": last["화면_단계문구"], "비고": SUMMARY_NOTE.format(end=a2_end),
         "4거유형 사건 수": int(n_type4)}
    return v


def summary_table(columns) -> pd.DataFrame:
    """(집계) 요약 표 — columns = {열 이름: summary_values 결과}(순서 유지). 행은 첫 열 순서, 뒤 열에만 있는 행은 끝에."""
    rows = [{"시나리오": name, **vals} for name, vals in columns.items()]
    out = pd.DataFrame(rows).set_index("시나리오").T
    out.columns.name = None
    return out
