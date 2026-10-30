"""화면용 결과 통로 (F5) — data/tension 결과 CSV를 화면이 쓰기 좋은 모양으로 읽는다. Streamlit을 모른다.

화면(`utils/loader.py`의 `load_tension_*`)이 이 함수들을 부른다. 계산 규칙은 바꾸지 않는다 — 결과 CSV를 읽고,
화면 이름 열을 더하고, 화면에서만 쓰는 값(지속일수·상위% 숨김·완화 할인 δ·사건별 남은 점수)을 만든다.
10-29 사용자 결정: 평소대비 = 7일 표시값(원값은 `평소대비_원값`) · 상위 %는 첫 365일 숨김 · 점수 구성 = 묶음별 + 사건별 10건 ·
주체국을 못 붙이면 "미상" · 완화 할인은 실제 δ · 시나리오는 기본이 주, 확장은 추이 그림 점선.
F6(10-29 사용자): 비교선 T_basic(⑮′ — 정규화 효과만, 설명 자리용) · GPR 한국 월별 비교(순위% 두 선) · 반감기 민감도 표 ·
반감기 설명 문구 · 유사 시기 그달 주요 사건.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

import config
from utils.tension import core, io as tio, summary as sm

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / config.TENSION_DATA_DIR
PROCESSED_DIR = ROOT / "data" / "processed"
SCENARIOS = {"기본": config.BUNDLES_BASE, "확장": config.BUNDLES_EXT}
SUMMARY_COLUMN = {"기본": "기본", "확장": "확장(C5 포함)"}   # 요약.csv 열 이름(v0.1.4와 같음)
TOP_PCT_HIDE_DAYS = 365       # 사용자 10-29: 누적 비교 표본이 작은 첫 365일(2010년)은 상위 % 숨김
UNKNOWN_ACTOR = "미상"         # 사용자 10-29: data/processed에 없는 보완행
STAGE_MEANING = {1: "평상시", 2: "적 출현", 3: "경계 접근", 4: "경계 침범", 5: "교전"}   # 봉수 원뜻(산출식 단계 표)
KIND = {config.BUNDLE_RELIEF: "완화(할인)", config.BUNDLE_PHYS: "하한 대상", config.BUNDLE_E5: "하한 대상",
        "북러(표시만)": "표시만"}

# 자료 충실도 표·각주·판독문(단계 5 인계 5.4절 문구 그대로) — 화면이 그대로 보여 준다
DATA_COVERAGE = pd.DataFrame({
    "요소": ["A2 미사일", "A3 저강도", "A7 물리 충돌", "C1 위협 성명", "A5 전략자산"],
    "충실도": [f"{config.A2_DATA_END} 이후 자료 없음", "2022년부터 수집(원자료 범위) — 2010~2021 해당 없음",
            "2020-05-03 철원 GP 총격 미포함(팀 결정)", "2021년 기록 없음(팀: 그대로 진행)", "2018~2021 기록 없음(팀: 그대로 진행)"]})
FOOTNOTES = ("2020~2021: 실제 소강기(코로나·대화 중단·훈련 축소). 일부 요소는 기록이 적어 실제보다 낮게 나올 수 있음.",
             "2022년 이후: 요소별 기록 밀도가 2010년대의 2~5배 — 과거보다 높게 나오는 경향.")
READING_NOTES = ("기본점수·묶음 가중을 ±50% 흔들어도 일별 단계 86~91%(중앙) 유지.",
                 "외부 대조: CrisisWatch(International Crisis Group) 악화 판정 달의 85%에서 봉수 2거 이상, "
                 "방향 쌍 63~69% 일치(내부 대조용, 출처: Crisis Group).",
                 "북미 정상외교·국내 정치 사건은 지수 밖 — 완화는 남북 회담만.",
                 "반복 발사·정책 문서처럼 국제 보도는 적지만 군사 신호가 큰 달은 봉수가 GPR보다 높다(행동 vs 관심).")
# F6 — GPR 비교 판독문 3줄(앞 2줄은 위 READING_NOTES와 같은 문구, 셋째 줄은 10-29 사용자 결정)
GPR_NOTE_2018 = ("2018년 정상회담기에는 GPR이 높고 봉수가 낮다 — GPR은 보도량(관심)을, "
                 "봉수는 남북 회담에 따른 완화(행동)를 반영한다(설계상 차이).")
GPR_NOTES = (READING_NOTES[2], READING_NOTES[3], GPR_NOTE_2018)
# F6 — 비교선 판독문 1줄(설명 자리 "묶음 정규화 효과" 그림 아래, 사용자 확인 대기 문구)
NORMALIZATION_NOTE = ("묶음마다 평소로 나눈 우리 방식과 단순 합(묶음 구분 없이 더함)의 차이는 지금 자료에서 작다 — "
                      "상승 묶음의 평소값이 비슷하기 때문이다. 물리 충돌·북러 밀착은 단순 합에 묻히지 않도록 하한으로 따로 반영한다.")
GPR_SOURCE = ("GPR 한국 = GPRC_KOR(Caldara & Iacoviello, 한국 관련 지정학 위험 기사 비율 %, 월별). "
              "비교 지수로만 씀(가중치를 맞추지 않음). 출처 matteoiacoviello.com/gpr.htm")
# F6 — 반감기 설명 문구(docs/tension/감쇠_표시_단계유예_조사.md 4절 그대로, ADR-006 5번)
HALF_LIFE_NOTE = (
    "봉수는 기록된 사건의 영향을 \"반감기 14일\"로 셉니다. 사건 점수는 14일마다 절반이 되어 30일 뒤 약 23%, "
    "60일 뒤 약 5%가 남습니다. 14일은 두 가지를 근거로 골랐습니다.",
    "① 통일부 남북관계연표에서 큰 도발(핵실험·ICBM·물리 충돌 18건) 뒤 그 사건을 직접 언급한 기록이 줄어드는 속도를 쟀습니다. "
    "추정 반감기는 약 15일이고 95% 구간은 12~62일입니다.",
    "② 분쟁 사건 연구에서 한 사건의 영향이 이어지는 기간은 대체로 수일~수주로 보고됩니다.",
    "이 값은 \"앞으로 며칠 위험하다\"는 예측이 아니라, 지나간 사건을 얼마나 오래 세는지에 대한 설계 선택입니다. "
    "반감기를 7·21·30일로 바꾼 결과도 함께 공개합니다.")


def _check(scenario):
    if scenario not in SCENARIOS:
        raise ValueError(f"시나리오는 {list(SCENARIOS)} 중 하나: {scenario}")


def stage_names():
    """(화면) 단계 이름 — config.STAGE_NAMES(화면 설정)가 있으면 그것, 없으면 평온~심각."""
    return getattr(config, "STAGE_NAMES", {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"})


def relief_delta(scenario="기본", days=None, data_dir=DATA_DIR) -> pd.Series:
    """(화면) 완화 할인 δ — 사건표로 ⑦ δ를 다시 계산(결과 CSV `완화할인` 열은 T⁺ = 0인 날 0이라 화면 설명에 안 맞음, 사용자 10-29)."""
    _check(scenario)
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    if days is None:
        days = pd.DatetimeIndex(daily_raw(scenario, data_dir).index)
    comp, _ = core.tension_components(events, pd.DatetimeIndex(days), list(SCENARIOS[scenario]))
    return comp["delta"]


def daily_raw(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 결과 일별 CSV 그대로(날짜 인덱스) — 그림 함수용."""
    _check(scenario)
    return tio.read_csv_kr(Path(data_dir) / f"일별_{scenario}.csv", index_col=0, parse_dates=True)


def daily(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 일별 — 결과 열 전부 + 화면 이름 열. `날짜`는 열(datetime).

    더하는 열: 평소대비(= T_표시7일) · 평소대비_원값(= T_원값) · 원점수(= 원점수_게이지) · 최종단계(= 단계_최종) ·
    단계이름 · 지속일수(4거 이상 며칠째) · 상위%_표시(첫 365일 NaN) · 완화할인_δ.
    """
    raw = daily_raw(scenario, data_dir)
    d = raw.reset_index()
    d["평소대비"] = d["T_표시7일"]
    d["평소대비_원값"] = d["T_원값"]
    d["원점수"] = d["원점수_게이지"]
    d["최종단계"] = d["단계_최종"].astype("int64")
    d["단계이름"] = d["최종단계"].map(stage_names())
    d["지속일수"] = sm.stage_streak(d["최종단계"]).to_numpy()
    top = d["그날까지_상위%"].astype(float).copy()
    top.iloc[:TOP_PCT_HIDE_DAYS] = np.nan
    d["상위%_표시"] = np.round(top, 1)   # 사용자 10-30: 요약.csv·그림 hover와 같은 반올림(np.round) — 화면 :.1f는 x.x5에서 달랐음(43.15 → 43.1)
    d["완화할인_δ"] = relief_delta(scenario, raw.index, data_dir).round(3).to_numpy()
    return d


def _period(fname, scenario, data_dir):
    _check(scenario)
    t = tio.read_csv_kr(Path(data_dir) / fname)
    t = t[t["시나리오"] == scenario].drop(columns="시나리오").reset_index(drop=True)
    t["평소대비"] = t["T_평균"]
    t["원점수"] = t["원점수_평균"]
    t["최종단계"] = t["단계_최고"]
    return t


def monthly(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 월별 — 월별.csv의 그 시나리오 + 화면 이름 열(평소대비 = T_평균 · 원점수 = 원점수_평균 · 최종단계 = 단계_최고)."""
    return _period("월별.csv", scenario, data_dir)


def yearly(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 연도별 — 연도별.csv의 그 시나리오 + 화면 이름 열(월별과 같음)."""
    return _period("연도별.csv", scenario, data_dir)


def summary(data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 요약 — 요약.csv 그대로(행 = 지표, 열 = 기본·확장(C5 포함), 값은 글자)."""
    return tio.read_csv_kr(Path(data_dir) / "요약.csv", index_col=0, dtype=str, keep_default_na=False)


def cuts(scenario="기본", data_dir=DATA_DIR) -> tuple:
    """(화면) T 구간 4개(2·3·4·5거 시작) — 요약.csv `T구간(2·3·4·5거 시작)`에서. 숫자를 코드에 적지 않는다(ADR-018 규칙으로 매번 뽑음)."""
    _check(scenario)
    text = summary(data_dir).loc["T구간(2·3·4·5거 시작)", SUMMARY_COLUMN[scenario]]
    return tuple(int(float(v)) for v in text.split("/"))


def stage_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 단계 기준표 — 단계 · 이름 · T 구간(이상) · 봉수 원뜻 · 하한으로 켜지는 경우(문턱은 config 값으로 씀)."""
    c = cuts(scenario, data_dir)
    names = stage_names()
    pf, ef = config.PHYS_FLOOR, config.E5_FLOOR
    floors = {1: "—", 2: "—",
              3: f"핵실험·ICBM(S≥{config.EVENT_FLOOR_ICBM_S:g}) 당일 · 물리 충돌 원점수 ≥ {pf['3거']:g} · "
                 f"풍선 ≥ {pf['풍선3거']:g} · 북러 밀착 ≥ {ef['3거']:g}",
              4: f"물리 충돌 원점수 ≥ {pf['4거']:g} · 4거 유형 사건 당일(침범·교전·사상자) · 북러 밀착 ≥ {ef['4거']:g}",
              5: "사망·침몰 당일(천안함·연평도)"}
    return pd.DataFrame({"단계": [1, 2, 3, 4, 5],
                         "이름": [f"{k}거 · {names[k]}" for k in range(1, 6)],
                         "T 구간(이상)": [0, *c],
                         "봉수 원뜻": [STAGE_MEANING[k] for k in range(1, 6)],
                         "하한으로 켜지는 경우": [floors[k] for k in range(1, 6)]})


def crisis_marks(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 위기 눈금 — 내부 위기 10건의 날짜·종류·14일 안 최고 단계·게이지 눈금(요약.csv에서)."""
    _check(scenario)
    s = summary(data_dir)[SUMMARY_COLUMN[scenario]]
    return pd.DataFrame({"위기": [n for n, _, _ in config.CRISIS_LIST],
                         "날짜": pd.to_datetime([d for _, d, _ in config.CRISIS_LIST]),
                         "종류": [k for _, _, k in config.CRISIS_LIST],
                         "단계": [int(s[n]) for n, _, _ in config.CRISIS_LIST],
                         "게이지 눈금": [float(s[f"게이지_{n}"]) for n, _, _ in config.CRISIS_LIST]})


@lru_cache(maxsize=1)
def _actor_map(processed_dir=PROCESSED_DIR) -> dict:
    """(보조) 사건ID → 주체국 — data/processed 아래 CSV 중 사건ID·주체국 열이 있는 것(처음 나온 값)."""
    out = {}
    for f in sorted(Path(processed_dir).glob("*/*.csv")):
        try:
            t = tio.read_csv_kr(f, dtype=str, keep_default_na=False, usecols=lambda c: c in ("사건ID", "주체국"))
        except (ValueError, UnicodeDecodeError):
            continue
        if {"사건ID", "주체국"} <= set(t.columns):
            for k, v in zip(t["사건ID"], t["주체국"]):
                if k and v and k not in out:
                    out[k] = v
    return out


def contributions(day=None, scenario="기본", top=10, data_dir=DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(화면) 점수 구성 — (묶음별 표, 사건별 남은 점수 상위 top건). day = 기준일(None이면 마지막 날, 그 전 마지막 날 기준).

    묶음별: 상승 묶음 T_g · 상승 지수 T⁺(평균) · 완화 할인 δ · T. 사건별: 남은 점수 = S · 2^(−경과일/반감기),
    구분 = 상승 / 완화(할인) / 하한 대상(물리 충돌·북러 밀착 — T에 더하지 않고 하한에만) / 표시만.
    """
    d = daily(scenario, data_dir)
    day = d["날짜"].iloc[-1] if day is None else pd.Timestamp(day)
    row = d[d["날짜"] <= day].iloc[-1]
    bundles = list(SCENARIOS[scenario])
    tg = [float(row[f"Tg_{b}"]) for b in bundles]
    t_plus = float(np.mean(tg))
    table = pd.DataFrame({"항목": [*bundles, "상승 지수 T⁺(평균)", "완화 할인 δ", "T = T⁺ × (1 − δ)"],
                          "값": [*tg, t_plus, float(row["완화할인_δ"]), float(row["T_원값"])],
                          "설명": [*["묶음별 평소 대비(평소 = 100)"] * len(bundles), "상승 묶음의 평균",
                                 "남북 회담(F2)에 따른 할인율(0~0.5)", "그날 긴장도 원값"]})
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    ev = events[events["date"] <= row["날짜"]].copy()
    ev["경과일"] = (row["날짜"] - ev["date"]).dt.days
    ev["남은점수"] = (ev["S"] * 2.0 ** (-ev["경과일"] / config.HALF_LIFE_DAYS)).round(3)
    ev["구분"] = ev["묶음"].map(lambda b: "상승" if b in bundles else KIND.get(b, "그 밖"))
    actors = _actor_map()
    ev["주체국"] = ev["사건ID"].map(lambda k: actors.get(k, UNKNOWN_ACTOR))
    ev = ev.sort_values(["남은점수", "date"], ascending=[False, False]).head(top)
    ev = ev.rename(columns={"date": "날짜"})[["날짜", "사건ID", "요소", "묶음", "구분", "S", "남은점수", "주체국", "사건명"]]
    return table, ev.reset_index(drop=True)


def figure(scenario="기본", data_dir=DATA_DIR):
    """(화면) 추이 그림 — charts.trend_figure. 기본이면 확장을 점선으로 겹친다(사용자 10-29: 기본이 주)."""
    from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
    compare = daily_raw("확장", data_dir) if scenario == "기본" else None
    return charts.trend_figure(daily_raw(scenario, data_dir), cuts(scenario, data_dir), compare=compare)


# ===== F6 — 비교선 T_basic · GPR 비교 · 반감기 민감도 · 유사 시기 주요 사건 =====
def _by_scenario(fname, scenario, data_dir):
    _check(scenario)
    t = tio.read_csv_kr(Path(data_dir) / fname)
    return t[t["시나리오"] == scenario].drop(columns="시나리오").reset_index(drop=True)


def basic_line(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 비교선 — 날짜 · T_원값 · T_표시7일(주 지수) · T_basic · T_basic_표시7일 · 차이_표시7일(T_basic − 주 지수, 7일 평균).

    T_basic = 상승 묶음 R 합 ÷ 기준기간 평균 × 100 × (1 − δ)(⑮′) — 묶음별 정규화만 뺀 값(사용자 10-29). 설명 자리(산출 방법)용.
    """
    b = _by_scenario("비교선_일별.csv", scenario, data_dir)
    b["날짜"] = pd.to_datetime(b["날짜"])
    d = daily_raw(scenario, data_dir)[["T_원값", "T_표시7일"]].reset_index()
    if len(b) != len(d) or not b["날짜"].equals(d["날짜"]):
        raise ValueError(f"비교선_일별.csv와 일별_{scenario}.csv의 날짜가 다름 — run_tension.py로 함께 다시 만든다")
    out = d.merge(b, on="날짜")
    out["차이_표시7일"] = (out["T_basic_표시7일"] - out["T_표시7일"]).round(3)
    return out


def basic_stats(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 비교선 요약 — 항목·값: 주 지수와 상관(일별 원값) · 차이 최대·중앙(원값 절댓값) · 상승 묶음 평소값(요약.csv B_)."""
    b = basic_line(scenario, data_dir)
    diff = (b["T_basic"] - b["T_원값"]).abs()
    s = summary(data_dir)[SUMMARY_COLUMN[scenario]]
    base = " · ".join(f"{g} {float(s['B_' + g]):.2f}" for g in SCENARIOS[scenario])
    return pd.DataFrame({"항목": ["주 지수(T)와 상관", "차이 최대(원값)", "차이 중앙(원값)", "상승 묶음 평소값"],
                         "값": [f"{b['T_basic'].corr(b['T_원값']):.4f}", f"{diff.max():.1f}", f"{diff.median():.1f}", base]})


def gpr_monthly(path=None) -> pd.DataFrame:
    """(화면) GPR 한국 월별 원본 — 연월 · GPR(GPRC_KOR %). path 기본 = config.GPR_PATH."""
    return tio.load_gpr_monthly(ROOT / config.GPR_PATH if path is None else path)


def _pct_rank(x) -> pd.Series:
    """(보조) 백분위 순위 0~100 — 채점 v0 s3_GPR_비교.py와 같은 rank(pct=True) × 100(같은 값은 평균 순위)."""
    return x.rank(pct=True) * 100


def gpr_compare(scenario="기본", data_dir=DATA_DIR, gpr_path=None) -> pd.DataFrame:
    """(화면) 봉수 vs GPR 월별 — 연월 · 봉수_T평균(월별.csv T_평균) · GPR · 봉수_순위% · GPR_순위% · 순위차(봉수 − GPR).

    두 자료가 다 있는 달만(GPR 끝 달까지). 순위는 그 비교 기간 안 백분위(0~100, 사용자 10-29 — 순위% 두 선).
    """
    m = monthly(scenario, data_dir)[["연월", "T_평균"]].rename(columns={"T_평균": "봉수_T평균"})
    t = m.merge(gpr_monthly(gpr_path), on="연월", how="inner")
    t["봉수_순위%"] = _pct_rank(t["봉수_T평균"]).round(1)
    t["GPR_순위%"] = _pct_rank(t["GPR"]).round(1)
    t["순위차"] = (t["봉수_순위%"] - t["GPR_순위%"]).round(1)
    return t


def gpr_stats(scenario="기본", data_dir=DATA_DIR, gpr_path=None) -> pd.DataFrame:
    """(화면) 봉수 vs GPR 요약 — 항목·값: 비교 기간 · 달 수 · 피어슨 상관 · 순위 상관(스피어만 = 순위의 피어슨)."""
    t = gpr_compare(scenario, data_dir, gpr_path)
    pearson = t["봉수_T평균"].corr(t["GPR"])
    spearman = t["봉수_T평균"].rank().corr(t["GPR"].rank())
    return pd.DataFrame({"항목": ["비교 기간", "달 수", "피어슨 상관", "순위 상관"],
                         "값": [f"{t['연월'].iloc[0]} ~ {t['연월'].iloc[-1]}", str(len(t)), f"{pearson:.2f}", f"{spearman:.2f}"]})


def half_life_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 반감기 민감도 — 반감기_민감도.csv의 그 시나리오(반감기 7·14·21·30일 행, 열은 summary.half_life_table)."""
    return _by_scenario("반감기_민감도.csv", scenario, data_dir)


def month_events(month, scenario="기본", top=3, data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 그달 주요 사건 — month = 'YYYY-MM'. 그달 사건을 점수 S 큰 순으로 top건(같으면 늦은 날 먼저).

    열 = 날짜 · 사건ID · 요소 · 묶음 · 구분(상승 / 완화(할인) / 하한 대상 / 표시만) · S · 주체국 · 사건명.
    과거 유사 시기 카드의 "주요 사건"(개발 계획 2.3, 사용자 10-29)용. 사건표에 출처 열은 없다.
    """
    _check(scenario)
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    ev = events[events["date"].dt.strftime("%Y-%m") == str(month)].copy()
    bundles = list(SCENARIOS[scenario])
    ev["구분"] = ev["묶음"].map(lambda b: "상승" if b in bundles else KIND.get(b, "그 밖"))
    actors = _actor_map()
    ev["주체국"] = ev["사건ID"].map(lambda k: actors.get(k, UNKNOWN_ACTOR))
    ev = ev.sort_values(["S", "date"], ascending=[False, False]).head(top)
    ev = ev.rename(columns={"date": "날짜"})[["날짜", "사건ID", "요소", "묶음", "구분", "S", "주체국", "사건명"]]
    return ev.reset_index(drop=True)


def events_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 사건표 — 지수 계산에 들어간 사건 전부(기본 720건 · 확장 941건). 박성인 님 요청서 10-30 ①.

    열 = 사건ID · date(날짜형) · 요소 · 묶음 · S · 사건명 — CSV 열 이름 그대로(화면 이름 열은 더하지 않는다). CSV 순서 그대로.
    """
    _check(scenario)
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    return events.reset_index(drop=True)


def normalization_figure(scenario="기본", data_dir=DATA_DIR):
    """(화면) 묶음 정규화 효과 그림 — charts.normalization_figure(주 지수 vs T_basic, 7일 평균)."""
    from utils.tension import charts
    return charts.normalization_figure(basic_line(scenario, data_dir))


def gpr_figure(scenario="기본", data_dir=DATA_DIR, gpr_path=None):
    """(화면) GPR 비교 그림 — charts.gpr_figure(순위% 두 선)."""
    from utils.tension import charts
    return charts.gpr_figure(gpr_compare(scenario, data_dir, gpr_path))
