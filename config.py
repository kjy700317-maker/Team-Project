# ==========================================
# 🛡️ 국방 대시보드 프로젝트 전역 설정 파일 (config.py)
# ==========================================

# 1. 분석 관련 설정
HALF_LIFE_DAYS = 14          # 긴장도 감쇠 반감기 (일) — ADR-006
DEFAULT_PERIOD_MONTHS = 6    # 기본 조회 기간 (월 단위)

# 2. 데이터베이스 및 경로 설정
DB_PATH = "data/database.db" # SQLite 데이터베이스 파일 경로

# 3. API 및 기타 설정
# 필요한 공통 상수가 있다면 이곳에 추가하세요.

# 4. 긴장도 계산 파라미터 (utils/tension) — 값의 근거는 docs/decisions.md ADR 번호
#    함수는 이 값을 인자 기본값으로만 쓴다. 값을 바꾸면 모델 버전을 올리고 ADR에 기록한다.
TENSION_MODEL_VERSION = "v0.1.4"                 # ADR-018 확정판
CALC_START_DATE = "2010-01-01"                   # 계산 시작일(R 시작값 0)
END_DATE = None                                  # U3(10-28): None = 실행일. 회귀 검산은 "2026-10-27"로 넘겨 호출
BASE_PERIOD = (2010, 2019)                       # ADR-003 기준기간(평소값·T 구간)
BUNDLES_BASE = ("핵·미사일", "군사 과시", "위협 언어·교리")   # ADR-010 상승 묶음(기본) — s3_core.py 6행 UP3
BUNDLES_EXT = BUNDLES_BASE + ("제재·압박",)                # ADR-013 확장 시나리오 — compute_v014.py 63행
BUNDLE_RELIEF = "완화"                            # ADR-008·009 (F2만)
BUNDLE_PHYS = "물리 충돌"                          # ADR-007
BUNDLE_E5 = "북러 밀착"                            # ADR-014 (하한 대상 행만; "북러(표시만)"은 계산 제외)
STAGE_QUANTILES = (0.70, 0.90, 0.95, 0.98)       # ADR-018 2·3·4·5거 시작 분위(반올림 정수로 판정)
RELIEF_C = 0.1                                   # ADR-008 완화 세기 c
RELIEF_CAP = 0.5                                 # ADR-008 완화 상한 κ
F2_FIELD_FACTOR = {"정치·군사": 1.0, "경제·인도": 0.2, "사회문화": 0.2}  # ADR-015 — 사건표 생성 때 S에 곱함(core는 안 씀)
HALF_GAUSS_SIGMA = 10                            # ADR-006·014 전용 하한 원점수 exp(-k²/(2σ²))
FLOOR_WINDOW = 30                                # ADR-006·014 전용 하한 창(일)
PHYS_FLOOR = {"3거": 3, "4거": 7, "풍선3거": 6}   # ADR-007 풍선 뺀 A3·A7: ρ≥3 → 3거, ρ≥7 → 4거 / 오물풍선(A3, 사건명 Balloon): ρ≥6 → 3거
TYPE4_FLOOR_STAGE = 4                            # ADR-007 1-1 4거 유형 사건 당일
KILL_EVENTS = ("A7-0098", "A7-0100")             # ADR-007 사망·침몰 당일 5거(천안함·연평도)
KILL_FLOOR_STAGE = 5
E5_FLOOR = {"3거": 4, "4거": 10}                  # ADR-014 E5: ρ≥4 → 3거, ρ≥10 → 4거
EVENT_FLOOR_ICBM_S = 7.5                         # ADR-018 사건 하한: A1 또는 A2 S≥7.5(ICBM) 당일
EVENT_FLOOR_STAGE = 3
STEP_DOWN_DAYS = 7                               # ADR-006 하강: 더 낮은 판정 7일 → 한 단계
DISPLAY_MA_DAYS = 7                              # ADR-006 표시선 = 7일 후행 이동평균
PROVISIONAL_DAYS = 6                             # ADR-006 최근 6일 "잠정"
TREND_DAYS = 14                                  # U11 10-28 확정 — 14일 변화
TREND_PCT_MIN = 50                               # U11 10-28 확정 — 14일 전 표시값 50 미만이면 % 숨김
A2_DATA_END = "2024-11-05"                       # ADR-011a(A2 항목) 안 10-27 사용자 결정 — A2 자료 마지막 날(이후 "자료 없음" 표시)
CRISIS_LIST = (                                  # 내부 위기 목록 10건(검산·게이지 눈금용) — s3_core.py 9~11행 CR과 같음 [확인]
    ("천안함", "2010-03-26", "물리"),
    ("연평도", "2010-11-23", "물리"),
    ("3차 핵", "2013-02-12", "상승"),
    ("목함지뢰", "2015-08-04", "물리"),
    ("4차 핵", "2016-01-06", "상승"),
    ("6차 핵", "2017-09-03", "상승"),
    ("판문점 정상회담", "2018-04-27", "완화"),
    ("2022-11 집중발사", "2022-11-02", "상승"),
    ("2024-06 북러조약", "2024-06-19", "북러"),
    ("2026-09 DMZ 지뢰", "2026-09-21", "물리"),
)
CRISIS_WINDOW_DAYS = 14                          # 위기 단계·게이지 눈금 = 위기일부터 14일 안 최댓값
TENSION_DATA_DIR = "data/tension"                # 결과 CSV 폴더(커밋)
TYPE4_TABLE_PATH = "data/tension/물리사건_유형판정표.csv"   # 유형판정표 사본(F1에서 복사, 커밋)
