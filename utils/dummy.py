import numpy as np
import pandas as pd
import config

def make_daily():
    dates = pd.date_range("2015-01-01", "2026-10-20", freq="D") # 시작일부터 끝일 까지 날짜 목록/freq="D" : DAY 하루 간격
    rng = np.random.default_rng(42) # 무작위 숫자 생성기, 42 = 시드 = 같은 시드를 주면 매번 똑같은 무작위 숫자를 부여, 고정
    raw = rng.normal(60, 20, len(dates)).clip(0) # 평균 60, 퍼짐정도 20안 숫자를 날짜 갯수(dates) 만큼 만든다.
    df = pd.DataFrame({"날짜": dates, "원점수": raw}) # 표로 만듬
    base = 60 # 평소 원전숨을 담은 더미 값 , 나중에 값이 바뀔떄 바뀔예정
    df["평소대비"] = (df["원점수"] / base * 100).round(1) # (df["원점수"] / base * 100): pandas에서는 컬럼 전체에 한 번에 계산이 적용,4천여 개 행을 반복문 없이 한 줄로 계산 / df["평소대비"] = - 표에 앖는 이름으로 값을 넣으면 새컬럼이 생김 평소 대비 긴장도 = (현재 원점수 ÷ 평소 원점수) × 100
    bins = [-np.inf] + config.RAM_CUTS + [np.inf]
    df["단계_기준선"] = pd.cut(df["원점수"], bins= bins, labels=[1, 2, 3, 4, 5], right=False).astype(int) # -np.infm np.inf : 마이너스 무한대와 플러스 무한대, 기준선 4개 (config.RAM_CUTS) 양끝에 븥어서 [-∞, 40, 60, 90, 120, ∞] 로 만들면 구간 5개가 생김 / 리스트끼리 + 를 쓰면 이어 붙는다 / pd.cut(값, bins=경계, labels=이름) : 각 값이 어느 구간에 들어 가는지 찾아서 이름을 붙여줌 / right=False : 구간의 왼쪽 끝은 포함하고 오른쪽 끝은 뺀단는 뜻, 40이면 1단계가 아니라 2단계가 됨 (하한 40부터는 2단계 규칙) / .astype(int) : 결과를 일반 정수로 바꿈, pd.cut의 결과는 범주라는 특수 형태임, 나중의 계산의 편의성을 위해 바꿈
    bins = [-np.inf] + config.RATIO_CUTS + [np.inf]
    df["단계_평소대비"] = pd.cut(df["평소대비"], bins=bins, labels=[1, 2, 3, 4, 5], right=False).astype(int)
    df["최종단계"] = df[["단계_기준선", "단계_평소대비"]].max(axis=1) # [[]] : 대괄호가 두 겹인 이유 바깥 [] 는 "df에서 꺼낸다", 안쪽 [] 는 "이 컬럼 목록" 이라는 뜻, 두 컬럼만 남긴 작은 표가 만들어진다. / axis=1 : 어느 방향으로 비교할지, 0 세로, 1 가로방향
    return df



