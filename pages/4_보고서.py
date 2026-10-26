import pandas as pd
import streamlit as st
import config
from utils.loader import load_daily, load_monthly, load_elements, load_events
from io import BytesIO                         # 파일 대신 쓸 메모리 공간
from docx import Document

# ===== 페이지 설정 =====
st.set_page_config(page_title="한반도 긴장도", layout="wide")# 워드 문서 만들기

# ===== 페이지 제목 =====
st.title("보고서 자동 작성")

# ===== 데이터 불러오기 =====
df = load_daily() # 결과_일별 표
monthly = load_monthly() # 결과_월별 표
elements = load_elements() # 최근 30일 요소별 점수 표
events = load_events() # 사건_일단위 표

# ===== 보고서에 넣을 숫자 모으기 =====
latest = df.iloc[-1] # 일별 표 맨 마지막 줄 = 가장 최근 날
day = latest["날짜"].strftime("%Y-%m-%d") # 날짜 → "2026-09-30" 글자
stage = int(latest["최종단계"])
stage_name = config.STAGE_NAMES[stage]  # 단계 번호 → 이름 (4 → 경계)
days = int(latest["지속일수"]) # 4단계 이상이 며칠째 이어지는지
ratio = latest["평소대비"]
raw = latest["원점수"]
recent = events[events["시작일"] > latest["날짜"] - pd.Timedelta(days=30)] # 마지막 날 기준 최근 30일 사건만
recent = recent.sort_values("시작일", ascending=False) # 최신순 정렬
top = elements.sort_values("점수", ascending=False).head(3) # 점수 상위 3개 요소
now = monthly.iloc[-1] # 월별 표 마지막 줄 = 이번 달
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy() # 최근 12개월을 뺀 과거 달들
past["차이"] = (past["평소대비"] - now["평소대비"]).abs() # 이번 달과 평소대비 차이
similar = past.nsmallest(config.SIMILAR_N, "차이") # 차이가 가장 작은 3개 달 = 과거 유사 시기

# ===== 문장 틀에 숫자 채우기 =====
report = f"""# 한반도 군사 긴장도 브리핑
기준일: {day}
## 1. 현재 상황
- 최종단계: **{stage}단계 {stage_name}** (4단계 이상 {days}일째)
- 평소대비: **{ratio:.0f}** (평소 = 100), 원점수 {raw:.1f}
- 최근 30일 사건: {len(recent)}건
## 2. 주요 요인 (최근 30일 점수 상위 3개)
"""
for i in range(len(top)): # 상위 요소 3줄
    row = top.iloc[i] # i번째 줄 꺼내기
    report += f"- {row['요소명']} ({row['주체국']}): {row['건수']}건, {row['점수']}점\n" # += : 기존 글 뒤에 이어 붙이기

report += "\n## 3. 최근 주요 사건\n"
for i in range(min(5, len(recent))): # 최대 5개 (사건이 5개보다 적으면 그만큼 min)
    row = recent.iloc[i]
    report += f"- {row['시작일']:%Y-%m-%d} [{config.ELEMENT_NAMES[row['카테고리코드']]}] {row['사건명']}\n" # 날짜 [요소명] 사건명

report += "\n## 4. 과거 유사 시기\n"
for i in range(len(similar)): # 유사 시기 3개
    row = similar.iloc[i] # i번째 달 꺼내기
    report += f"- {row['연월']}: 평소대비 {row['평소대비']:.0f}, {int(row['최종단계'])}단계 {config.STAGE_NAMES[int(row['최종단계'])]}\n"

report += "\n※ 이 보고서는 대시보드 숫자로 자동 작성되었습니다. 가중치·기준선은 팀 확정 전 임시값입니다.\n" # 맨 끝 안내 문구 (확정후 삭제예정)

# ===== 워드(.docx)로 만들기 =====
doc = Document() # 빈 워드 문서
for line in report.split("\n"): # 보고서 글을 한 줄씩
    text = line.replace("**", "") # 굵게 표시 ** 지우기
    if line.startswith("# "): # "# "로 시작하면
        doc.add_heading(text[2:], level=0) # 문서 제목 (text[2:]: 앞 2글자 "# " 떼기)
    elif line.startswith("## "): # 아니면 "## "로 시작하면
        doc.add_heading(text[3:], level=1) # 소제목 (앞 3글자 "## " 떼기)
    elif line.startswith("- "): # 아니면 "- "로 시작하면
        doc.add_paragraph(text[2:], style="List Bullet") # 글머리 기호 목록 *
    elif text.strip(): # 아니면, 빈 줄이 아니면 (strip: 앞뒤 공백 지우기)
        doc.add_paragraph(text) # 보통 문단
buffer = BytesIO() # 파일 대신 쓸 메모리 공간
doc.save(buffer) # 워드 문서를 메모리에 저장
st.download_button("워드로 내려받기 (.docx)", data=buffer.getvalue(), file_name=f"긴장도_브리핑_{day}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document") # getvalue(): 메모리 내용 꺼내기 / mime: "워드 파일"이라는 이름표

# =====  다운로드 버튼 & 화면에 보여 주기 =====
st.download_button("보고서 내려받기 (.md)", data=report, file_name=f"긴장도_브리핑_{day}.md", mime="text/markdown")
with st.container(border=True): # 테두리 상자 안에 그리기
    st.markdown(report) # 보고서를 마크다운 서식으로 화면에 표시

# ===== 확인용 =====
# st.write(day, stage, stage_name, days, ratio, raw, len(recent))