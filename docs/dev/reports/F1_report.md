# F1 보고서 — 입력 로더(io.py)·사건표 생성(build_events.py)
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-io`(develop 9e7ed0d에서) · 이슈 #16
- 커밋: `02a047d docs: F1 작업 프롬프트·설계 문서 반영` · `5ea4a99 feat: 사건표·유형판정표 로더 io.py 추가` · `2d9593a feat: 원자료에서 사건표 만드는 build_events 추가` · `b2cc494 chore: 물리사건 유형판정표 사본 추가` · `docs: F1 보고서`(이 파일)
- PR: https://github.com/kjy700317-maker/Team-Project/pull/17 (draft, 병합 안 함)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 / openpyxl 3.1.5

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | status·브랜치·origin/develop 9e7ed0d·`0 1` 모두 기대대로, 백업→develop ff→되살리기 후 상태 같음 | L1 |
| 2 | ✓ | `('사건ID', 'date', '요소', '묶음', 'S', '사건명') 8` | L5 |
| 3 | ✓ | 14 통과(스모크 3 + test_io 11) | L5 |
| 4 | ✓ | 오류 없음 · `φ 대조 통과 668` · `기본 720행 / 확장 941행 / 제외기록 177행` · 입력파일 16행, 2회 실행 `cmp` 같음 | L2 |
| 5 | ✓ | 4개 모두 `.gitignore:260 data/tension/events_*.csv` | L5 |
| 6 | ✓ | `전체: 통과` — 키·순서 동일, S 최대차 0.0, ①③④ v013과 동일, 판정표 37·Y 16·문제 0. 제외 사유별: ① 1 · ③ 129 · ④ 2 · ⑤ 18 · ⑥ 17 · ⑦ 10 | L4 |
| 7 | ✓ | `same`(커밋 blob도 원본과 바이트 같음) | L3 |
| 8 | ✓ | `정상` | L5 |
| 9 | ✓ | 두 grep 출력 없음 | L5 |
| 10 | ✓ | develop..HEAD = 8절 1~5 순서 | L6 |
| 11 | ✓ | 커밋 1~4 전 검사 모두 `OK`(보고서 커밋 전에도 실행) | L6 |
| 12 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | L6 |

## 2. 막힌 것 · 질문
없음.

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
0절 1~4 외에 판단한 곳(결과에는 영향 없음):
1. ⑥ 사유 중 표에 괄호 설명이 없는 B1·B4·F2는 조건을 설명으로 씀: `⑥ 기존 규칙: A2 동일 사건 명시` · `태세방향 완화` · `F2_연도별회담_정제.csv에 없음`.
2. `제외사유`가 빈 행은 기준(`str(nan)` → `nan`)과 달리 빈 문자열로 적음. ⑦에 `제외사유` 열이 없거나 빈 값이면 `⑦ 팀 사용여부 N`(끝 `: ` 없음).
3. ⑤·⑥·⑦ 행의 S는 점수 열 값(숫자가 아니면 빈칸). 제외기록 행 순서 = 사유 코드 → date → 사건ID.
4. "Y만" 요소에 `사용여부` 열이 없으면 멈추게 함("열 없음" 요소에 열이 생긴 경우와 짝 — 기준 `Y()`는 그냥 통과).
5. `build_events(raw_dir, start, end, files=None)` — 선택 인자 `files`를 더함(main이 찾은 파일 목록을 넘겨 입력 파일 기록과 같은 파일을 쓰게). 세 인자로 부르면 계약 그대로.
6. 콘솔(cp949)에서 한글 출력이 깨짐 — 파일 내용은 정상. 로그는 `PYTHONIOENCODING=utf-8`로 받음.
7. 제안: Git 전역 `core.autocrlf=true`이고 `.gitattributes`가 없어, 다른 Windows PC가 새로 체크아웃하면 `물리사건_유형판정표.csv`가 CRLF로 풀린다(리포 blob은 LF로 원본과 같음, 읽기는 문제없음). 바이트 동일이 필요하면 `.gitattributes`에 `data/tension/*.csv -text` 같은 규칙을 검토.

## 4. 바뀐 파일
- `utils/tension/io.py` — 사건표·유형판정표 읽기·검증, CSV 쓰기
- `tests/test_io.py` — 합성 자료 테스트 11개
- `scripts/build_events.py` — 원자료 → events_기본·확장·제외기록·입력파일(깃 제외)
- `data/tension/물리사건_유형판정표.csv` — 판정표 사본(바이트 그대로)
- `docs/decisions.md`·`docs/dev/식_함수_대응표.md`·`docs/dev/진행기록.md`·`docs/tension/산출식_정리.md`·`docs/dev/tasks/F1_io.md` — 구현 메인 문서, 내용 수정 없이 커밋
- `docs/dev/reports/F1_report.md`·`F1_log.md` — 이 보고서
- 작업트리에 남긴 변경: `?? .obsidian/`(건드리지 않음). 깃 제외 생성물 `data/tension/events_*.csv` 4개. 리포 밖 `$HOME/bongsu_F1_20261029/`(백업·검산 스크립트·출력)
