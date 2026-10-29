import config
from utils.dummy import make_daily, make_monthly, make_elements, make_yearly # 쉼표로 여러 개를 한 번에 가져올 수 있음
from utils.real import make_daily_real, make_recent_elements, make_events
import streamlit as st

# ===== 일별 표 통로 =====
@st.cache_data
def load_daily():
    if config.USE_DUMMY: # 스위치가 True면 더미, False면 진짜
        return make_daily()
    else:
        return make_daily_real() # 진짜 결과_일별

# ===== 월별 표 통로 =====
@st.cache_data
def load_monthly():
    if config.USE_DUMMY:
        return make_monthly(make_daily())
    else:
        return make_monthly(make_daily_real())  # make_monthly를 진짜 일별 표에 그대로 재사용

# ===== 점수 구성 통로 =====
@st.cache_data
def load_elements(day=None): # [수정] 기준일을 받을 수 있게 (안 주면 최신)
    if config.USE_DUMMY:
        return make_elements()
    else:
        return make_recent_elements(day) # 진짜 최근 30일 요소 / [수정] 기준일 전달

# ===== 사건 표 통로 =====
@st.cache_data
def load_events():
    return make_events()

# ===== 연별 표 통로 =====
@st.cache_data
def load_yearly():
    if config.USE_DUMMY:
        return make_yearly(make_daily())
    else:
        return make_yearly(make_daily_real()) # 진짜 일별 표를 연별로 묶기


# ===== [F5 추가 · 긴장도 담당] 긴장도 결과 통로 — data/tension 결과 CSV(utils/tension/screen.py) =====
# 위 기존 함수(load_daily 등)는 그대로 둔다. 화면 담당자가 화면을 고칠 때 아래 함수로 바꾼다(요청서 docs/dev/requests/).
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
