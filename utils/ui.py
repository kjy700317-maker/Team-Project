import config
import pandas as pd 
import streamlit as st

# ===== 5단계 눈금 (홈·보고서가 같이 씀) =====
def stage_scale(stage):   # 지금 단계 번호를 받아 눈금 5칸 HTML을 돌려줌
    scale = ""                                          # 칸 5개를 이어 붙일 빈 글
    for no, name in config.STAGE_NAMES.items():         # .items(): (번호, 이름)을 같이 꺼냄
        if no == stage:                                 # 지금 단계: 진한 색 + 흰 글씨 + 굵게
            bg, text, weight = config.STAGE_COLORS[no], "white", 700
        else:                                           # 나머지: 연한 색(뒤에 "40" = 투명도 25%) + 회색 글씨
            bg, text, weight = config.STAGE_COLORS[no] + "40", "#555", 400
        scale += (f"<div style='flex:1; background:{bg}; color:{text}; font-weight:{weight}; "
                  f"text-align:center; padding:6px 0; font-size:13px; border-radius:6px;'>{no}거 {name}</div>")
    return f"<div style='display:flex; gap:4px; margin-top:8px;'>{scale}</div>"   # flex: 칸을 가로로 나란히

# ===== 5단계 눈금 세로판 (Grid: 5줄 격자, 5단계가 맨 위) =====
def stage_scale_grid(stage):   # 지금 단계 번호를 받아 세로 눈금 5칸 HTML을 돌려줌
    scale = ""
    for no in sorted(config.STAGE_NAMES, reverse=True):   # 5,4,3,2,1 순서 (높은 단계가 위)
        name = config.STAGE_NAMES[no]
        if no == stage:
            bg, text, weight = config.STAGE_COLORS[no], "white", 700
        else:
            bg, text, weight = config.STAGE_COLORS[no] + "40", "#555", 400
        scale += (f"<div style='display:grid; place-items:center; background:{bg}; color:{text}; "
                  f"font-weight:{weight}; font-size:18px; border-radius:4px;'>{no}거 {name}</div>")   # place-items:center → 글자를 칸 가운데로
    return f"<div style='display:grid; grid-template-rows:repeat(5, 1fr); gap:3px;'>{scale}</div>"   # 5줄을 같은 높이(1fr)로

# ===== 사건의 지수 반영 표시 (2페이지 "지수 반영" 열) =====
def index_mark(b, v):                                   # 묶음(b)·S(v) → 화면 글자
    if pd.isna(v):                                      # 지수 사건표에 없음
        return "지수 밖"
    if b in (config.BUNDLE_PHYS, config.BUNDLE_E5):     # 하한 전용 묶음 (이름은 config에서)
        return f"{b} · <하한만>"
    return f"{b} · S {v:.1f}"                           # 예: "핵·미사일 · S 12.5"

# ===== 공통 디자인 (페이지마다 st.set_page_config 바로 아래에서 page_style() 한 번 부르기) =====
BOX_CSS = """
[class*="st-key-box_"] {
    background: white;
    border: 1px solid #DDE2E8 !important;
    border-radius: 12px;
}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {
    background: white;
}
[data-testid="stTabs"] {
    background: white;
    border: 1px solid #DDE2E8;
    border-radius: 12px;
    padding: 4px 16px 16px;
}
[data-testid="stPlotlyChart"] .main-svg:first-child {
    background: white !important;
}
[data-testid="stDateInputField"] {
    background: white !important;
    border: 1px solid #B8C2CF !important;
    border-radius: 8px;
}
"""   # 상자(key가 box_로 시작)·접기 칸·탭·그래프 → 흰 바탕

def page_style():
    tag = "style"   # HTML 태그 이름 (CSS를 넣는 칸)
    st.markdown(f"<{tag}>{BOX_CSS}</{tag}>", unsafe_allow_html=True)   # 화면에 CSS 넣기

# ===== 흰 표 (st.dataframe에 넣기 전에 감싸기: st.dataframe(white_table(표))) =====
def white_table(df):
    nums = df.select_dtypes("float").columns                    # 소수 열만
    return (df.style.set_properties(**{"background-color": "white"})   # 칸 바탕 흰색
              .format("{:g}", subset=nums))                      # 소수 끝 0 없애기 (6.250000 → 6.25)

# ===== 아이콘 (선 그림 SVG, 홈 카드·페이지 배너용) — 모양 출처: Lucide (lucide.dev, ISC 라이선스) =====
def icon(name, color="#1F3A5F", size=26):
    paths = {
        "gauge": "<path d='M12 14l4-4'/><path d='M3.3 19a10 10 0 1 1 17.4 0'/>",
        "search": "<circle cx='11' cy='11' r='7'/><path d='M21 21l-4.3-4.3'/>",
        "calendar": "<rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/>",
        "file": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><path d='M14 2v6h6M8 13h8M8 17h8'/>",
        "sliders": "<path d='M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6'/>",
    }
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='2' "
            f"stroke-linecap='round' stroke-linejoin='round' style='vertical-align:-5px; margin-right:6px;'>{paths[name]}</svg>")
 
# ===== 제목 배너 (남색 띠 + 홈은 봉수 불꽃 그림, 페이지는 선 아이콘) =====
def hero(title, subtitle, art=None):   # art: 아이콘 이름 (없으면 봉수 불꽃)
    beacon = ("<svg width='64' height='64' viewBox='0 0 64 64' fill='none'>"
              "<path d='M18 56h28l-5-18H23z' fill='#ffffff22' stroke='#ffffffaa' stroke-width='2' stroke-linejoin='round'/>"   # 봉수대
              "<path d='M32 36c-7-3-9-10-4-17 1 4 4 6 6 4 2-3 1-7-1-11 8 4 12 13 7 20-2 3-5 4-8 4z' fill='#F2B544'/>"          # 불꽃
              "<path d='M32 36c-3-2-3-6 0-9 1 2 2 3 3 2 1 3 0 6-3 7z' fill='#FFE29A'/></svg>")
    if art:   # 페이지 배너: 흰 선 아이콘
        beacon = f"<div style='width:64px; text-align:center;'>{icon(art, color='white', size=44)}</div>"
    return (f"<div style='display:flex; align-items:center; gap:18px; background:linear-gradient(120deg,#3D5A80,#5B7BA3); "
            f"color:white; padding:22px 28px; border-radius:14px; margin-bottom:14px;'>{beacon}"
            f"<div><div style='font-size:30px; font-weight:700; letter-spacing:-0.5px;'>{title}</div>"
            f"<div style='font-size:15px; opacity:0.85; margin-top:4px;'>{subtitle}</div></div></div>")
    
# ===== 기간 달력 + [전체 기간] [초기화] 버튼 (2페이지·5페이지가 같이 씀) =====
def period_picker(key, first, last, default, sidebar=False, quick=()):   # quick: (90, 365) 처럼 주면 "최근 N일" 버튼도 만듦
    import streamlit as st
    from datetime import timedelta

    def set_period(value):                                       # 버튼을 누르면 실행: 달력 값을 바꿈
        st.session_state[key] = value

    st.session_state.setdefault(key, default)                    # 처음 열었을 때만 기본값 넣어 두기
    where = st.sidebar if sidebar else st                        # 그릴 곳: 사이드바 또는 본문
    if sidebar:                                                  # 사이드바: 달력 아래에 버튼 2개
        cal = st.sidebar
        b1, b2 = st.sidebar.columns(2)
    else:                                                        # 본문: 달력 | 버튼 | 버튼 한 줄
        cal, b1, b2 = st.columns([3, 1, 1], vertical_alignment="bottom")
    period = cal.date_input("기간", key=key, min_value=first, max_value=last)
    b1.button("전체 기간", key=f"{key}_all", on_click=set_period, args=((first, last),), width="stretch")
    b2.button("초기화", key=f"{key}_reset", on_click=set_period, args=(default,), width="stretch")
    if quick:                                                    # "최근 N일" 버튼 줄 (선택)
        for col, days in zip(where.columns(len(quick)), quick):
            col.button(f"최근 {days}일", key=f"{key}_{days}", on_click=set_period,
                       args=((max(first, last - timedelta(days=days)), last),), width="stretch")   # 처음 날보다 앞서지 않게
    return period[0], period[-1]                                 # 시작일만 고른 순간에도 에러 안 나게 [0], [-1]