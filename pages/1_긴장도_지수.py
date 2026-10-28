import pandas as pd
import streamlit as st
import config # 맨 위 폴더의 config.py를 불러온다. streamlit은  app.py가 있는 폴더를 기준으로 파일을 찾아서, pages 안에서도 이렇게 불러 올 수 있다.
from utils.loader import load_daily, load_monthly, load_elements, load_events   # [수정] 사건 표도 불러옴
import plotly.express as px

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")

# ===== 페이지 제목 =====
st.title("한반도 군사 긴장 지수")

# ===== 데이터 불러오기 =====
df = load_daily()

# ===== [수정] 기준일 고르기 (발표용 단계별 사례) =====
case = st.selectbox("기준일 (단계별 사례 보기)", list(config.CASES.keys()))   # 펼쳐서 하나 고르는 칸 / [수정] 사례 목록은 config.CASES 한 곳에
day = config.CASES[case]   # 고른 이름 → 날짜 글자
if day == "pick":
    day = st.date_input("날짜", value=df["날짜"].iloc[-1], min_value=df["날짜"].iloc[0], max_value=df["날짜"].iloc[-1])
if day is not None:
    day = pd.Timestamp(day)   # 글자·날짜를 pandas 날짜로 통일
    latest = df[df["날짜"] <= day].iloc[-1]   # 그날(또는 그 전 마지막 날) 줄
else:
    latest = df.iloc[-1] # 몇 번째 줄 위치로 꺼내는 방법, 0은 첫줄 -1은 맨 마지막줄: 파이썬에서 음수 번호는 뒤에서 부터 센다는 뜻
monthly = load_monthly()
st.caption(f"기준일 {latest['날짜']:%Y-%m-%d} · 최근 {config.WINDOW_DAYS}일 사건 점수 합으로 계산")   # [수정] 30 → config.WINDOW_DAYS   # latest를 만든 뒤라서 이곳에 작성

# ===== 상단 카드 3개 =====
stage = int(latest["최종단계"]) # 표에서 꺼낸 숫자는 pandas 형식이라 딕셔너리 키로 쓰기 전에 일반 정수로 맞춰 주는 과줭
days = int(latest["지속일수"])
col1, col2, col3 = st.columns(3) # 3칸으로 나누기
# --- 카드 1: 현재 단계 ---
with col1:
    color = config.STAGE_COLORS[stage]   # [수정] 단계 색
    st.markdown(f"<div style='font-size:14px;'>단계</div><div style='background:{color}; color:white; font-size:30px; font-weight:700; "
                f"padding:4px 14px; border-radius:8px; display:inline-block;'>{stage}단계 {config.STAGE_NAMES[stage]}</div>",
                unsafe_allow_html=True)   # [수정] 단계 이름을 단계 색 상자에
    st.caption(f"원점수 기준 {int(latest['단계_기준선'])}단계 · 평소대비 기준 {int(latest['단계_평소대비'])}단계 → 높은 쪽" + (f" · 4단계 이상 {days}일째" if days > 0 else ""))   # [수정] 두 판정을 같이 보여 줌 / 지속일수는 4단계 이상일 때만 / caption: 화살표 없는 작은 회색 글씨
# --- 카드 2: 평소 대비 ---
with col2:
    ratio = latest["평소대비"]
    st.metric("평소 대비", round(ratio), f"{ratio - 100:+.0f} (평소=100)", delta_color="inverse") # f"{ratio - 100:+.0f}: 평소(100) 보다 얼마나 높은지 계산, +는 양수에도 + 기호를 붙임 / inverse: 화살표 색을 반전 시킴
# --- 카드 3: 원점수와 다음 기준선 ---
with col3:
    raw = latest["원점수"]
    next_cut = None # None 아직 아무것도 없음, 값을 찾기 전에 빈 상태로 시작
    for cut in config.RAM_CUTS: # 기준선을 40 -> 60 -> 90 -> 120 순서 대로 하나씩 꺼내봄
        if raw < cut:
            next_cut = cut
            break
    if next_cut is None: # 반복을 다 돌았는데도 못 찾았다면 120꺼자 다넘은 최고 단계라는 뜻, is : None 인지 확인 할 때는 == 대신 is를 쓰는 것이 파이썬 관습임
        st.metric("원점수", f"{raw:.1f}")
        st.caption(f"최고 기준선({config.RAM_CUTS[-1]}) 초과")   # [수정] delta → caption
    else: # 120 초과 하지 않았다면 남은 거리를 표시
        st.metric("원점수", round(raw, 1))
        st.caption(f"다음 기준선 {next_cut}까지 {next_cut - raw:.1f}")   # [수정] delta → caption
# ===== 5단계 기준표 =====
st.subheader("단계 기준표")
stage_table = pd.DataFrame({"단계": [1, 2, 3, 4, 5], "이름": list(config.STAGE_NAMES.values()), "원점수 (이상)": [0] + config.RAM_CUTS, "평소대비 (이상)": [0] + config.RATIO_CUTS}) # [0] + 기준선: 기준선은 4개인데 단계는 5개라 1단계 0을 앞에 추가 [0, 40, 60, 90, 120]   # [수정] 주석 4개 → 5개
def paint(row):   # [수정] 표 한 줄마다 배경색 정하기
    no = row["단계"]
    alpha = "FF" if no == stage else "30"   # 지금 단계 줄은 진하게(FF), 나머지는 연하게(30)
    text = "white" if no == stage else "black"
    return [f"background-color: {config.STAGE_COLORS[no]}{alpha}; color: {text}"] * len(row)   # 그 줄의 칸 수만큼 같은 색
stage_table["현재"] = ["◀ 현재" if no == stage else "" for no in stage_table["단계"]]   # [수정] 지금 단계 줄 표시
st.dataframe(stage_table.style.apply(paint, axis=1), hide_index=True) # 줄 번호 숨기기 / [수정] .style.apply(함수, axis=1): 줄마다 색칠

# ===== 추이 그래프 =====
st.subheader("긴장도 추이")
c1, c2 = st.columns([3, 1])   # [수정] 슬라이더와 확대 칸을 한 줄에 (3:1)
first_year, last_year = int(df["날짜"].dt.year.min()), int(df["날짜"].dt.year.max())   # [수정] 데이터 첫 해·마지막 해 (2026 직접 쓰지 않기)
start_year = c1.slider("그래프 시작 연도", first_year, last_year, max(first_year, min(2015, latest["날짜"].year - 2)))   # [수정] 기본값이 최소(1945)보다 작아지지 않게 max   # 끌어서 시작 연도 고르기 (제목, 최소, 최대, 기본값)
zoom = c2.toggle("기준선 근처 확대", value=True)   # [수정] 켜기/끄기 스위치 (기본 켜짐)
view = df[df["날짜"].dt.year >= start_year]                    # 그래프에만 쓸 기간 / .dt.year: 날짜에서 연도만
fig = px.line(view, x="날짜", y="평소대비")                     # px.line(표, x=가로축 컬럼, y=세로축 컬럼): 선 그래프를 만듦 / df 대신 view
fig.add_hline(y=100, line_color="gray", annotation_text="평소 100", annotation_position="bottom left")   # [수정] 아래 왼쪽: 150 숫자와 안 겹치게   # .add_hline(): 가로선 추가 / y=: 세로축 위치 / line_color: 선 색 / annotation_text: 선 이름 / annotation_position: 이름 위치(왼쪽 위)
for cut in config.RATIO_CUTS[1:]: # [1:] 1부터 끝까지 -> 두번째 부터 끝까지
    fig.add_hline(y=cut, line_dash="dash", line_color="gray", annotation_text=str(cut)) # dash : 점선 / [수정] 확대하면 줄 사이가 벌어져 숫자가 안 겹침
lows = [min(0, view["평소대비"].min())] + config.RATIO_CUTS   # [수정] 각 단계 아래 끝 [0(또는 최저), 100, 150, 200, 300] / 맨 아래 띠는 음수까지
highs = config.RATIO_CUTS + [max(config.RATIO_CUTS[-1] * 2, view["평소대비"].max())]   # [수정] 각 단계 위 끝 / 5단계 띠는 그래프 맨 위까지 (전에는 350에서 끊김)
for no, low, high in zip([1, 2, 3, 4, 5], lows, highs): # zip(A,B,C): 리스트 여러 개를 같은 순서 끼리 짝을 지음
    fig.add_hrect(y0=low, y1=high, fillcolor=config.STAGE_COLORS[no], opacity=0.1, line_width=0) # 가로 사각행 / y~y : 범위 / opacity=0.1: 투명도, line_width=0: 사각형 테두리, 0 -> 사각형 테두리를 그리지 않는다
if zoom:   # 확대가 켜져 있으면
    fig.update_yaxes(range=[min(0, view["평소대비"].min()), config.RATIO_CUTS[-1] * 2])   # [수정] 세로축 범위: 0(또는 최저)부터 마지막 기준선의 2배까지
fig.add_vline(x=latest["날짜"], line_color=color, line_width=2)   # [수정] 기준일 세로선
st.plotly_chart(fig) # st.plotly_chart(): 완성된 그림을 Streamlit 화면에 올림

# ===== 과거 유사 시기 =====
st.subheader("과거 유사 시기")
monthly = monthly[monthly["연월"] <= f"{latest['날짜']:%Y-%m}"]   # [수정] 기준일이 든 달까지만
now = monthly.iloc[-1] # 이번달 - 마지막 줄
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy() # 최근 config.SIMILAR_EXCLUDE_MONTHS개월을 뺸 지난달, 뒤에서부터 뺀 값 / .copy() 변형을 대비
past["차이"] = (past["평소대비"] - now["평소대비"]).abs() # 이번달과 평소대비 차이 / .abs(): 절댓값, 부호를 삭제 - 음수를 인식해 가장 작은값으로 뽑는 것을 방지
similar = past.nsmallest(config.SIMILAR_N, "차이") # 차이가 가작 작은값, 반대 .nlargest() 가장큰줄 인식
# ===== 유사 시기 카드 ===== 카드 순서 연월 , 평소대비, 단게 순서
if len(similar) == 0:   # [수정] 1945~1946년처럼 비교할 지난달이 없으면
    st.info("비교할 과거 시기가 없습니다.")
cols = st.columns(config.SIMILAR_N) # 고른 개수만큼 가로 칸 나누기
for i in range(len(similar)):   # [수정] SIMILAR_N → len(similar): 3개보다 적을 때 에러 방지
    row = similar.iloc[i] # 1번째 줄 꺼내기 (한달)
    past_stage = int(row["최종단계"]) # 그달의 단계 번호
    with cols[i]: # 1번째 칸안에 그리기
        st.metric(row["연월"], round(row["평소대비"]))   # 큰 숫자 = 그달 평소대비 평균
        st.caption(f"그달 최고 {past_stage}단계 {config.STAGE_NAMES[past_stage]}")   # [수정] max로 구한 단계라 "최고"를 붙임
# ===== [수정] 최근 사건 + 주체별·유형별 기여도 =====
elements = load_elements(day).sort_values("점수", ascending=False) # 기준일 전 N일 요소별 점수 (합계 = 원점수)
events = load_events()
end = latest["날짜"]                                                           # 기준일
recent = events[(events["시작일"] > end - pd.Timedelta(days=config.WINDOW_DAYS)) & (events["시작일"] <= end)]
recent = recent.sort_values("시작일", ascending=False).head(6)                  # 최신 6건

ACTOR_NAMES = {"PRK": "북한", "KOR": "한국", "USA": "미국", "KOR_USA": "한미연합", "CHN": "중국",
               "RUS": "러시아", "JPN": "일본", "MUL": "다자", "UN": "유엔"}         # 주체국 코드 → 한글
ACTOR_COLORS = {"PRK": "#C0392B", "KOR": "#2E6DB4", "USA": "#34495E", "KOR_USA": "#9A7B1C"}   # 칩 색 (나머지는 회색)
GROUPS = {"A": "A 군사행동", "B": "B 군비·능력", "C": "C 선언·외교", "E": "E·F 남북관계", "F": "E·F 남북관계"}
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

plus = elements[elements["점수"] > 0]                                          # 지수를 올린 요소만 (상승분)
by_actor = plus.groupby("주체국")["점수"].sum().sort_values(ascending=False)   # 주체별 점수 합
by_group = plus.groupby(plus["요소코드"].str[0].map(GROUPS))["점수"].sum().sort_values(ascending=False)   # 유형별 점수 합
total = plus["점수"].sum()

left, right = st.columns([11, 9])
with left:
    rows = ""
    for _, r in recent.iterrows():                                            # 사건 한 줄씩 HTML 표 줄로
        w = config.WEIGHTS.get(r["카테고리코드"], 0)                            # 이 사건 1건의 기여(가중치)
        w_color = "#C0392B" if w > 0 else "#2E6DB4"                            # 올리면 빨강, 내리면 파랑 / [수정] color → w_color (위의 단계 색 color와 이름이 겹치지 않게)
        td = "style='border:none; border-bottom:1px solid #eee; padding:10px 6px;"   # 칸 공통 모양 (세로줄 없이 아래 줄만)
        rows += (f"<tr><td {td} font-family:monospace; white-space:nowrap;'>{r['시작일']:%m-%d}</td>"   # nowrap: 줄바꿈 안 함
                 f"<td {td}'>{chip(r['주체국'])}</td><td {td}'>{r['사건명']} ({r['카테고리코드']})</td>"
                 f"<td {td} text-align:right; color:{w_color}; font-family:monospace;'>{w:+d}</td></tr>")
    st.markdown(f"<div style='margin:4px 0 10px;'><b style='font-size:17px;'>최근 사건</b> <span style='color:#888; font-size:13px;'>최근 {config.WINDOW_DAYS}일 · 최신 6건</span></div>"
                f"<table style='width:100%; border-collapse:collapse; border:none; font-size:14px;'><tr>"
                + "".join(f"<th style='border:none; border-bottom:1px solid #ddd; color:#888; font-weight:400; padding:6px; white-space:nowrap; text-align:{a};'>{h}</th>"
                          for h, a in [("날짜", "left"), ("주체", "left"), ("사건", "left"), ("기여", "right")])   # 머리 줄 4칸
                + f"</tr>{rows}</table>",
                unsafe_allow_html=True)
with right:
    if total > 0:   # 올린 점수가 있을 때만 (0으로 나누기 방지)
        st.markdown(bars("주체별 기여도", f"최근 {config.WINDOW_DAYS}일 · 상승분 중 비중",
                         {ACTOR_NAMES.get(k, k): v / total for k, v in by_actor.items()}), unsafe_allow_html=True)   # 딕셔너리 한 줄 만들기
        st.markdown(bars("유형별 기여도", "A 군사행동 · B 군비 · C 외교 · E·F 남북",
                         {k: v / total for k, v in by_group.items()}), unsafe_allow_html=True)
    else:
        st.info("이 기간에는 지수를 올린 사건이 없습니다.")

# ===== 점수 구성표 =====
with st.expander(f"점수 구성표 자세히 (최근 {config.WINDOW_DAYS}일)"):   # [수정] 접었다 펴는 상자 안으로
    st.dataframe(elements, hide_index=True)
    st.caption(f"합계 {elements['점수'].sum()}점 (가중치가 음수인 요소는 점수를 깎음)") # 표 아래 작은 회색 글씨
