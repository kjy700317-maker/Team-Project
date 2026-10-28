import streamlit as st
import config
from utils.loader import load_monthly, load_yearly, load_events   # [수정] 사건 표도 불러옴 (TOP 5 카드용)
import plotly.express as px

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")

# ===== 페이지 제목 =====
st.title("월별·연별 추이")
st.caption("막대 높이 = 그 기간 평소대비 평균, 막대 색 = 그 기간에 가장 높았던 날의 단계")   # [수정] 읽는 법 설명

# ===== 보기 단위 고르기 필터, 슬라이더=====
c1, c2 = st.columns([1, 3])   # [수정] 단위와 슬라이더를 한 줄에 (1:3)
unit = c1.radio("보기 단위", ["연별", "월별"], horizontal=True)
start_year = c2.slider("시작 연도", 1945, 2026, 1990) # 끌어서 숫자 고르기(제목, 최소, 최대, 기본값)
if unit == "연별":
    data = load_yearly()
    data = data[data["연도"] >= start_year].copy() # 시작 연도부터만 / 걸러낸 표에 단계 3개 생성 할 거라 미리 복제함, 오류 예방
    x = "연도"
else:
    data = load_monthly()
    data = data[data["연월"].str[:4].astype(int) >= start_year].copy() # "2024-06" → "2024" → 2024
    x = "연월"

# ===== 막대그래프 =====
data["최고 단계"] = data["최종단계"].map(config.STAGE_NAMES) # 4 → 경계 / [수정] max로 구한 단계라 이름을 "최고 단계"로
color_map = {} # 빈 딕셔너리
for no in config.STAGE_NAMES: # no = 1, 2, 3, 4, 5
    color_map[config.STAGE_NAMES[no]] = config.STAGE_COLORS[no] # {"평온": 초록, "관심": 파랑, ...}

fig = px.bar(data, x=x, y="평소대비", color="최고 단계", color_discrete_map=color_map, category_orders={"최고 단계": list(config.STAGE_NAMES.values())})
# color: 이 칸 값마다 색을 다르게함, 단계 이름마다 다른 색 막대가 됨 / _discrete_ma: 어떤 값에 어떤 색인지 지정함 / _orders: 범례 순서: 평온 -> 심각 로 나오게함
fig.add_hline(y=100, line_color="gray", annotation_text="평소 100", annotation_position="top left")   # [수정] 숫자를 왼쪽 위로 (오른쪽 막대와 안 겹치게)
st.plotly_chart(fig)

# ===== 가장 긴장이 높았던 시기 TOP 5 =====
st.subheader(f"가장 긴장이 높았던 {unit[:1]} TOP 5") # "연별"[:1] → 연별이면 "연", 월별이면 "월" (첫 글자)
top = data.nlargest(5, "평소대비") # nlargest(5, 칸): nsmallest의 반대 - 그 칸의 큰 순서로 5개

# ===== [수정] TOP 5 카드 (표 대신 단계 색 카드 5장) =====
events = load_events().copy()
events["가중치"] = events["카테고리코드"].map(config.WEIGHTS)            # 사건 1건의 기여
events["종류"] = events["카테고리코드"].map(config.ELEMENT_NAMES)         # A2 → 미사일 발사
events["연도"] = events["시작일"].dt.year                                 # 2017
events["연월"] = events["시작일"].dt.strftime("%Y-%m")                     # "2017-09"

cols = st.columns(5)                                                       # 카드 5장 가로로
for i in range(len(top)):
    row = top.iloc[i]                                                      # i등 시기
    no = int(row["최종단계"])                                              # 그 시기 최고 단계 번호
    c = config.STAGE_COLORS[no]                                            # 단계 색
    e = events[events[x] == row[x]]                                        # 그 시기 사건만 (x = "연도" 또는 "연월")
    kinds = e[e["가중치"] > 0]["종류"].value_counts().head(3)              # 지수를 올린 사건 종류별 건수 상위 3개
    kind_text = "<br>".join(f"{k} {n}건" for k, n in kinds.items())       # "미사일 발사 12건" 줄마다
    with cols[i]:
        st.markdown(
            f"<div style='background:{c}1A; border-top:5px solid {c}; border-radius:10px; padding:12px 14px; min-height:210px;'>"   # 1A = 아주 연한 단계 색
            f"<div style='color:#888; font-size:13px;'>{i + 1}위</div>"
            f"<div style='font-size:20px; font-weight:700;'>{row[x]}</div>"
            f"<div style='font-size:12px; color:#888; margin-top:6px;'>평소대비 (평소=100)</div>"   # [수정] 숫자 위에 이름표
            f"<div style='font-size:30px; font-weight:700; color:{c}; line-height:1.1;'>{row['평소대비']:.0f}</div>"   # 평소대비 (단계 색 글씨)
            f"<div style='display:inline-block; background:{c}; color:white; border-radius:6px; padding:1px 8px; font-size:13px;'>최고 {no}단계 {config.STAGE_NAMES[no]}</div>"
            f"<div style='margin-top:10px; font-size:13px; color:#444; line-height:1.6;'>{kind_text}</div></div>",
            unsafe_allow_html=True)
        with st.expander(f"사건 {len(e)}건 보기"):                         # 펼치면 사건 목록
            e = e.sort_values(["가중치", "시작일"], ascending=[False, True])   # 기여 큰 순
            for _, r in e.head(10).iterrows():                             # 최대 10건
                st.caption(f"{r['시작일']:%m-%d} · {r['종류']} · {r['사건명']}")
            if len(e) > 10:
                st.caption(f"외 {len(e) - 10}건은 사건 기록 페이지에서")
