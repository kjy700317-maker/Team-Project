import config
import pandas as pd 

# ===== [수정] 5단계 눈금 (홈·보고서가 같이 씀, 두 곳에 있던 코드를 여기로 모음) =====
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

# ===== [수정] 5단계 눈금 세로판 (Grid: 5줄 격자, 5단계가 맨 위) =====
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

# ===== [추가] 사건의 지수 반영 표시 (2페이지 "지수 반영" 열) =====
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
    border: 1px solid #C9DCEB !important;
    border-radius: 12px;
}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {
    background: white;
}
[data-testid="stTabs"] {
    background: white;
    border: 1px solid #C9DCEB;
    border-radius: 12px;
    padding: 4px 16px 16px;
}
[data-testid="stPlotlyChart"] .main-svg:first-child {
    background: white !important;
}
"""   # 상자(key가 box_로 시작)·접기 칸·탭·그래프 → 흰 바탕

def page_style():
    import streamlit as st
    tag = "style"   # HTML 태그 이름 (CSS를 넣는 칸)
    st.markdown(f"<{tag}>{BOX_CSS}</{tag}>", unsafe_allow_html=True)   # 화면에 CSS 넣기

# ===== 흰 표 (st.dataframe에 넣기 전에 감싸기: st.dataframe(white_table(표))) =====
def white_table(df):
    nums = df.select_dtypes("float").columns                    # 소수 열만
    return (df.style.set_properties(**{"background-color": "white"})   # 칸 바탕 흰색
              .format("{:g}", subset=nums))                      # 소수 끝 0 없애기 (6.250000 → 6.25)
