import streamlit as st
import config
from utils.loader import load_events # 정리된 사건 표 통로
from datetime import timedelta # 날짜 빼기용
import plotly.express as px # 막대그레프

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")

# ===== 페이지 제목 =====
st.title("사건 기록") # 정리된 사건 표 창구

# ===== 데이터 불러오기 =====
events = load_events() # 사건_일단위 표

# ===== 요소명 붙이기 & 정렬 =====
events = events.sort_values("시작일", ascending=False) # 최신 사건이 맨 위
events["요소명"] = events["카테고리코드"].map(config.ELEMENT_NAMES)  # A2 → 미사일 발사
events["시작일"] = events["시작일"].dt.date # 시,분,초 떼고 날짜만
events = events[["시작일", "카테고리코드", "요소명", "주체국", "대상국", "사건명", "사건ID"]]   # 칸 순서 정하기 /  칸을 고르면서 순서도 정함

# ===== 사이드바 필터 =====
st.sidebar.header("필터") # st.sidebar. = 왼쪽 메뉴 영역에 그리기 , 위젯을 왼쪽 메뉴 아래에 그림
first = events["시작일"].min() # 가장 오래된 날 (1945-07-16)
last = events["시작일"].max() # 가장 최근 날 (2026-09-30)
period = st.sidebar.date_input("기간", value=(last - timedelta(days=365), last), min_value=first, max_value=last) # 기본: 최근 1년, 값을 두 개 주면 기간 선택 달력이 됨
start, end = period[0], period[-1] # 달력에서 시작일만 누른 순간에는 값이 하나뿐이라 period[1] 입력시 오류 / 시작일만 골랐을 때도 에러 안 나게 [0], [-1]
kinds = st.sidebar.multiselect("사건 종류 (비우면 전체)", list(config.ELEMENT_NAMES.values())) # 여러 개 고르기
actors = st.sidebar.multiselect("주체국 (비우면 전체)", sorted(events["주체국"].unique())) # unique: 중복 없이, sorted: 가나다순
word = st.sidebar.text_input("사건명 검색") # 글자 입력칸

events = events[(events["시작일"] >= start) & (events["시작일"] <= end)] # 기간 안의 사건만
if kinds: # 하나라도 골랐으면
    events = events[events["요소명"].isin(kinds)] # isin: 고른 목록 안에 있는 줄만
if actors:
    events = events[events["주체국"].isin(actors)]
if word: # 검색어를 썼으면
    events = events[events["사건명"].str.contains(word, na=False)] # 사건명에 그 글자가 들어간 줄만

# ===== 요약 카드, 종류별 막대그래프, 표 =====
if len(events) == 0: # 필터 결과가 0건이면
    st.warning("조건에 맞는 사건이 없습니다.") # 노란 안내 상자
    st.stop() # 아래 코드는 실행하지 않고 멈춤

col1, col2, col3 = st.columns(3)
col1.metric("사건 수", f"{len(events)}건")
col2.metric("가장 많은 종류", events["요소명"].value_counts().index[0]) # 건수 1등의 이름
col3.metric("가장 많은 주체국", events["주체국"].value_counts().index[0])

counts = events["요소명"].value_counts().reset_index() # 표로 바꾸기: 요소명 | count
fig = px.bar(counts, x="요소명", y="count", labels={"count": "건수"}) # labels: 축 이름 바꾸기
st.plotly_chart(fig)

st.subheader("사건 목록")
st.dataframe(events, hide_index=True)

# ===== 확인용 =====
# st.write(len(events)) # 몇 건
# st.dataframe(events, hide_index=True)

