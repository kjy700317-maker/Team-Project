import config
from utils.dummy import make_daily, make_monthly, make_elements # 쉼표로 여러 개를 한 번에 가져올 수 있음
from utils.real import make_daily_real, make_recent_elements
import streamlit as st
# ===== 테이블 통로 =====
@st.cache_data
def load_daily():
    if config.USE_DUMMY: # 스위치가 True면 아래 줄을 실행
        return make_daily() # 더미 자판기에서 받은 표를 그대로 넘겨줌
    else:
        raise NotImplementedError("테이블 아직 실제 DB 연결을 하지 않음") # 일부러 에러를 내는 명령 실제 데이터가 아직 넣지 않았기에 사전에 공지하는 용도

# ===== 월별 표 통로 =====
@st.cache_data
def load_monthly():
    if config.USE_DUMMY:
        return make_monthly(make_daily()) # 더미 일별 표를 만들어서 월별로 묶어 알려줌
    else:
        raise NotImplementedError("월별 표 아직 실제 DB 연결을 하지 않음")

# ===== 점수구성 통로 =====
@st.cache_data
def load_elements():
    if config.USE_DUMMY:
        return make_elements()
    else:
        raise NotImplementedError("점수 아직 실제 DB 연결을 하지 않음")

@st.cache_data
def load_daily():
    if config.USE_DUMMY:
        return make_daily()
    else:
        return make_daily_real()              # 진짜 결과_일별

@st.cache_data
def load_monthly():
    if config.USE_DUMMY:
        return make_monthly(make_daily())
    else:
        return make_monthly(make_daily_real())  #  make_monthly를 진짜 일별 표에 그대로 재사용

@st.cache_data
def load_elements():
    if config.USE_DUMMY:
        return make_elements()
    else:
        return make_recent_elements()          # 진짜 최근 30일 요소