import pandas as pd
import numpy as np
import config
# ===== 사건 파일 목록 (E1 UN표결은 팀 결정 전까지 제외) =====
EVENT_FILES = ["A/A1_핵실험_일단위_CSV.csv",
               "A/A2_미사일_발사_CSV.csv",
               "A/A3_저강도_물리_도발_CSV.csv",
               "A/A4_군사훈련_CSV.csv",
               "A/A5_미_전력자산_전개_일단위_CSV.csv",
               "A/A6_열병식_CSV.csv",
               "A/A7_포격_총격_물리_충돌_CSV.csv",
               "B/B1_신형무기개발시험_전처리.csv",
               "B/B3_군비이벤트_전처리.csv",
               "B/B4_핵태세확장억제_사건.csv",
               "C/C1_위협성명담화_전처리.csv",
               "C/C2_교리법제_전처리.csv",
               "C/C3_동맹협의_사건.csv",
               "C/C4_대화협상합의_전처리.csv",
               "C/C5_제재_결의_수출통제.csv",
               "E/E5_남북관계연표_정제.csv",
               "F/F2_연도별회담_정제.csv"]
# ===== 사건 파일 =====
def read_events(path):
    df = pd.read_csv(path, encoding="utf-8-sig") # sig: 맨앞 보이지 않는 표시를 때고 읽음, 첫칸이름이 깨지는 것을 방지
    df = df[df["사용여부"] == "Y"] # 사용여부가 Y인 줄만 남기기 (ERD 규칙) / 안쪽 df: 줄마다 Y인지 물어봐서 T/F 목록을 만듬 / 바깥 df: 목록에서 T인 줄만 남김 필터
    return df

# ===== 사건파일 결합 =====
def read_all_events():
    tables = []
    for name in EVENT_FILES:
        tables.append(read_events("data/processed/" + name)) # 앞에 폴더 경로를 붙여 읽고 리스트에 추가
    return pd.concat(tables) # 리스트 속 표들을 위아래로 이어 붙임 (컬럼 결합및 추가)

# ===== 사건 표 정리 (ERD 사건_일단위) =====
def make_events():
    events = read_all_events()
    events = events[["사건ID", "시작일", "주체국", "대상국", "사건명"]].copy()
    events["카테고리코드"] = events["사건ID"].str[:2] # .str[:2]: 글자의 앞 두글자만 자름 A2-0001 -> A2
    events = events.dropna(subset=["시작일", "주체국"]) # na값 없음: 지정한 칸 중 하나라도 비어 있으면 그줄을 제외
    events["시작일"] = pd.to_datetime(events["시작일"]) # 날짜 데이터가 문자로 되어있어 날짜롷 바꿈 str - date
    # A1 1796건 중 북한은 6건 나머지는 냉전 떄 미국, 소련(러시아)임 -> 이대로 두면 1958 ~ 1962 년이 한반도 긴장 최고 시기로 인식됨, 실제로는 한반도와 상관없는 사건 -> 그레서 북한만 인식하게 아레 코드를 짜둠 - 현재 가중치는 임의로 두었음 건수로 계산중
    # events = events[~((events["카테고리코드"] == "A1") & (events["주체국"] != "PRK"))]   # A1은 북한 것만
    return events

# ===== 날짜, 카테고리, 주체국별 건수와 점수 (ERD 결과_일별_요소) =====
def make_daily_elements(events):
    elements = events.groupby(["시작일", "카테고리코드", "주체국"]).size().reset_index(name="건수") # 같은 날 미사일이 3번 쐈으면 한 묶음 / size: 건수 / 묶음줄 건수 칸에 이름을 부여 "건수"
    elements["가중치"] = elements["카테고리코드"].map(config.WEIGHTS)  # 코드로 가중치 찾아 붙이기
    elements["점수"] = elements["건수"] * elements["가중치"] # ERD: 점수 = 건수 × 가중치
    return elements

# ===== 원점수 = 최근 30일 점수 합 (ERD 결과_일별) =====
def make_raw_daily(elements):
    daily = elements.groupby("시작일")["점수"].sum() # 날짜로 묶어서 점수 칸만 더함, 날짜별 점수 합(사건 있는 날만)
    all_days = pd.date_range(daily.index.min(), daily.index.max()) # 사건 닐 - 마지막 사건 날
    daily = daily.reindex(all_days, fill_value=0) # 사건 없는 날을 0점으로 채움, 날짜 빈칸이 존재 - 비는 날에 0울 넣어 30일 달력을 완성
    raw = daily.rolling(30, min_periods=1).sum() # rolling: 이동합, min_periods=1: 30일이 안된 구간도 있는 만큼 더함
    # 회담, 합의는 음수 가중치라서 사건이 몰린 시기 (2018년도)는 30알 헙이 마이너스가 되는것을 확인 -> 평소대비 %가 음수로 나와서 이상한 뜻으로 변질됨 -> 그레서 아레 코드를 짜둠 - 0보다 작은 값은 전부 0이되고 나머지는 그대로 유지
    # raw = raw.clip(lower=0)
    return pd.DataFrame({"날짜": all_days, "원점수": raw.values}) # .values: 날짜 꼬리표를 때고 숫자만 꺼냄, 꼬리표 끼리 엉키는 것을 방지

# ===== 평소대비 (ERD 결과_일별) =====
def make_daily_real():
    df = make_raw_daily(make_daily_elements(make_events())) # 상자 안에 상자를 넣는 모양 / make_events -> make_daily_elements-> make_raw_daily 집어 넣는 순서
    base_rows = df[(df["날짜"] >= config.BASE_START) & (df["날짜"] <= config.BASE_END)] # 기준기간 줄만 남기기 / 필터 조건 동시 2개
    base = base_rows["원점수"].mean() # 평소는 기준기간 원점수 평균 / 평소 원점수
    df["평소대비"] = (df["원점수"] / base * 100).round(1) # 오늘 원점수 + 평소 원점수 * 100
    bins = [-np.inf] + config.RAM_CUTS + [np.inf] # dummy 3. 단계 설명
    df["단계_기준선"] = pd.cut(df["원점수"], bins=bins, labels=[1, 2, 3, 4, 5], right=False).astype(int)
    bins = [-np.inf] + config.RATIO_CUTS + [np.inf]
    df["단계_평소대비"] = pd.cut(df["평소대비"], bins=bins, labels=[1, 2, 3, 4, 5], right=False).astype(int)
    df["최종단계"] = df[["단계_기준선", "단계_평소대비"]].max(axis=1)
    days = []
    count = 0
    for stage in df["최종단계"]:
        if stage >= 4:
            count = count + 1
        else:
            count = 0
        days.append(count)
    df["지속일수"] = days
    return df

# ===== 점수 구성표: 마지막 30일 요소 합계 =====
def make_recent_elements():
    elements = make_daily_elements(make_events())
    last_day = elements["시작일"].max() # 마지막 사건 날
    recent = elements[elements["시작일"] > last_day - pd.Timedelta(days=30)] # 최근 30일
    recent = recent.groupby(["카테고리코드", "주체국", "가중치"])[["건수", "점수"]].sum().reset_index() # 30일 동안 같은 요소 같은 나라는 하나로 합침 / 북한 미사일 등이 3일에 걸쳐 있으면 한줄로 함
    recent["요소명"] = recent["카테고리코드"].map(config.ELEMENT_NAMES)
    recent = recent.rename(columns={"카테고리코드": "요소코드"}) # 칸이름을 변경 - 화면 코드가 요소코드이기에 통일함
    return recent[["요소코드", "요소명", "주체국", "가중치", "건수", "점수"]]