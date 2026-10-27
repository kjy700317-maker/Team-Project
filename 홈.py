import streamlit as st
import config
from utils.loader import load_daily, load_events

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide", page_icon="🛡️")

# ===== 데이터 불러오기 (홈에도 지금 단계를 보여 주기 위해) =====
df = load_daily()                                   # 결과_일별 표
events = load_events()                              # 사건_일단위 표
latest = df.iloc[-1]                                # 가장 최근 날
stage = int(latest["최종단계"])
color = config.STAGE_COLORS[stage]                  # 지금 단계 색

# ===== 제목 =====
st.title("🛡️ 한반도 군사 긴장도 대시보드")
st.caption("사건 데이터를 점수로 바꿔, 지금 한반도의 군사 긴장이 평소보다 얼마나 높은지 보여 줍니다.")

# ===== 지금 단계 띠 =====
st.markdown(
    f"<div style='background:{color}; color:white; padding:18px 22px; border-radius:12px;'>"
    f"<div style='font-size:14px; opacity:0.9;'>{latest['날짜']:%Y-%m-%d} 기준 현재 단계</div>"
    f"<div style='font-size:30px; font-weight:700;'>{stage}단계 {config.STAGE_NAMES[stage]}</div>"
    f"<div style='font-size:15px;'>평소대비 {latest['평소대비']:.0f} · 4단계 이상 {int(latest['지속일수'])}일째</div></div>",
    unsafe_allow_html=True)   # 글 안의 HTML(색 상자)을 그대로 그리게 허락

# ===== 5단계 눈금 (지금 단계만 진하게) =====
scale = ""                                          # 칸 5개를 이어 붙일 빈 글
for no, name in config.STAGE_NAMES.items():         # .items(): (번호, 이름)을 같이 꺼냄
    if no == stage:                                 # 지금 단계: 진한 색 + 흰 글씨 + 굵게
        bg, text, weight = config.STAGE_COLORS[no], "white", 700
    else:                                           # 나머지: 연한 색(뒤에 "40" = 투명도 25%) + 회색 글씨
        bg, text, weight = config.STAGE_COLORS[no] + "40", "#555", 400
    scale += (f"<div style='flex:1; background:{bg}; color:{text}; font-weight:{weight}; "
              f"text-align:center; padding:6px 0; font-size:13px; border-radius:6px;'>{no} {name}</div>")
st.markdown(f"<div style='display:flex; gap:4px; margin-top:8px;'>{scale}</div>",   # flex: 칸을 가로로 나란히
            unsafe_allow_html=True)
st.write("")

# ===== 페이지 안내 카드 (2 × 2) =====
pages = [   # (파일, 제목, 아이콘, 설명) 4개를 목록으로 모아 두기
    ("pages/1_긴장도_지수.py", "긴장도 지수", "⚠️", "지금 몇 단계인지, 평소보다 얼마나 높은지"),
    ("pages/2_사건_기록.py", "사건 기록", "🔎", "기간·종류·검색어로 어떤 사건이 있었는지"),
    ("pages/3_월별_연별.py", "월별·연별 추이", "📆", "언제 긴장이 높았는지, 가장 높았던 시기 TOP 5"),
    ("pages/4_보고서.py", "보고서", "📃", "숫자로 자동 작성한 브리핑, 워드로 내려받기"),
]
cols = st.columns(2)                                # 2칸
for i, (path, title, icon, desc) in enumerate(pages):   # 4개를 하나씩, i = 0,1,2,3
    with cols[i % 2]:                               # i % 2: 2로 나눈 나머지 → 0,1,0,1 → 왼쪽·오른쪽 번갈아
        with st.container(border=True):
            st.page_link(path, label=f"**{title}**", icon=icon)
            st.caption(desc)

# ===== 데이터 안내 =====
st.divider()                                        # 가는 가로줄
st.caption(f"사건 {len(events):,}건 · {events['시작일'].min():%Y-%m-%d} ~ {events['시작일'].max():%Y-%m-%d} · "
           "가중치·기준선은 현재 진행도 기준 임시값이며 추후 결정됩니다.")   # :, → 천 단위 쉼표 (3,860)
