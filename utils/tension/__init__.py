"""봉수 긴장도 계산 패키지 (v0.1.4 이식).

모듈(예정):
    io      — 사건표·유형판정표·결과 CSV 로드와 검증 (F1)
    core    — 산출식 ①~⑰, 순수 함수 (F2)
    charts  — Plotly 그림 (F4)

규칙의 근거는 docs/decisions.md(ADR), 수식은 docs/tension/산출식_정리.md 1A절.
파라미터 값은 config.py에 있고, 함수는 인자로 받는다.
"""

__all__: list[str] = []
