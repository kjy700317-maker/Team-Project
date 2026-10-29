# F4 작업 프롬프트 — 결과 산출: 요약·월별·연도별(summary.py) · 추이 그림(charts.py) · run_tension 인자 · 결과 CSV·사건표 커밋

작성 2026-10-29 · 구현 메인(채팅 ④) → Claude Code · 브랜치 **`feature/tension-output`(PR #21 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행** — PR #21은 10-29 05:32 UTC 병합 확인(일반 merge `c807dcc`). 10-29 사용자 결정 반영: 사건표 커밋 · 월별 CSV 커밋 · 요약 함수 새 모듈 `summary.py` · 추이 그림(T 구간 띠 + 최종 단계 띠 + 위기선 + A2 빗금) · 결과 열 이름은 우리 이름 그대로(화면 이름으로 바꿔 읽기는 F5) · 월별·연도별 열 제안대로 · 옛 원격 브랜치 4개 삭제
권장 모델·노력: **Opus 5.5 · 중간**(파일은 부록 그대로 저장 + 실행·커밋 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F4_20261029`.
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. F3에서 설치한 로컬 `commit-msg` 훅이 있는지 1절에서 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 8절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`utils/tension/core.py`·`utils/tension/io.py`·`config.py`·`requirements.txt`·`홈.py`·`pages/` 수정**(테스트가 실패하면 코드를 고치지 말고 보고). 부록 파일은 **글자 그대로** — md5 기대값과 다르면 다시 저장(코드 블록을 파이썬으로 잘라 **LF로** 저장해도 된다).

---

## 0. 목표
- 부록 파일을 리포에 글자 그대로 저장하고, 결과 CSV를 처음으로 만들어 커밋한다. 코드와 테스트는 구현 메인이 리포 밖에서 최신 develop(`c807dcc`) 코드에 얹어 돌려 통과시킨 것이다 `[확인 10-29: python 3.13 · pandas 3.0.5 · plotly 7.1 → 73 passed / python 3.10 · pandas 2.3.3에서 run_tension 출력 5개 파일 md5가 같음]`.
  - `utils/tension/summary.py`(부록 A, 새 파일): 요약(`summary_values`·`summary_table` — v0.1.4 `요약_v014`와 같은 행 이름·순서·반올림), 월별·연도별(`period_table`·`period_tables`), 지속일수(`stage_streak`)
  - `utils/tension/charts.py`(부록 B, 새 파일): 추이 그림 `trend_figure`(T 구간 가로 띠·문턱선 · 표시선·원값 · 비교 시나리오 점선 · 위기 10건 세로선 · A2 자료 끝 빗금 · 아래 `단계_최종` 색 띠) · `save_html`. Streamlit을 모른다
  - `scripts/run_tension.py`(부록 C, 덮어씀): 인자 `--end`·`--events-dir`·`--out`·`--scenario`·`--figure`. 기본 출력 = `data/tension/일별_기본.csv`·`일별_확장.csv`·`요약.csv`·`월별.csv`·`연도별.csv`
  - 테스트: `tests/test_summary.py`(부록 D, 6개) · `tests/test_charts.py`(부록 E, 4개) · `tests/test_regression.py`(부록 F, 덮어씀 — 요약 계산을 `summary.py`로 바꾸고 요약 글자 비교·바이트 비교·연도별 대조 추가, run_tension은 임시 폴더로 출력해 5개 파일 확인 — 16개) · 기준 파일 `tests/fixtures/v014_연도별_기본.csv`·`_확장.csv`(로컬 v0.1.4 바이트 복사) · `tests/fixtures/README.md`(부록 G, 덮어씀)
  - 사건표 커밋 전환(사용자 10-29): `.gitignore`·`CLAUDE.md` 2절 한 줄씩(부록 H 스크립트) + `data/tension/events_기본.csv`·`events_확장.csv` 커밋. 제외기록·입력 파일 기록은 계속 깃 제외
  - 결과 CSV 5개 커밋(D1). 끝날 = **실행일**(U3 — `config.END_DATE = None`). 2026-10-27까지는 v0.1.4와 같아야 한다(부록 I 확인)
- **기대 결과:** `<py> -m pytest` → **73 passed**(기존 61 − 옛 회귀 14 + 새 회귀 16 + test_summary 6 + test_charts 4). `-m "not regression"` → 57 passed · 16 deselected.

## 1. 시작 점검 · 옛 브랜치 삭제 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F4_20261029"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관 · 한글 경로가 "\354…"처럼 보여도 같은 것): " M docs/dev/진행기록.md", "?? docs/dev/tasks/F4_output.md", "?? .obsidian/"
git branch --show-current                          # 기대: feature/tension-tests
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 21 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop                # 기대: c807dcc(이후 커밋이 있으면 log에 적고 계속)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 develop으로
for f in docs/dev/진행기록.md docs/dev/tasks/F4_output.md; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git restore docs/dev/진행기록.md
git switch develop
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함

# 1-2 옛 브랜치 삭제(사용자 10-29 — 병합된 기능 브랜치 4개, README 5절 "머지가 완료된 서브 브랜치는 원격 및 로컬에서 삭제")
for b in feature/tension-scaffold feature/tension-io feature/tension-core feature/tension-tests; do
  git merge-base --is-ancestor "origin/$b" origin/develop && echo "$b 병합됨" || echo "$b 병합 안 됨 — 이 브랜치는 지우지 말고 log에 적음"
done
git push origin --delete feature/tension-scaffold feature/tension-io feature/tension-core feature/tension-tests   # 위에서 "병합 안 됨"이 나온 것은 빼고
for b in feature/tension-scaffold feature/tension-io feature/tension-core feature/tension-tests; do
  git show-ref --verify --quiet "refs/heads/$b" && git branch -d "$b"
done                                               # -d가 거부하면(병합 안 됨) 지우지 말고 log에 적음 — -D 금지
git branch -a | grep -E 'tension-(scaffold|io|core|tests)' || echo "옛 브랜치 없음"

# 1-3 되살리기 → 브랜치
for f in docs/dev/진행기록.md docs/dev/tasks/F4_output.md; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-output
# 1-4 이슈: 본문 "$B/issue_F4.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 0절 목록, 완료 조건 = 7절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F4.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 긴장도 결과 산출·그림(F4)" --label feat --body-file "$B/issue_F4.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__)"
#   plotly가 없으면 멈추고 보고(pip install 금지 — requirements.txt에 plotly>=5.0.0이 이미 있음)
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 61 passed(F3까지)
ls data/tension/events_기본.csv data/tension/events_확장.csv   # 있어야 함 — 없으면 멈추고 보고
```
**커밋 1** `docs: F4 작업 프롬프트·설계 문서 반영` — `docs/dev/tasks/F4_output.md`, `docs/dev/진행기록.md`(내용 수정 없이 — U2). 8절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 코드·테스트 파일 저장 (부록 A~G — 모두 저장한 뒤 3절에서 한꺼번에 돌린다)
| 부록 | 저장 위치 | md5 |
|---|---|---|
| A | `utils/tension/summary.py`(새) | `6eb4a579c02888890d5292999c5fc491` |
| B | `utils/tension/charts.py`(새) | `857005aac710e298e6ac7c6207ba6f20` |
| C | `scripts/run_tension.py`(덮어씀) | `ad2e6a34aa170011ba6d748e552a452e` |
| D | `tests/test_summary.py`(새) | `808683758a51fbec56e09c51c6916ae3` |
| E | `tests/test_charts.py`(새) | `89c2211a115a9a4b38c4fffc56a59744` |
| F | `tests/test_regression.py`(덮어씀) | `80adf9b5ae72c24be3ca0bd73a96bcee` |
| G | `tests/fixtures/README.md`(덮어씀) | `ed7473f6d3989d7cd7c48066279e796b` |
```bash
md5sum utils/tension/summary.py utils/tension/charts.py scripts/run_tension.py tests/test_summary.py tests/test_charts.py tests/test_regression.py tests/fixtures/README.md   # 위 표와 모두 같아야 함
# 기준 파일 2개 — 로컬 v0.1.4 연도별을 바이트 그대로 복사(원본은 읽기만)
for n in 기본 확장; do cp "진행 현황 및 계획 정리/v0.1_시험/v0.1.4/연도별_v014_$n.csv" "tests/fixtures/v014_연도별_$n.csv"; done
md5sum tests/fixtures/v014_연도별_*.csv
#   기대: 9750f27e12002a7679238d28889631a8 (기본, 432바이트) · ea32176480a978fc92ae5e414a731a77 (확장, 430바이트)
git diff --stat                                    # run_tension.py·test_regression.py·fixtures/README.md만(진행기록 등 다른 것 없음)
```

## 3. 테스트
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_summary.py tests/test_charts.py   # 기대: 10 passed
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_regression.py                     # 기대: 16 passed
PYTHONIOENCODING=utf-8 <py> -m pytest                                              # 기대: 73 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                          # 기대: 57 passed, 16 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest                      # 기대: 73 passed(경고 0)
git status --porcelain                             # 테스트가 리포 안에 파일을 만들지 않아야 함(run_tension 시험은 임시 폴더)
```
- 기대와 다르면 테스트도 코드도 고치지 말고 실패 출력 전부를 log에 남기고 멈추고 보고한다. `test_charts`만 실패하고 메시지가 `fillpattern` 관련이면 plotly 버전(1-4 출력)을 적는다(빗금은 plotly 5.7 이상 기능 `[해석]`).

**커밋 2** `feat: 요약·월별·연도별 집계(summary.py)` — `utils/tension/summary.py`
**커밋 3** `feat: 긴장도 추이 그림(charts.py)` — `utils/tension/charts.py`
**커밋 4** `feat: run_tension 인자·결과 CSV 출력` — `scripts/run_tension.py`
**커밋 5** `test: 요약·그림 테스트·연도별 기준 파일` — `tests/test_summary.py`, `tests/test_charts.py`, `tests/test_regression.py`, `tests/fixtures/v014_연도별_기본.csv`, `tests/fixtures/v014_연도별_확장.csv`, `tests/fixtures/README.md`. 스테이징 뒤 `git ls-files --eol tests/fixtures/v014_연도별_*.csv` → 두 줄 모두 `i/lf` · `attr/text eol=lf`.

## 4. 사건표 커밋 전환 (부록 H)
```bash
# 커밋할 사건표가 원자료에서 다시 만든 것과 같은지 먼저 확인(리포 밖으로 출력)
PYTHONIOENCODING=utf-8 <py> scripts/build_events.py --out-dir "$B/ev"
for n in 기본 확장; do cmp "$B/ev/events_$n.csv" "data/tension/events_$n.csv" && echo "events_$n 같음"; done
#   다르면 멈추고 보고(사건표를 바꾸지 않는다). build_events.py 인자 이름이 다르면 --help를 log에 적고 멈춤
# 부록 H를 "$B/edit_ignore_claude.py"로 저장(md5 d0e78b9fa366c2976a916f22d5b9404a), 리포 루트에서
PYTHONIOENCODING=utf-8 <py> "$B/edit_ignore_claude.py"     # 기대: ".gitignore: 바꿈" · "CLAUDE.md: 바꿈"
git diff .gitignore CLAUDE.md | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '
#   기대: .gitignore − 2줄(사건표 주석·events_*.csv) + 3줄(새 주석·events_제외기록.csv·events_입력파일.csv), CLAUDE.md − 1줄 + 1줄(2절 data/tension 줄)
git check-ignore -v data/tension/events_기본.csv data/tension/events_확장.csv || echo "사건표 2개 추적 대상"
git check-ignore -q data/tension/events_제외기록.csv data/tension/events_입력파일.csv && echo "제외기록·입력파일 계속 제외"
git add .gitignore CLAUDE.md data/tension/events_기본.csv data/tension/events_확장.csv
git ls-files --eol data/tension/events_*.csv        # 기대: 두 줄 모두 i/lf · attr/text eol=lf
```
**커밋 6** `chore: 사건표 기본·확장 깃 추적 시작` — `.gitignore`, `CLAUDE.md`, `data/tension/events_기본.csv`, `data/tension/events_확장.csv`(이 커밋의 금지 경로 검사는 8절의 "커밋 6용").

## 5. 결과 CSV 산출 · 확인 (부록 I)
```bash
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --figure data/tension/_check
#   기대: "계산 기간 2010-01-01 ~ <실행일>" · [기본] T구간 115/256/315/378 · [확장] T구간 110/237/314/374 · 사건 720·941행 · load 제외 0
#         · 쓴 파일 일별_기본·일별_확장·요약·월별·연도별 · 그림 data/tension/_check/추이_기본.html·추이_확장.html
# 부록 I를 "$B/check_results.py"로 저장(md5 cd661e111c5e2fa9ff321c4a73b79e60), 리포 루트에서
PYTHONIOENCODING=utf-8 <py> "$B/check_results.py"          # 기대: 마지막 줄 "전체: 통과"
git status --porcelain
#   기대: "?? data/tension/일별_기본.csv" "?? data/tension/일별_확장.csv" "?? data/tension/요약.csv" "?? data/tension/월별.csv" "?? data/tension/연도별.csv" "?? .obsidian/"
#   (_check/ 아래 HTML은 깃 제외라 보이지 않아야 함)
git add data/tension/일별_기본.csv data/tension/일별_확장.csv data/tension/요약.csv data/tension/월별.csv data/tension/연도별.csv
git ls-files --eol data/tension/일별_*.csv data/tension/요약.csv data/tension/월별.csv data/tension/연도별.csv   # 기대: 모두 i/lf · attr/text eol=lf
```
- `check_results.py`가 실패하면 결과를 커밋하지 말고 출력 전부를 log에 남기고 멈춘다.
- 그림 확인(선택, 사용자): `data/tension/_check/추이_기본.html`을 브라우저로 연다(plotly.js를 CDN에서 받으므로 인터넷 필요). 보고서에 "사용자 화면 확인 = 했음/안 함"만 적는다 — 그림을 고치지 않는다.

**커밋 7** `feat: 긴장도 결과 CSV 첫 산출` — 위 5개 파일. 커밋 메시지 본문에 한 줄: `끝날 <실행일> · 모델 v0.1.4 · run_tension.py 기본값`.

## 6. 하지 않는 것
- `core.py`·`io.py`·`config.py`·`requirements.txt` 수정(그림 색은 `charts.py` 안 상수 — F5에서 화면 config와 합칠지 정한다)
- 화면(`홈.py`·`pages/`·`utils/loader.py` 등) 연결 — F5. 화면 브랜치(`feature/tension-dashboard`)를 건드리거나 합치지 않는다
- 부록과 다른 함수·테스트를 더하거나 빼기, 그림 모양 바꾸기(고치고 싶은 것은 보고서 3절)
- `data/tension/_check/` 아래 파일 커밋

## 7. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #21 MERGED, 훅 있음, 61 passed, plotly 버전 적음 |
| 2 | 1-2 옛 브랜치 | 원격·로컬 4개 삭제(병합 안 된 것이 있으면 남기고 적음) |
| 3 | 1-3·1-4 | 새 브랜치 `feature/tension-output`, 이슈 번호 |
| 4 | 2절 | 부록 7개 md5 모두 같음, 연도별 기준 2개 md5 같음 |
| 5 | 3절 | 10 / 16 / 73 passed · not regression 57/16 · FutureWarning 경고 0 · 테스트 뒤 리포에 새 파일 없음 |
| 6 | 4절 | 다시 만든 사건표 = 커밋할 사건표(cmp 같음), .gitignore·CLAUDE.md diff가 기대대로, 사건표 2개 추적·제외기록·입력파일 제외, eol LF |
| 7 | 5절 | run_tension 출력 기대대로, `check_results.py` "전체: 통과", 결과 5개 eol LF |
| 8 | 커밋 | 8절 순서 7개 + 보고서 |
| 9 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 10 | 8절 AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 11 | 마지막 status | `?? .obsidian/` 하나만 |

## 8. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
# 커밋 1~5·7용
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
# 커밋 6용(사건표 2개만 허용)
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F4 작업 프롬프트·설계 문서 반영` 2. `feat: 요약·월별·연도별 집계(summary.py)` 3. `feat: 긴장도 추이 그림(charts.py)` 4. `feat: run_tension 인자·결과 CSV 출력` 5. `test: 요약·그림 테스트·연도별 기준 파일` 6. `chore: 사건표 기본·확장 깃 추적 시작` 7. `feat: 긴장도 결과 CSV 첫 산출` 8. `docs: F4 보고서`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 73 passed
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고(히스토리 고치지 않음)" || echo "OK"
git push -u origin feature/tension-output
# 본문 "$B/pr_F4.md" = .github/pull_request_template.md 양식 · closes #<1-4 이슈> · 변경 = 0절 목록 · 테스트 = 7절 결과(73 passed, check_results 통과)
#   · 체크리스트 아래에 팀원 안내 두 줄:
#     "결과 CSV(data/tension/일별_기본·일별_확장·요약·월별·연도별)와 사건표(events_기본·확장)가 이제 커밋됩니다. 화면 연결은 F5에서 합니다."
#     "사건을 바꾸면: scripts/build_events.py → scripts/run_tension.py → 결과 CSV 커밋(자세한 절차는 F7 운영 문서)."
grep -inE "$AI" "$B/pr_F4.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 결과 산출·그림(F4)" --body-file "$B/pr_F4.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 9. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F4_report.md`(60줄 이내): 1절 = 7절 표 11행 ✓/✗ · 결과 끝날·마지막 날 화면 단계(기본·확장) · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F4_log.md`: 1~5절 출력 전부(옛 브랜치 삭제 출력, md5, 테스트, cmp, check_results), 커밋·푸시·PR 출력.

---

## 부록 A. `utils/tension/summary.py` (글자 그대로 저장)
```python
"""요약·월별·연도별·지속일수 (F4) — 일별 결과(core.daily_table 출력)를 모으는 집계 함수.

식 ①~⑰은 core.py. 여기는 일별 표를 세고 평균 내는 일만 한다(규칙 없음). Streamlit·파일 경로를 모른다.
요약 행 이름·순서는 v0.1.4 `요약_v014.csv`(tests/fixtures/v014_요약.csv)와 같다.
"""
import numpy as np
import pandas as pd

import config
from utils.tension import core

PERIOD_COLUMNS = ("일수", "T_평균", "T표시_최고", "원점수_평균", "단계_최고", "단계_평균",
                  "1거일", "2거일", "3거일", "4거일", "5거일")
SUMMARY_NOTE = "A2 자료 {end}까지 — 그 뒤 미사일·ICBM 사건 하한 없음"


def stage_streak(L, min_stage=4) -> pd.Series:
    """(집계) 지속일수 — 단계_최종이 min_stage 이상인 날이 오늘까지 며칠째 이어지는지(아니면 0)."""
    on = (L >= min_stage).to_numpy()
    out = np.zeros(len(on), dtype="int64")
    run = 0
    for i, v in enumerate(on):
        run = run + 1 if v else 0
        out[i] = run
    return pd.Series(out, index=L.index, name="지속일수")


def period_table(daily, freq) -> pd.DataFrame:
    """(집계) 월별(freq="월") 또는 연도별(freq="연") — PERIOD_COLUMNS. T·원점수 3자리, 단계_평균 2자리."""
    if freq == "월":
        key, label = daily.index.strftime("%Y-%m"), "연월"
    elif freq == "연":
        key, label = daily.index.year, "연도"
    else:
        raise ValueError(f"freq는 '월' 또는 '연': {freq}")
    L = daily["단계_최종"].astype("int64")
    g = pd.DataFrame({"T": daily["T_원값"], "Tb": daily["T_표시7일"], "R": daily["원점수_게이지"], "L": L}).groupby(key)
    out = pd.DataFrame({
        "일수": g.size().astype("int64"),
        "T_평균": g["T"].mean().round(3),
        "T표시_최고": g["Tb"].max().round(3),
        "원점수_평균": g["R"].mean().round(3),
        "단계_최고": g["L"].max().astype("int64"),
        "단계_평균": g["L"].mean().round(2),
        **{f"{k}거일": g["L"].apply(lambda s, k=k: int((s == k).sum())).astype("int64") for k in range(1, 6)},
    })
    out.index.name = label
    return out.reset_index()


def period_tables(dailies, freq) -> pd.DataFrame:
    """(집계) 시나리오 여러 개를 한 표로 — 첫 열 `시나리오`. dailies = {시나리오 이름: 일별 표}(순서 유지)."""
    parts = [period_table(d, freq).assign(시나리오=name) for name, d in dailies.items()]
    out = pd.concat(parts, ignore_index=True)
    return out[["시나리오", *[c for c in out.columns if c != "시나리오"]]]


def summary_values(daily, info, days, bundles, *, input_name, n_type4, base_period=config.BASE_PERIOD,
                   crises=config.CRISIS_LIST, relief_cap=config.RELIEF_CAP, a2_end=config.A2_DATA_END) -> dict:
    """(집계) 요약 한 열 — v0.1.4 `요약_v014.csv`와 같은 행 이름·순서·반올림. 현재 행 이름은 끝날(`현재(MM-DD)`)."""
    L = daily["단계_최종"]
    bm = core.base_mask(days, base_period)
    last = daily.iloc[-1]
    stages = core.crisis_window_max(L, crises)
    marks = core.crisis_window_max(daily["원점수_게이지"], crises)
    other = daily[["단계_T", "하한_물리", "하한_사건"]].max(axis=1)
    v = {"입력": input_name, "묶음": " · ".join(bundles), "기준기간": f"{base_period[0]}~{base_period[1]}",
         **{f"B_{b}": round(float(x), 3) for b, x in info["B"].items()},
         "T구간(2·3·4·5거 시작)": "/".join(f"{x:g}" for x in info["cuts"]),
         "T구간_반올림전": "/".join(f"{x:.2f}" for x in info["quantiles_raw"]),
         "경계_x.5_주의": bool(info["half_warning"]),
         **{f"{k}거%": round((L == k).mean() * 100, 1) for k in range(1, 6)},
         "바뀜/년": round((L.diff().fillna(0) != 0).sum() / (len(days) / 365.25), 1),
         **{name: int(stages[name]) for name, _, _ in crises},
         "2018 평균단계": round(L.loc["2018"].mean(), 2), "2018 3거이상일": int((L.loc["2018"] >= 3).sum()),
         "2021 평균단계": round(L.loc["2021"].mean(), 2),
         "2023 4거이상%": round((L.loc["2023"] >= 4).mean() * 100, 0), "2023 5거%": round((L.loc["2023"] == 5).mean() * 100, 0),
         f"현재({days[-1]:%m-%d})": int(L.iloc[-1]),
         "사건하한 날 수": int((daily["하한_사건"] > 1).sum()), "물리 4거유형 사건일 수": int(daily["물리_4거유형일"].sum()),
         "E5하한 3거↑ 날": int((daily["하한_E5"] >= 3).sum()), "E5가 판정을 올린 날": int((daily["하한_E5"] > other).sum()),
         "물리하한 3거↑ 날": int((daily["하한_물리"] >= 3).sum()), "물리하한 4거↑ 날": int((daily["하한_물리"] >= 4).sum()),
         "물리하한 5거 날": int((daily["하한_물리"] == 5).sum()),
         "완화 상한에 붙은 날": int((info["components"]["delta"] >= relief_cap - 1e-12).sum()),
         "원점수 기준기간 평균": round(float(daily["원점수_게이지"][bm].mean()), 2),
         **{f"게이지_{name}": round(float(marks[name]), 1) for name, _, _ in crises},
         "T원값 최대": round(daily["T_원값"].max()), "표시선 최대": round(daily["T_표시7일"].max()),
         "현재 표시(잠정)": round(last["T_표시7일"], 1), "현재 그날까지 상위%": round(last["그날까지_상위%"], 1),
         "현재 원점수": round(last["원점수_게이지"], 1), "현재 14일 변화": round(last["변화14_표시"], 1),
         "현재 화면 단계": last["화면_단계문구"], "비고": SUMMARY_NOTE.format(end=a2_end),
         "4거유형 사건 수": int(n_type4)}
    return v


def summary_table(columns) -> pd.DataFrame:
    """(집계) 요약 표 — columns = {열 이름: summary_values 결과}(순서 유지). 행은 첫 열 순서, 뒤 열에만 있는 행은 끝에."""
    rows = [{"시나리오": name, **vals} for name, vals in columns.items()]
    out = pd.DataFrame(rows).set_index("시나리오").T
    out.columns.name = None
    return out
```

## 부록 B. `utils/tension/charts.py` (글자 그대로 저장)
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

# 화면 브랜치(feature/tension-dashboard) config.STAGE_COLORS·STAGE_NAMES와 같은 값 — F5에서 config 한 곳으로 합칠지 정한다
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
                 a2_end=config.A2_DATA_END, colors=STAGE_COLORS, names=STAGE_NAMES, title=None, height=620) -> go.Figure:
    """(그림) 추이 — daily = 일별 표(날짜 인덱스), cuts = T 구간 4개(2·3·4·5거 시작), compare = 비교할 다른 일별 표(선택)."""
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

## 부록 C. `scripts/run_tension.py` (글자 그대로 저장)
```python
"""긴장도 계산(F4) — 사건표 → 결과 CSV(일별·요약·월별·연도별) + 추이 그림(선택).

기본: data/tension/events_기본.csv·_확장.csv → data/tension/일별_기본.csv·일별_확장.csv·요약.csv·월별.csv·연도별.csv
(결과 CSV는 커밋 — D1). 끝날 기본값은 config.END_DATE(None = 실행일, U3). 회귀 검산은 --end 2026-10-27.

사용: python scripts/run_tension.py [--end YYYY-MM-DD] [--events-dir DIR] [--out DIR] [--scenario 기본 확장] [--figure DIR]
  --figure DIR : 추이_<시나리오>.html을 DIR에 저장(확인용 — 커밋하지 않는 data/tension/_check 권장)
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from utils.tension import core  # noqa: E402
from utils.tension import io as tio  # noqa: E402
from utils.tension import summary as sm  # noqa: E402

# 시나리오 이름 → (요약 열 이름, 묶음) — 요약 열 이름은 v0.1.4 요약과 같게
SCENARIOS = {"기본": ("기본", config.BUNDLES_BASE), "확장": ("확장(C5 포함)", config.BUNDLES_EXT)}
DATA_DIR = ROOT / config.TENSION_DATA_DIR


def _end_date(text):
    """--end 값 검사 — YYYY-MM-DD 형식의 실제 날짜만(F2 검토 9)."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise argparse.ArgumentTypeError(f"YYYY-MM-DD 형식이 아님: {text}")
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"없는 날짜: {text}") from None
    return text


def _run(end, events_dir, out_dir, names, figure_dir) -> None:
    table = tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH)
    type4 = tio.type4_event_ids(table)
    if not type4:
        raise ValueError("판정표에 4거 유형(Y) 사건이 없음")
    days = core.calc_days(config.CALC_START_DATE, end)
    print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")
    results = []
    for name in names:
        label, bundles = SCENARIOS[name]
        path = events_dir / f"events_{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"사건표 없음: {path} - scripts/build_events.py로 먼저 만든다")
        events, excluded = tio.load_events(path)
        problems = tio.check_type4_against_events(table, events)
        if len(problems):
            listed = "; ".join(f"{r.사건ID} {r.문제}" for r in problems.head(10).itertuples())
            raise ValueError(f"[{name}] 판정표와 사건표가 맞지 않음 {len(problems)}건: {listed}")
        daily, info = core.daily_table(events, days, bundles, type4)
        vals = sm.summary_values(daily, info, days, bundles, input_name=path.name, n_type4=len(type4))
        results.append((name, label, events, excluded, daily, info, vals))
    # 모든 시나리오가 계산된 뒤에만 쓴다(중간에 멈추면 아무 파일도 바꾸지 않음)
    for name, label, events, excluded, daily, info, vals in results:
        out = out_dir / f"일별_{name}.csv"
        tio.write_csv(daily.round(3), out, index=True)
        print(f"[{name}] 사건 {len(events)}행 · load 제외 {len(excluded)} · T구간 {vals['T구간(2·3·4·5거 시작)']}"
              f" · 마지막 날 {daily['화면_단계문구'].iloc[-1]}")
        print(f"  쓴 파일: {out}")
        if info["half_warning"]:
            print("  경고: T 구간 분위가 정확히 x.5 - 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")
    tio.write_csv(sm.summary_table({label: vals for _, label, *_, vals in results}), out_dir / "요약.csv", index=True)
    dailies = {name: daily for name, _, _, _, daily, _, _ in results}
    tio.write_csv(sm.period_tables(dailies, "월"), out_dir / "월별.csv")
    tio.write_csv(sm.period_tables(dailies, "연"), out_dir / "연도별.csv")
    print(f"  쓴 파일: {out_dir / '요약.csv'} · 월별.csv · 연도별.csv")
    if figure_dir is not None:
        from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
        for name, label, _, _, daily, info, _ in results:
            compare = dailies.get("확장") if name == "기본" else None
            fig = charts.trend_figure(daily, info["cuts"], compare=compare,
                                      title=f"봉수 긴장도 {config.TENSION_MODEL_VERSION} · {label} · {days[-1]:%Y-%m-%d}")
            print(f"  그림: {charts.save_html(fig, figure_dir / f'추이_{name}.html')}")


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):   # cp949 콘솔에 없는 글자가 있어도 멈추지 않게(F2 검토 6)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="사건표 → 일별·요약·월별·연도별 결과 CSV")
    p.add_argument("--end", default=config.END_DATE, type=_end_date, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
    p.add_argument("--events-dir", type=Path, default=DATA_DIR, help="사건표 폴더(events_<시나리오>.csv)")
    p.add_argument("--out", type=Path, default=DATA_DIR, help="결과 폴더")
    p.add_argument("--scenario", nargs="+", choices=list(SCENARIOS), default=list(SCENARIOS), help="계산할 시나리오")
    p.add_argument("--figure", type=Path, default=None, help="추이 그림 HTML 폴더(없으면 그리지 않음)")
    args = p.parse_args(argv)
    names = [n for n in SCENARIOS if n in args.scenario]   # 순서는 기본 → 확장
    try:
        _run(args.end, args.events_dir, args.out, names, args.figure)
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"멈춤: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 부록 D. `tests/test_summary.py` (글자 그대로 저장)
```python
"""summary.py 단위 테스트(F4) — 작은 합성 일별 표로 집계 규칙 확인(사건표 없이 돈다)."""
import numpy as np
import pandas as pd
import pytest

from utils.tension import summary as sm


def _daily(stages, start="2024-12-30"):
    days = pd.date_range(start, periods=len(stages), name="날짜")
    n = len(stages)
    return pd.DataFrame({"T_원값": np.arange(n, dtype=float), "T_표시7일": np.arange(n, dtype=float) * 2,
                         "원점수_게이지": np.full(n, 1.5), "단계_최종": stages}, index=days)


def test_stage_streak_counts_and_resets():
    s = sm.stage_streak(pd.Series([1, 4, 5, 4, 3, 4, 4]))
    assert s.tolist() == [0, 1, 2, 3, 0, 1, 2]
    assert sm.stage_streak(pd.Series([3, 3, 2]), min_stage=3).tolist() == [1, 2, 0]


def test_period_table_month_and_year():
    d = _daily([1, 2, 3, 4, 5])                     # 2024-12-30 ~ 2025-01-03
    m = sm.period_table(d, "월")
    assert list(m.columns) == ["연월", *sm.PERIOD_COLUMNS]
    assert m["연월"].tolist() == ["2024-12", "2025-01"] and m["일수"].tolist() == [2, 3]
    assert m["T_평균"].tolist() == [0.5, 3.0] and m["T표시_최고"].tolist() == [2.0, 8.0]
    assert m["단계_최고"].tolist() == [2, 5] and m["단계_평균"].tolist() == [1.5, 4.0]
    assert m[["1거일", "2거일", "3거일", "4거일", "5거일"]].sum(axis=1).tolist() == [2, 3]
    y = sm.period_table(d, "연")
    assert y["연도"].tolist() == [2024, 2025] and y["원점수_평균"].tolist() == [1.5, 1.5]


def test_period_table_rounding():
    d = _daily([1, 2, 2], start="2025-01-01")
    d["T_원값"] = [1.00049, 1.0, 1.0]
    assert sm.period_table(d, "연")["T_평균"].iloc[0] == round(np.mean([1.00049, 1.0, 1.0]), 3)
    assert sm.period_table(d, "연")["단계_평균"].iloc[0] == 1.67


def test_period_table_bad_freq():
    with pytest.raises(ValueError):
        sm.period_table(_daily([1]), "주")


def test_period_tables_scenario_column():
    t = sm.period_tables({"기본": _daily([1, 2, 3]), "확장": _daily([3, 4, 5])}, "월")   # 2024-12·2025-01 걸침
    assert t.columns[0] == "시나리오" and t["시나리오"].tolist() == ["기본", "기본", "확장", "확장"]


def test_summary_table_row_union_order():
    t = sm.summary_table({"기본": {"a": 1, "b": 2}, "확장": {"a": 3, "b": 4, "c": 5}})
    assert list(t.index) == ["a", "b", "c"] and list(t.columns) == ["기본", "확장"]
    assert pd.isna(t.loc["c", "기본"])
```

## 부록 E. `tests/test_charts.py` (글자 그대로 저장)
```python
"""charts.py 테스트(F4) — Streamlit 없이 Figure를 만들고 HTML로 저장되는지(사건표 없이 돈다)."""
import subprocess
import sys
from pathlib import Path

import plotly.graph_objects as go

from utils.tension import charts, io as tio

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
CUTS = (115, 256, 315, 378)


def _daily(name="기본"):
    return tio.read_csv_kr(FIX / f"v014_일별_{name}.csv", index_col=0, parse_dates=True)


def test_trend_figure_parts():
    fig = charts.trend_figure(_daily(), CUTS, compare=_daily("확장"))
    assert isinstance(fig, go.Figure)
    names = [t.name for t in fig.data]
    assert names == ["A2 자료 없음(2024-11-05 이후)", "T 원값(단계 판정)", "표시선 = 7일 평균",
                     "확장(C5 포함) 7일 평균", "최종 단계"]
    rects = [s for s in fig.layout.shapes if s.type == "rect"]
    assert len(rects) == 5                                         # T 구간 띠 5개
    texts = [a.text for a in fig.layout.annotations]
    assert [f"{k}거 {c}" for k, c in zip(range(2, 6), CUTS)] == [t for t in texts if "거 " in t]
    assert "천안함" in texts and "2026-09 DMZ 지뢰" in texts           # 위기 10건 세로선 이름
    assert list(fig.data[-1].z[0]) == _daily()["단계_최종"].tolist()   # 아래 띠 = 단계_최종


def test_trend_figure_without_a2_period():
    d = _daily().loc[:"2024-06-30"]
    fig = charts.trend_figure(d, CUTS)
    assert [t.name for t in fig.data] == ["T 원값(단계 판정)", "표시선 = 7일 평균", "최종 단계"]


def test_save_html(tmp_path):
    out = charts.save_html(charts.trend_figure(_daily(), CUTS), tmp_path / "a" / "추이.html")
    assert out.exists() and out.stat().st_size > 10_000
    assert "plotly" in out.read_text(encoding="utf-8").lower()


def test_charts_does_not_import_streamlit():
    code = "import sys; import utils.tension.charts; assert 'streamlit' not in sys.modules"
    p = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
```

## 부록 F. `tests/test_regression.py` (글자 그대로 저장)
```python
"""v0.1.4 회귀(F3·F4) — 사건표로 계산한 일별·요약·연도별이 tests/fixtures의 v0.1.4 기준과 같은지.

사건표(data/tension/events_기본·확장.csv)는 F4부터 커밋한다(사용자 10-29). 그래도 없으면 **실패**한다 — 실패 메시지에 만드는 법을 적는다.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import config
from utils.tension import core, io as tio, summary as sm

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
END = "2026-10-27"
SCEN = {"기본": ("기본", config.BUNDLES_BASE), "확장": ("확장(C5 포함)", config.BUNDLES_EXT)}
ROWS = {"기본": 720, "확장": 941}
INT_COLS = ["단계_T", "하한_물리", "하한_E5", "하한_사건", "단계_판정", "단계_최종"]
BOOL_COLS = ["잠정", "물리_4거유형일"]
STR_COLS = ["A2자료", "화면_단계문구"]
RAW_DIR = ROOT / "data" / "raw" / "긴장도_산출식_세부_기준"


def _events_path(name):
    return ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv"


def _missing():
    return [_events_path(n).relative_to(ROOT).as_posix() for n in SCEN if not _events_path(n).exists()]


def _missing_message(missing):
    raw = "있음" if RAW_DIR.exists() else "없음 — 팀 드라이브에서 받아 이 위치에 둔다"
    return (f"회귀 테스트 입력 사건표가 없다: {missing}\n"
            f"  사건표는 커밋된다(F4) — git pull로 받거나 원자료로 만든다. 원자료 {RAW_DIR.relative_to(ROOT).as_posix()}/ : {raw}\n"
            f"  만들기: python scripts/build_events.py --end {END}  → 그다음 pytest 다시\n"
            f"  회귀만 빼고 돌리기: python -m pytest -m \"not regression\"")


def test_events_present():
    """사건표가 있어야 회귀가 돈다 — 없으면 이 테스트 하나가 원인과 만드는 법을 알리며 실패하고 나머지는 건너뛴다."""
    missing = _missing()
    if missing:
        pytest.fail(_missing_message(missing), pytrace=False)


@pytest.fixture(scope="module")
def computed():
    if _missing():
        pytest.skip("사건표 없음 — test_events_present의 실패 메시지 참고")
    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
    days = core.calc_days(config.CALC_START_DATE, END)
    out = {}
    for name, (_, bundles) in SCEN.items():
        events, excluded = tio.load_events(_events_path(name))
        daily, info = core.daily_table(events, days, bundles, type4)
        out[name] = {"events": events, "excluded": excluded, "daily": daily, "info": info}
    return {"days": days, "type4": type4, "res": out}


def _ref_daily(name):
    return tio.read_csv_kr(FIX / f"v014_일별_{name}.csv", index_col=0, parse_dates=True)


def _diff_cells(new, ref, tol=0.001):
    """열마다 (다른 칸 수, 처음 다른 날짜 5개). 실수 = |차| ≥ tol 또는 NaN 위치 다름 · 그 밖 = 값 다름(문자열 빈칸 = '')."""
    bad = {}
    for c in ref.columns:
        a, b = new[c], ref[c]
        if c in INT_COLS:
            m = a.to_numpy("int64") != b.to_numpy("int64")
        elif c in BOOL_COLS:
            m = a.to_numpy(bool) != b.to_numpy(bool)
        elif c in STR_COLS:
            m = a.fillna("").astype(str).to_numpy() != b.fillna("").astype(str).to_numpy()
        else:
            av, bv = a.to_numpy(float), b.to_numpy(float)
            m = (np.isnan(av) != np.isnan(bv)) | (np.abs(np.nan_to_num(av) - np.nan_to_num(bv)) >= tol)
        if m.any():
            bad[c] = (int(m.sum()), [f"{d:%Y-%m-%d}" for d in ref.index[m][:5]])
    return bad


def _summary_csv(computed, tmp_path, input_names=None):
    """summary.py로 만든 요약을 CSV로 쓰고 문자열로 다시 읽는다(기준 파일과 글자 그대로 비교)."""
    cols = {}
    for name, (label, bundles) in SCEN.items():
        r = computed["res"][name]
        inp = (input_names or {}).get(name, f"events_{name}.csv")
        cols[label] = sm.summary_values(r["daily"], r["info"], computed["days"], bundles, input_name=inp,
                                        n_type4=len(computed["type4"]))
    out = tmp_path / "요약.csv"
    tio.write_csv(sm.summary_table(cols), out, index=True)
    return out


def _read_str(path):
    return tio.read_csv_kr(path, index_col=0, dtype=str, keep_default_na=False)


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_events_loaded(computed, name):
    r = computed["res"][name]
    assert len(r["excluded"]) == 0, r["excluded"].head()
    assert len(r["events"]) == ROWS[name]


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_daily_shape(computed, name):
    daily, ref = computed["res"][name]["daily"], _ref_daily(name)
    assert list(daily.columns) == list(ref.columns)
    assert daily.index.name == "날짜" and len(daily) == 6144
    assert np.array_equal(daily.index.to_numpy(), ref.index.to_numpy())


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_daily_all_columns_match_v014(computed, name):
    bad = _diff_cells(computed["res"][name]["daily"], _ref_daily(name))
    assert not bad, f"v0.1.4와 다른 열(칸 수, 처음 날짜): {bad}"


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_completion_criteria(computed, name):
    """지시서 0절 완료 기준 — 단계_최종 다른 날 0, T_원값 최대 절대차 < 0.001."""
    daily, ref = computed["res"][name]["daily"], _ref_daily(name)
    assert int((daily["단계_최종"].to_numpy() != ref["단계_최종"].to_numpy()).sum()) == 0
    assert float((daily["T_원값"] - ref["T_원값"]).abs().max()) < 0.001


def test_summary_matches_v014(computed, tmp_path):
    """요약 = v0.1.4 요약과 행 이름·순서·값이 글자 그대로 같다(입력 행만 파일 이름이 다름)."""
    got = _read_str(_summary_csv(computed, tmp_path))
    ref = _read_str(FIX / "v014_요약.csv")
    assert list(got.index) == list(ref.index) and list(got.columns) == list(ref.columns)
    diff = got.drop(index="입력").compare(ref.drop(index="입력"))
    assert diff.empty, f"요약이 다름:\n{diff}"
    assert list(got.loc["입력"]) == ["events_기본.csv", "events_확장.csv"]


def test_summary_bytes_match_v014(computed, tmp_path):
    """입력 이름을 v0.1.4와 같게 주면 요약 CSV가 바이트까지 같다(인코딩·줄바꿈·숫자 표기)."""
    out = _summary_csv(computed, tmp_path, {"기본": "사건표_v014_기본.csv", "확장": "사건표_v014_확장.csv"})
    assert out.read_bytes() == (FIX / "v014_요약.csv").read_bytes()


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_yearly_matches_v014(computed, name):
    """연도별 = v0.1.4 연도별_v014(T원값_평균·평균단계·사거이상일·오거일)."""
    y = sm.period_table(computed["res"][name]["daily"], "연")
    ref = tio.read_csv_kr(FIX / f"v014_연도별_{name}.csv")
    assert y["연도"].tolist() == ref["연도"].tolist()
    assert float((y["T_평균"] - ref["T원값_평균"]).abs().max()) <= 0.0051   # 기준은 2자리, 새 값은 3자리
    assert y["단계_평균"].tolist() == ref["평균단계"].tolist()
    assert (y["4거일"] + y["5거일"]).tolist() == ref["사거이상일"].tolist()
    assert y["5거일"].tolist() == ref["오거일"].tolist()


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_end_extension_keeps_past(computed, name):
    r, days = computed["res"][name], computed["days"]
    longer, _ = core.daily_table(r["events"], core.calc_days(config.CALC_START_DATE, "2026-11-10"), SCEN[name][1], computed["type4"])
    assert longer.loc[days].drop(columns="잠정").equals(r["daily"].drop(columns="잠정"))
    assert int((longer.loc[days, "잠정"] != r["daily"]["잠정"]).sum()) == config.PROVISIONAL_DAYS


def test_run_tension_output_matches_v014(computed, tmp_path):
    """run_tension.py --end 2026-10-27 --out <임시> → 일별 2개·요약·월별·연도별이 v0.1.4와 맞는다."""
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", END, "--out", str(tmp_path)],
                       cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    for name in SCEN:
        out = tmp_path / f"일별_{name}.csv"
        raw = out.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
        assert raw == (FIX / f"v014_일별_{name}.csv").read_bytes()
    got, ref = _read_str(tmp_path / "요약.csv"), _read_str(FIX / "v014_요약.csv")
    assert got.drop(index="입력").equals(ref.drop(index="입력"))
    for fname, n in (("월별.csv", 2 * 202), ("연도별.csv", 2 * 17)):
        t = tio.read_csv_kr(tmp_path / fname)
        assert list(t.columns) == ["시나리오", "연월" if fname == "월별.csv" else "연도", *sm.PERIOD_COLUMNS]
        assert len(t) == n and t.groupby("시나리오")["일수"].sum().to_dict() == {"기본": 6144, "확장": 6144}
```

## 부록 G. `tests/fixtures/README.md` (글자 그대로 저장)
```markdown
# tests/fixtures — v0.1.4 회귀 기준 (F3·F4, 2026-10-29)

- `v014_일별_기본.csv`·`v014_일별_확장.csv`: `진행 현황 및 계획 정리/v0.1_시험/v0.1.4/일별_v014_*.csv`를 바이트 그대로 복사(compute_v014.py 2026-10-28, ADR-018 확정판). 2010-01-01~2026-10-27, 6,144일.
- `v014_요약.csv`: `요약_v014.csv` 복사 + 빈칸 `완화 상한에 붙은 날`을 272로 채움(기준 구현 요약의 빈칸 — `docs/dev/식_함수_대응표.md` 4절).
- `v014_연도별_기본.csv`·`v014_연도별_확장.csv`(F4): `연도별_v014_*.csv`를 바이트 그대로 복사. 열 `T원값_평균·평균단계·사거이상일·오거일` — F4 연도별(`T_평균·단계_평균·4거일+5거일·5거일`)과 대조.
- 이 파일들은 고치지 않는다. 규칙이 바뀌어 기준이 바뀌면(새 모델 버전) 새 파일(`v015_…`)을 더하고 ADR에 적는다.
- 회귀 테스트(`tests/test_regression.py`)는 사건표(`data/tension/events_기본·확장.csv`)로 돈다. F4부터 사건표도 커밋한다(사용자 10-29). 그래도 없으면 `test_events_present`가 만드는 법을 알리며 실패한다. 회귀만 빼려면 `python -m pytest -m "not regression"`.
```

## 부록 H. `$B/edit_ignore_claude.py` (글자 그대로 저장)
```python
"""F4 4절 — 사건표 기본·확장을 깃에 올리도록 .gitignore 2줄과 CLAUDE.md 2절 1줄을 바꾼다(사용자 10-29). 리포 루트에서 실행.
줄바꿈(LF/CRLF)은 파일에 있던 그대로 둔다. 바꿀 줄이 정확히 한 번 있지 않으면 아무것도 쓰지 않고 멈춘다."""
import sys
from pathlib import Path

EDITS = {
    ".gitignore": (
        ["# 사건표는 로컬 원자료에서 만든 입력 — 깃에 올리지 않음(D1). 결과 CSV·유형판정표·GPR 월별은 올림",
         "data/tension/events_*.csv"],
        ["# 사건표 기본·확장은 F4부터 커밋(사용자 10-29 — 화면이 사건별 S·묶음을 씀). 제외기록·입력 파일 기록은 로컬만",
         "data/tension/events_제외기록.csv",
         "data/tension/events_입력파일.csv"]),
    "CLAUDE.md": (
        ["data/tension/             # 결과 CSV·유형판정표 사본·GPR 월별 — 커밋. 사건표(events_*.csv)는 깃 제외"],
        ["data/tension/             # 결과 CSV·유형판정표 사본·GPR 월별·사건표(events_기본·확장.csv, F4~) — 커밋. 제외기록·입력파일 기록은 깃 제외"]),
}

out = {}
for name, (old, new) in EDITS.items():
    raw = Path(name).read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    o, n = eol.join(old) + eol, eol.join(new) + eol
    if raw.count(o) != 1:
        sys.exit(f"멈춤: {name}에서 바꿀 줄을 정확히 한 번 찾지 못함({raw.count(o)}번) — 아무 파일도 쓰지 않음")
    out[name] = raw.replace(o, n)
for name, text in out.items():
    Path(name).write_bytes(text.encode("utf-8"))
    print(f"{name}: 바꿈")
```

## 부록 I. `$B/check_results.py` (글자 그대로 저장)
```python
"""F4 5절 — 커밋할 결과(data/tension)가 v0.1.4와 맞는지(2026-10-27까지, 잠정 열 빼고 글자 그대로) · 요약·월별·연도별 모양. 리포 루트에서 실행."""
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from utils.tension import io as tio, summary as sm  # noqa: E402

FIX, D = ROOT / "tests" / "fixtures", ROOT / "data" / "tension"
rd = lambda p: tio.read_csv_kr(p, index_col=0, dtype=str, keep_default_na=False)  # noqa: E731
ok = True
n_days = None
for n in ("기본", "확장"):
    new, ref = rd(D / f"일별_{n}.csv"), rd(FIX / f"v014_일별_{n}.csv")
    part = new.loc[ref.index[0]:ref.index[-1]]
    same = list(new.columns) == list(ref.columns) and part.drop(columns="잠정").equals(ref.drop(columns="잠정"))
    n_days = len(new)
    print(f"[{n}] {new.index[0]} ~ {new.index[-1]} · {len(new)}일 · 2026-10-27까지 v0.1.4와 같음(잠정 빼고): {same}")
    print(f"  마지막 날 화면 단계: {new['화면_단계문구'].iloc[-1]} · 표시 {new['T_표시7일'].iloc[-1]}")
    ok &= same
s, r = rd(D / "요약.csv"), rd(FIX / "v014_요약.csv")
cur = [i for i in s.index if i.startswith("현재(")]
rows_ok = [i if not i.startswith("현재(") else "현재(10-27)" for i in s.index] == list(r.index) and list(s.columns) == list(r.columns)
same_rules = s.loc[["T구간(2·3·4·5거 시작)", "B_핵·미사일", "4거유형 사건 수"]].equals(r.loc[["T구간(2·3·4·5거 시작)", "B_핵·미사일", "4거유형 사건 수"]])
print(f"[요약] 행·열 이름 v0.1.4와 같음(현재 행 이름 빼고): {rows_ok} · 구간·B·판정표 같음: {same_rules} · {cur} = {list(s.loc[cur[0]])}")
ok &= rows_ok and same_rules
for fname, key in (("월별.csv", "연월"), ("연도별.csv", "연도")):
    t = tio.read_csv_kr(D / fname)
    cols_ok = list(t.columns) == ["시나리오", key, *sm.PERIOD_COLUMNS]
    days_ok = t.groupby("시나리오")["일수"].sum().to_dict() == {"기본": n_days, "확장": n_days}
    print(f"[{fname}] {len(t)}행 · 열 맞음: {cols_ok} · 시나리오별 일수 합 = 일별 날 수: {days_ok}")
    ok &= cols_ok and days_ok
print("전체:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
```
