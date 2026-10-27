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
