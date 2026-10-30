from utils.real import make_events
import streamlit as st

# ===== 사건 표 통로 (2페이지 사건 기록) =====
@st.cache_data
def load_events():
    return make_events()


# ===== [F5 추가 · 긴장도 담당] 긴장도 결과 통로 — data/tension 결과 CSV(utils/tension/screen.py) =====
# 옛 임시 계산 통로(load_daily·load_monthly·load_elements·load_yearly)·더미 모드는 F7c에서 지웠다(10-30 박성인 확인). 화면은 아래 함수를 쓴다.
from utils.tension import screen as tension_screen   # noqa: E402


@st.cache_data
def load_tension_daily(scenario="기본"):  # 일별 — 결과 열 + 화면 이름 열(평소대비·평소대비_원값·원점수·최종단계·단계이름·지속일수·상위%_표시·완화할인_δ)
    return tension_screen.daily(scenario)


@st.cache_data
def load_tension_monthly(scenario="기본"):  # 월별 — 평소대비 = T_평균 · 원점수 = 원점수_평균 · 최종단계 = 단계_최고
    return tension_screen.monthly(scenario)


@st.cache_data
def load_tension_yearly(scenario="기본"):  # 연도별 — 월별과 같은 열
    return tension_screen.yearly(scenario)


@st.cache_data
def load_tension_summary():  # 요약 — 행 = 지표, 열 = 기본·확장(C5 포함)
    return tension_screen.summary()


@st.cache_data
def load_tension_stage_table(scenario="기본"):  # 단계 기준표 — 단계·이름·T 구간(이상)·봉수 원뜻·하한으로 켜지는 경우
    return tension_screen.stage_table(scenario)


@st.cache_data
def load_tension_crisis_marks(scenario="기본"):  # 위기 10건 — 날짜·종류·14일 최고 단계·게이지 눈금
    return tension_screen.crisis_marks(scenario)


@st.cache_data
def load_tension_contrib(day=None, scenario="기본", top=10):  # 점수 구성 — (묶음별 표, 사건별 남은 점수 상위 top건)
    return tension_screen.contributions(day, scenario, top)


@st.cache_data
def load_tension_figure(scenario="기본"):  # 추이 그림(Plotly) — st.plotly_chart(load_tension_figure())
    return tension_screen.figure(scenario)


# ===== [F6 추가 · 긴장도 담당] 비교선 T_basic · GPR 비교 · 반감기 민감도 · 유사 시기 주요 사건 (utils/tension/screen.py) =====
# 위 함수는 그대로 둔다. 화면에 붙이는 일은 화면 담당자께 요청(docs/dev/requests/F6_화면요청.md).
@st.cache_data
def load_tension_basic(scenario="기본"):  # 비교선 — 날짜·T_원값·T_표시7일·T_basic·T_basic_표시7일·차이_표시7일(설명 자리용)
    return tension_screen.basic_line(scenario)


@st.cache_data
def load_tension_basic_stats(scenario="기본"):  # 비교선 요약 — 항목·값(상관·차이·상승 묶음 평소값)
    return tension_screen.basic_stats(scenario)


@st.cache_data
def load_tension_normalization_figure(scenario="기본"):  # 묶음 정규화 효과 그림(Plotly)
    return tension_screen.normalization_figure(scenario)


@st.cache_data
def load_tension_gpr(scenario="기본"):  # 봉수 vs GPR 월별 — 연월·봉수_T평균·GPR·봉수_순위%·GPR_순위%·순위차
    return tension_screen.gpr_compare(scenario)


@st.cache_data
def load_tension_gpr_stats(scenario="기본"):  # GPR 비교 요약 — 항목·값(비교 기간·달 수·피어슨·순위 상관)
    return tension_screen.gpr_stats(scenario)


@st.cache_data
def load_tension_gpr_figure(scenario="기본"):  # GPR 비교 그림(Plotly, 순위% 두 선)
    return tension_screen.gpr_figure(scenario)


@st.cache_data
def load_tension_half_life(scenario="기본"):  # 반감기 민감도 — 반감기 7·14·21·30일 행(T 구간·1~5거%·같은 날%·위기 10건·현재)
    return tension_screen.half_life_table(scenario)


@st.cache_data
def load_tension_month_events(month, scenario="기본", top=3):  # 그달 주요 사건(유사 시기 카드) — month = "YYYY-MM"
    return tension_screen.month_events(month, scenario, top)


@st.cache_data
def load_tension_events(scenario="기본"):  # 사건표 — 사건ID·date(날짜형)·요소·묶음·S·사건명 (지수에 들어간 사건 전부, 기본 720건·확장 941건)
    return tension_screen.events_table(scenario)
