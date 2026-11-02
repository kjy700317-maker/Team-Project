import streamlit as st
import config
from utils.loader import load_events, load_tension_events # 정리된 사건 표 통로
from datetime import timedelta # 날짜 빼기용
import plotly.express as px # 막대그래프
import pandas as pd
from utils.ui import index_mark, page_style, white_table, icon, hero, period_picker

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")
page_style()   # 공통 디자인

# ===== 페이지 제목 =====
st.markdown(hero("사건 기록", "왼쪽 필터로 기간·종류·주체국·검색어를 골라 보세요. 처음에는 최근 1년이 보입니다.", art="search"), unsafe_allow_html=True)   # 남색 제목 배너

# ===== 데이터 불러오기 =====
events = load_events() # 사건_일단위 표

# ===== 요소명 붙이기 & 정렬 =====
events = events.sort_values("시작일", ascending=False) # 최신 사건이 맨 위
events["요소명"] = events["카테고리코드"].map(config.ELEMENT_NAMES)  # A2 → 미사일 발사
events["시작일"] = events["시작일"].dt.date # 시,분,초 떼고 날짜만
events["분류"] = events["카테고리코드"].str[0].map(config.GROUPS)   # 분류표는 config.GROUPS (보고서도 같이 씀) / "A2"[0] → "A" → "군사행동"
events["대상국"] = events["대상국"].fillna("")   # 빈 칸(None)을 빈 글자로
index_events = load_tension_events()
events = events.merge(index_events[["사건ID", "묶음", "S"]], on="사건ID", how="left")   # 사건ID로 짝 맞추기, 없으면 빈 칸(NaN)
events["지수 반영"] = [index_mark(b, v) for b, v in zip(events["묶음"], events["S"])]   # 표시 규칙은 utils/ui.py
events = events[["시작일", "분류", "요소명", "주체국", "대상국", "사건명", "지수 반영"]]   # 마지막에 "지수 반영" 칸

# ===== 사이드바 필터 =====
st.sidebar.header("필터") # st.sidebar. = 왼쪽 메뉴 영역에 그리기 , 위젯을 왼쪽 메뉴 아래에 그림
first = events["시작일"].min() # 가장 오래된 날 (1945-07-16)
last = events["시작일"].max() # 가장 최근 날 (2026-09-30)
start, end = period_picker("p2_period", first, last, (last - timedelta(days=365), last), sidebar=True)   # 기본: 최근 1년, 함수는 utils/ui.py
kinds = st.sidebar.multiselect("사건 종류 (비우면 전체)", list(config.ELEMENT_NAMES.values())) # 여러 개 고르기
actors = st.sidebar.multiselect("주체국 (비우면 전체)", sorted(events["주체국"].unique())) # unique: 중복 없이, sorted: 가나다순
word = st.sidebar.text_input("사건명 검색") # 글자 입력칸


events = events[(events["시작일"] >= start) & (events["시작일"] <= end)] # 기간 안의 사건만
only_index = st.sidebar.checkbox("지수에 들어간 사건만")   # 체크하면 "지수 밖" 사건을 숨김
if kinds: # 하나라도 골랐으면
    events = events[events["요소명"].isin(kinds)] # isin: 고른 목록 안에 있는 줄만
if actors:
    events = events[events["주체국"].isin(actors)]
if word: # 검색어를 썼으면
    events = events[events["사건명"].str.contains(word, na=False)] # 사건명에 그 글자가 들어간 줄만
if only_index:
    events = events[events["지수 반영"] != "지수 밖"]   # 지수에 들어간 사건만
    
# ===== 요약 카드, 종류별 막대그래프, 표 =====
if len(events) == 0: # 필터 결과가 0건이면
    st.warning("조건에 맞는 사건이 없습니다.") # 노란 안내 상자
    st.stop() # 아래 코드는 실행하지 않고 멈춤

col1, col2, col3 = st.columns(3)
with col1.container(border=True, height="stretch", key="box_col1"):
    st.metric("사건 수", f"{len(events)}건")
    st.caption(f"그중 지수에 들어간 사건 {(events['지수 반영'] != '지수 밖').sum()}건")   # True 개수 = sum
with col2.container(border=True, height="stretch", key="box_col2"):
    st.metric("가장 많은 종류", events["요소명"].value_counts().index[0]) # 건수 1등의 이름
with col3.container(border=True, height="stretch", key="box_col3"):
    st.metric("가장 많은 주체국", events["주체국"].value_counts().index[0])

with st.container(border=True, key="box_chart"):   # 종류별 막대그래프 상자
    counts = events.groupby(["분류", "요소명"]).size().reset_index(name="건수")   # 분류·요소명별 건수 (size: 줄 수 세기)
    counts = counts.sort_values("건수")   # 가로 막대는 아래부터 그려서, 작은 것부터 정렬하면 큰 게 맨 위
    fig = px.bar(counts, x="건수", y="요소명", color="분류", orientation="h", height=max(300, 28 * len(counts)),
                 color_discrete_sequence=px.colors.qualitative.Set2)   # 차분한 기본 색 묶음 (빨강은 단계 색과 헷갈려서 피함)
    # orientation="h": 가로 막대 (긴 이름이 기울지 않음) / color="분류": 큰 분류마다 색 / height: 막대 수에 맞춰 높이
    fig.update_layout(yaxis_title=None)   # 세로축 제목 "요소명" 숨기기
    st.plotly_chart(fig)

with st.container(border=True, key="box_list"):   # 사건 목록 상자
    st.subheader("사건 목록")
    st.dataframe(white_table(events), hide_index=True, width="stretch",
                 column_config={"시작일": "날짜", "요소명": "종류", "사건명": st.column_config.TextColumn("사건명", width="large")})
# column_config: 칸 이름 바꾸기·사건명 칸 넓게
