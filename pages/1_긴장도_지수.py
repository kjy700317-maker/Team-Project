import pandas as pd
import streamlit as st
import config # 맨 위 폴더의 config.py를 불러온다. streamlit은  app.py가 있는 폴더를 기준으로 파일을 찾아서, pages 안에서도 이렇게 불러 올 수 있다.
from utils.loader import load_daily, load_monthly, load_elements
import plotly.express as px

# ===== 페이지 제목 =====
st.title("한반도 군사 긴장 지수")
st.write("이곳에 긴장도 지수 대시보드가 들어갈 예정입니다")
st.write("더미 데이터 사용중:", config.USE_DUMMY) # config.USE_DUMMY : config 파일 안의 USE_DUMMY 값을 꺼내 온다 "파일이름.변수이름"형태 / st.write에 쉽표로 여러개를 넣으면 이어서 보여준다.
# from utils.dummy import make_daily # utils 폴더 → dummy.py 파일 → make_daily 함수를 꺼내옴 , 맨아레
# st.dataframe(make_daily()) # 표를 화면에 보여줌

# ===== 데이터 불러오기 =====
df = load_daily()
latest = df.iloc[-1] # 몇 번째 줄 위치로 꺼내는 방법, 0은 첫줄 -1은 맨 마지막줄: 파이썬에서 음수 번호는 뒤에서 부터 센다는 뜻
# st.write(latest) # 확인용 한줄
monthly = load_monthly()

# ===== 상단 카드 3개 =====
stage = int(latest["최종단계"]) # 표에서 꺼낸 숫자는 pandas 형식이라 딕셔너리 키로 쓰기 전에 일반 정수로 맞춰 주는 과줭
days = int(latest["지속일수"])
col1, col2, col3 = st.columns(3) # 3칸으로 나누기
# --- 카드 1: 현재 단계 ---
with col1:
    st.metric("현재 단계", f"{stage}단계 {config.STAGE_NAMES[stage]}", f"4단계 이상 {days}일째", delta_color="off") # metric(제목, 큰 값, 작은 값): 세번째 칸(delta)에 지속일수를 넣음 / delta_color="off": 원래 초록 빨강 화살표로 표시 -> 색 없이 회색으로 끔, 색으로 의미를 부여하지 않기 위해 지움
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
        st.metric("원점수", round(raw, 1), "최고 기준선(120) 초과", delta_color="off")
    else: # 120 초과 하지 않았다면 남은 거리를 표시
        st.metric("원점수", round(raw, 1), f"다음 기준선 {next_cut}까지 {next_cut - raw:.1f}" , delta_color="off")
# ===== 5단계 기준표 =====
st.subheader("단계 기준표")
stage_table = pd.DataFrame({"단계": [1, 2, 3, 4, 5], "이름": list(config.STAGE_NAMES.values()), "원점수 (이상)": [0] + config.RAM_CUTS, "평소대비 (이상)": [0] + config.RATIO_CUTS}) # [0] + ..., ... : [0] + ...) : 기준선은 4개인데 단계는 4개라 1단계 0을 추가 [0, 40, 60, 90, 120]
st.dataframe(stage_table, hide_index=True) # 줄 번호 숨기기
# ===== 확인용: 전체 표 =====
st.subheader("긴장도 추이")
fig = px.line(df, x="날짜", y="평소대비") # px.line(표, x=가로축 컬럼, y=세로축 컬럼): 선 그레프를 만듬
fig.add_hline(y=100, line_color="gray", annotation_text="평소 100") # .add_hline() : 가로선을 추가 / y=: 세로축 위치 / line_color: 선색 / annotation_text: 선옆에 붙은 작은 글씨
for cut in config.RATIO_CUTS[1:]: # [1:] 1부터 끝까지 -> 두번째 부터 끝까지
    fig.add_hline(y=cut, line_dash="dash", line_color="gray", annotation_text=str(cut)) # dash : 점선
lows = [0] + config.RATIO_CUTS # 각 단계 아레 끝 [1, 100, 150, 200, 300]
highs = config.RATIO_CUTS + [config.RATIO_CUTS[-1] + 50] # 각 단계 위 끝 / [-1] 은 맨 마지막이라는 뜻
for no, low, high in zip([1, 2, 3, 4, 5], lows, highs): # zip(A,B,C): 리스트 여러 개를 같은 순서 끼리 짝을 지음
    fig.add_hrect(y0=low, y1=high, fillcolor=config.STAGE_COLORS[no], opacity=0.1, line_width=0) # 가로 사각행 / y~y : 범위 / opacity=0.1: 투명도, line_width=0: 사각형 테두리, 0 -> 사각형 테두리를 그리지 않는다
st.plotly_chart(fig) # st.plotly_chart(): 완성된 그림을 Streamlit 화면에 올림
st.dataframe(df)

# ===== 과거 유사 시기 =====
st.subheader("과거 유사 시기")
now = monthly.iloc[-1] # 이번달 - 마지막 줄
past = monthly.iloc[:-config.SIMILAR_EXCLUDE_MONTHS].copy() # 최근 config.SIMILAR_EXCLUDE_MONTHS개월을 뺸 지난달, 뒤에서부터 뺀 값 / .copy() 변형을 대비
past["차이"] = (past["평소대비"] - now["평소대비"]).abs() # 이번달과 평소대비 차이 / .abs(): 절댓값, 부호를 삭제 - 음수를 인식해 가장 작은값으로 뽑는 것을 방지
similar = past.nsmallest(config.SIMILAR_N, "차이") # 차이가 가작 작은값, 반대 .nlargest() 가장큰줄 인식
st.dataframe(similar, hide_index=True)
# ===== 유사 시기 카드 ===== 카드 순서 연월 , 평소대비, 단게 순서
cols = st.columns(config.SIMILAR_N) # 고른 개수만큼 가로 칸 나누기
for i in range(config.SIMILAR_N):
    row = similar.iloc[i] # 1번째 줄 꺼내기 (한달)
    past_stage = int(row["최종단계"]) # 그달의 단계 번호
    with cols[i]: # 1번째 칸안에 그리기
        st.metric(row["연월"], round(row["평소대비"]), f"{past_stage}단계 {config.STAGE_NAMES[past_stage]}", delta_color="off")
# ===== 점수 구성표 =====
st.subheader("점수 구성 (최근 30일)")
elements = load_elements().sort_values("점수", ascending=False) # ascending: 오름차순 / elements = elements.srot_values() : 정렬한 결과를 같은 이름에 담는 작업 : 실행하지 않으면 정렬한 표가 그냥 버려짐
st.dataframe(elements, hide_index=True) #
st.caption(f"합계 {elements['점수'].sum()}점 (가중치가 음수인 요소는 점수를 깎음)") # 표 아래 작은 회색 글씨

# 월별 표 확인용
# from utils.dummy import make_monthly
# st.dataframe(make_monthly(df))
#월별 표 확인용 2
# st.dataframe(monthly)
# 점수 구성 확인용
# from utils.loader import load_elements
# st.dataframe(load_elements(), hide_index= True)
