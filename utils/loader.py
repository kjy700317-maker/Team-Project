import config
from utils.dummy import make_daily, make_monthly, make_elements # 쉼표로 여러 개를 한 번에 가져올 수 있음

# ===== 테이블 통로 =====
def load_daily():
    if config.USE_DUMMY: # 스위치가 True면 아래 줄을 실행
        return make_daily() # 더미 자판기에서 받은 표를 그대로 넘겨줌
    else:
        raise NotImplementedError("테이블 아직 실제 DB 연결을 하지 않음") # 일부러 에러를 내는 명령 실제 데이터가 아직 넣지 않았기에 사전에 공지하는 용도

# ===== 월별 표 통로 =====
def load_monthly():
    if config.USE_DUMMY:
        return make_monthly(make_daily()) # 더미 일별 표를 만들어서 월별로 묶어 알려줌
    else:
        raise NotImplementedError("월별 표 아직 실제 DB 연결을 하지 않음")

# ===== 점수구성 통로 =====
def load_elements():
    if config.USE_DUMMY:
        return make_elements()
    else:
        raise NotImplementedError("점수 아직 실제 DB 연결을 하지 않음")