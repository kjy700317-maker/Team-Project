import streamlit as st
import config
import pandas as pd
from utils.loader import load_tension_daily, load_tension_events   # 산출식 v0.1.4 결과
from utils.ui import stage_scale_grid, page_style, icon, hero   # 세로 눈금 (Grid)
 
# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide", page_icon="🛡️")
page_style()
 
# ===== 데이터 불러오기 (홈에도 지금 단계를 보여 주기 위해) =====
df = load_tension_daily()                           # 일별 결과 (2010-01-01 ~ 계산일)
events = load_tension_events()
latest = df.iloc[-1]                                # 가장 최근 날
stage = int(latest["최종단계"])
color = config.STAGE_COLORS[stage]                  # 지금 단계 색
 
# ===== 제목 =====
st.markdown(hero("한반도 군사 긴장도 대시보드", "사건 데이터를 점수로 바꿔, 지금 한반도의 군사 긴장이 평소보다 얼마나 높은지 보여 줍니다."), unsafe_allow_html=True)   # 남색 제목 배너
 
# ===== 지금 단계 띠 + 세로 눈금 =====
top = "—" if pd.isna(latest["상위%_표시"]) else f"그날까지 상위 {latest['상위%_표시']:.1f}%"   # 2010년은 NaN → "—"
note = " (잠정)" if latest["잠정"] else ""                                                    # 최근 6일은 잠정
band = (f"<div style='background:{color}; color:white; padding:18px 22px; border-radius:12px;'>"   # 폭은 바깥 격자가 정함
        f"<div style='font-size:14px; opacity:0.9;'>{latest['날짜']:%Y-%m-%d} 기준 현재 단계{note}</div>"
        f"<div style='font-size:40px; font-weight:700;'>{latest['화면_단계문구']} · {latest['단계이름']}</div>"   # 예: "2거 · 하강 중(판정 1거) · 관심"
        f"<div style='font-size:15px;'>평소대비 {latest['평소대비']:.1f} · {top}"                   # 평소대비 = 7일 표시값
        + (f" · 4거 이상 {int(latest['지속일수'])}일째" if latest["지속일수"] > 0 else "") + "</div></div>")   # 0이면 숨김
st.markdown(f"<div style='display:grid; grid-template-columns:1fr 160px; gap:8px;'>{band}{stage_scale_grid(stage)}</div>",   # 2칸 격자: 띠 = 남는 폭 전부(1fr), 눈금 = 160px
            unsafe_allow_html=True)
st.write("")
 
# ===== 페이지 안내 카드 (2 × 2) =====
pages = [   # (파일, 제목, 아이콘, 설명) 4개를 목록으로 모아 두기
    ("pages/1_긴장도_지수.py", "긴장도 지수", icon("gauge"), "지금 몇 단계인지, 평소보다 얼마나 높은지"),
    ("pages/2_사건_기록.py", "사건 기록", icon("search"), "기간·종류·검색어로 어떤 사건이 있었는지"),
    ("pages/3_월별_연별.py", "월별·연별 추이", icon("calendar"), "언제 긴장이 높았는지, 가장 높았던 시기 TOP 5"),
    ("pages/4_보고서.py", "보고서", icon("file"), "숫자로 자동 작성한 브리핑, 워드로 내려받기"),
]
 
card_style = ("display:block; text-decoration:none; color:inherit; background:white; border:1px solid #DDE2E8; border-radius:12px;"
             "padding:22px 24px; margin-bottom:16px; min-height:120px;") # 카드 전체 모양
cols = st.columns(2)   # 2칸
for i, (path, title, icon, desc) in enumerate(pages):   # 4개를 하나씩, i = 0,1,2,3
    url = "/" + path.split("/")[1][2:-3] # pages, .py 제거
    with cols[i % 2]: # i % 2: 2로 나눈 나머지 → 0,1,0,1 → 왼쪽·오른쪽 번갈아
        st.markdown(f"<a href='{url}' target='_self' class='home-card' style='{card_style}'>"
                    f"<span style='display:block; font-size:22px; font-weight:700; margin-bottom:8px;'>{icon} {title}</span>"
                    f"<span style='display:block; font-size:16px; color:#666;'>{desc}</span></a>",
                    unsafe_allow_html=True)
# ===== 데이터 안내 =====
st.caption(f"지수에 들어간 사건 {len(events):,}건 ({config.CALC_START_DATE[:4]}년~) · "
           f"계산 끝날 {df['날짜'].max():%Y-%m-%d} · A2 미사일 자료 {config.A2_DATA_END}까지")   # 자료 한계 표시
 
# ===== 데이터 출처 (평소엔 접혀 있고, 누르면 펼쳐짐) =====
SOURCES = [   # (분야, 출처) — 화면·지수 계산에 실제로 쓴 자료만, 미사용 자료와 전체 이용 조건은 레포의 SOURCES.md
    ("A 군사행동", "핵실험: Our World in Data · Arms Control Association / "
                   "미사일: CNS North Korea Missile Test Database (NTI 제공) / "
                   "도발·훈련·충돌: CSIS Beyond Parallel / 미 전략자산: NCAFP 보고서, 언론·군 발표 / "
                   "열병식: 통일연구원 CO20-26(e) (공공누리 제2유형)"),
    ("B 군비·능력", "신형 무기: CSIS Beyond Parallel / 확장억제: 국방부·외교부(정책브리핑, 공공누리 제1유형), 미 국방부, 백악관 아카이브 / "
                   "국방비(사건 기록만): 국방부·방위사업청 보도자료, e-나라지표, 국회예산정책처"),
    ("C 선언·외교", "위협 성명: 언론 보도, UMD 디지털 아카이브, UN Digital Library / "
                   "교리·법제: 정책브리핑, 국가법령정보센터 / 동맹·정상회담: 외교부(공공누리 제1유형), 언론 보도 / "
                   "대화·합의(사건 기록만): 통일부 남북회담본부, 국가기록원 / "
                   "제재(확장 계산만): UN 안보리, 미 재무부 OFAC, 외교부"),
    ("E·F 관계·정치", "북러: 통일부 북한정보포털 / 남북회담: 통일부 남북회담본부 (dialogue.unikorea.go.kr)"),
    ("비교 지표", "GPR 지수 (Caldara & Iacoviello 2022)"),
    ("화면 디자인", "선 아이콘: Lucide (lucide.dev, ISC 라이선스) · 홈 배너 봉수대 그림: 직접 제작"),
]
with st.expander("📚 데이터 출처 보기"):    # 기본은 접힌 상태
    for field, src in SOURCES:
        st.markdown(f"**{field}** · {src}")
    st.caption("원자료에서 사건을 골라 팀이 직접 점수화·계산한 결과이며, 각 기관의 공식 자료·수정본·평가가 아닙니다. 비상업 교육용. "
               "북한 발언·결정은 조선중앙통신을 인용한 보도에 근거합니다. "
               "미사용 자료와 이용 조건 전체는 GitHub의 SOURCES.md에 있습니다.")
 