# F2-3 보고서 — F2 검토 반영: 자료 이상 멈춤 · daily_table params · run_tension 입력 검사
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-core`(이어서) · 이슈 #18
- 커밋: `6177205 docs: F2-3 작업 프롬프트·설계 문서 반영` · `8eb9002 fix: 계산 코어 자료 이상 멈춤·daily_table params` · `91fa47d fix: run_tension 입력 검사·메시지` · `docs: F2-3 보고서`(이 파일). merge 커밋 없음(develop 쪽 0 — 1-3·7절 모두)
- PR: https://github.com/kjy700317-maker/Team-Project/pull/19 (draft 유지, 본문 갱신, 병합·ready 안 함)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | status 4줄·`feature/tension-core`·ahead/behind 없음·`604f4f2 docs: F2 검토 보고서`·PR OPEN·draft·14 passed | L1 |
| 2 | ✓ | 금지 경로 `OK`, `15  0` → merge 건너뜀 | L1-2·L1-3 |
| 3 | ✓ | `git apply --check` 첫 시도 통과·적용, `--stat` = `scripts/run_tension.py`·`utils/tension/core.py` 두 파일 | L2 |
| 4 | ✓ | 공개 함수 31개(첫 줄 식 번호/`(보조)`), 3-2 grep 두 줄 모두 출력 없음 | L3 |
| 5 | ✓ | 14 passed · 도움말 `--end` 하나 | L3 |
| 6 | ✓ | `전체: 통과`(rc 0) — 값 그대로, 기본·확장 바이트까지 같음 True | L4-1 |
| 7 | ✓ | `전체: 통과`(rc 0) | L4-2 |
| 8 | ✓ | develop..HEAD = 이전 14개 + 6절 1·3·4(+ 보고서 5) | L6 |
| 9 | ✓ | 커밋 1·3·4 전 모두 `OK`(보고서 커밋 전도 확인) | L1-2·L6 |
| 10 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | (커밋 뒤 확인) |

검산 요약:
- 4-1(v0.1.4 대조): 일별 기본·확장 BOM·LF·6145줄, 허용 밖 다른 칸 0, 글자까지 다른 칸 0, 기준 CSV와 바이트까지 같음 True — 이번 패치로 값이 바뀌지 않음. T 구간 확장 110/237/314/374
- 4-2 [1] 자료 이상 멈춤: core 11경우 모두 기대 예외(ValueError 9 — 이른 END·늦은 시작·tension_components 직접·완화 0건·핵·미사일 0건·사건 0행·θ₁ = 0·사망 사건 없음·판정표 Y 사건 없음 / TypeError 2 — type4_ids·kill_ids 문자열). END 2019-12-31은 3652일 계산, 빈 type4 집합은 core에서 허용
- 4-2 [2] params: `PARAM_KEYS` 20개 = 검산 키, None·{}·config 값 → 기본과 같음, 모르는 키 ValueError, 20키 각각 기대 열이 바뀌고 열 이름·순서 그대로, relief_c·sigma·window가 개별 함수 호출과 같음
- 4-2 [3] run_tension: 이른 END rc 1 · 형식·없는 날짜 4경우 rc 2 · cp949에서 UnicodeEncodeError 없음 · 멈춘 실행은 `_check` 파일 안 씀 · 사건표 없음 rc 1 · 정상 rc 0, Traceback 없음

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
1. 패치·검산 파일은 손으로 옮겨 적지 않고 프롬프트 파일의 코드 블록을 파이썬으로 잘라 저장했다(`$B/extract.py` — 줄 수가 프롬프트 범위와 같음을 확인). 내용은 글자 그대로.
2. 1-3에서 develop 쪽 0이라 merge·pytest 재실행을 건너뜀(프롬프트대로). 7절 fetch 뒤에도 0이라 merge 안 함, pytest 14 passed 후 push.
3. PR 본문 "변경 사항"에는 프롬프트대로 6절 3·4 커밋만 더했다(이전 본문은 docs 커밋도 적어 왔지만 F2-3 docs 커밋 줄은 넣지 않음). 첫 편집에서 멈춤 경우 수를 12로 잘못 적어 바로 11로 고쳐 다시 편집했다.
4. 의견(고치지 않음): 4-2의 "사건표 없음" 확인은 `config.TENSION_DATA_DIR`를 바꾸지만 `run_tension.OUT_DIR`는 import 때 묶여 정상 경로 그대로다 — 멈춤이 먼저라 지금은 문제없음. F3 테스트로 옮길 때 참고.

## 4. 바뀐 파일
- `utils/tension/core.py` — 부록 C 그대로: `_require_full_base`·`_require_ids`·`_pick`·`PARAM_KEYS`, `tension_components`·`type4_days`·`floor_physical`·`floor_e5`·`daily_table`·`relief_discount` docstring
- `scripts/run_tension.py` — 부록 C 그대로: `_end_date`·`_run`·`main`(멈춤 메시지·`errors="replace"`)
- `docs/dev/tasks/F2-3_fix.md`·`docs/dev/진행기록.md`·`docs/tension/산출식_정리.md` — 구현 메인 문서, 내용 수정 없이 커밋
- `docs/dev/reports/F2-3_report.md`·`F2-3_log.md` — 이 보고서
- 작업트리에 남긴 것: `?? .obsidian/`(건드리지 않음) · `data/tension/_check/일별_*.csv`(깃 제외 — 4-1·4-2 정상 실행이 다시 씀). 리포 밖 `$HOME/bongsu_F2-3_20261029/`(패치·검산·추출 스크립트, 출력, PR 본문 이전·이후)
