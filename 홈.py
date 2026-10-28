import streamlit as st
import config
from utils.loader import load_daily, load_events
from utils.ui import stage_scale   # [수정] 5단계 눈금 (보고서와 같이 씀)

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
    f"<div style='font-size:15px;'>평소대비 {latest['평소대비']:.0f}"
    + (f" · 4단계 이상 {int(latest['지속일수'])}일째" if latest["지속일수"] > 0 else "") + "</div></div>",   # [수정] 지속일수는 4단계 이상일 때만 (1·4페이지와 같게)
    unsafe_allow_html=True)   # 글 안의 HTML(색 상자)을 그대로 그리게 허락

# ===== 5단계 눈금 (지금 단계만 진하게) =====
st.markdown(stage_scale(stage), unsafe_allow_html=True)   # [수정] 눈금 만드는 코드는 utils/ui.py로 옮김
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
