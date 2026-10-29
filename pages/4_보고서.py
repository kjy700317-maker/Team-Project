import pandas as pd
import streamlit as st
import plotly.express as px                     # 그래프
import config
from utils.loader import load_daily, load_monthly, load_elements, load_events
from utils.ui import stage_scale                # 5단계 눈금 (홈과 같이 씀)
from io import BytesIO                          # 파일 대신 쓸 메모리 공간
from docx import Document                       # 워드 문서 만들기
from docx.shared import Pt, RGBColor, Cm        # 글자 크기(Pt), 글자 색(RGB), 길이(Cm)
from docx.enum.text import WD_ALIGN_PARAGRAPH   # 문단 정렬(가운데, 오른쪽)
from docx.oxml.ns import qn                     # 한글 글꼴 지정용 이름표
from docx.oxml import OxmlElement               # 워드 표 칸 배경색·쪽번호 지정용

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")

# ===== 화면: 제목 =====
st.title("긴장도 브리핑")

# ===== 데이터 불러오기 =====
df = load_daily()           # 결과_일별 표
monthly = load_monthly()    # 결과_월별 표
events = load_events()      # 사건_일단위 표

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
elements = load_elements(pick)                  # 기준일 전 N일 요소별 점수 (None이면 최신)
monthly = monthly[monthly["연월"] <= f"{latest['날짜']:%Y-%m}"]   # 기준일이 든 달까지만 (유사 시기용)

# ===== 보고서에 넣을 숫자 모으기 =====
day = latest["날짜"].strftime("%Y-%m-%d")             # 날짜 → "2026-09-30" 글자
stage = int(latest["최종단계"])
stage_name = config.STAGE_NAMES[stage]                # 4 → 경계
color = config.STAGE_COLORS[stage]                    # 단계 색 ("#FB8C00")
days = int(latest["지속일수"])
ratio = latest["평소대비"]
raw = latest["원점수"]
window = pd.Timedelta(days=config.WINDOW_DAYS)        # 30일 길이
recent = events[(events["시작일"] > latest["날짜"] - window) & (events["시작일"] <= latest["날짜"])]   # 최근 N일 사건
recent = recent.sort_values("시작일", ascending=False)                       # 최신순
before = events[(events["시작일"] > latest["날짜"] - 2 * window) & (events["시작일"] <= latest["날짜"] - window)]   # [수정] 그 전 N일 사건 (사건 수 비교용)
top = elements.sort_values("점수", ascending=False).head(3)                  # 점수 상위 3개 요소
now = monthly.iloc[-1]
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy()
past["차이"] = (past["평소대비"] - now["평소대비"]).abs()
similar = past.nsmallest(config.SIMILAR_N, "차이")

# ===== [수정] 7일 전·30일 전 숫자 (변화 보기용) =====
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

# ===== [수정] 기여도 표 (원인 분석용: 주체별·유형별·요소별) =====
elements["분류"] = elements["요소코드"].str[0].map(config.GROUPS)   # "A7"[0] → "A" → "군사행동"
by_actor = elements.groupby("주체국")["점수"].sum().reset_index()    # 주체국별 점수 합
by_group = elements.groupby("분류")["점수"].sum().reset_index()      # 큰 분류별 점수 합
by_elem = elements.groupby("요소명")["점수"].sum().reset_index()     # 요소별 점수 합

# ===== 보고서 표 만들기 (화면·워드·md가 같은 표를 같이 씀) =====
factor_table = pd.DataFrame({                                  # 주요 요인 표
    "요소": top["요소명"], "주체": top["주체국"], "건수": top["건수"], "점수": top["점수"]})
all_events = pd.DataFrame({                                    # [수정] 최근 N일 사건 전체
    "날짜": recent["시작일"].dt.strftime("%Y-%m-%d"),
    "종류": recent["카테고리코드"].map(config.ELEMENT_NAMES),  # .map(딕셔너리): 코드 → 이름으로 한 번에 바꾸기
    "주체": recent["주체국"],
    "기여": recent["카테고리코드"].map(config.WEIGHTS),       # 사건 1건의 기여(가중치)
    "사건": recent["사건명"]}).reset_index(drop=True)          # reset_index: 줄 번호를 0,1,2..로 새로
event_table = all_events.head(5)                               # 최근 주요 사건 (최대 5개)
next_ratio = []                                                # [수정] 유사 시기의 다음 달 평소대비
for ym in similar["연월"]:
    nxt = monthly[monthly["연월"] > ym].head(1)                 # 바로 다음 달 한 줄
    next_ratio.append(int(round(nxt["평소대비"].iloc[0])) if len(nxt) > 0 else None)
similar_table = pd.DataFrame({                                 # 과거 유사 시기 표
    "연월": similar["연월"],
    "월평균 평소대비": similar["평소대비"].round(0).astype(int),   # [수정] 그날 값이 아니라 그달 평균이라 이름을 분명하게
    "최고 단계": similar["최종단계"].astype(int).map(lambda s: f"{s}단계 {config.STAGE_NAMES[s]}"),   # lambda: 한 줄짜리 작은 함수
    "다음 달 월평균": next_ratio})                            # [수정] 그 뒤 어떻게 됐는지 (참고)
change_table = pd.DataFrame({                                  # [수정] 변화 표
    "항목": ["평소대비", "원점수", f"최근 {config.WINDOW_DAYS}일 사건"],
    "지금": [f"{ratio:.0f}", f"{raw:.1f}", f"{len(recent)}건"],
    "7일 전 대비": [fmt(d7), fmt(r7), "-"],
    "30일 전 대비": [fmt(d30), fmt(r30), fmt(ev_diff, "건")]})

# ===== [수정] 핵심 판단 3줄 (판단 / 근거 / 상황) =====
judge = f"{stage}단계({stage_name}). 평소의 {ratio / 100:.1f}배 수준입니다."
up = elements[elements["점수"] > 0].sort_values("점수", ascending=False).head(3)   # [수정] 올린 요소 (양수만)
down = elements[elements["점수"] < 0].sort_values("점수")                            # [수정] 내린 요소 (대화·회담)
def join(t):   # 요소 목록 → "포격·총격·충돌(PRK) +8점, ..." 글자
    return ", ".join(f"{r['요소명']}({r['주체국']}) {r['점수']:+.0f}점" for _, r in t.iterrows())
if len(up) > 0:
    basis = f"최근 {config.WINDOW_DAYS}일 점수를 가장 많이 올린 요소는 {join(up)}입니다."
else:
    basis = f"최근 {config.WINDOW_DAYS}일 동안 점수를 올린 사건이 없습니다."
if len(down) > 0:
    basis += f" 점수를 내린 요소는 {join(down)}입니다."
if d7 is None:
    trend_text = "비교할 7일 전 자료가 없습니다."
elif round(d7) == 0:                                           # [수정] 변화가 없으면 "같습니다"
    trend_text = "평소대비가 7일 전과 같습니다."
else:
    trend_text = f"7일 전보다 평소대비가 {abs(d7):.0f} {'올랐' if d7 > 0 else '내렸'}습니다."
if s30:                                                        # 0이나 None이면 건너뜀
    trend_text += f" 30일 전보다 단계가 {abs(s30)}칸 {'높아졌' if s30 > 0 else '낮아졌'}습니다."
if days > 0:
    trend_text += f" 4단계 이상이 {days}일째입니다."
JUDGE = [("판단", judge), ("근거", basis), ("상황", trend_text)]

doc_no = f"BR-{latest['날짜']:%Y%m%d}"                                   # [수정] 문서번호 = 기준일로 만듦
made = pd.Timestamp.today().strftime("%Y-%m-%d")                        # 작성일 = 오늘
period = f"{events['시작일'].min():%Y-%m-%d} ~ {events['시작일'].max():%Y-%m-%d}"   # 데이터 기간
METHOD = [                                                             # [수정] 산출 방법 (화면 각주·워드 부록)
    f"원점수 = 최근 {config.WINDOW_DAYS}일 사건의 (건수 × 가중치) 합",
    f"평소대비 = 원점수 ÷ 평소 × 100 (평소 = {config.BASE_START[:4]}~{config.BASE_END[:4]}년 원점수 평균)",
    f"단계 = 원점수 기준선 {config.RAM_CUTS}와 평소대비 기준선 {config.RATIO_CUTS} 중 높은 쪽",
    f"과거 유사 시기 = 월평균 평소대비가 지금 달과 가장 비슷한 달 {config.SIMILAR_N}개 (최근 {config.SIMILAR_EXCLUDE_MONTHS}개월 제외)",
]
NOTE = "※ 대시보드 숫자로 자동 작성되었습니다. 가중치·기준선은 현재 진행도 기준 임시값이며 추후 결정됩니다."

# ===== [수정] 화면: 문서 머리 줄 =====
st.markdown(
    f"<div style='display:flex; gap:24px; font-size:13px; color:#666; border-top:2px solid #333; "
    f"border-bottom:1px solid #ccc; padding:6px 2px; margin-bottom:10px;'>"
    f"<span>문서번호 <b>{doc_no}</b></span><span>기준일 <b>{day}</b></span>"
    f"<span>작성일 {made}</span><span>데이터 기간 {period}</span></div>",
    unsafe_allow_html=True)   # unsafe_allow_html=True: 글 안의 HTML을 그대로 그리게 허락

# ===== 화면: 단계 띠 + 5단계 눈금 =====
st.markdown(
    f"<div style='background:{color}; color:white; padding:16px 20px; border-radius:10px; font-size:22px;'>"
    f"<b>{stage}단계 {stage_name}</b> &nbsp;·&nbsp; 평소대비 {ratio:.0f}"
    + (f" &nbsp;·&nbsp; 4단계 이상 {days}일째" if days > 0 else "") + "</div>",
    unsafe_allow_html=True)
st.markdown(stage_scale(stage), unsafe_allow_html=True)
st.write("")

# ===== [수정] 화면: 핵심 판단 박스 (왼쪽 단계 색 선) =====
lines = "".join(f"<div style='margin:4px 0;'><b style='display:inline-block; width:48px; color:{color};'>{k}</b>{v}</div>"
                for k, v in JUDGE)                              # 3줄을 이어 붙임
st.markdown(f"<div style='border-left:6px solid {color}; background:#F7F7F7; padding:10px 16px; "
            f"border-radius:4px; font-size:15px;'>{lines}</div>", unsafe_allow_html=True)
st.write("")

# ===== [수정] 화면: 숫자 카드 (7일 전 대비 변화) =====
col1, col2, col3 = st.columns(3)
col1.metric("평소 대비 (평소 = 100)", f"{ratio:.0f}", delta=None if d7 is None else f"{d7:+.0f} (7일 전 대비)", delta_color="inverse")
col1.caption(f"30일 전 대비 {fmt(d30)}")                       # delta_color="inverse": 오르면 빨강 (긴장이 오른 거라)
col2.metric(f"원점수 ({config.WINDOW_DAYS}일 합)", f"{raw:.1f}", delta=None if r7 is None else f"{r7:+.1f} (7일 전 대비)", delta_color="inverse")
col2.caption(f"30일 전 대비 {fmt(r30)}")
col3.metric(f"최근 {config.WINDOW_DAYS}일 사건", f"{len(recent)}건", delta=f"{ev_diff:+d}건 (그 전 {config.WINDOW_DAYS}일 대비)", delta_color="inverse")

# ===== 화면: 표 색칠 함수 =====
def paint_event(row):   # 사건 표: 기여 칸만 올리면 빨강, 내리면 파랑 글씨
    return ["" if col != "기여" else ("color: #C0392B; font-weight: 700" if row["기여"] > 0 else "color: #2E6DB4; font-weight: 700")
            for col in row.index]

def paint_similar(row):   # 유사 시기 표: 최고 단계 칸을 단계 색으로
    no = int(row["최고 단계"][0])                               # "4단계 경계"[0] → "4" → 4
    return ["" if col != "최고 단계" else f"background-color: {config.STAGE_COLORS[no]}; color: white"
            for col in row.index]

def bar(table, name):   # [수정] 기여도 가로 막대 (올린 건 빨강, 내린 건 파랑)
    t = table.sort_values("점수")                                # 작은 것부터 → 큰 게 맨 위
    t["방향"] = t["점수"].map(lambda v: "올림" if v > 0 else "내림")
    fig = px.bar(t, x="점수", y=t.columns[0], orientation="h", color="방향", title=name,
                 color_discrete_map={"올림": "#F87171", "내림": "#60A5FA"}, height=max(220, 40 * len(t) + 80))
    fig.update_layout(showlegend=False, yaxis_title=None, margin=dict(l=0, r=0, t=40, b=0))
    return fig

# ===== [수정] 화면: 탭 4개 =====
tab1, tab2, tab3, tab4 = st.tabs(["요약", "원인 분석", "사건", "과거 비교"])

with tab1:   # 요약: 90일 추이 + 주요 요인
    trend = df[(df["날짜"] > latest["날짜"] - pd.Timedelta(days=90)) & (df["날짜"] <= latest["날짜"])]   # 기준일 전 90일
    fig = px.line(trend, x="날짜", y="평소대비", height=260)
    lows = [min(0, trend["평소대비"].min() - 10)] + config.RATIO_CUTS               # 맨 아래 띠는 음수까지
    highs = config.RATIO_CUTS + [max(config.RATIO_CUTS[-1] + 50, trend["평소대비"].max() + 10)]   # 맨 위 띠는 그래프 끝까지
    for no, low, high in zip([1, 2, 3, 4, 5], lows, highs):
        fig.add_hrect(y0=low, y1=high, fillcolor=config.STAGE_COLORS[no], opacity=0.1, line_width=0)
    fig.add_hline(y=100, line_color="gray", annotation_text="평소 100", annotation_position="bottom left")
    fig.update_traces(line_color=color, line_width=3)                              # 선 색 = 지금 단계 색
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title="최근 90일 평소대비", xaxis_title=None)
    st.plotly_chart(fig)
    left, right = st.columns(2)
    left.markdown("**주요 요인 (점수 상위 3개)**")
    left.dataframe(factor_table, hide_index=True, use_container_width=True)
    right.markdown("**변화**")
    right.dataframe(change_table, hide_index=True, use_container_width=True)

with tab2:   # 원인 분석: 무엇이 점수를 올렸나
    if len(elements) == 0:
        st.info(f"최근 {config.WINDOW_DAYS}일 동안 점수에 들어간 사건이 없습니다.")
    else:
        a, b, c = st.columns(3)
        a.plotly_chart(bar(by_actor, "주체별"))
        b.plotly_chart(bar(by_group, "유형별"))
        c.plotly_chart(bar(by_elem, "요소별"))
        st.caption("빨강 = 긴장을 올린 점수, 파랑 = 내린 점수 (대화·회담)")

with tab3:   # 사건: 최근 N일 사건 점 그래프 + 전체 목록
    if len(all_events) == 0:
        st.info(f"최근 {config.WINDOW_DAYS}일 동안 사건이 없습니다.")
    else:
        dots = all_events.copy()
        dots["크기"] = dots["기여"].abs()                              # 점 크기 = 기여 크기
        dots["방향"] = dots["기여"].map(lambda v: "올림" if v > 0 else "내림")
        fig = px.scatter(dots, x="날짜", y="종류", size="크기", color="방향", hover_name="사건", height=320,
                         color_discrete_map={"올림": "#C0392B", "내림": "#2E6DB4"}, title=f"최근 {config.WINDOW_DAYS}일 사건")
        fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig)
        st.dataframe(all_events.style.apply(paint_event, axis=1), hide_index=True, use_container_width=True,
                     column_config={"기여": st.column_config.NumberColumn("기여", format="%+d")})   # format="%+d": 5 → +5

with tab4:   # 과거 비교: 유사 시기 표 + 겹친 선
    if len(similar) == 0:
        st.info("비교할 과거 자료가 없습니다.")
    else:
        st.dataframe(similar_table.style.apply(paint_similar, axis=1), hide_index=True, use_container_width=True)
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
        st.caption("0 오른쪽은 과거 시기가 그 뒤 30일 동안 어떻게 흘렀는지입니다. 가중치가 임시값이라 참고용입니다.")

# ===== [수정] 화면: 산출 방법 각주 =====
st.caption("산출 방법 · " + " · ".join(METHOD))
st.caption(NOTE)

# ===== 워드(.docx) 만들기 =====
def shade(cell, hex_color):                                     # 워드 표 칸 배경색 칠하기
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))               # "#FB8C00" → "FB8C00"
    cell._tc.get_or_add_tcPr().append(shd)

def add_table(doc, table, widths=None):                        # 표(DataFrame)를 워드 표로 옮기는 함수 / [수정] widths: 칸 너비(cm) 목록
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
            cells[i].text = "-" if pd.isna(value) else str(value)   # [수정] 빈 값은 "-"
            col = table.columns[i]
            if col == "기여":                                  # 기여 칸: 올리면 빨강, 내리면 파랑 글씨
                cells[i].text = f"{int(value):+d}"
                run = cells[i].paragraphs[0].runs[0]
                run.bold = True
                run.font.color.rgb = RGBColor.from_string("C0392B" if value > 0 else "2E6DB4")
            if col == "최고 단계":                             # 단계 칸: 단계 색 배경 + 흰 글씨
                shade(cells[i], config.STAGE_COLORS[int(str(value)[0])])
                cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if widths:                                                 # [수정] 칸 너비 정하기 (칸마다 하나씩 지정해야 적용됨)
        t.autofit = False                                      # 글자 길이에 맞춰 자동으로 바뀌지 않게
        for col, w in zip(t.columns, widths):
            col.width = Cm(w)
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = Cm(w)
    doc.add_paragraph()
    return t

def add_bars(doc, table, name):                                # [수정] 기여도 글자 막대 (■ 개수 = 점수 크기)
    doc.add_paragraph().add_run(name).bold = True
    t = table.sort_values("점수", ascending=False)
    biggest = t["점수"].abs().max()
    box = doc.add_table(rows=0, cols=3)
    box.autofit = False
    for col, w in zip(box.columns, [3, 1.5, 11]):
        col.width = Cm(w)
    for _, row in t.iterrows():
        cells = box.add_row().cells
        cells[0].text = str(row.iloc[0])                       # 이름 (주체국 / 분류)
        cells[1].text = f"{row['점수']:+.0f}"
        n = max(1, round(abs(row["점수"]) / biggest * 15))     # 가장 큰 값 = ■ 15개
        run = cells[2].paragraphs[0].add_run("■" * n)
        run.font.color.rgb = RGBColor.from_string("C0392B" if row["점수"] > 0 else "2E6DB4")
        run.font.size = Pt(8)
        for cell, w in zip(cells, [3, 1.5, 11]):               # 칸 너비: 이름 / 점수 / 막대
            cell.width = Cm(w)
    doc.add_paragraph()

def page_number(paragraph):                                    # [수정] 쪽번호 칸 넣기 (워드가 열 때 숫자를 채움)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)

doc = Document()
style = doc.styles["Normal"]
style.font.name = "맑은 고딕"
style.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")    # 한글 글꼴은 따로 지정해야 적용됨
style.font.size = Pt(10.5)

section = doc.sections[0]                                      # [수정] 머리글·바닥글
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
info = pd.DataFrame({"문서번호": [doc_no], "기준일": [day], "작성일": [made], "데이터 기간": [period]})   # [수정] 문서 머리 정보
add_table(doc, info)

doc.add_heading("1. 핵심 판단", level=1)                       # [수정]
p = doc.add_paragraph()
run = p.add_run(f"{stage}단계 {stage_name}")
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor.from_string(color[1:])
for k, v in JUDGE:
    p = doc.add_paragraph()
    p.add_run(f"{k}  ").bold = True
    p.add_run(v)

doc.add_heading("2. 변화", level=1)                            # [수정]
add_table(doc, change_table)

doc.add_heading("3. 원인 분석", level=1)                       # [수정]
add_table(doc, factor_table)
if len(elements) > 0:
    add_bars(doc, by_actor, "주체별 기여")
    add_bars(doc, by_group, "유형별 기여")

doc.add_heading(f"4. 최근 {config.WINDOW_DAYS}일 사건", level=1)   # [수정] 5개 → 전체
if len(all_events) > 0:
    add_table(doc, all_events, widths=[2.6, 3.2, 1.4, 1.2, 8.1])   # 사건 칸을 넓게
else:
    doc.add_paragraph("사건이 없습니다.")

doc.add_heading("5. 과거 유사 시기", level=1)
add_table(doc, similar_table)
doc.add_paragraph("월평균 평소대비가 지금 달과 가장 비슷한 달입니다. 다음 달 월평균은 그 시기 뒤 흐름을 참고로 보여 줍니다.").runs[0].font.size = Pt(9)

doc.add_heading("부록. 산출 방법", level=1)                    # [수정]
for m in METHOD:
    doc.add_paragraph(m, style="List Bullet")
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
          f"## 1. 핵심 판단\n**{stage}단계 {stage_name}**\n\n" + "\n".join(f"- **{k}** {v}" for k, v in JUDGE) + "\n\n"
          f"## 2. 변화\n{md_table(change_table)}\n\n"
          f"## 3. 원인 분석\n{md_table(factor_table)}\n\n"
          f"## 4. 최근 {config.WINDOW_DAYS}일 사건\n{md_table(all_events)}\n\n"
          f"## 5. 과거 유사 시기\n{md_table(similar_table)}\n\n"
          f"## 부록. 산출 방법\n" + "\n".join(f"- {m}" for m in METHOD) + f"\n\n{NOTE}\n")

# ===== 내려받기 버튼 (나란히) =====
b1, b2, _ = st.columns([1, 1, 3])
b1.download_button("워드로 내려받기", data=buffer.getvalue(), file_name=f"긴장도_브리핑_{day}.docx",
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
b2.download_button("md로 내려받기", data=report, file_name=f"긴장도_브리핑_{day}.md", mime="text/markdown")
