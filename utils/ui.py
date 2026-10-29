import config

# ===== [수정] 5단계 눈금 (홈·보고서가 같이 씀, 두 곳에 있던 코드를 여기로 모음) =====
def stage_scale(stage):   # 지금 단계 번호를 받아 눈금 5칸 HTML을 돌려줌
    scale = ""                                          # 칸 5개를 이어 붙일 빈 글
    for no, name in config.STAGE_NAMES.items():         # .items(): (번호, 이름)을 같이 꺼냄
        if no == stage:                                 # 지금 단계: 진한 색 + 흰 글씨 + 굵게
            bg, text, weight = config.STAGE_COLORS[no], "white", 700
        else:                                           # 나머지: 연한 색(뒤에 "40" = 투명도 25%) + 회색 글씨
            bg, text, weight = config.STAGE_COLORS[no] + "40", "#555", 400
        scale += (f"<div style='flex:1; background:{bg}; color:{text}; font-weight:{weight}; "
                  f"text-align:center; padding:6px 0; font-size:13px; border-radius:6px;'>{no} {name}</div>")
    return f"<div style='display:flex; gap:4px; margin-top:8px;'>{scale}</div>"   # flex: 칸을 가로로 나란히
