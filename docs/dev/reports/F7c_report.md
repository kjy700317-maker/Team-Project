# F7c 보고서 — 옛 임시 계산 통로·더미 모드·config 임시값 정리
- 결과: 완료
- 2026-10-30 · feature/tension-cleanup · 이슈 #34 · 커밋 5개(docs 반영 / refactor 통로 / refactor config / test / docs README) + 보고서 · PR [#35](https://github.com/kjy700317-maker/Team-Project/pull/35) (draft, 병합 안 함)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 (plotly 7.1.0, streamlit 1.65.0, autocrlf=true)

## 1. 완료 조건
| # | ✓/✗ | 근거 (log) |
|---|---|---|
| 1 | ✓ | PR #33 MERGED, 훅 있음, 117 passed, md5 4개 같음 (L1) |
| 2 | ✓ | 브랜치 feature/tension-cleanup, 이슈 #34 (L1) |
| 3 | ✓ | 패치·스크립트 md5, real.py 전후 md5, hash 5개, grep 기대대로 (L2) |
| 4 | ✓ | 117 passed · 100/17 · FutureWarning 12 passed (L2) |
| 5 | ✓ | 결과 CSV 7개 cmp 같음, data/ 변경 없음 (L2) |
| 6 | ✓ | load_events 3882행, 옛 load_* 없음, config 5개 없음 (L2) |
| 7 | ✓ | 커밋 2~5 --cached --stat 기대와 같음, ls-tree hash 같음 (L3) |
| 8 | ✓ | 금지 경로 검사 매번 OK (L3) |
| 9 | ✓ | 이슈·커밋·PR 본문 AI 표기 없음 (L4) |
| 10 | ✓ | 마지막 status `?? .obsidian/` 하나 (L3) |

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
없음 (프롬프트 그대로). 참고: `홈.py` 4행 주석의 `load_daily`는 화면 파일이라 그대로 둠.

## 4. 바뀐 파일
- `utils/dummy.py` 삭제 · `utils/real.py` 사건 표 함수만 남김 · `utils/loader.py` 옛 통로 4개 삭제
- `config.py` 임시값 5개 삭제·절 제목 정리 · `tests/test_screen.py` 96행 검사 수정 · `README.md` 폴더 구조 3줄
- `docs/dev/` 구현 메인 문서 5개(내용 수정 없이 커밋) · 보고서 2개
- 작업트리에 남긴 변경: `.obsidian/`(미추적)
