# F3 실행 로그

python = `C:/Users/money/anaconda3/envs/python311/python.exe`(아래 `<py>`), 모든 python 명령 앞 `PYTHONIOENCODING=utf-8`. `$B` = `$HOME/bongsu_F3_20261029`.
부록 A·B·C·D·E·F·G·H는 `$B/extract.py`(프롬프트의 `## 부록 X.` 다음 첫 코드 블록을 바이트 그대로 저장)로 잘라 저장했다.

## L1 시작 점검 · develop 최신화 · 브랜치 · 이슈

```
$ git status --porcelain
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F3_tests.md
$ git branch --show-current
feature/tension-core
$ gh pr view 19 --json state,mergedAt
{"mergedAt":"2026-10-29T05:08:19Z","state":"MERGED"}
$ git log --oneline -1 origin/develop
041dda5 Merge pull request #19 from kjy700317-maker/feature/tension-core
```

### L1-1·1-2 백업 → develop → 되살리기 → 브랜치
```
(백업: $B/docs/docs/dev/진행기록.md 27391 B, $B/docs/docs/dev/tasks/F3_tests.md 38792 B)
$ git restore docs/dev/진행기록.md && git switch develop && git pull --ff-only origin develop
Switched to branch 'develop'
Your branch is behind 'origin/develop' by 19 commits, and can be fast-forwarded.
Updating 869cfcb..041dda5
Fast-forward
 19 files changed, 3750 insertions(+), 9 deletions(-)
$ git log --oneline -1
041dda5 Merge pull request #19 from kjy700317-maker/feature/tension-core
(되살린 뒤) $ git status --porcelain
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F3_tests.md
$ git switch -c feature/tension-tests
Switched to a new branch 'feature/tension-tests'
```

### L1-3 이슈 · 환경 · 테스트
```
$ grep -inE "$AI" "$B/issue_F3.md" ... → OK
$ gh issue create --title "[FEAT] 긴장도 단위·회귀 테스트(F3)" --label feat --body-file "$B/issue_F3.md"
https://github.com/kjy700317-maker/Team-Project/issues/20
$ <py> --version
Python 3.11.17
$ <py> -c "import numpy, pandas, pytest; ..."
2.4.6 3.0.6 9.0.3
$ <py> -m pytest
14 passed in 1.31s
$ ls -la data/tension/events_기본.csv data/tension/events_확장.csv
-rw-r--r-- 1 money 197613 65462 Oct 29 01:59 data/tension/events_기본.csv
-rw-r--r-- 1 money 197613 84633 Oct 29 01:59 data/tension/events_확장.csv
```

### L1-4 commit-msg 훅
```
$ <py> $B/extract.py docs/dev/tasks/F3_tests.md F $B/appendix_F
부록 F → .../appendix_F: 9줄 398바이트
$ cp "$B/appendix_F" .git/hooks/commit-msg && chmod +x ...
→ 처음 시도는 Claude Code 자동 모드 안전 검사가 거부("Unauthorized Persistence").
  사용자가 채팅에서 "네가 할 수 있으면 네가 해"라고 허락한 뒤 다시 실행해 설치.
-rwxr-xr-x 1 money 197613 398 Oct 29 14:21 .git/hooks/commit-msg
부록 F와 같음 (cmp)
$ sh .git/hooks/commit-msg "$B/msg_test.txt" && cat "$B/msg_test.txt"
docs: 시험

본문

[끝]
$ git status --porcelain → 1절 첫 기대와 같음(훅은 .git 안)
```
커밋 1 `11916c8 docs: F3 작업 프롬프트·설계 문서 반영` — 금지 경로 검사 OK, `git log -1 --format=%B | grep -inE "$AI"` → 없음(OK).
```
 docs/dev/tasks/F3_tests.md  | 701 +++
 docs/dev/진행기록.md         |  15 +-
 2 files changed, 713 insertions(+), 3 deletions(-)
```

### L1-5 CLAUDE.md
```
$ <py> "$B/add_no_ai_rule.py"
CLAUDE.md: 6절에 AI 표기 금지 규칙 1줄 넣음
$ git diff --stat CLAUDE.md
 CLAUDE.md | 1 +
 1 file changed, 1 insertion(+)
```
커밋 2 `39eb14b docs: CLAUDE.md AI 표기 금지 규칙` — 금지 경로 검사 OK.

### L1-6 PR #15·#17 본문
```
지운 줄 3개(끝 빈 줄 포함) → .../pr15_new.md
== diff #15
28,30d27
<
< 🤖 Generated with [Claude Code](https://claude.com/claude-code)
<
지운 줄 3개(끝 빈 줄 포함) → .../pr17_new.md
== diff #17
24,26d23
<
< 🤖 Generated with [Claude Code](https://claude.com/claude-code)
<
$ gh pr edit 15 --body-file ... → https://github.com/kjy700317-maker/Team-Project/pull/15
#15 OK
$ gh pr edit 17 --body-file ... → https://github.com/kjy700317-maker/Team-Project/pull/17
#17 OK
```
(기대 "지운 줄 1~2개"와 달리 3개 — AI 표기 줄 앞 빈 줄 + 표기 줄 + `gh -q`가 붙인 끝 빈 줄. diff상 표기 줄과 빈 줄만 빠짐.)

## L2 기준 파일
```
$ <py> "$B/make_fixtures.py"
v014_요약.csv 2051 바이트
v014_일별_기본.csv 709627 바이트
v014_일별_확장.csv 754704 바이트
부록 B → tests/fixtures/README.md: 6줄 910바이트
$ cmp ...
기본 같음
확장 같음
$ grep "완화 상한" tests/fixtures/v014_요약.csv
완화 상한에 붙은 날,272,272
$ git add tests/fixtures/ && git ls-files --eol tests/fixtures/*.csv
i/lf    w/lf    attr/text eol=lf      	tests/fixtures/v014_요약.csv
i/lf    w/lf    attr/text eol=lf      	tests/fixtures/v014_일별_기본.csv
i/lf    w/lf    attr/text eol=lf      	tests/fixtures/v014_일별_확장.csv
 tests/fixtures/README.md          |    6 +
 tests/fixtures/v014_요약.csv       |   62 +
 tests/fixtures/v014_일별_기본.csv  | 6145 +++
 tests/fixtures/v014_일별_확장.csv  | 6145 +++
 4 files changed, 12358 insertions(+)
```
(`git add`는 커밋 1·2를 섞지 않으려고 커밋 3 직전에 했다.) 커밋 3 `0f85a43 test: v0.1.4 회귀 기준 파일(fixtures)` — 금지 경로 검사 OK.

## L3 테스트 파일
```
부록 C → pytest.ini: 6줄 199바이트
부록 D → tests/test_core.py: 255줄 10588바이트
부록 E → tests/test_regression.py: 185줄 9269바이트
$ git diff pytest.ini | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '
warning: in the working copy of 'pytest.ini', LF will be replaced by CRLF the next time Git touches it
+markers =
+    regression: v0.1.4 회귀 — 로컬 사건표(data/tension/events_*.csv) 필요, 없으면 실패. 빼려면 -m "not regression"
$ git ls-files --eol pytest.ini
i/lf    w/lf    attr/                 	pytest.ini      (core.autocrlf=true)
$ <py> -m pytest tests/test_core.py
33 passed in 1.66s
```
커밋 4 `35647c9 test: 계산 코어 단위 테스트(test_core)` — 금지 경로 검사 OK.

## L4 회귀 · 전체 · 사건표 없음
```
$ <py> -m pytest tests/test_regression.py
14 passed in 3.69s
$ <py> -m pytest
61 passed in 4.58s
$ <py> -m pytest -m "not regression"
47 passed, 14 deselected in 1.75s
$ mv data/tension/events_기본.csv "$B/"
$ <py> -m pytest tests/test_regression.py -rs
Fsssssssssssss                                                           [100%]
================================== FAILURES ===================================
_____________________________ test_events_present _____________________________
회귀 테스트 입력 사건표가 없다: ['data/tension/events_기본.csv']
  사건표는 깃에 올리지 않는다(D1). 원자료 data/raw/긴장도_산출식_세부_기준/ : 있음
  만들기: python scripts/build_events.py --end 2026-10-27  → 그다음 pytest 다시
  회귀만 빼고 돌리기: python -m pytest -m "not regression"
=========================== short test summary info ===========================
SKIPPED [2] tests\test_regression.py:130: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [2] tests\test_regression.py:137: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [2] tests\test_regression.py:145: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [2] tests\test_regression.py:151: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [2] tests\test_regression.py:159: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [2] tests\test_regression.py:168: 사건표 없음 — test_events_present의 실패 메시지 참고
SKIPPED [1] tests\test_regression.py:176: 사건표 없음 — test_events_present의 실패 메시지 참고
1 failed, 13 skipped in 1.18s
$ mv "$B/events_기본.csv" data/tension/
-rw-r--r-- 1 money 197613 65462 Oct 29 01:59 data/tension/events_기본.csv
$ <py> -m pytest
61 passed in 4.35s
$ <py> -W error::FutureWarning -m pytest
61 passed in 4.35s
$ git check-ignore -v data/tension/_check/일별_기본.csv
.gitignore:262:data/tension/_*	data/tension/_check/일별_기본.csv
```
커밋 5 `d0411af test: v0.1.4 회귀 테스트·regression 표시` — `pytest.ini | 2 +`, `tests/test_regression.py | 185 +`, 금지 경로 검사 OK.

## L6 확인 명령
```
$ git diff --stat origin/develop...HEAD -- tests pytest.ini
 pytest.ini                        |    2 +
 tests/fixtures/README.md          |    6 +
 tests/fixtures/v014_요약.csv       |   62 +
 tests/fixtures/v014_일별_기본.csv  | 6145 +++
 tests/fixtures/v014_일별_확장.csv  | 6145 +++
 tests/test_core.py                |  255 +
 tests/test_regression.py          |  185 +
 7 files changed, 12800 insertions(+)
$ git status --porcelain
?? .obsidian/
```

## L8 커밋 · 푸시 · PR
```
$ git log --oneline -5
d0411af test: v0.1.4 회귀 테스트·regression 표시
35647c9 test: 계산 코어 단위 테스트(test_core)
0f85a43 test: v0.1.4 회귀 기준 파일(fixtures)
39eb14b docs: CLAUDE.md AI 표기 금지 규칙
11916c8 docs: F3 작업 프롬프트·설계 문서 반영
$ git fetch origin && git merge origin/develop
Already up to date.
$ <py> -m pytest
61 passed in 3.91s
$ git log --format=%B origin/develop..HEAD | grep -inE "$AI" → OK
$ git push -u origin feature/tension-tests
 * [new branch]      feature/tension-tests -> feature/tension-tests
branch 'feature/tension-tests' set up to track 'origin/feature/tension-tests'.
$ grep -inE "$AI" "$B/pr_F3.md" → OK
$ gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 단위·회귀 테스트(F3)" --body-file "$B/pr_F3.md"
Warning: 1 uncommitted change
https://github.com/kjy700317-maker/Team-Project/pull/21
$ gh pr view --json body -q .body | grep -inE "$AI" → OK
```
("1 uncommitted change" = `.obsidian/` 미추적 폴더.)
