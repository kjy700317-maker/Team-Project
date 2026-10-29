# F3 보고서 — 테스트: 단위(test_core) · v0.1.4 회귀(test_regression) · 기준 파일(fixtures)
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-tests`(develop `041dda5`에서) · 이슈 #20
- 커밋: `11916c8` docs: F3 작업 프롬프트·설계 문서 반영 / `39eb14b` docs: CLAUDE.md AI 표기 금지 규칙 / `0f85a43` test: v0.1.4 회귀 기준 파일(fixtures) / `35647c9` test: 계산 코어 단위 테스트(test_core) / `d0411af` test: v0.1.4 회귀 테스트·regression 표시 / (이 파일) docs: F3 보고서
- PR: https://github.com/kjy700317-maker/Team-Project/pull/21 (draft, 병합하지 않음)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 (pytest 9.0.3)

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | PR #19 MERGED, `feature/tension-tests` 새로, 이슈 #20, 14 passed | L1 |
| 2 | ✓ | 일별 2개 `cmp` 같음, 요약 `완화 상한에 붙은 날,272,272`, 세 CSV `i/lf w/lf attr/text eol=lf` | L2 |
| 3 | ✓ | pytest.ini diff는 markers 두 줄 +만, test_core 33 passed | L3 |
| 4 | ✓ | test_regression 14 passed | L4 |
| 5 | ✓ | 전체 61 passed · not regression 47 passed/14 deselected · `-W error::FutureWarning` 61 passed | L4 |
| 6 | ✓ | 사건표 치움 → 1 failed + 13 skipped, 메시지에 없는 파일·만드는 법·빼는 법. 되돌린 뒤 61 passed | L4 |
| 7 | ✓ | 커밋 1~6이 8절 순서대로 | L8 |
| 8 | ✓ | 커밋 1~6 전 금지 경로 검사 모두 OK | L1~L4 |
| 9 | ✓ | 마지막 status `?? .obsidian/` 하나만 | L6 |
| 10 | ✓ | 시험 메시지에서 AI 표기 줄 지워짐, 커밋 1 메시지 표기 없음(설치 과정은 2절) | L1-4 |
| 11 | ✓ | CLAUDE.md `1 file changed, 1 insertion(+)` | L1-5 |
| 12 | ✓ | PR #15·#17 본문 모두 OK | L1-6 |
| 13 | ✓ | 이슈 본문·커밋 메시지 전부(`origin/develop..HEAD`)·PR 본문 파일·올라간 PR 본문 모두 OK | L1-3, L8 |

테스트 수: 기존 14 + test_core 33 + test_regression 14 = **61 passed**. 구현 메인 확인 환경(pandas 2.3.3)과 달리 pandas 3.0.6에서도 결과는 기대와 같았다.

## 2. 막힌 것 · 질문
- 1-4 훅 설치(`.git/hooks/commit-msg`)를 Claude Code 자동 모드 안전 검사가 처음에 "Unauthorized Persistence"로 거부했다. 커밋 전 작업까지 하고 멈춘 뒤, 사용자가 채팅에서 허락해 다시 실행했고 설치됐다(부록 F와 `cmp` 같음). 커밋은 모두 훅 설치 뒤에 했다. 다음 프롬프트에 `.git/hooks` 쓰기가 있으면 사용자 허락을 미리 받아 두면 멈추지 않는다.
- 그 밖에는 없음.

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
- 프롬프트와 다른 점: 1-6에서 `clean_pr_body.py`가 지운 줄은 PR마다 3개였다(기대 1~2개). AI 표기 줄 앞 빈 줄과 `gh -q`가 붙인 끝 빈 줄까지 센 것이고, diff상 빠진 것은 표기 줄과 빈 줄뿐이다(L1-6).
- 2절 `git add tests/fixtures/`는 커밋 1·2에 섞이지 않게 커밋 3 직전에 했다(순서만 다름).
- 부록 파일은 모두 `$B/extract.py`로 프롬프트 코드 블록을 바이트 그대로 잘라 저장했다(줄 수는 L3).
- 고치고 싶은 것: 없음.

## 4. 바뀐 파일
- `docs/dev/tasks/F3_tests.md` · `docs/dev/진행기록.md` — 구현 메인 문서, 내용 수정 없이 커밋(U2)
- `CLAUDE.md` — 6절에 AI 표기 금지 규칙 1줄
- `tests/fixtures/v014_일별_기본.csv` · `v014_일별_확장.csv` · `v014_요약.csv` · `README.md` — v0.1.4 회귀 기준
- `pytest.ini` — `markers`에 `regression`
- `tests/test_core.py` — 단위 테스트 33개
- `tests/test_regression.py` — 회귀 테스트 14개
- `docs/dev/reports/F3_report.md` · `F3_log.md` — 이 보고서
- 리포 밖: `.git/hooks/commit-msg`(로컬, 커밋 안 함), PR #15·#17 본문(AI 표기 줄 삭제)
- 작업트리에 남긴 변경: `?? .obsidian/`(내가 만들지 않음, 건드리지 않음)
