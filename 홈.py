import streamlit as st

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide", page_icon="🛡️")

# ===== 홈 화면 ====='
st.title(" 🛡️ 한반도 군사 긴장도 대시보드")
st.write("사건 데이터를 점수로 바꿔, 지금 한반도의 군사 긴장이 평소보다 얼마나 높은지 보여 줍니다.")

st.write("")  # 여백 추가

# 세로
with st.container(border=True):
    st.page_link("pages/1_긴장도_지수.py", label="긴장도 지수: 지금 몇 단계인지", icon="⚠️")
with st.container(border=True):
    st.page_link("pages/2_사건_기록.py", label="사건 기록: 어떤 사건이 있었는지", icon="🔎")
with st.container(border=True):
    st.page_link("pages/3_월별_연별.py", label="월별·연별 추이: 언제 높았는지", icon="📆")
with st.container(border=True):
    st.page_link("pages/4_보고서.py", label="보고서: 브리핑 작성", icon="📃")

# 가로
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     with st.container(border=True):
#         st.page_link("pages/1_긴장도_지수.py", label="긴장도 지수: 지금 몇 단계인지", icon="⚠️")
# with col2:
#     with st.container(border=True):
#         st.page_link("pages/2_사건_기록.py", label="사건 기록: 어떤 사건이 있었는지", icon="🔎")
# with col3:
#     with st.container(border=True):
#         st.page_link("pages/3_월별_연별.py", label="월별·연별 추이: 언제 높았는지", icon="📆")
# with col4:
#     with st.container(border=True):
#         st.page_link("pages/4_보고서.py", label="보고서: 브리핑 작성", icon="📃")

# 원문
# st.page_link("pages/1_긴장도_지수.py", label="긴장도 지수: 지금 몇 단계인지", icon="⚠️")
# st.page_link("pages/2_사건_기록.py", label="사건 기록: 어떤 사건이 있었는지", icon="🔎")
# st.page_link("pages/3_월별_연별.py", label="월별·연별 추이: 언제 높았는지", icon="📆")
# st.page_link("pages/4_보고서.py", label="보고서: 브리핑 작성", icon="📃")