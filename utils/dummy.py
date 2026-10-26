import numpy as np
import pandas as pd
import config

def make_daily(): # 지속일수
# ===== 1. 날짜 =====
    dates = pd.date_range("2015-01-01", "2026-10-20", freq="D") # 시작일부터 끝일 까지 날짜 목록/freq="D" : DAY 하루 간격
    rng = np.random.default_rng(42) # 무작위 숫자 생성기, 42 = 시드 = 같은 시드를 주면 매번 똑같은 무작위 숫자를 부여, 고정
    # raw = rng.normal(60, 20, len(dates)).clip(0) # 평균 60, 퍼짐정도 20안 숫자를 날짜 갯수(dates) 만큼 만든다.
# ===== 6. 원점수 (어제 값을 이어받는 방식) =====
    raw = [] # 오늘 점수 = 어제 점수애서 조금 변환딘 값
    x = 60 # [] , x : 빈리스트, 사적점수 / 첫날 평소 60 시작
    for i in range(len(dates)): # range(n): n-1
        x = 60 + 0.97 * (x - 60) + rng.normal(0, 6) # (x - 60): 어제 점수와 비교해 높낮이 / 0.97 *: 그차이를 97%만 남김, 매일 3%씩 평소 쪽으로 돌아가는 방식, 1에 가까울 수록 어레 유지 되고 0에 가까울 수록 금방 돌아감 / + rng.normal(0, 6): 오늘 생긴 사건만큼 평균 0, 폭 6 정도로 무작위 숫자를 부여
        raw.append(max(x, 0)) # max(x, 0): x와 0중 큰값, 음수가 0이됨, .clip(0)과 같은 역할
    df = pd.DataFrame({"날짜": dates, "원점수": raw}) # 표로 만듬
# ===== 2. 평소대비 =====
    base = 60 # 평소 원전숨을 담은 더미 값 , 나중에 값이 바뀔떄 바뀔예정
    df["평소대비"] = (df["원점수"] / base * 100).round(1) # (df["원점수"] / base * 100): pandas에서는 컬럼 전체에 한 번에 계산이 적용,4천여 개 행을 반복문 없이 한 줄로 계산 / df["평소대비"] = - 표에 앖는 이름으로 값을 넣으면 새컬럼이 생김 평소 대비 긴장도 = (현재 원점수 ÷ 평소 원점수) × 100
# ===== 3. 단계 (기준선 기준 / 평소대비 기준) =====
    bins = [-np.inf] + config.RAM_CUTS + [np.inf]
    df["단계_기준선"] = pd.cut(df["원점수"], bins= bins, labels=[1, 2, 3, 4, 5], right=False).astype(int) # -np.infm np.inf : 마이너스 무한대와 플러스 무한대, 기준선 4개 (config.RAM_CUTS) 양끝에 븥어서 [-∞, 40, 60, 90, 120, ∞] 로 만들면 구간 5개가 생김 / 리스트끼리 + 를 쓰면 이어 붙는다 / pd.cut(값, bins=경계, labels=이름) : 각 값이 어느 구간에 들어 가는지 찾아서 이름을 붙여줌 / right=False : 구간의 왼쪽 끝은 포함하고 오른쪽 끝은 뺀단는 뜻, 40이면 1단계가 아니라 2단계가 됨 (하한 40부터는 2단계 규칙) / .astype(int) : 결과를 일반 정수로 바꿈, pd.cut의 결과는 범주라는 특수 형태임, 나중의 계산의 편의성을 위해 바꿈
    bins = [-np.inf] + config.RATIO_CUTS + [np.inf]
# ===== 4. 최종단계 = 둘 중 높은 쪽 =====
    df["단계_평소대비"] = pd.cut(df["평소대비"], bins=bins, labels=[1, 2, 3, 4, 5], right=False).astype(int)
    df["최종단계"] = df[["단계_기준선", "단계_평소대비"]].max(axis=1) # [[]] : 대괄호가 두 겹인 이유 바깥 [] 는 "df에서 꺼낸다", 안쪽 [] 는 "이 컬럼 목록" 이라는 뜻, 두 컬럼만 남긴 작은 표가 만들어진다. / axis=1 : 어느 방향으로 비교할지, 0 세로, 1 가로방향
# ===== 5. 지속일수 = 4단계 이상 며칠째인지 =====
    days = []
    count = 0 # 연속 일수를 세는 계수기
    for stage in df["최종단계"]:
        if stage >= 4: # 오늘이 4단계 이상이면
            count = count + 1 # 계수기에 1을 더함
        else:
            count = 0 # 그렇지 않으면 계수기를 리셋
        days.append(count) # 끝
    df["지속일수"] = days # 컬럼
    return df
# ===== 월별 표 결과_월별 모양) =====
def make_monthly(daily): # daily 매개변수
    m = daily.copy() # 복사본 생성, 연월 컬럼을 붙이면 원래 일별 표까지 변형되기에 사전에 복사
    m["연월"] = m["날짜"].dt.strftime("%Y-%m") # 날짜를 2026-10 같은 글자로 변경, .dt는 날짜기능 사용, %Y는 4자리 연도, %m 은 2자리 월
    monthly = m.groupby("연월").agg(원점수=("원점수", "mean"), 평소대비=("평소대비", "mean"), 최종단계=("최종단계", "max")).reset_index() # 가틍ㄴ 연월끼리 묶음, 엑셀의 피벗 테이블과 같은 개념 / .reset_index() : .groupby를 하면 연월이 표의 줄이름을로 올라가기에 다시 일반컬럼으로 내림
    monthly["원점수"] = monthly["원점수"].round(1)
    monthly["평소대비"] = monthly["평소대비"].round(1)
    return monthly

def make_yearly(daily):  # 일별 표를 받아서 결과_연별 모양으로 묶어 돌려줌
    y = daily.copy()
    y["연도"] = y["날짜"].dt.year # 날짜 → 2024 (숫자)
    yearly = y.groupby("연도").agg( 원점수=("원점수", "mean"), 평소대비=("평소대비", "mean"), 최종단계=("최종단계", "max")).reset_index() # 최종단계=("최종단계", "max") :그해 가장 높았던 단계
    yearly["원점수"] = yearly["원점수"].round(1)
    yearly["평소대비"] = yearly["평소대비"].round(1)
    return yearly

# ===== 점수 구성 (결과 일별 요소, 최근 30일 합계로 단순화) =====
def make_elements():
    rng = np.random.default_rng(7)
    elements = pd.DataFrame({"요소코드": ["X1","X2","X3","X4","X5"], "요소명": ["미사일 발사", "군사훈련", "무력 충돌", "외교 비난", "정상화담"], "주체국": ["PRK", "USA", "PRK", "CHN", "KOR"], "가중치": [5,2,8,1,-3]}) # 음수는 긴장을 낮추는 사건
    elements["건수"] = rng.integers(0, 6, size=len(elements)) # elements의 정수 뽑기 (0 ~ 5 사이)
    elements ["점수"] = elements["건수"] * elements["가중치"] # ERD규칙: 점수 = 건수 * 가중치
    return elements

