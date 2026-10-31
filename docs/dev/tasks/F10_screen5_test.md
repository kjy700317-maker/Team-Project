# F10 작업 프롬프트 — 화면 AppTest에 5페이지(가정 바꿔 보기) 추가 + 단계 6 문서 반영

작성 2026-10-31 · 구현 메인(채팅 ⑨) → Claude Code · 브랜치 **`feature/tension-screen5-test`(최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행** — 이 세션은 PR을 draft로 올리고 병합하지 않는다(병합은 사용자 몫)
권장 모델·노력: **Sonnet 5.5 · 중간**(정해진 한 줄 수정 + 문서를 그대로 커밋 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F10_20261031`(리포 밖 작업 폴더).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 검사한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **바꾸는 코드는 `tests/test_app_smoke.py` 한 파일, 두 줄뿐이다**(2절 커밋 2의 파이썬으로만). 그 밖의 코드(`utils/`·`scripts/`·`config.py`·`홈.py`·`pages/`)·`data/`·`README.md`는 한 줄도 바꾸지 않는다. 화면 파일(`홈.py`·`pages/`)은 박성인 님 담당 — 5페이지가 AppTest에서 실패하면 고치지 말고 멈추고 보고.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`·`git rm`(지울 일은 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, `.obsidian/` 스테이징, 아래 문서 3개의 **내용 수정**(CLAUDE.md 3·6절 U2 — 고치지 않고 그대로 커밋), `git commit <경로>` 꼴(항상 `git add <경로>` 뒤 `git commit -m`).

---

## 0. 목표
- 박성인 님 PR #41(develop `754cf80`)로 새 화면 `pages/5_가정_바꿔보기.py`가 들어왔다. 화면 AppTest(`tests/test_app_smoke.py`)의 `SCREENS`에 이 페이지를 넣어, 앞으로 계산 통로(`load_tension_recompute`)나 화면이 바뀌어도 5페이지가 예외 없이 뜨는지 테스트가 잡게 한다(테스트 파일은 우리 몫).
- 같은 PR로, 작업트리에 커밋 안 된 채 남은 구현 메인 문서를 **내용 그대로** 올린다.
- 올리는 파일:
  | 파일 | 작업트리 상태 | 내용 |
  |---|---|---|
  | `docs/dev/진행기록.md` | ` M` | 10-30 F9 검토 뒤 행 ~ 10-31 채팅 ⑨ 행(PR #41 확인 등) |
  | `docs/dev/지시서_구현_메인_채팅9.md` | `??` | 채팅 ⑨ 인계 지시서 |
  | `docs/dev/tasks/F10_screen5_test.md` | `??` | 이 프롬프트 |
  | `tests/test_app_smoke.py` | (커밋 2에서 수정) | docstring 1줄 + `SCREENS`에 5페이지 |
- **결과 CSV·계산 코드는 바뀌지 않는다.** 테스트는 137 → **138 passed**(새 AppTest 1개), not regression 120 → **121**, regression 17 그대로.

## 1. 시작 점검 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F10_20261031"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git -c core.quotepath=off status --porcelain
#   기대(순서 무관):
#     " M docs/dev/진행기록.md" "?? docs/dev/지시서_구현_메인_채팅9.md" "?? docs/dev/tasks/F10_screen5_test.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 3절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: develop (그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git config --get core.autocrlf                     # log에 남김(true 예상)
git fetch origin
git log --oneline -3 origin/develop                # 기대: 맨 위 754cf80 (PR #41 병합)
git log --oneline -1                               # 기대: 0a83fbd (PC develop은 #41 병합 전) — 754cf80이면 1-2 건너뜀
gh pr list --state open --json number,title,headRefName,author   # log에 남김(판단 없이)

# 1-1 구현 메인 문서 백업(리포 밖) → md5 확인
DOCS="docs/dev/진행기록.md docs/dev/지시서_구현_메인_채팅9.md"
for f in $DOCS docs/dev/tasks/F10_screen5_test.md; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표 (다르면 멈추고 보고)
```
1-1 `md5sum` 기대 — 줄바꿈은 CRLF/LF 어느 쪽이든 **`tr -d '\r' < 파일 | md5sum`**으로 같게 본다(아래 값은 CR을 뺀 md5):
```
6a1101c3e5ef1f3d040e602d1746df59  docs/dev/진행기록.md
976744717f034547ad66472f46588285  docs/dev/지시서_구현_메인_채팅9.md
```
(이 프롬프트 자신은 md5를 적지 않는다.)

```bash
# 1-2 HEAD가 origin/develop(754cf80)보다 뒤에 있을 때만:
git -c core.quotepath=off diff --name-only HEAD origin/develop     # log에 남김. 기대: 화면 6개(홈.py · pages/1·2·4·5 · utils/ui.py)
#   위 목록에 docs/ 또는 tests/ 경로가 있으면 → 멈추고 보고(구현 메인이 다시 맞춘다)
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # 기대: 754cf80
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 1-1 표와 같아야 함
git -c core.quotepath=off status --porcelain       # 맨 위 기대와 같아야 함
git rev-parse HEAD:tests/test_app_smoke.py         # 기대: 2843a965014dd70b1310e4262b401f91050b4e46
git switch -c feature/tension-screen5-test
# 1-3 이슈: 본문 "$B/issue_F10.md" = .github/ISSUE_TEMPLATE/feature.md 양식
#   (배경 = 0절 첫 줄 · 범위 = 0절 표 4개 파일, 하지 않는 것 = 화면·계산 코드·데이터·README · 완료 조건 = 4절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F10.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[CHORE] 화면 AppTest에 가정 바꿔 보기 페이지 추가 · 단계 6 문서 반영(F10)" --label chore --body-file "$B/issue_F10.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 137 passed (수정 전)
```

## 2. 커밋
금지 경로 검사(각 커밋 전):
```bash
git -c core.quotepath=off diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F10 작업 프롬프트·설계 문서 반영` — 세 경로를 하나씩 적어 `git add`(와일드카드·`git add .`·`-A` 금지)
   ```bash
   git add docs/dev/진행기록.md docs/dev/지시서_구현_메인_채팅9.md docs/dev/tasks/F10_screen5_test.md
   git -c core.quotepath=off diff --cached --stat     # 기대: 정확히 3 files (.obsidian·코드·data 없음)
   ```
   금지 경로 검사 `OK` 뒤 `git commit -m "docs: F10 작업 프롬프트·설계 문서 반영"`. 커밋 뒤 확인:
   ```bash
   git log -1 --format=%B | grep -inE "$AI" && echo "AI 표기 있음 — 멈추고 보고" || echo "OK"
   for f in $DOCS; do echo "$(MSYS_NO_PATHCONV=1 git show HEAD:"$f" | tr -d '\r' | md5sum | cut -c1-32)  $f"; done   # 1-1 표와 같아야 함
   git -c core.quotepath=off status --porcelain       # 기대: "?? .obsidian/" 하나만
   ```
2. `test: 화면 AppTest에 5페이지 추가` — 아래 파이썬을 `$B/edit_smoke.py`로 저장해 **리포 루트에서** 실행한다(정확한 문자열 두 개를 한 번씩만 바꿈 — 줄바꿈은 원래대로 둠). **저장할 때 목록 들여쓰기(각 줄 앞 공백 3칸)는 빼고 첫 줄 `from pathlib import Path`가 0칸에서 시작하게** 한다(안 빼면 IndentationError):
   ```python
   from pathlib import Path
   p = Path("tests/test_app_smoke.py")
   b = p.read_bytes()
   pairs = [
       ("화면 브랜치를 합친 뒤 홈과 페이지 4개가 예외 없이 뜨는지.",
        "화면 브랜치를 합친 뒤 홈과 페이지 5개가 예외 없이 뜨는지(5페이지 = 가정 바꿔 보기, F10)."),
       ('"pages/4_보고서.py"]',
        '"pages/4_보고서.py", "pages/5_가정_바꿔보기.py"]'),
   ]
   for old, new in pairs:
       o, n = old.encode("utf-8"), new.encode("utf-8")
       assert b.count(o) == 1, f"찾는 문자열이 {b.count(o)}번 — 멈춤: {old}"
       b = b.replace(o, n)
   p.write_bytes(b)
   print("OK")
   ```
   ```bash
   PYTHONIOENCODING=utf-8 <py> "$B/edit_smoke.py"     # 기대: OK
   git hash-object tests/test_app_smoke.py            # 기대: 28e48236500b52b42cae8981df9a5b46e0d04fb8 (다르면 멈추고 보고)
   git diff -- tests/test_app_smoke.py | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '   # 기대: - 2줄 · + 2줄(docstring · SCREENS)
   PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_app_smoke.py -v   # 기대: 6 passed (홈 + 페이지 1~5)
   PYTHONIOENCODING=utf-8 <py> -m pytest                               # 기대: 138 passed
   PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"           # 기대: 121 passed, 17 deselected
   git add tests/test_app_smoke.py
   git -c core.quotepath=off diff --cached --stat     # 기대: 1 file (tests/test_app_smoke.py)
   ```
   금지 경로 검사 `OK` 뒤 `git commit -m "test: 화면 AppTest에 5페이지 추가"`. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI"` → `OK` · `git rev-parse HEAD:tests/test_app_smoke.py` = `28e48236500b52b42cae8981df9a5b46e0d04fb8`.
   5페이지 AppTest가 실패하면 화면·계산 코드를 고치지 말고 실패 메시지를 log에 남기고 멈춘다(커밋 2 하지 않음).
3. `docs: F10 보고서` — `docs/dev/reports/F10_report.md` · `F10_log.md` (6절 · PR 생성 뒤 5절 순서대로)

## 3. 하지 않는 것
- 위 문서 3개의 내용 수정(줄바꿈 변환 포함 — `git add` 때 LF→CRLF 경고는 정상이니 그냥 둔다), 다른 문서·코드·`data/`·`README.md`·`tests/fixtures/` 수정
- `tests/test_app_smoke.py`의 두 문자열 밖 수정(형식 정리·import 순서 등 포함)
- `.obsidian/` 스테이징, 이미 병합된 보고서(`docs/dev/reports/F9_*` 등) 수정
- 원격·로컬 브랜치 삭제, PR 병합·ready 전환. 고치고 싶은 것은 고치지 말고 보고서 3절에 적기

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 브랜치 develop, 훅 있음, status가 기대와 같음, 버전·autocrlf 적음, 1-1 md5 2개 같음 |
| 2 | 1-2·1-3 | `pull --ff-only` 뒤 HEAD `754cf80`, md5 다시 같음, `HEAD:tests/test_app_smoke.py` = `2843a96…`, 137 passed, 새 브랜치 `feature/tension-screen5-test`, 이슈 번호 |
| 3 | 커밋 1 | `--cached --stat`이 정확히 3 files, 금지 경로 검사 OK, `HEAD:` md5 2개가 1-1 표와 같음, 커밋 뒤 status = `?? .obsidian/` 하나 |
| 4 | 커밋 2 | 스크립트 `OK`, blob `28e4823…`, diff −2/+2, smoke 6 passed, **138 passed**, not regression 121/17 |
| 5 | 푸시 전 | `git merge origin/develop` 충돌 없음(있으면 abort·멈춤), 138 passed |
| 6 | 변경 범위 | `git diff --name-only origin/develop..HEAD`가 6개(문서 3 + `tests/test_app_smoke.py` + 보고서 2)뿐 |
| 7 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문(올리기 전·후) 모두 `OK` |
| 8 | PR | draft, base `develop`, 라벨 `chore`, `closes #<이슈>`, 병합 안 함 |
| 9 | 마지막 status | `?? .obsidian/` 하나만 |

## 5. 푸시 · PR
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 138 passed
git -c core.quotepath=off diff --name-only origin/develop..HEAD       # 이 시점(커밋 1·2) 기대: 4개(문서 3 + tests/test_app_smoke.py)
git -c core.quotepath=off diff --name-only origin/develop..HEAD | grep -vE '^(docs/|tests/test_app_smoke\.py$)' && echo "범위 밖 변경 있음 — 멈추고 보고" || echo "OK"
git log --format='%h %an' origin/develop..HEAD                 # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-screen5-test
# 본문 "$B/pr_F10.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> ·
#   요약 = 화면 AppTest에 5페이지 추가 + 문서 반영 · 변경 = 0절 표 4개 파일 한 줄씩 ·
#   테스트 = 138 passed(새 AppTest 1개), not regression 121/17, develop 대비 변경이 docs/와 tests/test_app_smoke.py뿐 ·
#   체크리스트 아래에 팀원 안내 두 줄:
#     "화면 코드(홈.py·pages/)와 계산 코드·결과 CSV는 바뀌지 않았습니다 — 화면 테스트 목록에 5페이지(가정 바꿔 보기)만 더했습니다."
#     "앞으로 5페이지가 예외로 안 뜨게 되면 pytest의 test_app_smoke가 잡습니다."
grep -inE "$AI" "$B/pr_F10.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label chore --title "[CHORE] 화면 AppTest에 가정 바꿔 보기 페이지 추가 · 단계 6 문서 반영(F10)" --body-file "$B/pr_F10.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다).
**순서 정리:** 커밋 1 → 커밋 2 → 위 검사·push → PR 생성 → 보고서 두 파일을 쓰고(PR 링크 포함) **커밋 3** → 변경 범위 다시 확인(`git diff --name-only origin/develop..HEAD`가 6개, 범위 밖 검사 `OK`) → `git push` → 끝.

## 6. 보고서 (CLAUDE.md 7절 — 두 파일)
- `docs/dev/reports/F10_report.md` = 요약, **60줄 이내**, 명령 출력 없음. 양식:
  ```markdown
  # F10 보고서 — 화면 AppTest 5페이지 추가 · 단계 6 문서 반영
  - 결과: 완료 / 일부 / 멈춤(이유 한 줄)
  - 날짜 · 브랜치 · 이슈(번호) · 커밋(해시 + 메시지) · PR(링크)
  - 환경: python / numpy / pandas / streamlit
  ## 1. 완료 조건 (4절 표의 # · ✓/✗ · 한 줄 근거 · log 절)
  ## 2. 막힌 것 · 질문 (구현 메인이 답할 것 — 없으면 "없음")
  ## 3. 프롬프트와 다르게 한 것 · 고치고 싶은 것 (제안만 — 없으면 "없음")
  ## 4. 바뀐 파일 (경로 · 한 줄) · 작업트리에 남긴 변경
  ```
- `docs/dev/reports/F10_log.md` = 실행한 명령과 출력 전부. `# F10 실행 로그` 아래 `## L1 시작 점검`(1절) · `## L2 커밋`(2절) · `## L3 푸시·PR`(5절)로 나누고 report의 각 항목이 절 번호를 가리키게 한다. PR을 못 만들면 PR 본문 초안을 log 끝에 둔다.
- 두 파일을 커밋한 뒤 세션을 끝낸다.
