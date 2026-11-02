import pandas as pd
import streamlit as st
import plotly.express as px                     # 그래프
import config
from utils.loader import (load_tension_daily, load_tension_monthly, load_tension_contrib, load_tension_stage_table,
                          load_tension_month_events, load_tension_half_life, load_tension_normalization_figure,
                          load_tension_basic_stats, load_tension_events)   # 산출식 v0.1.4 결과
from utils.tension.screen import READING_NOTES, HALF_LIFE_NOTE, NORMALIZATION_NOTE   # 판독문·반감기 설명·정규화 설명 문구
from utils.ui import stage_scale, page_style, white_table, icon, hero   # 5단계 눈금 (홈과 같이 씀), 공통 디자인
from io import BytesIO                          # 파일 대신 쓸 메모리 공간
from docx import Document                       # 워드 문서 만들기
from docx.shared import Pt, RGBColor, Cm        # 글자 크기(Pt), 글자 색(RGB), 길이(Cm)
from docx.enum.text import WD_ALIGN_PARAGRAPH   # 문단 정렬(가운데, 오른쪽)
from docx.oxml.ns import qn                     # 한글 글꼴 지정용 이름표
from docx.oxml import OxmlElement               # 워드 표 칸 배경색·쪽번호 지정용

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")
page_style()   # 공통 디자인

# ===== 화면: 제목 =====
st.markdown(hero("긴장도 브리핑", "숫자로 자동 작성한 브리핑입니다. 아래에서 워드·md로 내려받을 수 있어요.", art="file"), unsafe_allow_html=True)   # 남색 제목 배너

# ===== 데이터 불러오기 =====
df = load_tension_daily()           # 결과_일별 표
monthly = load_tension_monthly()    # 결과_월별 표
events = load_tension_events().rename(columns={"date": "시작일"})     # 글자 → 날짜
RECENT = 30                                                           # 최근 사건을 세는 기간(일) — 화면 표시용

# ===== 기준일 고르기 (1페이지와 같은 사례 목록) =====
c1, c2 = st.columns([2, 1])   # 고르는 칸과 달력을 한 줄에
case = c1.selectbox("기준일 (단계별 사례 보기)", list(config.CASES.keys()))
pick = config.CASES[case]   # 고른 이름 → 날짜 글자
if pick == "pick":
    pick = c2.date_input("날짜", value=df["날짜"].iloc[-1], min_value=df["날짜"].iloc[0], max_value=df["날짜"].iloc[-1])
if pick is not None:
    pick = pd.Timestamp(pick)                   # 글자·날짜를 pandas 날짜로 통일
    latest = df[df["날짜"] <= pick].iloc[-1]    # 그날(또는 그 전 마지막 날) 줄
else:
    latest = df.iloc[-1]                        # 가장 최근 날
bundle_table, ev = load_tension_contrib(pick, top=None)   # (묶음별 표, 사건별 남은 점수 전체) / None이면 최신
month = f"{latest['날짜']:%Y-%m}"                          # 기준일이 든 달
monthly = monthly[monthly["연월"] <= month]                 # 기준일이 든 달까지만 (유사 시기용)


# ===== 보고서에 넣을 숫자 모으기 =====
day = latest["날짜"].strftime("%Y-%m-%d")             # 날짜 → "2026-09-30" 글자
stage = int(latest["최종단계"])
stage_name = config.STAGE_NAMES[stage]                # 4 → 경계
stage_text = f"{latest['화면_단계문구']} · {stage_name}"  # "2거 · 하강 중(판정 1거) 관심" (홈과 같은 문구)
color = config.STAGE_COLORS[stage]                    # 단계 색 ("#FB8C00")
days = int(latest["지속일수"])
ratio = latest["평소대비"]                            # 7일 표시값
raw = latest["원점수"]                                # 원점수 게이지
delta = latest["완화할인_δ"]                          # 완화 할인 (0~0.5)
window = pd.Timedelta(days=RECENT)                    # 30일 길이
recent = events[(events["시작일"] > latest["날짜"] - window) & (events["시작일"] <= latest["날짜"])]   # 최근 30일 지수 사건
before = events[(events["시작일"] > latest["날짜"] - 2 * window) & (events["시작일"] <= latest["날짜"] - window)]   # 그 전 30일 사건 (사건 수 비교용)
up_ev = ev[ev["구분"] == "상승"]                      # T를 올린 사건만
top = up_ev.head(3)                                   # 남은 점수 상위 3건 (ev는 이미 남은 점수 큰 순)
this_month = df[(df["날짜"].dt.strftime("%Y-%m") == month) & (df["날짜"] <= latest["날짜"])]   # 이번 달 1일 ~ 기준일
now = {"평소대비": this_month["평소대비_원값"].mean()}   # 기준일 뒤 날짜가 섞이지 않게 기준일까지만 평균
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy()
past["차이"] = (past["평소대비"] - now["평소대비"]).abs()
similar = past.nsmallest(config.SIMILAR_N, "차이")

# ===== 7일 전·30일 전 숫자 (변화 보기용) =====
def ago(n):   # n일 전 줄을 돌려줌 (데이터 시작보다 앞이면 None)
    rows = df[df["날짜"] <= latest["날짜"] - pd.Timedelta(days=n)]
    return rows.iloc[-1] if len(rows) > 0 else None

def change(n, col):   # 지금 값 - n일 전 값 (n일 전이 없으면 None)
    old = ago(n)
    return None if old is None else latest[col] - old[col]

def fmt(v, unit=""):   # 변화 숫자를 "+12" 모양 글자로 (없으면 "-")
    return "-" if v is None else f"{v:+.0f}{unit}"

d7, d30 = change(7, "평소대비"), change(30, "평소대비")
r7, r30 = change(7, "원점수"), change(30, "원점수")
s30 = change(30, "최종단계")                          # 30일 전보다 단계가 몇 칸 바뀌었는지
ev_diff = len(recent) - len(before)                   # 사건 수 변화

# ===== 기여도 표 (원인 분석용: 주체별·묶음별·요소별, 점수 = 남은 점수) =====
up_ev = up_ev.assign(요소명=up_ev["요소"].map(config.ELEMENT_NAMES))   # A2 → 미사일 발사
by_actor = up_ev.groupby("주체국")["남은점수"].sum().reset_index(name="점수")    # 주체국별 남은 점수 합
by_group = up_ev.groupby("묶음")["남은점수"].sum().reset_index(name="점수")      # 묶음별 남은 점수 합
by_elem = up_ev.groupby("요소명")["남은점수"].sum().reset_index(name="점수")     # 요소별 남은 점수 합
for t in (by_actor, by_group, by_elem):
    t["점수"] = t["점수"].round(1)
    

# ===== 보고서 표 만들기 (화면·워드·md가 같은 표를 같이 씀) =====
factor_table = pd.DataFrame({                                  # 주요 요인 표 = 남은 점수 큰 사건 3건
    "사건": top["사건명"], "묶음": top["묶음"], "주체": top["주체국"],
    "S": top["S"].round(1), "남은 점수": top["남은점수"].round(1)})
recent_ev = ev[ev["날짜"] > latest["날짜"] - window].sort_values("날짜", ascending=False)   # 최근 30일 사건 (남은 점수 붙은 표)
all_events = pd.DataFrame({                                    # 최근 30일 사건 전체
    "날짜": recent_ev["날짜"].dt.strftime("%Y-%m-%d"),
    "묶음": recent_ev["묶음"],
    "구분": recent_ev["구분"],                                 # 상승 · 완화(할인) · 하한 대상 · 표시만
    "주체": recent_ev["주체국"],
    "S": recent_ev["S"].round(1),                              # 사건 점수
    "남은 점수": recent_ev["남은점수"].round(1),              # 기준일에 남은 점수
    "사건": recent_ev["사건명"]}).reset_index(drop=True)       # reset_index: 줄 번호를 0,1,2..로 새로
event_table = all_events.head(5)                               # 최근 주요 사건 (최대 5개)
next_ratio = []                                                # 유사 시기의 다음 달 평소대비
main_event = []                                                # 유사 시기 그달 1위 사건
for ym in similar["연월"]:
    nxt = monthly[monthly["연월"] > ym].head(1)                 # 바로 다음 달 한 줄
    next_ratio.append(int(round(nxt["평소대비"].iloc[0])) if len(nxt) > 0 else None)
    first = load_tension_month_events(ym, top=1)               # 그달 S 1위 사건
    main_event.append(first["사건명"].iloc[0] if len(first) > 0 else "기록된 사건 없음")
similar_table = pd.DataFrame({                                 # 과거 유사 시기 표
    "연월": similar["연월"],
    "월평균 평소대비": similar["평소대비"].round(0).astype(int),   # 그날 값이 아니라 그달 평균
    "최고 단계": similar["최종단계"].astype(int).map(lambda s: f"{s}거 · {config.STAGE_NAMES[s]}"),   # lambda: 한 줄짜리 작은 함수
    "다음 달 월평균": next_ratio,                              # 그 뒤 어떻게 됐는지 (참고)
    "주요 사건": main_event})
change_table = pd.DataFrame({                                  # 변화 표
    "항목": ["평소대비 (7일 평균)", "원점수 게이지", f"최근 {RECENT}일 지수 사건"],
    "지금": [f"{ratio:.1f}", f"{raw:.1f}", f"{len(recent)}건"],
    "7일 전 대비": [fmt(d7), fmt(r7), "-"],
    "30일 전 대비": [fmt(d30), fmt(r30), fmt(ev_diff, "건")]})
half_life = load_tension_half_life()                           # 반감기 민감도 표 (7·14·21·30일)
HL_COLS = ["반감기", "T구간(2·3·4·5거 시작)", "1거%", "2거%", "3거%", "4거%", "5거%", "기준 반감기와 단계 같은 날%", "한 단계 안%"]
hl_table = half_life[HL_COLS]                                  # 먼저 보여 줄 열만


# ===== 핵심 판단 3줄 (판단 / 근거 / 상황) =====
judge = f"{stage_text}. 평소의 {ratio / 100:.1f}배 수준입니다."
tg = {b: latest[f"Tg_{b}"] for b in config.BUNDLES_BASE}       # 묶음별 평소 대비
big = max(tg, key=tg.get)                                      # 가장 큰 묶음 이름
basis = f"가장 크게 오른 묶음은 {big}(평소 대비 {tg[big]:.0f})입니다."
if len(top) > 0:
    basis += " 점수가 가장 많이 남은 사건은 " + ", ".join(f"{r['사건명']}({r['주체국']}) {r['남은점수']:.1f}점" for _, r in top.iterrows()) + "입니다."
if delta > 0:
    basis += f" 남북 회담에 따른 완화 할인 {delta * 100:.0f}%가 적용됐습니다."   # 내린 점수 = 빼기가 아니라 할인
if d7 is None:
    trend_text = "비교할 7일 전 자료가 없습니다."
elif round(d7) == 0:                                           # 변화가 없으면 "같습니다"
    trend_text = "평소대비가 7일 전과 같습니다."
else:
    trend_text = f"7일 전보다 평소대비가 {abs(d7):.1f} {'올랐' if d7 > 0 else '내렸'}습니다."
if d30 is not None and round(d30) != 0:                        # 30일 변화도 같이
    trend_text += f" 30일 전보다는 {abs(d30):.1f} {'높' if d30 > 0 else '낮'}습니다."
if s30:                                                        # 0이나 None이면 건너뜀
    trend_text += f" 30일 전보다 단계가 {abs(s30)}칸 {'높아졌' if s30 > 0 else '낮아졌'}습니다."
if "하강 중" in latest["화면_단계문구"]:                        # 7일 유예 중인지
    trend_text += " 지금은 판정이 낮아졌지만 7일 유예 중이라 단계가 내려가는 중입니다."
if days > 0:
    trend_text += f" 4거 이상이 {days}일째입니다."
JUDGE = [("판단", judge), ("근거", basis), ("상황", trend_text)]

doc_no = f"BR-{latest['날짜']:%Y%m%d}"                                   # 문서번호 = 기준일로 만듦
made = pd.Timestamp.today().strftime("%Y-%m-%d")                        # 작성일 = 오늘
period = f"{df['날짜'].min():%Y-%m-%d} ~ {df['날짜'].max():%Y-%m-%d}"   # 데이터 기간 = 계산 기간
METHOD = [                                                             # 산출 방법 (산출식 v0.1.4)
    "사건 점수 S = 기본점수 B × 세부계수 C",
    f"반감기 {config.HALF_LIFE_DAYS}일 감쇠 누적 → 묶음별 평소 대비({config.BASE_START[:4]}~{config.BASE_END[:4]} = 100)",
    "상승 묶음 평균 × (1 − 완화 할인) = T",
    "단계 = T 구간(기준기간 70·90·95·98분위) · 전용 하한(물리 충돌·북러 밀착·핵실험/ICBM 당일) 중 높은 쪽",
    "내릴 때는 7일 유예 (\"하강 중\" 표시)",
    f"과거 유사 시기 = 월평균 평소대비가 지금 달(기준일까지)과 가장 비슷한 달 {config.SIMILAR_N}개 (최근 {config.SIMILAR_EXCLUDE_MONTHS}개월 제외)",
]
NOTE = "※ 대시보드 숫자로 자동 작성되었습니다. 산출식 v0.1.4 결과 기준입니다."


# ===== 화면: 문서 머리 줄 =====
st.markdown(
    f"<div style='display:flex; gap:24px; font-size:13px; color:#666; border-top:2px solid #333; "
    f"border-bottom:1px solid #ccc; padding:6px 2px; margin-bottom:10px;'>"
    f"<span>문서번호 <b>{doc_no}</b></span><span>기준일 <b>{day}</b></span>"
    f"<span>작성일 {made}</span><span>데이터 기간 {period}</span></div>",
    unsafe_allow_html=True)   # unsafe_allow_html=True: 글 안의 HTML을 그대로 그리게 허락

# ===== 화면: 단계 띠 + 5단계 눈금 =====
st.markdown(
    f"<div style='background:{color}; color:white; padding:16px 20px; border-radius:10px; font-size:22px;'>"
    f"<b>{stage_text}</b> &nbsp;·&nbsp; 평소대비 {ratio:.1f}"
    + (f" &nbsp;·&nbsp; 4거 이상 {days}일째" if days > 0 else "") + "</div>",
    unsafe_allow_html=True)   # 단계 문구 = 홈과 같게
st.markdown(stage_scale(stage), unsafe_allow_html=True)
st.write("")

# ===== 화면: 핵심 판단 박스 (왼쪽 단계 색 선) =====
lines = "".join(f"<div style='margin:4px 0;'><b style='display:inline-block; width:48px; color:{color};'>{k}</b>{v}</div>"
                for k, v in JUDGE)                              # 3줄을 이어 붙임
st.markdown(f"<div style='border-left:6px solid {color}; background:#F7F7F7; padding:10px 16px; "
            f"border-radius:4px; font-size:15px;'>{lines}</div>", unsafe_allow_html=True)
st.write("")

# ===== 화면: 숫자 카드 (7일 전 대비 변화) =====
col1, col2, col3 = st.columns(3)
with col1.container(border=True, height="stretch", key="box_col1"):
    st.metric("평소 대비 (7일 평균, 평소 = 100)", f"{ratio:.1f}", delta=None if d7 is None else f"{d7:+.1f} (7일 전 대비)", delta_color="inverse")
    st.caption(f"30일 전 대비 {fmt(d30)}")                       # delta_color="inverse": 오르면 빨강 (긴장이 오른 거라)
with col2.container(border=True, height="stretch", key="box_col2"):
    st.metric("원점수 게이지", f"{raw:.1f}", delta=None if r7 is None else f"{r7:+.1f} (7일 전 대비)", delta_color="inverse")
    st.caption(f"30일 전 대비 {fmt(r30)} · 단계 판정에는 안 씀")
with col3.container(border=True, height="stretch", key="box_col3"):
    st.metric(f"최근 {RECENT}일 지수 사건", f"{len(recent)}건", delta=f"{ev_diff:+d}건 (그 전 {RECENT}일 대비)", delta_color="inverse")   # 지수에 들어간 사건 수

# ===== 화면: 표 색칠 함수 =====
KIND_COLORS = {"상승": "#C0392B", "완화(할인)": "#2E6DB4", "하한 대상": "#8E44AD", "표시만": "#7F8C8D"}   # 구분별 색
def paint_event(row):   # 사건 표: 구분 칸을 구분 색 글씨로
    return ["" if col != "구분" else f"color: {KIND_COLORS.get(row['구분'], '#333')}; font-weight: 700"
            for col in row.index]

def paint_similar(row):   # 유사 시기 표: 최고 단계 칸을 단계 색으로
    no = int(row["최고 단계"][0])                               # "4거 경계"[0] → "4" → 4
    return ["" if col != "최고 단계" else f"background-color: {config.STAGE_COLORS[no]}; color: white"
            for col in row.index]

def paint_half_life(row):   # 민감도 표: 기준 반감기 행 강조
    return ["background-color: #FFF3CD; font-weight: 700" if row["반감기"] == config.HALF_LIFE_DAYS else ""] * len(row)

def bar(table, name):   # 기여도 가로 막대 / 남은 점수는 모두 양수라 한 색
    t = table.sort_values("점수")                                # 작은 것부터 → 큰 게 맨 위
    fig = px.bar(t, x="점수", y=t.columns[0], orientation="h", title=name,
                 color_discrete_sequence=["#F87171"], height=max(220, 40 * len(t) + 80))
    fig.update_layout(showlegend=False, yaxis_title=None, margin=dict(l=0, r=0, t=40, b=0))
    return fig


# ===== 화면: 탭 5개 =====
tab1, tab2, tab3, tab4, tab5 = st.tabs(["요약", "원인 분석", "사건", "과거 비교", "산출 방법"])   # 산출 방법 탭

with tab1:   # 요약: 90일 추이 + 주요 요인
    trend = df[(df["날짜"] > latest["날짜"] - pd.Timedelta(days=90)) & (df["날짜"] <= latest["날짜"])]   # 기준일 전 90일
    fig = px.line(trend, x="날짜", y="평소대비", height=260)
    cuts = load_tension_stage_table()["T 구간(이상)"].tolist()[1:]                  # T 구간 [115, 256, 315, 378]
    lows = [0] + cuts                                                                # T는 음수가 없음
    highs = cuts + [max(cuts[-1] + 60, trend["평소대비"].max() + 10)]               # 맨 위 띠는 그래프 끝까지
    for no, low, high in zip([1, 2, 3, 4, 5], lows, highs):
        fig.add_hrect(y0=low, y1=high, fillcolor=config.STAGE_COLORS[no], opacity=0.1, line_width=0)
    fig.add_hline(y=100, line_color="gray", annotation_text="평소 100", annotation_position="bottom left")
    fig.update_traces(line_color=color, line_width=3)                              # 선 색 = 지금 단계 색
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title="최근 90일 평소대비 (7일 평균)", xaxis_title=None)
    st.plotly_chart(fig)
    left, right = st.columns(2)
    left.markdown("**주요 요인 (남은 점수 상위 3건)**")
    left.dataframe(white_table(factor_table), hide_index=True, width="stretch")
    right.markdown("**변화**")
    right.dataframe(white_table(change_table), hide_index=True, width="stretch")

with tab2:   # 원인 분석: 무엇이 점수를 올렸나
    if len(up_ev) == 0:
        st.info("지금 점수에 남아 있는 상승 사건이 없습니다.")
    else:
        a, b, c = st.columns(3)
        a.plotly_chart(bar(by_actor, "주체별"))
        b.plotly_chart(bar(by_group, "묶음별"))
        c.plotly_chart(bar(by_elem, "요소별"))
        st.caption(f"점수 = 기준일에 남은 점수 (S × 반감기 {config.HALF_LIFE_DAYS}일 감쇠). "
                   f"남북 회담은 점수를 빼지 않고 T 전체를 할인합니다 — 지금 완화 할인 {delta * 100:.0f}%")   # 완화 할인 δ
    st.dataframe(white_table(bundle_table), hide_index=True, width="stretch")   # 묶음별 평소 대비 → T⁺ → 할인 → T

with tab3:   # 사건: 최근 30일 사건 점 그래프 + 전체 목록
    if len(all_events) == 0:
        st.info(f"최근 {RECENT}일 동안 지수에 들어간 사건이 없습니다.")
    else:
        fig = px.scatter(all_events, x="날짜", y="묶음", size="S", color="구분", hover_name="사건", height=320,
                         color_discrete_map=KIND_COLORS, title=f"최근 {RECENT}일 사건 (점 크기 = S)")   # 크기 = S, 색 = 구분
        fig.update_layout(yaxis_title=None, xaxis_title=None, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig)
        st.dataframe(white_table(all_events).apply(paint_event, axis=1), hide_index=True, width="stretch")
        st.caption("'하한 대상'은 T에 더하지 않고 단계 하한에만 씁니다.")
        


with tab4:   # 과거 비교: 유사 시기 표 + 겹친 선
    if len(similar) == 0:
        st.info("비교할 과거 자료가 없습니다.")
    else:
        st.dataframe(white_table(similar_table).apply(paint_similar, axis=1), hide_index=True, width="stretch")
        lines_df = []                                                 # 겹쳐 그릴 선들을 모을 목록
        cur = df[(df["날짜"] > latest["날짜"] - pd.Timedelta(days=60)) & (df["날짜"] <= latest["날짜"])].copy()
        cur["며칠"] = (cur["날짜"] - latest["날짜"]).dt.days           # 기준일 = 0, 하루 전 = -1
        cur["시기"] = f"지금 ({day})"
        lines_df.append(cur)
        for ym in similar["연월"]:
            end = pd.Period(ym).end_time.normalize()                  # 그 달 마지막 날
            p = df[(df["날짜"] > end - pd.Timedelta(days=60)) & (df["날짜"] <= end + pd.Timedelta(days=30))].copy()   # 앞 60일 + 뒤 30일
            p["며칠"] = (p["날짜"] - end).dt.days
            p["시기"] = ym
            lines_df.append(p)
        fig = px.line(pd.concat(lines_df), x="며칠", y="평소대비", color="시기", height=320,
                      title="지금과 비슷했던 시기 겹쳐 보기 (0 = 기준일 / 그 달 말)",
                      color_discrete_sequence=[color, "#455A64", "#78909C", "#B0BEC5"])   # 지금 = 단계 색, 과거 = 회색 계열
        fig.update_traces(line_dash="dash")                           # 과거 선은 점선
        fig.update_traces(line_dash="solid", line_width=4, selector=dict(name=f"지금 ({day})"))   # 지금 선만 굵은 실선
        fig.add_vline(x=0, line_dash="dot", line_color="gray")
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), xaxis_title="기준일로부터 며칠")
        st.plotly_chart(fig)
        st.caption("0 오른쪽은 과거 시기가 그 뒤 30일 동안 어떻게 흘렀는지입니다. 참고용입니다.")

with tab5:   # 산출 방법 (F5·F6)
    st.markdown("**계산 순서**")
    for m in METHOD:
        st.markdown(f"- {m}")
    st.markdown("**반감기 14일을 쓰는 이유**")
    for text in HALF_LIFE_NOTE:                                     # 4문단 그대로 (문구 바꾸지 않기)
        st.write(text)
    st.markdown("**반감기를 바꾸면 (민감도)**")
    st.dataframe(white_table(hl_table).apply(paint_half_life, axis=1).format(precision=1), hide_index=True, width="stretch")   # 14일 행 강조 / 소수 한 자리
    with st.expander("위기 10건 단계 · 현재 (반감기별)"):
        st.dataframe(white_table(half_life.drop(columns=HL_COLS[1:])), hide_index=True, width="stretch")   # 반감기 + 나머지 열
    st.markdown("**묶음 정규화 효과**")
    st.plotly_chart(load_tension_normalization_figure())
    st.caption(NORMALIZATION_NOTE)
    st.dataframe(white_table(load_tension_basic_stats()), hide_index=True)
    st.markdown("**읽는 법**")
    for text in READING_NOTES:                                      # 판독문
        st.markdown(f"- {text}")

# ===== 화면: 산출 방법 각주 =====
st.caption("산출 방법 · " + " → ".join(METHOD[:5]))   # 화살표로 이어 보기
st.caption(NOTE)


# ===== 워드(.docx) 만들기 =====
def shade(cell, hex_color):                                     # 워드 표 칸 배경색 칠하기
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))               # "#FB8C00" → "FB8C00"
    cell._tc.get_or_add_tcPr().append(shd)

def add_table(doc, table, widths=None):                        # 표(DataFrame)를 워드 표로 옮기는 함수 / widths: 칸 너비(cm) 목록
    t = doc.add_table(rows=1, cols=len(table.columns))
    t.style = "Table Grid"
    for i, name in enumerate(table.columns):
        cell = t.rows[0].cells[i]
        cell.text = str(name)
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)        # 머리 줄 글자 흰색
        shade(cell, "#5D6D7E")                                 # 머리 줄 배경 진회색
    for _, row in table.iterrows():
        cells = t.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = "-" if pd.isna(value) else str(value)   # 빈 값은 "-"
            col = table.columns[i]
            if col == "최고 단계":                             # 단계 칸: 단계 색 배경 + 흰 글씨
                shade(cells[i], config.STAGE_COLORS[int(str(value)[0])])
                cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if widths:                                                 # 칸 너비 정하기 (칸마다 하나씩 지정해야 적용됨)
        t.autofit = False                                      # 글자 길이에 맞춰 자동으로 바뀌지 않게
        for col, w in zip(t.columns, widths):
            col.width = Cm(w)
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = Cm(w)
    doc.add_paragraph()
    return t

def add_bars(doc, table, name):                                # 기여도 글자 막대 (■ 개수 = 점수 크기)
    doc.add_paragraph().add_run(name).bold = True
    t = table.sort_values("점수", ascending=False)
    biggest = t["점수"].abs().max()
    box = doc.add_table(rows=0, cols=3)
    box.autofit = False
    for col, w in zip(box.columns, [3, 1.5, 11]):
        col.width = Cm(w)
    for _, row in t.iterrows():
        cells = box.add_row().cells
        cells[0].text = str(row.iloc[0])                       # 이름 (주체국 / 묶음)
        cells[1].text = f"{row['점수']:.1f}"                   # 남은 점수는 소수 한 자리
        n = max(1, round(abs(row["점수"]) / biggest * 15))     # 가장 큰 값 = ■ 15개
        run = cells[2].paragraphs[0].add_run("■" * n)
        run.font.color.rgb = RGBColor.from_string("C0392B")    # 남은 점수는 모두 올린 점수라 빨강
        run.font.size = Pt(8)
        for cell, w in zip(cells, [3, 1.5, 11]):               # 칸 너비: 이름 / 점수 / 막대
            cell.width = Cm(w)
    doc.add_paragraph()

def page_number(paragraph):                                    # 쪽번호 칸 넣기 (워드가 열 때 숫자를 채움)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)
    

doc = Document()
style = doc.styles["Normal"]
style.font.name = "맑은 고딕"
style.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")    # 한글 글꼴은 따로 지정해야 적용됨
style.font.size = Pt(10.5)

section = doc.sections[0]                                      # 머리글·바닥글
head = section.header.paragraphs[0]
head.text = f"한반도 군사 긴장도 브리핑 · {doc_no}"
head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
head.runs[0].font.size = Pt(8)
head.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)
foot = section.footer.paragraphs[0]
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
page_number(foot)

title = doc.add_heading("한반도 군사 긴장도 브리핑", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
info = pd.DataFrame({"문서번호": [doc_no], "기준일": [day], "작성일": [made], "데이터 기간": [period]})   # 문서 머리 정보
add_table(doc, info)

doc.add_heading("1. 핵심 판단", level=1)
p = doc.add_paragraph()
run = p.add_run(stage_text)   # 홈과 같은 단계 문구
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor.from_string(color[1:])
for k, v in JUDGE:
    p = doc.add_paragraph()
    p.add_run(f"{k}  ").bold = True
    p.add_run(v)

doc.add_heading("2. 변화", level=1)
add_table(doc, change_table)

doc.add_heading("3. 원인 분석", level=1)
add_table(doc, factor_table)
if len(up_ev) > 0:
    add_bars(doc, by_actor, "주체별 기여 (남은 점수)")
    add_bars(doc, by_group, "묶음별 기여 (남은 점수)")

doc.add_heading(f"4. 최근 {RECENT}일 사건", level=1)
if len(all_events) > 0:
    add_table(doc, all_events, widths=[2.3, 2.4, 1.8, 1.3, 1.1, 1.5, 6.1])   # 칸 7개, 사건 칸을 넓게
else:
    doc.add_paragraph("사건이 없습니다.")

doc.add_heading("5. 과거 유사 시기", level=1)
add_table(doc, similar_table)
doc.add_paragraph("월평균 평소대비가 지금 달과 가장 비슷한 달입니다. 다음 달 월평균은 그 시기 뒤 흐름을 참고로 보여 줍니다.").runs[0].font.size = Pt(9)

doc.add_heading("부록. 산출 방법", level=1)
for m in METHOD:
    doc.add_paragraph(m, style="List Bullet")
doc.add_paragraph().add_run("반감기 14일을 쓰는 이유").bold = True   # 반감기 설명 4문단
for text in HALF_LIFE_NOTE:
    doc.add_paragraph(text)
doc.add_paragraph().add_run("반감기 민감도").bold = True             # 민감도 4행
add_table(doc, hl_table)
p = doc.add_paragraph(NOTE)
p.runs[0].font.size = Pt(8)
p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)

buffer = BytesIO()
doc.save(buffer)


# ===== md 글 만들기 =====
def md_table(table):                                           # 표 → md 표 글자
    lines = ["| " + " | ".join(table.columns) + " |",
             "|" + "---|" * len(table.columns)]
    for _, row in table.iterrows():
        lines.append("| " + " | ".join("-" if pd.isna(v) else str(v) for v in row) + " |")
    return "\n".join(lines)

report = (f"# 한반도 군사 긴장도 브리핑\n문서번호 {doc_no} · 기준일 {day} · 작성일 {made} · 데이터 기간 {period}\n\n"
          f"## 1. 핵심 판단\n**{stage_text}**\n\n" + "\n".join(f"- **{k}** {v}" for k, v in JUDGE) + "\n\n"
          f"## 2. 변화\n{md_table(change_table)}\n\n"
          f"## 3. 원인 분석\n{md_table(factor_table)}\n\n"
          f"## 4. 최근 {RECENT}일 사건\n{md_table(all_events)}\n\n"
          f"## 5. 과거 유사 시기\n{md_table(similar_table)}\n\n"
          f"## 부록. 산출 방법\n" + "\n".join(f"- {m}" for m in METHOD) + "\n\n"
          f"### 반감기 14일을 쓰는 이유\n" + "\n\n".join(HALF_LIFE_NOTE) + "\n\n"
          f"### 반감기 민감도\n{md_table(hl_table)}\n\n{NOTE}\n")

# ===== 내려받기 버튼 (나란히) =====
b1, b2, _ = st.columns([1, 1, 3])
b1.download_button("워드로 내려받기", data=buffer.getvalue(), file_name=f"긴장도_브리핑_{day}.docx",
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
b2.download_button("md로 내려받기", data=report, file_name=f"긴장도_브리핑_{day}.md", mime="text/markdown")