# F7c 작업 프롬프트 — 옛 임시 계산 통로·더미 모드·config 임시값 정리 (박성인 님 요청서 10-30 ④)

작성 2026-10-30 · 구현 메인(채팅 ⑦) → Claude Code · 브랜치 **`feature/tension-cleanup`(최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행**(10-30 조건 충족: ⓐ 화면 PR #33 병합 `fad8310` ⓑ 박성인 님 "더미 지움 괜찮음") — 이 세션은 PR을 draft로 올리고 병합하지 않는다(병합은 사용자 몫)
권장 모델·노력: **Sonnet 5.5 · 중간**(패치·스크립트 적용 + 실행 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F7c_20261030`(`export B=…` — 2절 파이썬이 읽음).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 5절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **팀원 파일 중 이 작업이 바꾸는 것(박성인 님 요청 ④ — 담당 파일 원칙의 예외):** `utils/dummy.py`(파일 삭제) · `utils/real.py`(사건 표 함수만 남김) · `utils/loader.py` **앞부분**(옛 통로 4개 삭제 — `load_events`와 끝 블록 `load_tension_*`는 그대로) · `config.py` 1·3·4·5절(임시값 5개 삭제 + 절 제목) · `README.md` 4절 폴더 구조 3줄. 화면(`홈.py`·`pages/`·`utils/ui.py`)은 건드리지 않는다.
> **줄바꿈(중요):** `utils/real.py`·`utils/dummy.py`는 저장소 blob이 **CRLF**다(다른 파일은 LF). 그래서 두 파일은 패치에 넣지 않았다 — `real.py`는 부록 B 스크립트(바이트 편집, CRLF 유지)로 고치고 **`git -c core.autocrlf=false add utils/real.py`**로만 스테이징한다(그냥 `git add`하면 autocrlf=true PC에서 파일 전체 줄바꿈이 바뀐다). `dummy.py`는 `$B`로 `mv`한 뒤 `git add -u utils/dummy.py`.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`·`git rm`(지울 일은 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`홈.py`·`pages/`·`utils/ui.py`·`utils/tension/**`·`scripts/**` 수정**, `load_events()`·`make_events`·`load_tension_*` 수정·삭제, `data/tension/**` 결과 파일 수정, 부록 밖의 코드·테스트·문서 변경, `git commit <경로>` 꼴(작업트리에서 다시 읽어 real.py 줄바꿈이 바뀐다 — 항상 `git add` 뒤 `git commit -m`).

---

## 0. 목표 (박성인 님 요청서 10-30 ④ · F5 요청서 4절)
- 화면 PR #33(develop `fad8310`)으로 화면이 모두 `load_tension_*`로 바뀌어, 옛 임시 계산 통로(건수 × 임시 가중치)와 더미 모드를 아무도 쓰지 않는다. `[확인 10-30: develop fad8310 grep — 옛 통로를 부르는 곳은 utils/loader.py 앞부분과 tests/test_screen.py 96행뿐, 홈.py는 주석 1줄]`
- **지움:** `utils/dummy.py` 전체 · `utils/loader.py`의 `load_daily`·`load_monthly`·`load_elements`·`load_yearly`(+ dummy·real 옛 함수 import, `import config`) · `utils/real.py`의 `make_daily_elements`·`make_raw_daily`·`make_daily_real`·`make_recent_elements`(+ 안 쓰게 된 `import numpy as np`·`import config`) · `config.py`의 `USE_DUMMY`(1절 통째로)·`RAM_CUTS`·`RATIO_CUTS`·`WEIGHTS`·`WINDOW_DAYS`.
- **남김:** `load_events()`(2페이지 사건 기록)·`make_events`·`read_all_events`·`read_events`·`EVENT_FILES` · config 이름 15개(`CASES SIMILAR_N SIMILAR_EXCLUDE_MONTHS ELEMENT_NAMES GROUPS BUNDLES_BASE BUNDLE_RELIEF HALF_LIFE_DAYS BASE_START BASE_END TENSION_DATA_DIR CALC_START_DATE A2_DATA_END STAGE_NAMES STAGE_COLORS`) · `load_tension_*` 전부.
- 같이 고침: `config.py` 절 제목 3·4·5를 남은 값에 맞게("3. 단계 이름·색 · 유사 시기 (화면 공통)" · "4. 요소 이름" · "5. 기준기간 (화면 공통)") · `tests/test_screen.py` 96행(옛 함수 존재 검사 → `load_events` 있음 + 옛 4개 없음) · README 4절 폴더 구조 3줄.
- **식·값·결과 CSV는 바뀌지 않는다** — 결과 CSV 7개가 바이트까지 같아야 한다. 테스트 개수 그대로(117 — 96행 assert 1줄이 2줄이 됨).
- 구현 메인 시험본 `[확인 10-30: PC .git 사본 develop fad8310 · python 3.13 · numpy 2.4.6 · pandas 3.0.6 · plotly 7.1.0 · streamlit 1.65.0]`: 부록 A 패치(`git apply --check` 통과, core.autocrlf=true 체크아웃에서도) + 부록 B 스크립트 + dummy `mv` → **117 passed**, `-m "not regression"` 100 passed · 17 deselected, `-W error::FutureWarning tests/test_screen.py` 12 passed, `run_tension --end 2026-10-29` 결과 7개 = 커밋된 결과와 **바이트 같음**, AppTest 5화면 통과.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F7c_20261030"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/dev/진행기록.md" " M docs/dev/requests/F5_화면요청.md"
#     "?? docs/dev/requests/F8_화면요청.md" "?? docs/dev/지시서_구현_메인_채팅7.md" "?? docs/dev/tasks/F7c_cleanup.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 4절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: develop (그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 33 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤
git log --oneline -3 origin/develop                # 기대: 맨 위 fad8310(뒤에 커밋이 있으면 누구의 무엇인지 log에 적고 계속 — 2절 git apply --check나 부록 B 확인이 실패하면 거기서 멈춤)
gh pr list --state open --json number,title,headRefName,author   # log에 남김(판단 없이)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 최신 develop으로
DOCS_M="docs/dev/진행기록.md docs/dev/requests/F5_화면요청.md"
DOCS_N="docs/dev/requests/F8_화면요청.md docs/dev/지시서_구현_메인_채팅7.md docs/dev/tasks/F7c_cleanup.md"
DOCS="$DOCS_M $DOCS_N"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표(F7c_cleanup.md 제외 4개 — 내용이 다르면 멈추고 보고)
git restore $DOCS_M
git switch develop                                  # 이미 develop이면 그대로
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in $DOCS; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-cleanup
# 1-3 이슈: 본문 "$B/issue_F7c.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절 첫 줄, 범위 = 0절 지움·남김, 완료 조건 = 4절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F7c.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[REFACTOR] 옛 임시 계산 통로·더미 모드·config 임시값 정리(F7c)" --label refactor --body-file "$B/issue_F7c.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 117 passed
git config --get core.autocrlf                     # log에 남김(true 예상)
```
1-1 `md5sum` 기대(줄바꿈은 Windows 체크아웃 때문에 CRLF/LF 어느 쪽이든 **`tr -d '\r' < 파일 | md5sum`**으로 같게 본다 — 아래 값은 CR을 뺀 md5):
```
7b662876f241ae0855ac13210dc3a11b  docs/dev/진행기록.md
ed3732bc6c2d88ba77eedd8091c3a763  docs/dev/requests/F5_화면요청.md
a5cfc5a37c64a212671508a197ad8940  docs/dev/requests/F8_화면요청.md
06e2d62e7d922ddcef02e6e93a88d3fd  docs/dev/지시서_구현_메인_채팅7.md
```

**커밋 1** `docs: F7c 작업 프롬프트·설계 문서 반영` — 위 `$DOCS` 5개(내용 수정 없이 — U2). 5절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 패치(부록 A)·스크립트(부록 B) 적용 → 확인 → 테스트 → 결과 바이트 확인
```bash
PYTHONIOENCODING=utf-8 <py> - <<'EOF2'
import os, re, pathlib
t = pathlib.Path("docs/dev/tasks/F7c_cleanup.md").read_text(encoding="utf-8")
for name, lang in (("f7c_code.patch", "diff"), ("f7c_real_edit.py", "python")):
    m = re.search(r"<!-- F7c\." + re.escape(name) + r" 시작 -->\n```" + lang + r"\n(.*?)```\n<!-- F7c\." + re.escape(name) + r" 끝 -->", t, re.S)
    pathlib.Path(os.environ["B"], name).write_bytes(m.group(1).encode("utf-8"))
    print("저장:", name, len(m.group(1).splitlines()), "줄")
EOF2
md5sum "$B/f7c_code.patch" "$B/f7c_real_edit.py"
#   기대: 1301459568bcad8aa71a0336f0f702d4  f7c_code.patch (123줄)
#         e6f021b8b6a39490c0c772107bec2fea  f7c_real_edit.py (15줄)
git apply --check "$B/f7c_code.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply "$B/f7c_code.patch"
PYTHONIOENCODING=utf-8 <py> "$B/f7c_real_edit.py"
#   기대: "전 md5(CR 뺀): fce258577cceeb81a5338a5dba18a2fa" / "후 md5(CR 뺀): 9470ee12b3d2f8e133a26f7d80d5680a · 줄 42"
#         (AssertionError가 나면 멈추고 보고 — real.py를 손으로 고치지 않는다)
mv utils/dummy.py "$B/dummy.py.removed"
git hash-object config.py utils/loader.py tests/test_screen.py README.md
git -c core.autocrlf=false hash-object utils/real.py
#   기대(순서대로):
#     config.py            6ba57f5db6bec2465550f31af33f835d9849fe4b
#     utils/loader.py      53d92204022334b896986180b68609823d6f9fed
#     tests/test_screen.py a6bae6fd6936cd4a4ef3e8d4ae259454afbe1cd2
#     README.md            8b7da2c24db3a146e4de03f3fd5faeb3d533692d
#     utils/real.py        3fc848908e42f10e710ed4387260c0d1170df149   (CRLF 유지된 값)
#   하나라도 다르면 멈추고 보고
grep -rnE '^[^#]*(USE_DUMMY|RAM_CUTS|RATIO_CUTS|\bWEIGHTS\b|[^_]WINDOW_DAYS|utils\.dummy|make_daily_real|make_recent_elements|make_daily_elements|make_raw_daily)' --include=*.py . 
#   기대: 줄 없음
grep -rnE '^[^#]*(load_daily|load_monthly|load_elements|load_yearly)' --include=*.py .
#   기대: tests/test_screen.py 한 줄뿐(옛 4개가 "없음"을 확인하는 assert)
```
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest                                    # 기대: 117 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                # 기대: 100 passed, 17 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_screen.py   # 기대: 12 passed
mkdir -p "$B/after"
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --end 2026-10-29 --out "$B/after"
for f in 일별_기본 일별_확장 요약 월별 연도별 비교선_일별 반감기_민감도; do cmp "$B/after/$f.csv" "data/tension/$f.csv" && echo "같음 $f" || echo "다름 $f — 멈추고 보고"; done
git status --porcelain data/                       # 기대: 줄 없음(결과는 $B/after에만 썼다)
PYTHONIOENCODING=utf-8 <py> -c "
from utils import loader
import config
print(callable(loader.load_events), len(loader.load_events()), sorted(n for n in dir(loader) if n.startswith('load_') and not n.startswith('load_tension')))
print([n for n in ('USE_DUMMY', 'RAM_CUTS', 'RATIO_CUTS', 'WEIGHTS', 'WINDOW_DAYS') if hasattr(config, n)])
"
#   기대: True 3882 ['load_events'] / []   (streamlit 경고 줄이 앞에 나와도 됨)
```
- 다르면: 파일도 코드도 고치지 말고 차이를 log에 남기고 멈추고 보고한다(버전 차이로 보이면 그렇게 적는다).
- `--end`를 반드시 `2026-10-29`로 고정한다.

**커밋 2** `refactor: 옛 임시 계산 통로와 더미 모드 정리` — 스테이징은 **이 세 줄 그대로**:
```bash
git add -u utils/dummy.py
git -c core.autocrlf=false add utils/real.py
git add utils/loader.py
git diff --cached --stat     # 기대: 3 files changed, 3 insertions(+), 150 deletions(-)  (dummy.py 62 삭제 · real.py 51 삭제 · loader.py 3+/37−)
```
**커밋 3** `refactor: config 임시값 정리` — `git add config.py` (기대 `--cached --stat`: 1 file, 3 insertions, 13 deletions)
**커밋 4** `test: 옛 통로 삭제를 확인하도록 화면 통로 테스트 수정` — `git add tests/test_screen.py` (1 file, 2 insertions, 1 deletion)
**커밋 5** `docs: README 폴더 구조에서 더미 설명 정리` — `git add README.md` (1 file, 2 insertions, 3 deletions)
커밋 5 뒤:
```bash
git diff --stat origin/develop..HEAD -- utils config.py tests README.md   # 기대: 6 files changed, 10 insertions(+), 167 deletions(-)
git ls-tree HEAD -- config.py utils/loader.py tests/test_screen.py README.md utils/real.py utils/dummy.py
#   기대: 2절 hash 5개 그대로 · utils/dummy.py 줄 없음
git status --porcelain       # 기대: "?? .obsidian/" 하나만(real.py가 M으로 보이면 멈추고 보고)
```

## 3. 하지 않는 것
- 문서 5개·설계 문서의 내용 수정(커밋 1은 그대로), 화면(`홈.py`·`pages/`)·`utils/ui.py`·`utils/tension/**`·`scripts/**` 수정 — `홈.py` 4행 주석의 `load_daily`도 그대로 둔다(화면 파일)
- `load_events()`·`make_events`·`read_all_events`·`EVENT_FILES`·`load_tension_*` 수정·삭제, config 15개 이름 수정·삭제, `config.py` 6절 이후 수정
- `data/tension/` 결과·사건표·판정표 수정(검산 결과는 `$B/after`에만), 부록 A가 바꾸는 한 줄 말고 기존 테스트 수정, `tests/fixtures/` 수정
- 부록과 다른 코드·문서를 더하거나 빼기(고치고 싶은 것은 보고서 3절), 원격·로컬 브랜치 삭제, README 4절 밖 수정

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #33 MERGED, 훅 있음, 117 passed, 버전·autocrlf 적음, 1-1 md5 4개 같음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-cleanup`, 이슈 번호 |
| 3 | 2절 적용 | 패치·스크립트 md5 같음, `git apply --check` 통과, 스크립트 전·후 md5 같음, hash 5개 같음, grep 기대대로 |
| 4 | 2절 테스트 | 117 passed · not regression 100/17 · FutureWarning 12 passed |
| 5 | 2절 결과 | `run_tension --end 2026-10-29` 결과 7개가 커밋된 결과와 바이트 같음, `data/` 변경 없음 |
| 6 | 2절 통로 확인 | `load_events` 3882행 · 옛 `load_*` 없음 · config 임시값 5개 없음 |
| 7 | 커밋 | 5절 순서 6개, 커밋 2~5의 `--cached --stat`이 기대와 같음, 커밋 5 뒤 `ls-tree` hash 같음 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 10 | 마지막 status | `?? .obsidian/` 하나만 |

## 5. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F7c 작업 프롬프트·설계 문서 반영` — 1절 `$DOCS` 5개
2. `refactor: 옛 임시 계산 통로와 더미 모드 정리` — `utils/dummy.py`(삭제) · `utils/real.py` · `utils/loader.py` (2절 세 줄로 스테이징)
3. `refactor: config 임시값 정리` — `config.py`
4. `test: 옛 통로 삭제를 확인하도록 화면 통로 테스트 수정` — `tests/test_screen.py`
5. `docs: README 폴더 구조에서 더미 설명 정리` — `README.md`
6. `docs: F7c 보고서` — `docs/dev/reports/F7c_report.md` · `F7c_log.md`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 117 passed
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-cleanup
# 본문 "$B/pr_F7c.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 지움·남김 · 테스트 = 2절 결과(117 passed, 결과 CSV 바이트 동일, AppTest 5화면)
#   · 체크리스트 아래에 팀원 안내 네 줄:
#     "박성인 님 요청 ④(10-30, 더미 지움 확인)를 처리했습니다: utils/dummy.py 삭제, 옛 load_daily·load_monthly·load_elements·load_yearly 삭제, real.py는 사건 표(make_events)만 남겼습니다."
#     "config.py에서 USE_DUMMY·RAM_CUTS·RATIO_CUTS·WEIGHTS·WINDOW_DAYS를 지우고 절 제목 3·4·5를 남은 값에 맞게 고쳤습니다(1절 데이터 스위치는 통째로 없어짐). 화면이 쓰는 이름(STAGE_NAMES·STAGE_COLORS·SIMILAR_N·ELEMENT_NAMES·BASE_START·BASE_END·CASES·GROUPS 등)은 그대로입니다."
#     "2페이지가 쓰는 load_events()와 load_tension_*는 그대로입니다. 화면 파일(홈.py·pages/·ui.py)은 바꾸지 않았습니다(홈.py 4행 주석의 load_daily는 담당자께서 다음에 정리해 주세요)."
#     "README 4절 폴더 구조에서 dummy.py 줄을 빼고 loader.py·real.py 설명을 고쳤습니다. 로컬에서 USE_DUMMY를 켜 두셨다면 이제 그 스위치는 없습니다."
grep -inE "$AI" "$B/pr_F7c.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label refactor --title "[REFACTOR] 옛 임시 계산 통로·더미 모드·config 임시값 정리(F7c)" --body-file "$B/pr_F7c.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다). 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 6. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F7c_report.md`(60줄 이내): 1절 = 4절 표 10행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F7c_log.md`: 1~2절 출력 전부(문서 md5, 패치·스크립트 md5, 스크립트 출력, hash, grep, 테스트 결과, 결과 7개 cmp, 통로 확인 출력), 커밋별 `--cached --stat`, 작성자 목록, 커밋·푸시·PR 출력.

---

## 부록 A. `$B/f7c_code.patch` (2절 파이썬으로 잘라 저장 — 글자 그대로, md5 `1301459568bcad8aa71a0336f0f702d4`, 123줄 · README·config·loader·test_screen 4개 LF 파일)

<!-- F7c.f7c_code.patch 시작 -->
```diff
diff --git a/README.md b/README.md
index c509beb..8b7da2c 100644
--- a/README.md
+++ b/README.md
@@ -69,11 +69,10 @@ Team-Project/
 ├── utils/                       # 공통 함수 및 전처리 모듈
 │   └── build_db.py                 # 1단계: processed CSV -> bongsu.db 통합 표 (사건, 수치, 참여국 등) + 검증
 │   └── build_erd.py                # 2단계: 통합 표 -> ERD v4 테이블 (사건_일단위, 지표값, 상세 13개) + 검증
-│   └── dummy.py                    # 결과 테이블과 같은 모양의 연습용 더미 데이터
 │   └── helpers.py                  # 초기 예시 함수 (현재 화면에서 안 씀)
-│   └── loader.py                   # 데이터 통로: USE_DUMMY에 따라 dummy 또는 real을 불러옴 (캐시 적용) · 긴장도 실제 결과는 `load_tension_*`
+│   └── loader.py                   # 데이터 통로(캐시 적용): 사건 표 `load_events` · 긴장도 결과 `load_tension_*`
 │   └── README.md                   # utils 폴더 설명
-│   └── real.py                     # 실제 사건 CSV → 원점수·평소대비·단계 계산 (결과_일별·월별·연별)
+│   └── real.py                     # 실제 사건 CSV 17종 → 사건 표 (2페이지 사건 기록)
 │   └── tension/                    # 긴장도 계산 (io·core·summary·screen·charts)
 │   └── ui.py                       # 공통 화면 조각 (5단계 눈금 stage_scale)
 ├── .gitignore                   # 깃 제외 파일 목록 (보안 키, 대용량 파일 차단)
diff --git a/config.py b/config.py
index 38c356d..6ba57f5 100644
--- a/config.py
+++ b/config.py
@@ -1,27 +1,17 @@
-# ===== 1. 데이터 스위치 =====
-USE_DUMMY = False   # True 더미 데이터 / False 실제 사건 CSV(data/processed)
-# [수정] DB_PATH 삭제: 어디서도 안 씀 (대시보드는 CSV를 직접 읽음, DB는 build_db.py가 따로 만듦)
-
-# ===== 3. 단계 기준선 (팀 확정 전 임시값) =====
-RAM_CUTS = [40, 60, 90, 120]
-RATIO_CUTS = [100, 150, 200, 300]
+# ===== 3. 단계 이름·색 · 유사 시기 (화면 공통) =====
 STAGE_NAMES = {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"}
 STAGE_COLORS = {1: "#81C784", 2: "#26A69A", 3: "#FBC02D", 4: "#FB8C00", 5: "#E53935"}
 SIMILAR_N = 3
 SIMILAR_EXCLUDE_MONTHS = 12
 
-# ===== 4. 요소 가중치 =====
-WEIGHTS = {"A1": 10, "A2": 5, "A3": 4, "A4": 2, "A5": 3, "A6": 1, "A7": 8, "B1": 4, "B3": 1, "B4": 2, "C1": 2, "C2": 1, "C3": 1, "C4": -3, "C5": 2, "E5": 1, "F2": -2}
-# ===== 4-1. 요소 이름 =====
+# ===== 4. 요소 이름 =====
 ELEMENT_NAMES = {
     "A1": "핵실험", "A2": "미사일 발사", "A3": "저강도 도발", "A4": "군사훈련", "A5": "미 전략자산 전개",
     "A6": "열병식", "A7": "포격·총격·충돌", "B1": "신형무기 시험", "B3": "국방비", "B4": "핵태세·확장억제",
     "C1": "위협 성명·담화", "C2": "교리·법제", "C3": "동맹협의", "C4": "대화·협상·합의", "C5": "제재·결의",
     "E5": "남북관계", "F2": "남북회담",
 }
-# ===== 5. 집계 기간 (팀 확정 전 임시값) =====
-WINDOW_DAYS = 30   # 원점수 = 최근 며칠 점수 합인지. 바꾸면 계산과 화면 글자가 같이 바뀜
-
+# ===== 5. 기준기간 (화면 공통) =====
 BASE_START = "2010-01-01"
 BASE_END = "2019-12-31"
 
diff --git a/tests/test_screen.py b/tests/test_screen.py
index d44a6a8..a6bae6f 100644
--- a/tests/test_screen.py
+++ b/tests/test_screen.py
@@ -93,7 +93,8 @@ def test_loader_functions_match_screen():
     t1, e1 = loader.load_tension_contrib("2026-10-29")
     t2, e2 = screen.contributions("2026-10-29")
     assert t1.equals(t2) and e1.equals(e2)
-    assert callable(loader.load_daily) and callable(loader.load_monthly)                # 기존 함수 그대로
+    assert callable(loader.load_events)                                                 # 2페이지 사건 기록 통로는 남김
+    assert not any(hasattr(loader, f) for f in ("load_daily", "load_monthly", "load_elements", "load_yearly"))  # F7c: 옛 임시 통로 지움
 
 
 def test_top_pct_display_matches_summary():
diff --git a/utils/loader.py b/utils/loader.py
index 30dd5c6..53d9220 100644
--- a/utils/loader.py
+++ b/utils/loader.py
@@ -1,48 +1,14 @@
-import config
-from utils.dummy import make_daily, make_monthly, make_elements, make_yearly # 쉼표로 여러 개를 한 번에 가져올 수 있음
-from utils.real import make_daily_real, make_recent_elements, make_events
+from utils.real import make_events
 import streamlit as st
 
-# ===== 일별 표 통로 =====
-@st.cache_data
-def load_daily():
-    if config.USE_DUMMY: # 스위치가 True면 더미, False면 진짜
-        return make_daily()
-    else:
-        return make_daily_real() # 진짜 결과_일별
-
-# ===== 월별 표 통로 =====
-@st.cache_data
-def load_monthly():
-    if config.USE_DUMMY:
-        return make_monthly(make_daily())
-    else:
-        return make_monthly(make_daily_real())  # make_monthly를 진짜 일별 표에 그대로 재사용
-
-# ===== 점수 구성 통로 =====
-@st.cache_data
-def load_elements(day=None): # [수정] 기준일을 받을 수 있게 (안 주면 최신)
-    if config.USE_DUMMY:
-        return make_elements()
-    else:
-        return make_recent_elements(day) # 진짜 최근 30일 요소 / [수정] 기준일 전달
-
-# ===== 사건 표 통로 =====
+# ===== 사건 표 통로 (2페이지 사건 기록) =====
 @st.cache_data
 def load_events():
     return make_events()
 
-# ===== 연별 표 통로 =====
-@st.cache_data
-def load_yearly():
-    if config.USE_DUMMY:
-        return make_yearly(make_daily())
-    else:
-        return make_yearly(make_daily_real()) # 진짜 일별 표를 연별로 묶기
-
 
 # ===== [F5 추가 · 긴장도 담당] 긴장도 결과 통로 — data/tension 결과 CSV(utils/tension/screen.py) =====
-# 위 기존 함수(load_daily 등)는 그대로 둔다. 화면 담당자가 화면을 고칠 때 아래 함수로 바꾼다(요청서 docs/dev/requests/).
+# 옛 임시 계산 통로(load_daily·load_monthly·load_elements·load_yearly)·더미 모드는 F7c에서 지웠다(10-30 박성인 확인). 화면은 아래 함수를 쓴다.
 from utils.tension import screen as tension_screen   # noqa: E402
 
 
```
<!-- F7c.f7c_code.patch 끝 -->

## 부록 B. `$B/f7c_real_edit.py` (2절 파이썬으로 잘라 저장 — md5 `e6f021b8b6a39490c0c772107bec2fea`, 15줄 · `utils/real.py` CRLF 그대로 바이트 편집: 머리 import 3줄 → 1줄, `# ===== 날짜, 카테고리, 주체국별 건수와 점수` 줄부터 끝까지 삭제)

<!-- F7c.f7c_real_edit.py 시작 -->
```python
import hashlib, pathlib
p = pathlib.Path("utils/real.py")
b = p.read_bytes()
nl = b"\r\n" if b"\r\n" in b else b"\n"
before = hashlib.md5(b.replace(b"\r", b"")).hexdigest()
print("전 md5(CR 뺀):", before)
assert before == "fce258577cceeb81a5338a5dba18a2fa", "real.py가 기대와 다름 — 멈추고 보고"
head = nl.join([b"import pandas as pd", b"import numpy as np", b"import config", b""])
assert b.startswith(head), "머리 3줄이 기대와 다름 — 멈추고 보고"
b = nl.join([b"import pandas as pd", b""]) + b[len(head):]
cut = "# ===== 날짜, 카테고리, 주체국별 건수와 점수".encode("utf-8")
assert b.count(cut) == 1, "자를 표시가 1개가 아님 — 멈추고 보고"
b = b[:b.index(cut)].rstrip(b"\r\n") + nl
p.write_bytes(b)
print("후 md5(CR 뺀):", hashlib.md5(b.replace(b"\r", b"")).hexdigest(), "· 줄", b.count(b"\n"))
```
<!-- F7c.f7c_real_edit.py 끝 -->
