import streamlit as st
import config
from utils.loader import load_monthly, load_yearly
import plotly.express as px

# ===== 페이지 제목 =====
st.title("월별·연별 추이")

# ===== 보기 단위 고르기 필터, 슬라이더=====
unit = st.radio("보기 단위", ["연별", "월별"], horizontal=True)
start_year = st.slider("시작 연도", 1945, 2026, 1990) # 끌어서 숫자 고르기(제목, 최소, 최대, 기본값)
if unit == "연별":
    data = load_yearly()
    data = data[data["연도"] >= start_year].copy() # 시작 연도부터만 / 걸러낸 표에 단계 3개 생성 할 거라 미리 복제함, 오류 예방
    x = "연도"
else:
    data = load_monthly()
    data = data[data["연월"].str[:4].astype(int) >= start_year].copy() # "2024-06" → "2024" → 2024
    x = "연월"
    
# ===== 막대그래프 =====
data["단계"] = data["최종단계"].map(config.STAGE_NAMES) # 4 → 경계
color_map = {} # 빈 딕셔너리
for no in config.STAGE_NAMES: # no = 1, 2, 3, 4, 5
    color_map[config.STAGE_NAMES[no]] = config.STAGE_COLORS[no] # {"평온": 초록, "관심": 파랑, ...}

fig = px.bar(data, x=x, y="평소대비", color="단계", color_discrete_map=color_map, category_orders={"단계": list(config.STAGE_NAMES.values())}) 
# color: 이 칸 값마다 색을 다르게함, 단계 이름마다 다른 색 막대가 됨 / _discrete_ma: 어떤 값에 어떤 색인지 지정함 / _orders: 범례 순서: 평온 -> 심각 로 나오게함
fig.add_hline(y=100, line_color="gray", annotation_text="평소 100")
st.plotly_chart(fig)

# ===== 가장 긴장이 높았던 시기 TOP 5 =====
st.subheader(f"가장 긴장이 높았던 {unit[:1]} TOP 5") # "연별"[:1] → 연별이면 "연", 월별이면 "월" (첫 글자)
top = data.nlargest(5, "평소대비") # nlargest(5, 칸): nsmallest의 반대 - 그 칸의 큰 순서로 5개
st.dataframe(top[[x, "원점수", "평소대비", "단계"]], hide_index=True)

# ===== 슬라이더 확인용 =====
# st.write(len(data))
# st.dataframe(data, hide_index=True)

# ===== 막대그래프 확인용 =====
st.write(len(data))