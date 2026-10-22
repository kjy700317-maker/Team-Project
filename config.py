# ==========================================
# 국방 대시보드 프로젝트 전역 설정 파일 (config.py)
# ==========================================

# 1. 분석 관련 설정
HALF_LIFE_DAYS = 14          # 위험도 계산 시 적용할 반감기 (일 단위)
DEFAULT_PERIOD_MONTHS = 6    # 기본 조회 기간 (월 단위)

# 2. 데이터베이스 및 경로 설정
USE_DUMMY = True # True 더미 데이터 사용 / False 실제 SQLite(DB_PATH) 사용
DB_PATH = "data/database.db" # SQLite 데이터베이스 파일 경로

# 3. API 및 기타 설정
RAM_CUTS = [40, 60, 90, 120] # 원점수 기준선
RATIO_CUTS = [100, 150, 200, 300] # 평소대비 기준선
STAGE_NAMES = {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"} # 긴장도 5단계
STAGE_COLORS = {1: "green", 2: "blue", 3: "yellow", 4: "orange", 5: "red"} # 임시 색
SIMILAR_N = 3 # 과거 유사 시기 몇 개 보여줄지 (팀의견 확정 전)
SIMILAR_EXCLUDE_MONTHS = 12 # 최근 몇 개월은 비교해서 뺄지 (팀의견 확정 전)
# 필요한 공통 상수가 있다면 이곳에 추가하세요.