import streamlit as st

st.title("🛡️ 국방 대시보드 프로젝트") # 화면 맨 위에 큰 제목
st.write("팀 표준 Python 3.11 및 가상환경 연동 완료!") # 일반 글

# 간단한 테스트용 지표
col1, col2 = st.columns(2)  # 화면을 가로로 두간으로 나누고, 각칸에 col1, col2 라는 이름을 붙여요
with col1: # 숫자 카드를 그린다, label운 작은 제목, value는 큰값, delta는 그 아레 작은 변화량
    st.metric(label="시스템 상태", value="정상 작동", delta="Stable")
with col2:
    st.metric(label="참여 인원", value="4명", delta="Team Project")