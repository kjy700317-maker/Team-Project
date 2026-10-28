import streamlit as st

st.title("🛡️ 국방 대시보드 프로젝트")
st.write("팀 표준 Python 3.11 및 가상환경 연동 완료!")

# 간단한 테스트용 지표
col1, col2 = st.columns(2)
with col1:
    st.metric(label="시스템 상태", value="정상 작동", delta="Stable")
with col2:
    st.metric(label="참여 인원", value="5명", delta="Team Project")