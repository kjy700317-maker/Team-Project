import streamlit as st
import config
import pandas as pd
from utils.loader import load_tension_daily, load_tension_events   # [수정] 산출식 v0.1.4 결과
from utils.ui import stage_scale_grid   # [수정] 세로 눈금 (Grid)

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide", page_icon="🛡️")

# ===== 데이터 불러오기 (홈에도 지금 단계를 보여 주기 위해) =====
df = load_tension_daily()                           # [수정] 일별 결과 (2010-01-01 ~ 계산일)
events = load_tension_events()
latest = df.iloc[-1]                                # 가장 최근 날
stage = int(latest["최종단계"])
color = config.STAGE_COLORS[stage]                  # 지금 단계 색

# ===== 제목 =====
st.title("🛡️ 한반도 군사 긴장도 대시보드")
st.caption("사건 데이터를 점수로 바꿔, 지금 한반도의 군사 긴장이 평소보다 얼마나 높은지 보여 줍니다.")

# ===== 지금 단계 띠 + 세로 눈금 =====
top = "—" if pd.isna(latest["상위%_표시"]) else f"그날까지 상위 {latest['상위%_표시']:.1f}%"   # [수정] 2010년은 NaN → "—"
note = " (잠정)" if latest["잠정"] else ""                                                    # [수정] 최근 6일은 잠정
band = (f"<div style='background:{color}; color:white; padding:18px 22px; border-radius:12px;'>"   # [수정] 폭은 바깥 격자가 정함
        f"<div style='font-size:14px; opacity:0.9;'>{latest['날짜']:%Y-%m-%d} 기준 현재 단계{note}</div>"
        f"<div style='font-size:40px; font-weight:700;'>{latest['화면_단계문구']} · {latest['단계이름']}</div>"   # [수정] 예: "2거 · 하강 중(판정 1거) · 관심"
        f"<div style='font-size:15px;'>평소대비 {latest['평소대비']:.1f} · {top}"                   # [수정] 평소대비 = 7일 표시값
        + (f" · 4거 이상 {int(latest['지속일수'])}일째" if latest["지속일수"] > 0 else "") + "</div></div>")   # [수정] 0이면 숨김
st.markdown(f"<div style='display:grid; grid-template-columns:1fr 160px; gap:8px;'>{band}{stage_scale_grid(stage)}</div>",   # [수정] 2칸 격자: 띠 = 남는 폭 전부(1fr), 눈금 = 160px
            unsafe_allow_html=True)
st.write("")

# ===== 페이지 안내 카드 (2 × 2) =====
pages = [   # (파일, 제목, 아이콘, 설명) 4개를 목록으로 모아 두기
    ("pages/1_긴장도_지수.py", "긴장도 지수", "⚠️", "지금 몇 단계인지, 평소보다 얼마나 높은지"),
    ("pages/2_사건_기록.py", "사건 기록", "🔎", "기간·종류·검색어로 어떤 사건이 있었는지"),
    ("pages/3_월별_연별.py", "월별·연별 추이", "📆", "언제 긴장이 높았는지, 가장 높았던 시기 TOP 5"),
    ("pages/4_보고서.py", "보고서", "📃", "숫자로 자동 작성한 브리핑, 워드로 내려받기"),
]

card_style = ("display:block; text-decoration:none; color:inherit; border:1px solid #ddd; border-radius:12px;"
             "padding:22px 24px; margin-bottom:16px; min-height:120px;") # [수정] 카드 전체 모양 
cols = st.columns(2) 
# 2칸
for i, (path, title, icon, desc) in enumerate(pages):   # 4개를 하나씩, i = 0,1,2,3
    url = "/" + path.split("/")[1][2:-3] # pages, .py 제거
    with cols[i % 2]: # i % 2: 2로 나눈 나머지 → 0,1,0,1 → 왼쪽·오른쪽 번갈아
        # with st.container(border=True):
        #     st.page_link(path, label=f"**{title}**", icon=icon)
        #     st.caption(desc)
        st.markdown(f"<a href='{url}' target='_self' class='home-card' style='{card_style}'>"
                    f"<span style='display:block; font-size:22px; font-weight:700; margin-bottom:8px;'>{icon} {title}</span>"
                    f"<span style='display:block; font-size:16px; color:#666;'>{desc}</span></a>",
                    unsafe_allow_html=True)
# ===== 데이터 안내 =====
st.caption(f"지수에 들어간 사건 {len(events):,}건 ({config.CALC_START_DATE[:4]}년~) · "
           f"계산 끝날 {df['날짜'].max():%Y-%m-%d} · A2 미사일 자료 {config.A2_DATA_END}까지")   # [수정] 자료 한계 표시, 임시값 문구 삭제
