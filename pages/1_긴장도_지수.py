import pandas as pd
import streamlit as st
import config # 맨 위 폴더의 config.py를 불러온다. streamlit은  app.py가 있는 폴더를 기준으로 파일을 찾아서, pages 안에서도 이렇게 불러 올 수 있다.
from utils.loader import (load_tension_daily, load_tension_monthly, load_tension_contrib, load_tension_stage_table,
                          load_tension_crisis_marks, load_tension_figure, load_tension_month_events, load_tension_events)   # 산출식 v0.1.4 결과
from utils.tension.screen import DATA_COVERAGE, FOOTNOTES, READING_NOTES   # 자료 충실도·각주·판독문 문구
import plotly.express as px
from utils.ui import page_style, white_table, hero

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")
page_style()   # 공통 디자인(테두리 상자 흰 배경 등)

# ===== 페이지 제목 =====
st.markdown(hero("한반도 군사 긴장 지수", "지금 몇 단계인지, 평소보다 얼마나 높은지 봅니다.", art="gauge"), unsafe_allow_html=True)   # 남색 제목 배너

# ===== 데이터 불러오기 =====
df = load_tension_daily()

# ===== 기준일 고르기 (발표용 단계별 사례) =====
case = st.selectbox("기준일 (단계별 사례 보기)", list(config.CASES.keys()))   # 펼쳐서 하나 고르는 칸 / 사례 목록은 config.CASES 한 곳에
day = config.CASES[case]   # 고른 이름 → 날짜 글자
if day == "pick":
    day = st.date_input("날짜", value=df["날짜"].iloc[-1], min_value=df["날짜"].iloc[0], max_value=df["날짜"].iloc[-1])
if day is not None:
    day = pd.Timestamp(day)   # 글자·날짜를 pandas 날짜로 통일
    latest = df[df["날짜"] <= day].iloc[-1]   # 그날(또는 그 전 마지막 날) 줄
else:
    latest = df.iloc[-1] # 몇 번째 줄 위치로 꺼내는 방법, 0은 첫줄 -1은 맨 마지막줄: 파이썬에서 음수 번호는 뒤에서 부터 센다는 뜻
monthly = load_tension_monthly()
note = " (잠정)" if latest["잠정"] else ""   # 최근 6일은 값이 바뀔 수 있음
st.caption(f"기준일 {latest['날짜']:%Y-%m-%d}{note} · 사건 점수(S)를 반감기 {config.HALF_LIFE_DAYS}일로 줄여 쌓은 뒤 평소(2010~2019)와 비교")   # latest를 만든 뒤라서 이곳에 작성

# ===== 상단 카드 3개 =====
stage = int(latest["최종단계"]) # 표에서 꺼낸 숫자는 pandas 형식이라 딕셔너리 키로 쓰기 전에 일반 정수로 맞춰 주는 과정
days = int(latest["지속일수"])
col1, col2, col3 = st.columns(3) # 3칸으로 나누기
# --- 카드 1: 현재 단계 ---
with col1.container(border=True, height="stretch", key="box_col1"):   # 칸마다 테두리 상자 (stretch: 세 상자 높이를 맞춤)
    color = config.STAGE_COLORS[stage]   # 단계 색
    st.markdown(f"<div style='font-size:14px;'>단계</div><div style='background:{color}; color:white; font-size:30px; font-weight:700; "
                f"padding:4px 14px; border-radius:8px; display:inline-block;'>{latest['화면_단계문구']} · {latest['단계이름']}</div>",
                unsafe_allow_html=True)   # 화면_단계문구 예: "2거 · 하강 중(판정 1거)"
    st.caption(f"T 구간 {int(latest['단계_T'])}거 · 하한(물리 {int(latest['하한_물리'])} / E5 {int(latest['하한_E5'])} / 사건 {int(latest['하한_사건'])}) "
               f"→ 판정 {int(latest['단계_판정'])}거 → 최종 {stage}거" + (f" · 4거 이상 {days}일째" if days > 0 else ""))   # 판정 근거 한 줄 / 지속일수는 4거 이상일 때만 / caption: 화살표 없는 작은 회색 글씨
# --- 카드 2: 평소 대비 ---
with col2.container(border=True, height="stretch", key="box_col2"):
    ratio = latest["평소대비"]   # 7일 표시값 (평소 = 100)
    chg, rate = latest["변화14_표시"], latest["변화율14_표시"]   # 14일 전과 비교
    delta = None if pd.isna(chg) else f"{chg:+.1f}" + ("" if pd.isna(rate) else f" ({rate:+.0f}%)") + " · 14일 전 대비"   # NaN이면 숨김
    st.metric(f"평소 대비 (7일 평균){note}", f"{ratio:.1f}", delta, delta_color="inverse") # 큰 숫자 = 7일 표시값 / inverse: 오르면 빨강
    top = "—" if pd.isna(latest["상위%_표시"]) else f"그날까지 상위 {latest['상위%_표시']:.1f}%"   # 2010년은 NaN → "—"
    st.caption(f"원값 {latest['평소대비_원값']:.1f} · {top}")   # 원값은 작게
# --- 카드 3: 원점수 게이지 ---
with col3.container(border=True, height="stretch", key="box_col3"):
    raw = latest["원점수"]   # 원점수 게이지 (단계 판정에는 쓰지 않음)
    marks = load_tension_crisis_marks()   # 위기 10건과 그때 게이지 눈금
    below = marks[marks["게이지 눈금"] <= raw].nlargest(1, "게이지 눈금")   # 지금보다 낮은 눈금 중 가장 가까운 위기
    above = marks[marks["게이지 눈금"] > raw].nsmallest(1, "게이지 눈금")    # 지금보다 높은 눈금 중 가장 가까운 위기
    st.metric("원점수 게이지", f"{raw:.1f}")
    near = [f"{r['위기']} {r['게이지 눈금']:.1f}" for _, r in pd.concat([below, above]).iterrows()]   # "6차 핵 33.8"
    st.caption("위기 눈금: " + (" · ".join(near) if near else "—") + " (참고용, 단계 판정에는 안 씀)")
# ===== 5단계 기준표 =====
with st.container(border=True, key="box_table"):   # 단계 기준표를 테두리 칸 하나로
    st.subheader("단계 기준표")
    stage_table = load_tension_stage_table()   # 단계·이름·T 구간(이상)·봉수 원뜻·하한으로 켜지는 경우
    def paint(row):   # 표 한 줄마다 배경색 정하기
        no = row["단계"]
        alpha = "FF" if no == stage else "30"   # 지금 단계 줄은 진하게(FF), 나머지는 연하게(30)
        text = "white" if no == stage else "black"
        return [f"background-color: {config.STAGE_COLORS[no]}{alpha}; color: {text}"] * len(row)   # 그 줄의 칸 수만큼 같은 색
    stage_table["현재"] = ["◀ 현재" if no == stage else "" for no in stage_table["단계"]]   # 지금 단계 줄 표시
    st.dataframe(stage_table.style.apply(paint, axis=1), hide_index=True) # 줄 번호 숨기기 / .style.apply(함수, axis=1): 줄마다 색칠

# ===== 추이 그래프 =====
with st.container(border=True, key="box_trend"):   # 추이 그래프를 테두리 칸 하나로
    st.subheader("긴장도 추이")
    first_year, last_year = int(df["날짜"].dt.year.min()), int(df["날짜"].dt.year.max())   # 데이터 첫 해·마지막 해 (2026 직접 쓰지 않기)
    start_year = st.slider("그래프 시작 연도", first_year, last_year, max(first_year, latest["날짜"].year - 2))   # 기본값 = 기준일 2년 전 (2010보다 작아지지 않게 max)
    fig = load_tension_figure()   # T 구간 띠 + 7일 표시선·원값 + 확장 점선 + 위기 세로선 + 아래 최종 단계 띠 (긴장도 담당이 만든 그림)
    fig.update_xaxes(range=[f"{start_year}-01-01", df["날짜"].max()])   # 슬라이더는 x축 범위만 바꿈
    fig.add_vline(x=latest["날짜"], line_color=color, line_width=2)   # 기준일 세로선
    fig.update_layout(paper_bgcolor="white")   # 그래프 바깥 여백도 흰색 (흰 상자와 맞춤)
    st.plotly_chart(fig) # st.plotly_chart(): 완성된 그림을 Streamlit 화면에 올림


# ===== 과거 유사 시기 =====
st.subheader("과거 유사 시기")
month = f"{latest['날짜']:%Y-%m}"   # 기준일이 든 달 "2017-09"
monthly = monthly[monthly["연월"] <= month]   # 기준일이 든 달까지만
this_month = df[(df["날짜"].dt.strftime("%Y-%m") == month) & (df["날짜"] <= latest["날짜"])]   # 이번 달 1일 ~ 기준일
now = {"평소대비": this_month["평소대비_원값"].mean()}   # 기준일 뒤 날짜가 섞이지 않게 기준일까지만 평균 (월별 평소대비 = T 원값 평균과 같은 방식)
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy() # 최근 config.SIMILAR_EXCLUDE_MONTHS개월을 뺀 지난달, 뒤에서부터 뺀 값 / .copy() 변형을 대비
past["차이"] = (past["평소대비"] - now["평소대비"]).abs() # 이번달과 평소대비 차이 / .abs(): 절댓값, 부호를 삭제 - 음수를 인식해 가장 작은값으로 뽑는 것을 방지
similar = past.nsmallest(config.SIMILAR_N, "차이") # 차이가 가장 작은값, 반대 .nlargest() 가장큰줄 인식
# ===== 유사 시기 카드 ===== 카드 순서 연월 , 평소대비, 단계 순서
if len(similar) == 0:   # 비교할 지난달이 없으면
    st.info("비교할 과거 시기가 없습니다.")
cols = st.columns(config.SIMILAR_N) # 고른 개수만큼 가로 칸 나누기
for i in range(len(similar)):   # SIMILAR_N → len(similar): 3개보다 적을 때 에러 방지
    row = similar.iloc[i] # 1번째 줄 꺼내기 (한달)
    past_stage = int(row["최종단계"]) # 그달의 단계 번호
    with cols[i].container(border=True, height="stretch", key=f"box_similar{i}"): # i번째 칸 안에 테두리 상자를 만들고 그리기
        st.metric(row["연월"], round(row["평소대비"]))   # 큰 숫자 = 그달 평소대비 평균
        st.caption(f"그달 최고 {past_stage}거 · {config.STAGE_NAMES[past_stage]}")   # max로 구한 단계라 "최고"를 붙임
        top3 = load_tension_month_events(row["연월"], top=3)   # 그달 주요 사건 (S 큰 순 3건)
        st.caption("<br>".join(f"· {r['사건명']} (S {r['S']:.1f})" for _, r in top3.iterrows()) if len(top3) else "기록된 사건 없음", unsafe_allow_html=True)
# ===== 지금 점수에 남은 사건 + 주체별·묶음별 기여도 =====
bundle_table, ev = load_tension_contrib(day, top=None)   # (묶음별 표, 사건별 남은 점수 전체) / day=None이면 최신
recent = ev.head(6)                                                             # 지금 점수에 가장 많이 남은 6건

ACTOR_NAMES = {"PRK": "북한", "KOR": "한국", "USA": "미국", "KOR_USA": "한미연합", "CHN": "중국",
               "RUS": "러시아", "JPN": "일본", "MUL": "다자", "UN": "유엔"}         # 주체국 코드 → 한글
ACTOR_COLORS = {"PRK": "#C0392B", "KOR": "#2E6DB4", "USA": "#34495E", "KOR_USA": "#9A7B1C"}   # 칩 색 (나머지는 회색)
BAR, TRACK = "#C8641E", "#F3EDE4"                                              # 막대 색, 막대 바탕색

def chip(code):   # 주체국 코드를 둥근 테두리 칩(HTML)으로
    c = ACTOR_COLORS.get(code, "#7F8C8D")                                       # .get(키, 기본값): 없으면 회색
    return f"<span style='border:1px solid {c}; color:{c}; border-radius:12px; padding:1px 9px; font-size:13px;'>{code}</span>"

def bars(title, sub, shares):   # 기여도 막대 묶음(HTML). shares: {이름: 비율(0~1)}
    html = f"<div style='margin:4px 0 10px;'><b style='font-size:17px;'>{title}</b> <span style='color:#888; font-size:13px;'>{sub}</span></div>"
    for name, share in shares.items():
        html += (f"<div style='display:flex; align-items:center; gap:12px; margin:10px 0;'>"
                 f"<div style='width:110px;'>{name}</div>"
                 f"<div style='flex:1; background:{TRACK}; border-radius:6px; height:12px;'>"
                 f"<div style='width:{share * 100:.0f}%; background:{BAR}; border-radius:6px; height:12px;'></div></div>"
                 f"<div style='width:40px; text-align:right; color:#666; font-family:monospace;'>{share * 100:.0f}%</div></div>")
    return html

plus = ev[ev["구분"] == "상승"]                                                 # T를 올린 사건만 (완화·하한 대상·표시만 제외)
by_actor = plus.groupby("주체국")["남은점수"].sum().sort_values(ascending=False)   # 주체별 남은 점수 합
by_group = plus.groupby("묶음")["남은점수"].sum().sort_values(ascending=False)     # 유형 = 묶음
total = plus["남은점수"].sum()

left, right = st.columns([11, 9])
with left.container(border=True, height="stretch", key="box_left"):   # 남은 사건 표 상자
    rows = ""
    for _, r in recent.iterrows():                                            # 사건 한 줄씩 HTML 표 줄로
        w_color = {"상승": "#C0392B", "완화(할인)": "#2E6DB4"}.get(r["구분"], "#888")   # 올리면 빨강, 완화는 파랑, 나머지 회색
        w_text = "하한만" if r["구분"] == "하한 대상" else f"{r['남은점수']:.1f}"     # 하한 대상은 T에 더하지 않음
        td = "style='border:none; border-bottom:1px solid #eee; padding:10px 6px;"   # 칸 공통 모양 (세로줄 없이 아래 줄만)
        rows += (f"<tr><td {td} font-family:monospace; white-space:nowrap;'>{r['날짜']:%m-%d}</td>"   # nowrap: 줄바꿈 안 함
                 f"<td {td}'>{chip(r['주체국'])}</td><td {td}'>{r['사건명']} ({r['묶음']})</td>"
                 f"<td {td} text-align:right; color:{w_color}; font-family:monospace;'>{w_text}</td></tr>")
    st.markdown(f"<div style='margin:4px 0 10px;'><b style='font-size:17px;'>지금 점수에 남은 사건</b> <span style='color:#888; font-size:13px;'>남은 점수 큰 순 6건 · 반감기 {config.HALF_LIFE_DAYS}일</span></div>"
                f"<table style='width:100%; border-collapse:collapse; border:none; font-size:14px;'><tr>"
                + "".join(f"<th style='border:none; border-bottom:1px solid #ddd; color:#888; font-weight:400; padding:6px; white-space:nowrap; text-align:{a};'>{h}</th>"
                          for h, a in [("날짜", "left"), ("주체", "left"), ("사건", "left"), ("남은 점수", "right")])   # 머리 줄 4칸
                + f"</tr>{rows}</table>",
                unsafe_allow_html=True)
with right.container(border=True, height="stretch", key="box_right"):   # 기여도 상자
    if total > 0:   # 올린 점수가 있을 때만 (0으로 나누기 방지)
        st.markdown(bars("주체별 기여도", "상승 사건 남은 점수 중 비중",
                         {ACTOR_NAMES.get(k, k): v / total for k, v in by_actor.items()}), unsafe_allow_html=True)   # 딕셔너리 한 줄 만들기
        st.markdown(bars("묶음별 기여도", " · ".join(config.BUNDLES_BASE),
                         {k: v / total for k, v in by_group.items()}), unsafe_allow_html=True)
    else:
        st.info("이 기간에는 지수를 올린 사건이 없습니다.")

# ===== 점수 구성표 =====
with st.expander("점수 구성표 자세히"):   # 묶음별 + 사건별 10건
    st.dataframe(white_table(bundle_table), hide_index=True)   # 흰 표 / 묶음별 평소 대비 → T⁺ → 완화 할인 → T
    st.caption(f"완화 할인 {latest['완화할인_δ'] * 100:.0f}% · 빼기가 아니라 할인 (남북 회담이 있으면 T를 최대 50%까지 깎음)")
    st.dataframe(white_table(ev.head(10).assign(날짜=ev["날짜"].dt.strftime("%Y-%m-%d"))), hide_index=True)    # 남은 점수 큰 사건 10건 / 날짜를 "2026-09-30" 글자로 (시간 00:00:00 숨김)
    st.caption("남은 점수 = S × 2^(−지난 날 수 ÷ 반감기). '하한 대상'은 T에 더하지 않고 단계 하한에만 씀")

# ===== 자료 충실도·각주·판독문 =====
with st.expander("자료 충실도 · 각주 · 읽는 법"):
    st.dataframe(white_table(DATA_COVERAGE), hide_index=True)   # 요소별 자료 범위
    for text in FOOTNOTES:      # 각주
        st.caption(text)
    for text in READING_NOTES:  # 판독문
        st.markdown(f"- {text}")