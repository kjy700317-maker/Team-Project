import pandas as pd
import streamlit as st
import plotly.express as px                     # [수정] 미니 추이 그래프
import config
from utils.loader import load_daily, load_monthly, load_elements, load_events
from utils.ui import stage_scale                # [수정] 5단계 눈금 (홈과 같이 씀)
from io import BytesIO                          # 파일 대신 쓸 메모리 공간
from docx import Document                       # 워드 문서 만들기
from docx.shared import Pt, RGBColor            # 글자 크기(Pt), 글자 색(RGB)
from docx.enum.text import WD_ALIGN_PARAGRAPH   # 문단 정렬(가운데, 오른쪽)
from docx.oxml.ns import qn                     # 한글 글꼴 지정용 이름표
from docx.oxml import OxmlElement               # [수정] 워드 표 칸 배경색 지정용

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")

# ===== 화면: 제목 =====
st.title("긴장도 브리핑")   # [수정] 기준일 고르는 칸보다 위에 오도록 맨 위로 옮김

# ===== 데이터 불러오기 =====
df = load_daily()           # 결과_일별 표
monthly = load_monthly()    # 결과_월별 표
events = load_events()      # 사건_일단위 표

# ===== [수정] 기준일 고르기 (1페이지와 같은 사례 목록) =====
c1, c2 = st.columns([2, 1])   # 고르는 칸과 달력을 한 줄에
case = c1.selectbox("기준일 (단계별 사례 보기)", list(config.CASES.keys()))   # [수정] 사례 목록은 config.CASES 한 곳에
pick = config.CASES[case]   # 고른 이름 → 날짜 글자
if pick == "pick":
    pick = c2.date_input("날짜", value=df["날짜"].iloc[-1], min_value=df["날짜"].iloc[0], max_value=df["날짜"].iloc[-1])
if pick is not None:
    pick = pd.Timestamp(pick)                   # 글자·날짜를 pandas 날짜로 통일
    latest = df[df["날짜"] <= pick].iloc[-1]    # 그날(또는 그 전 마지막 날) 줄
else:
    latest = df.iloc[-1]                        # 가장 최근 날
elements = load_elements(pick)                  # [수정] 기준일 전 N일 요소별 점수 (None이면 최신)
monthly = monthly[monthly["연월"] <= f"{latest['날짜']:%Y-%m}"]   # [수정] 기준일이 든 달까지만 (유사 시기용)

# ===== 보고서에 넣을 숫자 모으기 =====
day = latest["날짜"].strftime("%Y-%m-%d")             # 날짜 → "2026-09-30" 글자
stage = int(latest["최종단계"])
stage_name = config.STAGE_NAMES[stage]                # 4 → 경계
color = config.STAGE_COLORS[stage]                    # 단계 색 ("#FB8C00")
days = int(latest["지속일수"])
ratio = latest["평소대비"]
raw = latest["원점수"]
recent = events[(events["시작일"] > latest["날짜"] - pd.Timedelta(days=config.WINDOW_DAYS)) & (events["시작일"] <= latest["날짜"])]   # 최근 N일 사건 / [수정] 30 → config.WINDOW_DAYS, 기준일 뒤 사건은 빼기
recent = recent.sort_values("시작일", ascending=False)                       # 최신순
top = elements.sort_values("점수", ascending=False).head(3)                  # 점수 상위 3개 요소
now = monthly.iloc[-1]
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy()
past["차이"] = (past["평소대비"] - now["평소대비"]).abs()
similar = past.nsmallest(config.SIMILAR_N, "차이")

# ===== 보고서 표 3개 만들기 (화면·워드·md가 같은 표를 같이 씀) =====
factor_table = pd.DataFrame({                                  # 주요 요인 표
    "요소": top["요소명"], "주체": top["주체국"], "건수": top["건수"], "점수": top["점수"]})
event_table = pd.DataFrame({                                   # 최근 주요 사건 표 (최대 5개)
    "날짜": recent["시작일"].dt.strftime("%Y-%m-%d"),
    "종류": recent["카테고리코드"].map(config.ELEMENT_NAMES),  # .map(딕셔너리): 코드 → 이름으로 한 번에 바꾸기
    "기여": recent["카테고리코드"].map(config.WEIGHTS),       # [수정] 사건 1건의 기여(가중치) 칸 추가 (사건명이 길어서 앞쪽에)
    "사건": recent["사건명"]}).head(5).reset_index(drop=True)   # [수정] reset_index: 줄 번호를 0,1,2..로 새로 (파일 17개를 이어 붙여 번호가 겹쳐서 색칠이 에러남)
similar_table = pd.DataFrame({                                 # 과거 유사 시기 표
    "연월": similar["연월"],
    "평소대비": similar["평소대비"].round(0).astype(int),
    "최고 단계": similar["최종단계"].astype(int).map(lambda s: f"{s}단계 {config.STAGE_NAMES[s]}")})  # lambda: 한 줄짜리 작은 함수

# ===== 한 줄 요약 문장 =====
summary = (f"{day} 기준 한반도 군사 긴장도는 {stage}단계({stage_name})입니다. "
           f"평소의 {ratio / 100:.1f}배 수준이며, 최근 {config.WINDOW_DAYS}일 동안 사건 {len(recent)}건이 있었습니다.")
if days > 0:                                                    # 4단계 이상일 때만 지속일수 문장 붙이기
    summary += f" 4단계 이상이 {days}일째 이어지고 있습니다."
NOTE = "※ 대시보드 숫자로 자동 작성되었습니다. 가중치·기준선은 현재 진행도 기준 임시값이며 추후 결정됩니다."

# ===== 화면: 기준일 안내 =====
st.caption(f"기준일 {day} · 최근 {config.WINDOW_DAYS}일 사건 점수 합으로 계산")   # [수정] 30 → config.WINDOW_DAYS

# ===== 화면: 단계 띠 (단계 색으로 칠한 상자) =====
st.markdown(
    f"<div style='background:{color}; color:white; padding:16px 20px; border-radius:10px; font-size:22px;'>"
    f"<b>{stage}단계 {stage_name}</b> &nbsp;·&nbsp; 평소대비 {ratio:.0f}"
    + (f" &nbsp;·&nbsp; 4단계 이상 {days}일째" if days > 0 else "") + "</div>",   # [수정] 지속일수는 4단계 이상일 때만
    unsafe_allow_html=True)   # unsafe_allow_html=True: 글 안의 HTML(색 상자)을 그대로 그리게 허락

# ===== [수정] 화면: 5단계 눈금 (홈과 같은 방식, 지금 단계만 진하게) =====
st.markdown(stage_scale(stage), unsafe_allow_html=True)   # [수정] 눈금 만드는 코드는 utils/ui.py로 옮김
st.write("")                  # 여백

# ===== 화면: 요약 + 숫자 카드 =====
st.info(summary)              # 파란 안내 상자 안에 요약 문장
col1, col2, col3 = st.columns(3)
col1.metric("평소 대비", f"{ratio:.0f}")
col1.caption("평소 = 100")   # [수정] delta → caption (회색 화살표 없애기, 1페이지와 같게)
col2.metric(f"원점수 ({config.WINDOW_DAYS}일 합)", f"{raw:.1f}")
col3.metric(f"최근 {config.WINDOW_DAYS}일 사건", f"{len(recent)}건")

# ===== [수정] 화면: 미니 추이 그래프 (최근 90일) =====
trend = df[(df["날짜"] > latest["날짜"] - pd.Timedelta(days=90)) & (df["날짜"] <= latest["날짜"])]   # 기준일 전 90일 (기준일 뒤는 빼기)
fig = px.line(trend, x="날짜", y="평소대비", height=260)                        # height: 그래프 높이 (작게)
lows = [min(0, trend["평소대비"].min() - 10)] + config.RATIO_CUTS               # 1페이지와 같은 단계 색 띠 (맨 아래 띠는 음수까지)
highs = config.RATIO_CUTS + [max(config.RATIO_CUTS[-1] + 50, trend["평소대비"].max() + 10)]   # 맨 위 띠는 그래프 끝까지
for no, low, high in zip([1, 2, 3, 4, 5], lows, highs):
    fig.add_hrect(y0=low, y1=high, fillcolor=config.STAGE_COLORS[no], opacity=0.1, line_width=0)
fig.add_hline(y=100, line_color="gray", annotation_text="평소 100", annotation_position="bottom left")
fig.update_traces(line_color=color, line_width=3)                              # 선 색 = 지금 단계 색
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title="최근 90일 평소대비", xaxis_title=None)   # margin: 바깥 여백 줄이기
st.plotly_chart(fig)

# ===== [수정] 화면: 표 색칠 함수 =====
def paint_event(row):   # 사건 표: 기여 칸만 올리면 빨강, 내리면 파랑 글씨
    return ["" if col != "기여" else ("color: #C0392B; font-weight: 700" if row["기여"] > 0 else "color: #2E6DB4; font-weight: 700")
            for col in row.index]                                              # row.index: 그 줄의 칸 이름들

def paint_similar(row):   # 유사 시기 표: 최고 단계 칸을 단계 색으로
    no = int(row["최고 단계"][0])                                               # "4단계 경계"[0] → "4" → 4
    return ["" if col != "최고 단계" else f"background-color: {config.STAGE_COLORS[no]}; color: white"
            for col in row.index]

# ===== 화면: 표 3개 (왼쪽 2개, 오른쪽 1개) =====
left, right = st.columns([3, 2])   # [3, 2]: 왼쪽 칸을 오른쪽보다 넓게 (3:2)
with left:
    st.subheader("최근 주요 사건")
    st.dataframe(event_table.style.apply(paint_event, axis=1), hide_index=True, use_container_width=True,
                 column_config={"기여": st.column_config.NumberColumn("기여", format="%+d")})   # [수정] 색칠 / format="%+d": 5 → +5
    st.subheader("주요 요인 (점수 상위 3개)")
    st.dataframe(factor_table, hide_index=True, use_container_width=True)
with right:
    st.subheader("과거 유사 시기")
    st.dataframe(similar_table.style.apply(paint_similar, axis=1), hide_index=True, use_container_width=True)   # [수정] 색칠
st.caption(NOTE)

# ===== 워드(.docx) 만들기 =====
def shade(cell, hex_color):                                     # [수정] 워드 표 칸 배경색 칠하기 (python-docx에 명령이 없어서 직접 지정)
    shd = OxmlElement("w:shd")                                 # 칸 배경 설정 조각 만들기
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))               # "#FB8C00" → "FB8C00"
    cell._tc.get_or_add_tcPr().append(shd)                     # 칸 설정에 붙이기 (외울 필요 없음)

def add_table(doc, table):                                     # 표(DataFrame)를 워드 표로 옮기는 함수
    t = doc.add_table(rows=1, cols=len(table.columns))         # 머리 줄 1줄짜리 표
    t.style = "Table Grid"                                     # 워드 기본 표 디자인 (얇은 테두리)
    for i, name in enumerate(table.columns):                   # enumerate: 번호와 값을 같이 꺼냄
        cell = t.rows[0].cells[i]
        cell.text = str(name)                                  # 머리 줄 = 컬럼 이름
        run = cell.paragraphs[0].runs[0]
        run.bold = True                                        # 머리 줄 글자는 굵게
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)        # [수정] 머리 줄 글자 흰색
        shade(cell, "#5D6D7E")                                 # [수정] 머리 줄 배경 진회색
    for _, row in table.iterrows():                            # iterrows: 표를 한 줄씩
        cells = t.add_row().cells                              # 새 줄 추가
        for i, value in enumerate(row):
            cells[i].text = str(value)
            col = table.columns[i]                             # [수정] 지금 칸 이름
            if col == "기여":                                  # [수정] 기여 칸: 올리면 빨강, 내리면 파랑 글씨
                cells[i].text = f"{int(value):+d}"            # 5 → "+5", -3 → "-3"
                run = cells[i].paragraphs[0].runs[0]
                run.bold = True
                run.font.color.rgb = RGBColor.from_string("C0392B" if value > 0 else "2E6DB4")
            if col == "최고 단계":                             # [수정] 단계 칸: 단계 색 배경 + 흰 글씨
                shade(cells[i], config.STAGE_COLORS[int(str(value)[0])])
                cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    doc.add_paragraph()                                        # 표 아래 빈 줄

doc = Document()
style = doc.styles["Normal"]                                   # 기본 글자 모양
style.font.name = "맑은 고딕"
style.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")    # 한글 글꼴은 따로 지정해야 적용됨
style.font.size = Pt(10.5)

title = doc.add_heading("한반도 군사 긴장도 브리핑", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER                    # 제목 가운데
p = doc.add_paragraph(f"기준일 {day}")
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT                         # 기준일 오른쪽

doc.add_heading("1. 현재 상황", level=1)
p = doc.add_paragraph()
run = p.add_run(f"{stage}단계 {stage_name}")                   # run: 한 문단 안에서 모양이 다른 글 조각
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor.from_string(color[1:])           # "#FB8C00" → 앞의 # 떼고 색 지정
doc.add_paragraph(summary)

doc.add_heading("2. 최근 주요 사건", level=1)
add_table(doc, event_table)
doc.add_heading("3. 주요 요인 (점수 상위 3개)", level=1)
add_table(doc, factor_table)
doc.add_heading("4. 과거 유사 시기", level=1)
add_table(doc, similar_table)

p = doc.add_paragraph(NOTE)
p.runs[0].font.size = Pt(8)                                    # 안내 문구는 작게
p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)          # 회색

buffer = BytesIO()
doc.save(buffer)

# ===== md 글 만들기 =====
def md_table(table):                                           # 표 → md 표 글자 ("| 날짜 | 종류 |" 모양)
    lines = ["| " + " | ".join(table.columns) + " |",           # 머리 줄 / " | ".join: 사이사이에 | 넣어 잇기
             "|" + "---|" * len(table.columns)]                 # 구분 줄
    for _, row in table.iterrows():
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)                                     # 줄들을 줄바꿈으로 이어 붙이기

report = (f"# 한반도 군사 긴장도 브리핑\n기준일: {day}\n\n## 1. 현재 상황\n**{stage}단계 {stage_name}**\n\n{summary}\n\n"
          f"## 2. 최근 주요 사건\n{md_table(event_table)}\n\n"
          f"## 3. 주요 요인\n{md_table(factor_table)}\n\n"
          f"## 4. 과거 유사 시기\n{md_table(similar_table)}\n\n{NOTE}\n")

# ===== 내려받기 버튼 (나란히) =====
b1, b2, _ = st.columns([1, 1, 3])   # 버튼 2개를 왼쪽에 나란히, 나머지는 빈칸
b1.download_button("워드로 내려받기", data=buffer.getvalue(), file_name=f"긴장도_브리핑_{day}.docx",
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
b2.download_button("md로 내려받기", data=report, file_name=f"긴장도_브리핑_{day}.md", mime="text/markdown")
