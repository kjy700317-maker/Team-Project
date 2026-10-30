# F8 보고서 — 가정 바꿔 보기(슬라이더 재계산): 묶음 비중 ω + 재계산 통로
- 결과: 완료
- 날짜 2026-10-30 · 브랜치 feature/tension-slider · 이슈 #36 · 커밋 9400887 docs 문서 반영 / 0985f75 feat 재계산 통로 / 783283c test / 4463759 docs README (+ 보고서 커밋) · PR: https://github.com/kjy700317-maker/Team-Project/pull/37 (draft)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | PR 35 MERGED, 훅 있음, 117 passed, md5 6개 같음 | L1 |
| 2 | ✓ | feature/tension-slider, 이슈 #36 | L1 |
| 3 | ✓ | 패치 md5·hash 6개 같음, 5 files · 138 ins · 14 del | L2 |
| 4 | ✓ | 137 passed · 120/17 · FutureWarning 32 passed | L2 |
| 5 | ✓ | 결과 7개 cmp 같음, data/ 변경 없음 | L2 |
| 6 | ✓ | 100.0 / 111·251·302·342 90.8 / 50·25·25 116·267·330·392 83.0 98.4, 비교 표 20행 | L2 |
| 7 | ✓ | 커밋 5개(보고서 포함) | L3 |
| 8 | ✓ | 금지 경로 검사 매번 OK | L3 |
| 9 | ✓ | 이슈·커밋 AI 표기 OK (PR 본문은 생성 시 검사) | L1·L3 |
| 10 | ✓ | status `?? .obsidian/` 하나 | L3 |

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
없음 (패치 그대로 적용)

## 4. 바뀐 파일
- config.py · utils/tension/core.py · utils/tension/screen.py · utils/loader.py · tests/test_recompute.py(새) · README.md — 부록 A 패치
- 문서 7개(decisions, 진행기록, 대응표, 산출식, 변경이력, 운영, F8 프롬프트) — 내용 수정 없이 커밋 1
- docs/dev/reports/F8_report.md · F8_log.md
- 작업트리에 남긴 변경: `?? .obsidian/`
