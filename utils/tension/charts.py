"""긴장도 그림 (F4) — Plotly Figure를 돌려준다. Streamlit을 모른다(화면은 st.plotly_chart(fig)로 올림, 단독은 save_html).

추이 그림(사용자 10-29): 위 = T 구간 가로 띠 + 표시선(7일 평균)·원값 + 위기 세로선 + A2 자료 끝 빗금,
아래 = 단계_최종 색 띠(하한·하강 유예로 T 띠보다 높은 날이 보이게).
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import config

# 단계 색·이름은 화면 설정 config.STAGE_COLORS·STAGE_NAMES를 그릴 때 읽는다(사용자 10-29 — 색을 한 곳에서). 아래는 config에 없을 때만 쓰는 값
STAGE_COLORS = {1: "#4CAF50", 2: "#2196F3", 3: "#FBC02D", 4: "#FB8C00", 5: "#E53935"}
STAGE_NAMES = {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"}
LINE_MAIN, LINE_RAW, LINE_COMPARE, INK = "#26215C", "#7F77DD", "#B3541E", "#444441"


def _stage_colorscale(colors):
    """(보조) 단계 1~5를 끊어진 색으로 — z 범위 0.5~5.5."""
    scale = []
    for k in range(1, 6):
        lo, hi = (k - 1) / 5, k / 5
        scale += [[lo, colors[k]], [hi, colors[k]]]
    return scale


def trend_figure(daily, cuts, *, compare=None, compare_name="확장(C5 포함) 7일 평균", crises=config.CRISIS_LIST,
                 a2_end=config.A2_DATA_END, colors=None, names=None, title=None, height=620) -> go.Figure:
    """(그림) 추이 — daily = 일별 표(날짜 인덱스), cuts = T 구간 4개(2·3·4·5거 시작), compare = 비교할 다른 일별 표(선택).

    colors·names를 주지 않으면 config.STAGE_COLORS·STAGE_NAMES(없으면 이 모듈의 기본값).
    """
    colors = colors or getattr(config, "STAGE_COLORS", STAGE_COLORS)
    names = names or getattr(config, "STAGE_NAMES", STAGE_NAMES)
    cuts = [float(c) for c in cuts]
    x = daily.index
    top = max(float(daily["T_원값"].max()), cuts[-1]) * 1.08
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.88, 0.12], vertical_spacing=0.03)
    a2 = pd.Timestamp(a2_end)
    if x[-1] > a2:   # A2 자료 끝 빗금
        fig.add_trace(go.Scatter(x=[a2, x[-1], x[-1], a2, a2], y=[0, 0, top, top, 0], fill="toself", mode="lines",
                                 line=dict(width=0), fillcolor="rgba(0,0,0,0)",
                                 fillpattern=dict(shape="/", fgcolor="#9A9A94", size=8, solidity=0.15),
                                 name=f"A2 자료 없음({a2_end} 이후)", hoverinfo="skip"), row=1, col=1)
    custom = list(zip(daily["화면_단계문구"], daily["그날까지_상위%"].round(1)))
    fig.add_trace(go.Scatter(x=x, y=daily["T_원값"], mode="lines", line=dict(color=LINE_RAW, width=0.6), opacity=0.45,
                             name="T 원값(단계 판정)", hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=daily["T_표시7일"], mode="lines", line=dict(color=LINE_MAIN, width=1.6),
                             name="표시선 = 7일 평균", customdata=custom,
                             hovertemplate="%{x|%Y-%m-%d}<br>표시 %{y:.1f}<br>%{customdata[0]}<br>그날까지 상위 %{customdata[1]}%<extra></extra>"),
                  row=1, col=1)
    if compare is not None:
        fig.add_trace(go.Scatter(x=compare.index, y=compare["T_표시7일"], mode="lines",
                                 line=dict(color=LINE_COMPARE, width=1, dash="dash"), opacity=0.8, name=compare_name,
                                 hovertemplate="%{x|%Y-%m-%d} %{y:.1f}<extra>" + compare_name + "</extra>"), row=1, col=1)
    for name, date, _ in crises:   # 위기 세로선
        t = pd.Timestamp(date)
        if x[0] <= t <= x[-1]:
            fig.add_vline(x=t, line=dict(color=INK, width=0.6), row=1, col=1)
            fig.add_annotation(x=t, y=top * 0.98, text=name, textangle=-90, showarrow=False, xanchor="right",
                               yanchor="top", font=dict(size=10, color=INK), row=1, col=1)
    edges = [0.0, *cuts, top]   # T 구간 가로 띠·문턱선 — 선을 넣은 뒤에 그린다(Plotly는 빈 칸에 띠를 그리지 않음)
    for k in range(1, 6):
        fig.add_hrect(y0=edges[k - 1], y1=edges[k], fillcolor=colors[k], opacity=0.10, line_width=0, layer="below",
                      row=1, col=1)
    for k, c in zip(range(2, 6), cuts):
        fig.add_hline(y=c, line=dict(color=INK, width=0.6, dash="dot"), row=1, col=1,
                      annotation_text=f"{k}거 {c:g}", annotation_position="top left", annotation_font_size=10)
    L = daily["단계_최종"].astype(int)
    fig.add_trace(go.Heatmap(x=x, y=["최종 단계"], z=[L.to_list()], zmin=0.5, zmax=5.5,
                             colorscale=_stage_colorscale(colors), showscale=False,
                             customdata=[[f"{v}거 {names[v]}" for v in L]],
                             hovertemplate="%{x|%Y-%m-%d} %{customdata}<extra>최종 단계</extra>", name="최종 단계"),
                  row=2, col=1)
    fig.update_yaxes(range=[0, top], title_text="평소 = 100", row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=2, col=1)
    fig.update_layout(height=height, title=title, hovermode="x unified", margin=dict(l=10, r=10, t=90 if title else 50, b=10),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), plot_bgcolor="white")
    return fig


def save_html(fig, path) -> Path:
    """(그림) HTML 파일로 저장 — Streamlit 없이 확인용. plotly.js는 CDN(인터넷 필요, 파일 작음)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn")
    return path
