# F5 작업 프롬프트 — 화면 브랜치 병합 · 화면용 결과 통로(screen.py·loader 새 함수) · 그림 색 config

작성 2026-10-29 · 구현 메인(채팅 ④) → Claude Code · 브랜치 **`feature/tension-merge-data`(PR #23 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행** — 10-29 사용자·팀 결정 반영: 화면 브랜치(`feature/tension-dashboard` head `12598bc`)를 이 PR로 합침(팀 동의 받음 — 합치기·새 커밋 멈춤·리뷰) · **담당 파일 원칙**(화면 `홈.py`·`pages/`는 담당자만 고침 — 이 작업에서 고치지 않음) · 데이터 통로는 우리(loader에 새 함수만 더하고 기존 함수는 그대로) · README는 이원희 줄만 · 그림 색은 config에서 · 평소대비 = 7일 표시값 + 원값 · 상위 % 첫 365일 숨김 · 점수 구성 = 묶음별 + 사건별 10건 · 주체국 못 붙으면 "미상" · 완화 할인 = 실제 δ
권장 모델·노력: **Opus 5.5 · 중간**(파일은 부록 그대로 저장 + 실행·커밋 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F5_20261029`.
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 로컬 `commit-msg` 훅이 있는지 1절에서 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 7절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **이번 작업에만 있는 예외(사용자 10-29 — 이 프롬프트에만 적용, CLAUDE.md는 그대로):** 2절의 병합 충돌은 **부록 A 스크립트로만** 푼다. 2절에 적힌 4개 파일·4가지 충돌 상태가 아니면 손으로 풀지 말고 `git merge --abort` 하고 멈춘다. 팀원 파일 중 이 작업이 바꾸는 것은 ① 부록 A가 만드는 `홈.py`(화면 브랜치 것 그대로)·`README.md`(이원희 줄 한 줄)·`.gitignore`(한 줄)·`config.py`(화면 브랜치 것 + 긴장도 절) ② 부록 E가 `utils/loader.py` **끝에 붙이는** 블록뿐이다.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `git branch -d`·`push --delete`(원격·로컬 브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`홈.py`·`pages/`·`utils/ui.py`·`utils/dummy.py`·`utils/real.py` 수정**(부록 A 결과 외), `utils/loader.py`의 기존 줄 수정, `utils/tension/core.py`·`io.py`·`summary.py`·`scripts/`·`requirements.txt` 수정. 부록 파일은 **글자 그대로**(코드 블록을 파이썬으로 잘라 **LF로** 저장해도 된다) — `git hash-object` 기대값과 다르면 다시 저장.

---

## 0. 목표
- **화면 브랜치 병합:** `feature/tension-dashboard`(head `12598bc66c2595b4dc7e1bd55801d10f77e64503`)를 이 브랜치에 병합 커밋 하나로 합친다. 충돌 4곳(`홈.py`·`README.md`·`.gitignore`·`config.py`)은 부록 A가 정해진 방식대로 푼다. 화면 파일(`홈.py`·`pages/`·`utils/loader.py`·`ui.py`·`dummy.py`·`real.py`)은 병합 직후 화면 브랜치와 **같아야** 한다(`홈.py` 포함).
- **화면용 결과 통로:** `utils/tension/screen.py`(부록 B, 새 파일 — 결과 CSV를 화면 모양으로) + `utils/loader.py` 끝에 `load_tension_*` 함수 8개(부록 D 블록을 부록 E로 붙임). 기존 `load_daily`·`load_monthly`·`load_elements`·`load_events`·`load_yearly`는 그대로 — 화면은 아직 기존 함수를 쓰고, 담당자가 화면을 고칠 때 새 함수로 바꾼다(요청서는 구현 메인이 따로).
- **그림 색:** `utils/tension/charts.py`(부록 C, 덮어씀) — 단계 색·이름을 그릴 때 `config.STAGE_COLORS`·`STAGE_NAMES`에서 읽는다(화면 브랜치에서 1·2단계 색이 바뀜, 10-29).
- **테스트:** `tests/test_screen.py`(부록 F, 9개) · `tests/test_app_smoke.py`(부록 G, Streamlit AppTest — 홈과 페이지 4개가 예외 없이 뜸, 5개 — U10).
- 구현 메인 시험본 `[확인 10-29: python 3.13 · pandas 3.0.5 · streamlit 1.66.1 · plotly 7.1]`: develop `c691bf1`에서 이 순서 그대로 → 병합 직후 화면 파일 화면 브랜치와 같음, README는 develop 대비 1줄, **87 passed**(기존 73 + 9 + 5), `-m "not regression"` 71 passed · 16 deselected. AppTest 경고(`use_container_width` 사용 중단 예고)는 화면 코드의 경고라 고치지 않는다.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F5_20261029"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관): " M docs/dev/진행기록.md", "?? docs/dev/tasks/F5_merge_data.md", "?? .obsidian/"
git branch --show-current                          # 기대: feature/tension-output
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 23 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git rev-parse origin/feature/tension-dashboard     # 기대: 12598bc66c2595b4dc7e1bd55801d10f77e64503 — 다르면 멈추고 보고(팀원 새 커밋 → 해결본 다시 만듦)
git log --oneline -1 origin/develop                # 기대: c691bf1(뒤에 커밋이 있으면 log에 적고 계속 — 2절 충돌 상태가 다르면 거기서 멈춤)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 develop으로
for f in docs/dev/진행기록.md docs/dev/tasks/F5_merge_data.md; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git restore docs/dev/진행기록.md
git switch develop
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in docs/dev/진행기록.md docs/dev/tasks/F5_merge_data.md; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-merge-data
# 1-3 이슈: 본문 "$B/issue_F5.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 0절 목록, 완료 조건 = 6절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F5.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 화면 브랜치 병합·화면용 결과 통로(F5)" --label feat --body-file "$B/issue_F5.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
#   streamlit·docx(python-docx)가 없으면 멈추고 보고(pip install 금지 — requirements.txt에 이미 있음)
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 73 passed(F4까지)
```
**커밋 1** `docs: F5 작업 프롬프트·설계 문서 반영` — `docs/dev/tasks/F5_merge_data.md`, `docs/dev/진행기록.md`(내용 수정 없이 — U2). 7절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 화면 브랜치 병합 (부록 A — 이번 작업의 예외)
```bash
git merge --no-ff -m "chore: 화면 브랜치(feature/tension-dashboard) 병합" origin/feature/tension-dashboard
#   기대: 충돌로 멈춤(종료 코드 1). 충돌 없이 끝나거나 다른 오류면 멈추고 보고
git status --porcelain | grep -E '^(UU|AA|DU|UD|AU|UA|DD) '
#   기대: 정확히 이 4줄(순서 무관) — "UU .gitignore" "UU README.md" "UU config.py" "AA 홈.py"(한글이 "\355\231\210.py"로 보일 수 있음)
#   다르면: git merge --abort → 멈추고 보고(손으로 풀지 않는다)
# 부록 A를 "$B/resolve_merge.py"로 저장(md5 d154743360432920d0f637019ccd384b), 리포 루트에서
PYTHONIOENCODING=utf-8 <py> "$B/resolve_merge.py"
#   기대 출력(4줄, git hash-object):
#     홈.py: 6dab5079c5d99eed1e48bf5c4ca55fe474f7a9cf
#     README.md: c8c14c70c07fbea294c180f88c2001b0c429c86d
#     .gitignore: 6b72961c83c80cf424c91bf746ed2c95e9910e4c
#     config.py: 6624f6c53b973eb6f744913c23a536d3d5b16568
#   "멈춤:"이 나오거나 값이 하나라도 다르면: git merge --abort → 멈추고 보고
git add 홈.py README.md .gitignore config.py
git diff --cached --name-only --diff-filter=U      # 기대: 아무것도 없음
git grep -nE '^(<<<<<<<|>>>>>>>) ' -- . ':!data' && echo "충돌 표시 남음 — 멈춤" || echo "충돌 표시 없음"
git commit --no-edit                               # 병합 커밋 = 커밋 2
git log -1 --format='%h %P%n%B'                    # 부모 2개(develop 쪽·12598bc), 메시지 "chore: 화면 브랜치(feature/tension-dashboard) 병합", AI 표기 없음
# 확인: 화면 파일은 화면 브랜치와 같다 · README는 develop 대비 1줄만 · config.py는 화면 브랜치 대비 끝에 더한 줄만
git diff --stat origin/feature/tension-dashboard HEAD -- pages 홈.py utils/loader.py utils/ui.py utils/dummy.py utils/real.py   # 기대: 출력 없음
git diff origin/develop HEAD -- README.md | grep -E '^[-+]\|'        # 기대: 이원희 줄 − 1 · + 1 (2줄)
git diff origin/feature/tension-dashboard HEAD -- config.py | grep -E '^-[^-]' || echo "config.py 화면 쪽 줄 지운 것 없음"
PYTHONIOENCODING=utf-8 <py> -c "import config; print(config.HALF_LIFE_DAYS, config.TENSION_MODEL_VERSION, config.STAGE_COLORS[1], config.USE_DUMMY)"   # 기대: 14 v0.1.4 #81C784 False
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 73 passed(병합만 한 상태)
```
- 이 커밋은 화면 브랜치의 변경(페이지 4개·`utils/loader.py`·`ui.py`·`dummy.py`·`real.py`·`홈.py`·`config.py` 화면 설정)을 develop으로 가져온다. 팀원 커밋의 작성자 기록은 그대로 남는다. `data/processed`는 이미 develop과 같아 바뀌지 않는다.

## 3. 화면용 결과 통로 · 그림 색 (부록 B·C·D·E)
| 부록 | 저장 위치 | `git hash-object` 기대값 |
|---|---|---|
| B | `utils/tension/screen.py`(새) | `17cf9d58ec76f43e26c7d1d4d54a1b6880bdf735` |
| C | `utils/tension/charts.py`(덮어씀) | `7c139e7d6acddc3893f6c2058c4c1a2edf91f219` |
| D | `$B/loader_block.txt`(md5 `a06fc02eff80ea80b6dcd4be57a896bf`) → 부록 E로 `utils/loader.py` 끝에 붙임 | `utils/loader.py` = `f68be8072e3fcbbe1f9bec1abb5adaf7016697bc` |
| E | `$B/append_loader.py`(md5 `1ad1b4157ae6d42fcd44c968692043ee`) | — |
```bash
PYTHONIOENCODING=utf-8 <py> "$B/append_loader.py" "$B/loader_block.txt"   # 기대: "utils/loader.py: F5 블록 붙임"
git diff utils/loader.py | grep -E '^-[^-]' && echo "기존 줄이 바뀜 — 멈춤" || echo "기존 줄 그대로(더한 줄만)"
git hash-object utils/tension/screen.py utils/tension/charts.py utils/loader.py   # 위 표와 같아야 함
git diff utils/tension/charts.py | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '    # 색·이름 기본값 주석 1줄, trend_figure 인자 colors=None·names=None과 config에서 읽는 2줄·docstring
```
**커밋 3** `feat: 화면용 결과 통로(screen.py)` — `utils/tension/screen.py`
**커밋 4** `feat: loader에 긴장도 결과 함수 추가` — `utils/loader.py`
**커밋 5** `refactor: 그림 단계 색·이름을 config에서 읽기` — `utils/tension/charts.py`
(커밋 3~5는 4절 테스트가 통과한 뒤에 한다)

## 4. 테스트 (부록 F·G)
| 부록 | 저장 위치 | `git hash-object` 기대값 |
|---|---|---|
| F | `tests/test_screen.py`(새) | `0c3a1fb18fc5a33ba9662983466af94a48cfc72c` |
| G | `tests/test_app_smoke.py`(새) | `2843a965014dd70b1310e4262b401f91050b4e46` |
```bash
git hash-object tests/test_screen.py tests/test_app_smoke.py
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_screen.py tests/test_app_smoke.py   # 기대: 14 passed
PYTHONIOENCODING=utf-8 <py> -m pytest                                              # 기대: 87 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                          # 기대: 71 passed, 16 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_screen.py   # 기대: 9 passed(우리 코드 경고 0)
git status --porcelain
#   기대: " M utils/loader.py" " M utils/tension/charts.py" "?? utils/tension/screen.py" "?? tests/test_screen.py" "?? tests/test_app_smoke.py" "?? .obsidian/"(커밋 3~5 전)
```
- AppTest가 실패하면(화면 예외) 화면 코드를 고치지 말고 예외 원문 전부를 log에 남기고 멈추고 보고한다(담당 파일 원칙 — 담당자에게 요청할 일). pandas·streamlit 버전 차이로 보이면 그렇게 적는다.
- 그 밖에 기대와 다르면 테스트도 코드도 고치지 말고 실패 출력 전부를 log에 남기고 멈추고 보고한다.

**커밋 3·4·5**(3절) 다음 **커밋 6** `test: 화면 통로·화면 AppTest` — `tests/test_screen.py`, `tests/test_app_smoke.py`. 스테이징 뒤 마지막 `git status --porcelain` = `?? .obsidian/`만.

## 5. 하지 않는 것
- 화면(`홈.py`·`pages/`)·`utils/ui.py`·`dummy.py`·`real.py` 수정, `utils/loader.py` 기존 함수 수정·삭제(담당 파일 원칙 — 화면이 새 함수를 쓰게 바꾸는 일은 담당자에게 요청)
- `config.py`의 화면 설정 값(`USE_DUMMY`·`RAM_CUTS`·`RATIO_CUTS`·`WEIGHTS`·`WINDOW_DAYS`·`CASES` 등) 수정 — 화면이 아직 쓰는 값
- `use_container_width` 경고 고치기(화면 코드), 결과 CSV 다시 만들기(F4 결과 그대로), 원격·로컬 브랜치 삭제
- 부록과 다른 함수·테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절)

## 6. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #23 MERGED, 화면 브랜치 head `12598bc…`, 훅 있음, 73 passed, streamlit·plotly 버전 적음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-merge-data`, 이슈 번호 |
| 3 | 2절 병합 | 충돌 4곳 기대대로, 부록 A 출력 hash 4개 같음, 충돌 표시 없음, 병합 커밋 부모 2개 |
| 4 | 2절 확인 | 화면 파일 diff 없음, README 2줄, config 화면 쪽 지운 줄 없음, config 값 출력 기대대로, 73 passed |
| 5 | 3절 | hash 3개 같음, loader 기존 줄 그대로 |
| 6 | 4절 | 14 / 87 passed · not regression 71/16 · test_screen 경고 0 · AppTest 5개 예외 없음 |
| 7 | 커밋 | 7절 순서 6개 + 보고서 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | 7절 AI 표기 검사 | 이슈 본문·커밋 메시지 전부(팀원 커밋 제외 — 아래)·PR 본문 모두 `OK` |
| 10 | 마지막 status | `?? .obsidian/` 하나만 |

## 7. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전, 병합 커밋은 `git commit --no-edit` 전에):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F5 작업 프롬프트·설계 문서 반영` 2. `chore: 화면 브랜치(feature/tension-dashboard) 병합`(병합 커밋) 3. `feat: 화면용 결과 통로(screen.py)` 4. `feat: loader에 긴장도 결과 함수 추가` 5. `refactor: 그림 단계 색·이름을 config에서 읽기` 6. `test: 화면 통로·화면 AppTest` 7. `docs: F5 보고서`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 87 passed
# AI 표기 검사 — 이 PR에는 팀원 커밋(화면 브랜치)이 들어온다. 우리 커밋(작성자 = 이 PC의 git user.name)만 검사하고, 팀원 커밋은 걸리면 log에 적기만 한다(히스토리 고치지 않음)
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --author="$(git config user.name)" --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "우리 커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-merge-data
# 본문 "$B/pr_F5.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 목록 · 테스트 = 6절 결과(87 passed, AppTest 5개 예외 없음)
#   · 체크리스트 아래에 팀원 안내 세 줄:
#     "화면 브랜치(feature/tension-dashboard, 12598bc)를 이 PR로 합칩니다(팀 동의 10-29). 화면 파일은 화면 브랜치와 같고, 충돌 4곳은 config.py·.gitignore 두 쪽 모두 · 홈.py 화면 쪽 · README는 이원희 줄만 고쳤습니다."
#     "화면은 아직 기존 함수(load_daily 등)를 씁니다. 실제 결과는 새 함수 load_tension_*(utils/loader.py 끝)으로 읽으며, 화면에 붙이는 일은 담당자께 따로 요청드립니다."
#     "리뷰: 화면이 전처럼 뜨는지(AppTest 5개 통과) · 병합 해결이 의도에 맞는지 봐 주세요."
grep -inE "$AI" "$B/pr_F5.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 화면 브랜치 병합·화면용 결과 통로(F5)" --body-file "$B/pr_F5.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 8. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F5_report.md`(60줄 이내): 1절 = 6절 표 10행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일(팀원 파일은 병합으로 들어온 것과 우리가 바꾼 것 구분).
`docs/dev/reports/F5_log.md`: 1~4절 출력 전부(충돌 상태, 부록 A 출력, 화면 파일 diff, AppTest 결과·경고 요약), 작성자 목록, 커밋·푸시·PR 출력.

---

## 부록 A. `$B/resolve_merge.py` (글자 그대로 저장)
```python
"""F5 1-5 — 화면 브랜치(12598bc) 병합 충돌 4곳을 정해진 방식대로 푼다(사용자 10-29 결정). 리포 루트에서, 병합 충돌 상태일 때만 실행.

- 홈.py      : 화면 브랜치 것(theirs) 그대로
- README.md  : develop 것(ours) 그대로 + 2절 팀원 역할 표의 이원희 줄 한 줄만 바꿈
- .gitignore : develop 것(ours) + 화면 브랜치가 더한 `!.vscode/extensions.json` 한 줄
- config.py  : 화면 브랜치 것(theirs, 화면 설정 — 담당자 파일) 끝에 develop의 긴장도 파라미터 절을 붙임
               (develop에만 있던 DEFAULT_PERIOD_MONTHS·DB_PATH는 화면 브랜치가 지운 대로 둠 — 어디서도 안 씀)
파일은 LF로 쓴다. 다 쓴 뒤 각 파일의 `git hash-object` 값을 출력한다(작업 프롬프트의 기대값과 대조).
"""
import subprocess
import sys
from pathlib import Path


def stage(n, path):
    """병합 중 인덱스의 :n:path(2 = ours/develop, 3 = theirs/화면 브랜치) 내용을 LF 문자열로."""
    raw = subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True, check=True).stdout
    return raw.decode("utf-8").replace("\r\n", "\n")


def once(text, old, new, name):
    if text.count(old) != 1:
        sys.exit(f"멈춤: {name}에서 바꿀 부분을 정확히 한 번 찾지 못함({text.count(old)}번) — 아무 파일도 쓰지 않음")
    return text.replace(old, new)


OLD_LEE = "| **이원희** | AA | 긴장도 산출식 설계, D~F 세부 기준·상대 점수 설계 (수정예정) |"
NEW_LEE = ("| **이원희** | AA | 긴장도 산출식 설계·확정(v0.1.4), D~F 세부 기준·상대 점수 설계, "
           "긴장도 검증(위기 포착·견고성·외부 지수 대조), 긴장도 계산 코드화(utils/tension) |")
TENSION_HEAD = "# 4. 긴장도 계산 파라미터 (utils/tension)"
TENSION_TITLE = ("# ===== 8. 긴장도 계산 파라미터 (utils/tension — 긴장도 담당) — 값의 근거는 docs/decisions.md ADR 번호 =====\n"
                 "#    함수는 이 값을 인자 기본값으로만 쓴다. 값을 바꾸면 모델 버전을 올리고 ADR에 기록한다.\n"
                 "HALF_LIFE_DAYS = 14                              # ADR-006 긴장도 감쇠 반감기(일)\n")

out = {}
out["홈.py"] = stage(3, "홈.py")
out["README.md"] = once(stage(2, "README.md"), OLD_LEE, NEW_LEE, "README.md")
out[".gitignore"] = once(stage(2, ".gitignore"), ".vscode/*\n!.vscode/settings.default.json\n",
                         ".vscode/*\n!.vscode/extensions.json\n!.vscode/settings.default.json\n", ".gitignore")
ours_cfg, theirs_cfg = stage(2, "config.py"), stage(3, "config.py")
if ours_cfg.count(TENSION_HEAD) != 1:
    sys.exit("멈춤: develop config.py에서 긴장도 파라미터 절 머리를 찾지 못함 — 아무 파일도 쓰지 않음")
block = ours_cfg[ours_cfg.index(TENSION_HEAD):]
block = block[block.index("\n", block.index("함수는 이 값을")) + 1:]   # 원래 머리 두 줄을 뺀 나머지(TENSION_MODEL_VERSION부터)
out["config.py"] = theirs_cfg.rstrip("\n") + "\n\n" + TENSION_TITLE + block
for name, text in out.items():
    if any(m in text for m in ("<<<<<<<", ">>>>>>>")) or "\n=======\n" in text:
        sys.exit(f"멈춤: {name}에 충돌 표시가 남음 — 아무 파일도 쓰지 않음")
for name, text in out.items():
    Path(name).write_bytes(text.encode("utf-8"))
for name in out:
    h = subprocess.run(["git", "hash-object", name], capture_output=True, text=True, check=True).stdout.strip()
    print(f"{name}: {h}")
```

## 부록 B. `utils/tension/screen.py` (글자 그대로 저장)
```python
"""화면용 결과 통로 (F5) — data/tension 결과 CSV를 화면이 쓰기 좋은 모양으로 읽는다. Streamlit을 모른다.

화면(`utils/loader.py`의 `load_tension_*`)이 이 함수들을 부른다. 계산 규칙은 바꾸지 않는다 — 결과 CSV를 읽고,
화면 이름 열을 더하고, 화면에서만 쓰는 값(지속일수·상위% 숨김·완화 할인 δ·사건별 남은 점수)을 만든다.
10-29 사용자 결정: 평소대비 = 7일 표시값(원값은 `평소대비_원값`) · 상위 %는 첫 365일 숨김 · 점수 구성 = 묶음별 + 사건별 10건 ·
주체국을 못 붙이면 "미상" · 완화 할인은 실제 δ · 시나리오는 기본이 주, 확장은 추이 그림 점선.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

import config
from utils.tension import core, io as tio, summary as sm

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / config.TENSION_DATA_DIR
PROCESSED_DIR = ROOT / "data" / "processed"
SCENARIOS = {"기본": config.BUNDLES_BASE, "확장": config.BUNDLES_EXT}
SUMMARY_COLUMN = {"기본": "기본", "확장": "확장(C5 포함)"}   # 요약.csv 열 이름(v0.1.4와 같음)
TOP_PCT_HIDE_DAYS = 365       # 사용자 10-29: 누적 비교 표본이 작은 첫 365일(2010년)은 상위 % 숨김
UNKNOWN_ACTOR = "미상"         # 사용자 10-29: data/processed에 없는 보완행
STAGE_MEANING = {1: "평상시", 2: "적 출현", 3: "경계 접근", 4: "경계 침범", 5: "교전"}   # 봉수 원뜻(산출식 단계 표)
KIND = {config.BUNDLE_RELIEF: "완화(할인)", config.BUNDLE_PHYS: "하한 대상", config.BUNDLE_E5: "하한 대상",
        "북러(표시만)": "표시만"}

# 자료 충실도 표·각주·판독문(단계 5 인계 5.4절 문구 그대로) — 화면이 그대로 보여 준다
DATA_COVERAGE = pd.DataFrame({
    "요소": ["A2 미사일", "A3 저강도", "A7 물리 충돌", "C1 위협 성명", "A5 전략자산"],
    "충실도": [f"{config.A2_DATA_END} 이후 자료 없음", "2022년부터 수집(원자료 범위) — 2010~2021 해당 없음",
            "2020-05-03 철원 GP 총격 미포함(팀 결정)", "2021년 기록 없음(팀: 그대로 진행)", "2018~2021 기록 없음(팀: 그대로 진행)"]})
FOOTNOTES = ("2020~2021: 실제 소강기(코로나·대화 중단·훈련 축소). 일부 요소는 기록이 적어 실제보다 낮게 나올 수 있음.",
             "2022년 이후: 요소별 기록 밀도가 2010년대의 2~5배 — 과거보다 높게 나오는 경향.")
READING_NOTES = ("기본점수·묶음 가중을 ±50% 흔들어도 일별 단계 86~91%(중앙) 유지.",
                 "외부 대조: CrisisWatch(International Crisis Group) 악화 판정 달의 85%에서 봉수 2거 이상, "
                 "방향 쌍 63~69% 일치(내부 대조용, 출처: Crisis Group).",
                 "북미 정상외교·국내 정치 사건은 지수 밖 — 완화는 남북 회담만.",
                 "반복 발사·정책 문서처럼 국제 보도는 적지만 군사 신호가 큰 달은 봉수가 GPR보다 높다(행동 vs 관심).")


def _check(scenario):
    if scenario not in SCENARIOS:
        raise ValueError(f"시나리오는 {list(SCENARIOS)} 중 하나: {scenario}")


def stage_names():
    """(화면) 단계 이름 — config.STAGE_NAMES(화면 설정)가 있으면 그것, 없으면 평온~심각."""
    return getattr(config, "STAGE_NAMES", {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"})


def relief_delta(scenario="기본", days=None, data_dir=DATA_DIR) -> pd.Series:
    """(화면) 완화 할인 δ — 사건표로 ⑦ δ를 다시 계산(결과 CSV `완화할인` 열은 T⁺ = 0인 날 0이라 화면 설명에 안 맞음, 사용자 10-29)."""
    _check(scenario)
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    if days is None:
        days = pd.DatetimeIndex(daily_raw(scenario, data_dir).index)
    comp, _ = core.tension_components(events, pd.DatetimeIndex(days), list(SCENARIOS[scenario]))
    return comp["delta"]


def daily_raw(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 결과 일별 CSV 그대로(날짜 인덱스) — 그림 함수용."""
    _check(scenario)
    return tio.read_csv_kr(Path(data_dir) / f"일별_{scenario}.csv", index_col=0, parse_dates=True)


def daily(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 일별 — 결과 열 전부 + 화면 이름 열. `날짜`는 열(datetime).

    더하는 열: 평소대비(= T_표시7일) · 평소대비_원값(= T_원값) · 원점수(= 원점수_게이지) · 최종단계(= 단계_최종) ·
    단계이름 · 지속일수(4거 이상 며칠째) · 상위%_표시(첫 365일 NaN) · 완화할인_δ.
    """
    raw = daily_raw(scenario, data_dir)
    d = raw.reset_index()
    d["평소대비"] = d["T_표시7일"]
    d["평소대비_원값"] = d["T_원값"]
    d["원점수"] = d["원점수_게이지"]
    d["최종단계"] = d["단계_최종"].astype("int64")
    d["단계이름"] = d["최종단계"].map(stage_names())
    d["지속일수"] = sm.stage_streak(d["최종단계"]).to_numpy()
    top = d["그날까지_상위%"].astype(float).copy()
    top.iloc[:TOP_PCT_HIDE_DAYS] = np.nan
    d["상위%_표시"] = top
    d["완화할인_δ"] = relief_delta(scenario, raw.index, data_dir).round(3).to_numpy()
    return d


def _period(fname, scenario, data_dir):
    _check(scenario)
    t = tio.read_csv_kr(Path(data_dir) / fname)
    t = t[t["시나리오"] == scenario].drop(columns="시나리오").reset_index(drop=True)
    t["평소대비"] = t["T_평균"]
    t["원점수"] = t["원점수_평균"]
    t["최종단계"] = t["단계_최고"]
    return t


def monthly(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 월별 — 월별.csv의 그 시나리오 + 화면 이름 열(평소대비 = T_평균 · 원점수 = 원점수_평균 · 최종단계 = 단계_최고)."""
    return _period("월별.csv", scenario, data_dir)


def yearly(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 연도별 — 연도별.csv의 그 시나리오 + 화면 이름 열(월별과 같음)."""
    return _period("연도별.csv", scenario, data_dir)


def summary(data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 요약 — 요약.csv 그대로(행 = 지표, 열 = 기본·확장(C5 포함), 값은 글자)."""
    return tio.read_csv_kr(Path(data_dir) / "요약.csv", index_col=0, dtype=str, keep_default_na=False)


def cuts(scenario="기본", data_dir=DATA_DIR) -> tuple:
    """(화면) T 구간 4개(2·3·4·5거 시작) — 요약.csv `T구간(2·3·4·5거 시작)`에서. 숫자를 코드에 적지 않는다(ADR-018 규칙으로 매번 뽑음)."""
    _check(scenario)
    text = summary(data_dir).loc["T구간(2·3·4·5거 시작)", SUMMARY_COLUMN[scenario]]
    return tuple(int(float(v)) for v in text.split("/"))


def stage_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 단계 기준표 — 단계 · 이름 · T 구간(이상) · 봉수 원뜻 · 하한으로 켜지는 경우(문턱은 config 값으로 씀)."""
    c = cuts(scenario, data_dir)
    names = stage_names()
    pf, ef = config.PHYS_FLOOR, config.E5_FLOOR
    floors = {1: "—", 2: "—",
              3: f"핵실험·ICBM(S≥{config.EVENT_FLOOR_ICBM_S:g}) 당일 · 물리 충돌 원점수 ≥ {pf['3거']:g} · "
                 f"풍선 ≥ {pf['풍선3거']:g} · 북러 밀착 ≥ {ef['3거']:g}",
              4: f"물리 충돌 원점수 ≥ {pf['4거']:g} · 4거 유형 사건 당일(침범·교전·사상자) · 북러 밀착 ≥ {ef['4거']:g}",
              5: "사망·침몰 당일(천안함·연평도)"}
    return pd.DataFrame({"단계": [1, 2, 3, 4, 5],
                         "이름": [f"{k}거 · {names[k]}" for k in range(1, 6)],
                         "T 구간(이상)": [0, *c],
                         "봉수 원뜻": [STAGE_MEANING[k] for k in range(1, 6)],
                         "하한으로 켜지는 경우": [floors[k] for k in range(1, 6)]})


def crisis_marks(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
    """(화면) 위기 눈금 — 내부 위기 10건의 날짜·종류·14일 안 최고 단계·게이지 눈금(요약.csv에서)."""
    _check(scenario)
    s = summary(data_dir)[SUMMARY_COLUMN[scenario]]
    return pd.DataFrame({"위기": [n for n, _, _ in config.CRISIS_LIST],
                         "날짜": pd.to_datetime([d for _, d, _ in config.CRISIS_LIST]),
                         "종류": [k for _, _, k in config.CRISIS_LIST],
                         "단계": [int(s[n]) for n, _, _ in config.CRISIS_LIST],
                         "게이지 눈금": [float(s[f"게이지_{n}"]) for n, _, _ in config.CRISIS_LIST]})


@lru_cache(maxsize=1)
def _actor_map(processed_dir=PROCESSED_DIR) -> dict:
    """(보조) 사건ID → 주체국 — data/processed 아래 CSV 중 사건ID·주체국 열이 있는 것(처음 나온 값)."""
    out = {}
    for f in sorted(Path(processed_dir).glob("*/*.csv")):
        try:
            t = tio.read_csv_kr(f, dtype=str, keep_default_na=False, usecols=lambda c: c in ("사건ID", "주체국"))
        except (ValueError, UnicodeDecodeError):
            continue
        if {"사건ID", "주체국"} <= set(t.columns):
            for k, v in zip(t["사건ID"], t["주체국"]):
                if k and v and k not in out:
                    out[k] = v
    return out


def contributions(day=None, scenario="기본", top=10, data_dir=DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(화면) 점수 구성 — (묶음별 표, 사건별 남은 점수 상위 top건). day = 기준일(None이면 마지막 날, 그 전 마지막 날 기준).

    묶음별: 상승 묶음 T_g · 상승 지수 T⁺(평균) · 완화 할인 δ · T. 사건별: 남은 점수 = S · 2^(−경과일/반감기),
    구분 = 상승 / 완화(할인) / 하한 대상(물리 충돌·북러 밀착 — T에 더하지 않고 하한에만) / 표시만.
    """
    d = daily(scenario, data_dir)
    day = d["날짜"].iloc[-1] if day is None else pd.Timestamp(day)
    row = d[d["날짜"] <= day].iloc[-1]
    bundles = list(SCENARIOS[scenario])
    tg = [float(row[f"Tg_{b}"]) for b in bundles]
    t_plus = float(np.mean(tg))
    table = pd.DataFrame({"항목": [*bundles, "상승 지수 T⁺(평균)", "완화 할인 δ", "T = T⁺ × (1 − δ)"],
                          "값": [*tg, t_plus, float(row["완화할인_δ"]), float(row["T_원값"])],
                          "설명": [*["묶음별 평소 대비(평소 = 100)"] * len(bundles), "상승 묶음의 평균",
                                 "남북 회담(F2)에 따른 할인율(0~0.5)", "그날 긴장도 원값"]})
    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
    ev = events[events["date"] <= row["날짜"]].copy()
    ev["경과일"] = (row["날짜"] - ev["date"]).dt.days
    ev["남은점수"] = (ev["S"] * 2.0 ** (-ev["경과일"] / config.HALF_LIFE_DAYS)).round(3)
    ev["구분"] = ev["묶음"].map(lambda b: "상승" if b in bundles else KIND.get(b, "그 밖"))
    actors = _actor_map()
    ev["주체국"] = ev["사건ID"].map(lambda k: actors.get(k, UNKNOWN_ACTOR))
    ev = ev.sort_values(["남은점수", "date"], ascending=[False, False]).head(top)
    ev = ev.rename(columns={"date": "날짜"})[["날짜", "사건ID", "요소", "묶음", "구분", "S", "남은점수", "주체국", "사건명"]]
    return table, ev.reset_index(drop=True)


def figure(scenario="기본", data_dir=DATA_DIR):
    """(화면) 추이 그림 — charts.trend_figure. 기본이면 확장을 점선으로 겹친다(사용자 10-29: 기본이 주)."""
    from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
    compare = daily_raw("확장", data_dir) if scenario == "기본" else None
    return charts.trend_figure(daily_raw(scenario, data_dir), cuts(scenario, data_dir), compare=compare)
```

## 부록 C. `utils/tension/charts.py` (글자 그대로 저장)
```python
"""긴장도 그림 (F4) — Plotly Figure를 돌려준다. Streamlit을 모른다(화면은 st.plotly_chart(fig)로 올림, 단독은 save_html).

추이 그림(사용자 10-29): 위 = T 구간 가로 띠 + 표시선(7일 평균)·원값 + 위기 세로선 + A2 자료 끝 빗금,
아래 = 단계_최종 색 띠(하한·하강 유예로 T 띠보다 높은 날이 보이게).
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import config

# 단계 색·이름은 화면 설정 config.STAGE_COLORS·STAGE_NAMES를 그릴 때 읽는다(사용자 10-29 — 색을 한 곳에서). 아래는 config에 없을 때만 쓰는 값
STAGE_COLORS = {1: "#4CAF50", 2: "#2196F3", 3: "#FBC02D", 4: "#FB8C00", 5: "#E53935"}
STAGE_NAMES = {1: "평온", 2: "관심", 3: "주의", 4: "경계", 5: "심각"}
LINE_MAIN, LINE_RAW, LINE_COMPARE, INK = "#26215C", "#7F77DD", "#B3541E", "#444441"


def _stage_colorscale(colors):
    """(보조) 단계 1~5를 끊어진 색으로 — z 범위 0.5~5.5."""
    scale = []
    for k in range(1, 6):
        lo, hi = (k - 1) / 5, k / 5
        scale += [[lo, colors[k]], [hi, colors[k]]]
    return scale


def trend_figure(daily, cuts, *, compare=None, compare_name="확장(C5 포함) 7일 평균", crises=config.CRISIS_LIST,
                 a2_end=config.A2_DATA_END, colors=None, names=None, title=None, height=620) -> go.Figure:
    """(그림) 추이 — daily = 일별 표(날짜 인덱스), cuts = T 구간 4개(2·3·4·5거 시작), compare = 비교할 다른 일별 표(선택).

    colors·names를 주지 않으면 config.STAGE_COLORS·STAGE_NAMES(없으면 이 모듈의 기본값).
    """
    colors = colors or getattr(config, "STAGE_COLORS", STAGE_COLORS)
    names = names or getattr(config, "STAGE_NAMES", STAGE_NAMES)
    cuts = [float(c) for c in cuts]
    x = daily.index
    top = max(float(daily["T_원값"].max()), cuts[-1]) * 1.08
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.88, 0.12], vertical_spacing=0.03)
    a2 = pd.Timestamp(a2_end)
    if x[-1] > a2:   # A2 자료 끝 빗금
        fig.add_trace(go.Scatter(x=[a2, x[-1], x[-1], a2, a2], y=[0, 0, top, top, 0], fill="toself", mode="lines",
                                 line=dict(width=0), fillcolor="rgba(0,0,0,0)",
                                 fillpattern=dict(shape="/", fgcolor="#9A9A94", size=8, solidity=0.15),
                                 name=f"A2 자료 없음({a2_end} 이후)", hoverinfo="skip"), row=1, col=1)
    custom = list(zip(daily["화면_단계문구"], daily["그날까지_상위%"].round(1)))
    fig.add_trace(go.Scatter(x=x, y=daily["T_원값"], mode="lines", line=dict(color=LINE_RAW, width=0.6), opacity=0.45,
                             name="T 원값(단계 판정)", hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=daily["T_표시7일"], mode="lines", line=dict(color=LINE_MAIN, width=1.6),
                             name="표시선 = 7일 평균", customdata=custom,
                             hovertemplate="%{x|%Y-%m-%d}<br>표시 %{y:.1f}<br>%{customdata[0]}<br>그날까지 상위 %{customdata[1]}%<extra></extra>"),
                  row=1, col=1)
    if compare is not None:
        fig.add_trace(go.Scatter(x=compare.index, y=compare["T_표시7일"], mode="lines",
                                 line=dict(color=LINE_COMPARE, width=1, dash="dash"), opacity=0.8, name=compare_name,
                                 hovertemplate="%{x|%Y-%m-%d} %{y:.1f}<extra>" + compare_name + "</extra>"), row=1, col=1)
    for name, date, _ in crises:   # 위기 세로선
        t = pd.Timestamp(date)
        if x[0] <= t <= x[-1]:
            fig.add_vline(x=t, line=dict(color=INK, width=0.6), row=1, col=1)
            fig.add_annotation(x=t, y=top * 0.98, text=name, textangle=-90, showarrow=False, xanchor="right",
                               yanchor="top", font=dict(size=10, color=INK), row=1, col=1)
    edges = [0.0, *cuts, top]   # T 구간 가로 띠·문턱선 — 선을 넣은 뒤에 그린다(Plotly는 빈 칸에 띠를 그리지 않음)
    for k in range(1, 6):
        fig.add_hrect(y0=edges[k - 1], y1=edges[k], fillcolor=colors[k], opacity=0.10, line_width=0, layer="below",
                      row=1, col=1)
    for k, c in zip(range(2, 6), cuts):
        fig.add_hline(y=c, line=dict(color=INK, width=0.6, dash="dot"), row=1, col=1,
                      annotation_text=f"{k}거 {c:g}", annotation_position="top left", annotation_font_size=10)
    L = daily["단계_최종"].astype(int)
    fig.add_trace(go.Heatmap(x=x, y=["최종 단계"], z=[L.to_list()], zmin=0.5, zmax=5.5,
                             colorscale=_stage_colorscale(colors), showscale=False,
                             customdata=[[f"{v}거 {names[v]}" for v in L]],
                             hovertemplate="%{x|%Y-%m-%d} %{customdata}<extra>최종 단계</extra>", name="최종 단계"),
                  row=2, col=1)
    fig.update_yaxes(range=[0, top], title_text="평소 = 100", row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=2, col=1)
    fig.update_layout(height=height, title=title, hovermode="x unified", margin=dict(l=10, r=10, t=90 if title else 50, b=10),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), plot_bgcolor="white")
    return fig


def save_html(fig, path) -> Path:
    """(그림) HTML 파일로 저장 — Streamlit 없이 확인용. plotly.js는 CDN(인터넷 필요, 파일 작음)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn")
    return path
```

## 부록 D. `$B/loader_block.txt` — `utils/loader.py` 끝에 붙일 블록 (글자 그대로 저장)
```python
# ===== [F5 추가 · 긴장도 담당] 긴장도 결과 통로 — data/tension 결과 CSV(utils/tension/screen.py) =====
# 위 기존 함수(load_daily 등)는 그대로 둔다. 화면 담당자가 화면을 고칠 때 아래 함수로 바꾼다(요청서 docs/dev/requests/).
from utils.tension import screen as tension_screen   # noqa: E402


@st.cache_data
def load_tension_daily(scenario="기본"):  # 일별 — 결과 열 + 화면 이름 열(평소대비·평소대비_원값·원점수·최종단계·단계이름·지속일수·상위%_표시·완화할인_δ)
    return tension_screen.daily(scenario)


@st.cache_data
def load_tension_monthly(scenario="기본"):  # 월별 — 평소대비 = T_평균 · 원점수 = 원점수_평균 · 최종단계 = 단계_최고
    return tension_screen.monthly(scenario)


@st.cache_data
def load_tension_yearly(scenario="기본"):  # 연도별 — 월별과 같은 열
    return tension_screen.yearly(scenario)


@st.cache_data
def load_tension_summary():  # 요약 — 행 = 지표, 열 = 기본·확장(C5 포함)
    return tension_screen.summary()


@st.cache_data
def load_tension_stage_table(scenario="기본"):  # 단계 기준표 — 단계·이름·T 구간(이상)·봉수 원뜻·하한으로 켜지는 경우
    return tension_screen.stage_table(scenario)


@st.cache_data
def load_tension_crisis_marks(scenario="기본"):  # 위기 10건 — 날짜·종류·14일 최고 단계·게이지 눈금
    return tension_screen.crisis_marks(scenario)


@st.cache_data
def load_tension_contrib(day=None, scenario="기본", top=10):  # 점수 구성 — (묶음별 표, 사건별 남은 점수 상위 top건)
    return tension_screen.contributions(day, scenario, top)


@st.cache_data
def load_tension_figure(scenario="기본"):  # 추이 그림(Plotly) — st.plotly_chart(load_tension_figure())
    return tension_screen.figure(scenario)
```

## 부록 E. `$B/append_loader.py` (글자 그대로 저장)
```python
"""F5 3절 — utils/loader.py 끝에 긴장도 결과 함수 블록(부록 D)을 붙인다. 기존 줄은 한 글자도 바꾸지 않는다. 리포 루트에서.
사용: python append_loader.py <부록 D를 저장한 파일>   — 이미 붙어 있으면 멈춤. 줄바꿈 LF."""
import sys
from pathlib import Path

MARK = "# ===== [F5 추가 · 긴장도 담당] 긴장도 결과 통로"
p = Path("utils/loader.py")
old = p.read_bytes().decode("utf-8")
block = Path(sys.argv[1]).read_bytes().decode("utf-8").replace("\r\n", "\n")
if MARK in old:
    sys.exit("멈춤: 이미 F5 블록이 있음 — 아무것도 쓰지 않음")
if not block.lstrip("\n").startswith(MARK):
    sys.exit("멈춤: 부록 D 첫 줄이 표시 줄이 아님 — 저장한 파일 확인")
old = old.replace("\r\n", "\n")
p.write_bytes((old.rstrip("\n") + "\n\n\n" + block.lstrip("\n")).encode("utf-8"))   # 기존 끝 + 빈 줄 2개 + 블록
print("utils/loader.py: F5 블록 붙임")
```

## 부록 F. `tests/test_screen.py` (글자 그대로 저장)
```python
"""screen.py·loader 새 함수 테스트(F5) — 커밋된 결과 CSV(data/tension)를 화면 모양으로 읽는지. Streamlit 화면은 test_app_smoke.py."""
import numpy as np
import pandas as pd
import pytest

import config
from utils.tension import core, io as tio, screen

ROOT = screen.ROOT


@pytest.fixture(scope="module")
def d():
    return screen.daily("기본")


def test_daily_screen_columns(d):
    raw = screen.daily_raw("기본")
    assert len(d) == len(raw) and d["날짜"].tolist() == list(raw.index)
    assert list(d.columns[:len(raw.columns) + 1]) == ["날짜", *raw.columns]          # 결과 열은 그대로 앞에
    assert d["평소대비"].equals(d["T_표시7일"]) and d["평소대비_원값"].equals(d["T_원값"])
    assert d["원점수"].equals(d["원점수_게이지"]) and (d["최종단계"] == d["단계_최종"]).all()
    assert set(d["단계이름"]) <= set(config.STAGE_NAMES.values())


def test_streak_and_top_pct(d):
    on = (d["최종단계"] >= 4).to_numpy()
    assert ((d["지속일수"] > 0).to_numpy() == on).all()
    i = int(np.argmax(on))                                                            # 처음 4거 이상인 날
    assert d["지속일수"].iloc[i] == 1
    assert d["상위%_표시"].iloc[:365].isna().all() and d["상위%_표시"].iloc[365:].notna().all()
    assert d["상위%_표시"].iloc[365:].equals(d["그날까지_상위%"].iloc[365:].astype(float))


def test_relief_delta_matches_core(d):
    tg = d[[f"Tg_{b}" for b in config.BUNDLES_BASE]].mean(axis=1)
    on = tg > 0
    assert float((d.loc[on, "완화할인_δ"] - d.loc[on, "완화할인"]).abs().max()) < 0.0011   # T⁺ > 0이면 CSV 열과 같음
    assert int(((tg == 0) & (d["완화할인_δ"] > 0)).sum()) > 0                               # T⁺ = 0이어도 δ가 나옴
    assert d["완화할인_δ"].between(0, config.RELIEF_CAP).all()


def test_periods_and_cuts():
    m, y = screen.monthly("기본"), screen.yearly("확장")
    assert "시나리오" not in m.columns and m["평소대비"].equals(m["T_평균"]) and m["최종단계"].equals(m["단계_최고"])
    assert y["연도"].iloc[0] == 2010 and y["원점수"].equals(y["원점수_평균"])
    assert screen.cuts("기본") == (115, 256, 315, 378) and screen.cuts("확장") == (110, 237, 314, 374)
    with pytest.raises(ValueError):
        screen.cuts("다른것")


def test_stage_table_and_crisis():
    t = screen.stage_table("기본")
    assert t["T 구간(이상)"].tolist() == [0, 115, 256, 315, 378]
    assert t["이름"].tolist()[0] == f"1거 · {config.STAGE_NAMES[1]}" and len(t) == 5
    c = screen.crisis_marks("기본")
    assert len(c) == len(config.CRISIS_LIST) and c.loc[c["위기"] == "6차 핵", "게이지 눈금"].item() == 33.8


def test_contributions(d):
    table, ev = screen.contributions("2026-10-29", "기본", top=10)
    row = d.iloc[-1]
    assert table["값"].iloc[-1] == row["T_원값"] and len(table) == len(config.BUNDLES_BASE) + 3
    assert len(ev) == 10 and ev["남은점수"].is_monotonic_decreasing
    first = ev.iloc[0]
    k = (pd.Timestamp("2026-10-29") - first["날짜"]).days
    assert first["남은점수"] == round(first["S"] * 2 ** (-k / config.HALF_LIFE_DAYS), 3)
    assert set(ev["구분"]) <= {"상승", "완화(할인)", "하한 대상", "표시만", "그 밖"}
    _, before = screen.contributions("2026-09-25", "기본")                             # 기준일 뒤 사건은 빠짐
    assert (before["날짜"] <= "2026-09-25").all()


def test_unknown_actor():
    actors = screen._actor_map()
    for k in ("F2-0668", "E5-8978", "E5-8981", "E5-8983", "E5-8986"):
        assert k not in actors
    ev, _ = tio.load_events(ROOT / "data" / "tension" / "events_확장.csv")
    hit = ev["사건ID"].map(lambda k: k in actors)
    assert int((~hit).sum()) == 5


def test_figure_uses_config_colors():
    f = screen.figure("기본")
    assert [t.name for t in f.data][-2:] == ["확장(C5 포함) 7일 평균", "최종 단계"]
    scale = [c for _, c in f.data[-1].colorscale]
    assert [scale[2 * (k - 1)] for k in range(1, 6)] == [config.STAGE_COLORS[k] for k in range(1, 6)]


def test_loader_functions_match_screen():
    from utils import loader
    assert loader.load_tension_daily("기본").equals(screen.daily("기본"))
    assert loader.load_tension_stage_table().equals(screen.stage_table())
    t1, e1 = loader.load_tension_contrib("2026-10-29")
    t2, e2 = screen.contributions("2026-10-29")
    assert t1.equals(t2) and e1.equals(e2)
    assert callable(loader.load_daily) and callable(loader.load_monthly)                # 기존 함수 그대로
```

## 부록 G. `tests/test_app_smoke.py` (글자 그대로 저장)
```python
"""화면 AppTest(F5, U10) — 화면 브랜치를 합친 뒤 홈과 페이지 4개가 예외 없이 뜨는지. 화면 코드는 고치지 않는다(담당 파일 원칙)."""
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ["홈.py", "pages/1_긴장도_지수.py", "pages/2_사건_기록.py", "pages/3_월별_연별.py", "pages/4_보고서.py"]


@pytest.mark.parametrize("path", SCREENS)
def test_screen_runs_without_exception(path):
    at = AppTest.from_file(str(ROOT / path), default_timeout=120).run()
    assert not at.exception, [e.value for e in at.exception]
```
