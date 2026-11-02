import streamlit as st
import config
import pandas as pd
from datetime import timedelta
import plotly.graph_objects as go             # 그래프 조각(선·막대)
from plotly.subplots import make_subplots     # 그래프를 위아래 칸으로 나누기
from utils.loader import load_tension_recompute, load_tension_daily # 다시 계산 + 공식 결과
from utils.ui import page_style, white_table, icon, hero, period_picker

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")
page_style()   # 공통 디자인

# ===== 페이지 제목 =====
st.markdown(hero("가정 바꿔 보기", "여기부터는 공식 결과가 아니라, 계산 가정을 바꿔 보면 긴장도가 어떻게 달라지는지 보는 화면입니다.", art="sliders"), unsafe_allow_html=True)   # 남색 제목 배너

# ===== 기본값 · 빠른 선택 =====
BUNDLES = config.BUNDLES_BASE                            # ("핵·미사일", "군사 과시", "위협 언어·교리")
DEFAULT = {"half_life": config.HALF_LIFE_DAYS, "relief_c": config.RELIEF_C, "relief_cap": int(config.RELIEF_CAP * 100)}
DEFAULT.update({b: 1.0 for b in BUNDLES})                # 묶음 무게는 모두 1배
PRESETS = {                                              # 버튼 이름: 기본값에서 바꿀 것만
    "균형(기본)": {},
    "행동 중시": {"위협 언어·교리": 0.5},
    "핵·미사일 중시": {"핵·미사일": 2.0},
}

def apply(preset):                                       # 버튼을 누르면 실행: 슬라이더 값을 한 번에 바꿈
    for k, v in {**DEFAULT, **PRESETS[preset]}.items():  # 기본값 위에 프리셋을 덮어쓴 사전
        st.session_state[k] = v

for k, v in DEFAULT.items():                             # 처음 열었을 때만 기본값 넣어 두기
    st.session_state.setdefault(k, v)
    
left, right = st.columns([1, 2], gap="large")   # 왼쪽 1 : 오른쪽 2 → 조절판 1/3, 결과 2/3

# ===== 왼쪽: 조절판 =====
with left.container(border=True, key="box_left"):   # 조절판 상자
    st.subheader("조절판")
    b1, b2, b3 = st.columns(3)                                       # 빠른 선택 버튼 3개 가로로
    for col, name in zip((b1, b2, b3), PRESETS):
        col.button(name, on_click=apply, args=(name,), width="stretch")
    st.button("기본값으로 되돌리기", on_click=apply, args=("균형(기본)",), width="stretch")

    half_life = st.slider("기억 기간 (일)", *config.SLIDER_HALF_LIFE, step=1, key="half_life",
                          help="지나간 사건 점수가 절반으로 줄어드는 날수입니다. 늘리면 큰 사건의 여파가 오래 남고, 줄이면 최근 사건에만 민감해집니다.")
    relief_c = st.slider("회담 효과", *config.SLIDER_RELIEF_C, step=0.01, key="relief_c",
                         help="남북 회담 기록이 있을 때 긴장도를 깎는 힘의 세기입니다. 0이면 회담을 반영하지 않습니다.")
    relief_cap = st.slider("회담 효과 상한 (%)", 0, int(config.SLIDER_RELIEF_CAP[1] * 100), step=5, key="relief_cap",
                           help="회담이 아무리 많아도 이 비율 이상은 깎지 않습니다.") / 100   # 화면은 %, 함수에는 0~0.8

    st.markdown("**무게** (1배 = 보통)")
    weights = {}                                                     # {묶음: 배수}를 담을 빈 사전
    for name in BUNDLES:
        weights[name] = st.slider(name, *config.SLIDER_WEIGHT, step=0.1, key=name)   # key = 묶음 이름

    st.caption("바뀌지 않는 것: 물리 충돌·북러 밀착·핵실험/ICBM 당일 하한, 하강 7일 규칙, 평소 기간 2010~2019, 사건 점수 S")

# ===== 다시 계산 =====
daily, table, info = load_tension_recompute(half_life=half_life, relief_c=relief_c, relief_cap=relief_cap, weights=weights)

# ===== 오른쪽: 결과 =====
official = load_tension_daily()                       # 공식 결과 (비교용)
BUNDLE_COLORS = ["#C0392B", "#E67E22", "#8E44AD"]     # 비중 막대 색 (핵·미사일, 군사 과시, 위협 언어·교리)

def stage_card(title, row):                           # 제목 + 그날 한 줄(row) → 단계 색 카드 HTML
    color = config.STAGE_COLORS[int(row["최종단계"])]
    return (f"<div style='background:{color}; color:white; padding:14px 18px; border-radius:12px;'>"
            f"<div style='font-size:14px; opacity:0.9;'>{title}</div>"
            f"<div style='font-size:30px; font-weight:700;'>{row['화면_단계문구']} · {row['단계이름']}</div>"
            f"<div style='font-size:15px;'>평소대비 {row['평소대비']:.1f}</div></div>")

with right.container(border=True, key="box_right"):   # 결과 상자
    if not info["공식과_같음"]:                                        # 기본값과 다를 때만
        st.warning("공식 결과가 아닙니다 — 가정을 바꿔 다시 계산한 결과입니다.")

    c1, c2 = st.columns(2)                                             # 카드 2장 나란히
    c1.markdown(stage_card("공식 결과", official.iloc[-1]), unsafe_allow_html=True)
    c2.markdown(stage_card("내 설정", daily.iloc[-1]), unsafe_allow_html=True)

    bar = "".join(f"<div style='width:{pct}%; background:{c}; color:white; text-align:center; padding:4px 0; font-size:13px;'>{name} {pct:.0f}%</div>"
                  for (name, pct), c in zip(info["비중%"].items(), BUNDLE_COLORS))   # 묶음마다 폭 = 비중%
    st.markdown(f"<div style='margin-top:14px; font-size:14px;'>지금 비중 (합 100%)</div>"
                f"<div style='display:flex; border-radius:8px; overflow:hidden;'>{bar}</div>", unsafe_allow_html=True)
    
# ===== 공식 vs 내 설정 겹친 그래프 + 단계 띠 두 줄 =====
    first, last = official["날짜"].min().date(), official["날짜"].max().date()   # 공식 결과의 처음·마지막 날
    start, end = period_picker("p5_period", first, last, (last - timedelta(days=90), last), quick=(90, 365, 730))   # 기본: 최근 90일, 함수는 utils/ui.py
    a = official[official["날짜"].between(pd.Timestamp(start), pd.Timestamp(end))]   # 공식
    b = daily[daily["날짜"].between(pd.Timestamp(start), pd.Timestamp(end))]         # 내 설정
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2], vertical_spacing=0.04)   # 위: 선, 아래: 띠
    fig.add_trace(go.Scatter(x=a["날짜"], y=a["평소대비"], name="공식 결과", line=dict(color="#999", width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=b["날짜"], y=b["평소대비"], name="내 설정", line=dict(color="#C0392B", width=2)), row=1, col=1)
    fig.add_hline(y=100, line_dash="dot", line_color="#888", row=1, col=1)   # 평소 = 100
    for label, d in [("공식", a), ("내 설정", b)]:                          # 아래 띠 두 줄: 그날 단계 색 칸
        fig.add_trace(go.Bar(x=d["날짜"], y=[1] * len(d), base=[0 if label == "공식" else 1.1] * len(d),
                             marker_color=[config.STAGE_COLORS[int(s)] for s in d["최종단계"]], marker_line_width=0,
                             showlegend=False, hovertext=d["단계이름"], name=label), row=2, col=1)
    fig.update_yaxes(tickvals=[0.5, 1.6], ticktext=["공식", "내 설정"], range=[0, 2.1], row=2, col=1)
    fig.update_layout(height=420, bargap=0, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, width="stretch")
    
# ===== 비교표 + 안내 문구 =====
    st.markdown("**공식 vs 내 설정 비교**")
    st.dataframe(white_table(table), hide_index=True, width="stretch", height=740)   # 20줄 다 보이게 높이 지정
    st.caption("단계 구간은 같은 규칙(평소 기간 2010~2019의 70·90·95·98%)으로 다시 뽑았습니다. "
               "그래서 5거 비율은 크게 바뀌지 않고, 어느 날이 몇 거인지가 바뀝니다.")