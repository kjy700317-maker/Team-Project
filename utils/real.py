import pandas as pd
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
