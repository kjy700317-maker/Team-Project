# F0 작업 프롬프트 — 긴장도 코드화 뼈대·규칙

작성 2026-10-28 · 구현 메인 → Claude Code · 브랜치 `feature/tension-scaffold` · PR 대상 `develop`
v2 대조 수정 2026-10-28(새 구현 메인 채팅 — 기준 `진행 현황 및 계획 정리/지시서_구현_메인_긴장도_코드화.md` v2): 미정 번호를 v2 6절 U1~U13으로 바꿈, config 이름을 v2 부록 A.3에 맞춤, 확인 명령 추가 · **사용자 답 반영 2026-10-28**(F0-가·나, U1~U13 — `docs/dev/진행기록.md` 1절)
상태: **실행** (2026-10-28 — conda 환경 `python311` 확인, README 원격본 사용 확인)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요한 곳이 생기면 고치지 말고 보고서 5절에 적고 멈춘다.

---

## 0. 목표
v0.1.4 긴장도 계산을 리포 코드로 옮기기 위한 **빈 틀과 규칙**만 만든다. 계산 코드는 쓰지 않는다(F1~F4 몫).
완료되면: `CLAUDE.md`가 있고, `utils/tension/` 패키지가 import되고, `pytest`가 돌고, `requirements.txt` 버전이 고정되고, `config.py`에 파라미터가 있고, 로컬 전용 폴더가 깃에서 빠진다.

## 1. 시작 전 점검 (먼저 하고 결과를 보고서 0절에 적는다)
```bash
git status --porcelain
git branch --show-current          # develop 이어야 함
git fetch origin
git log --oneline -3 origin/develop
git rev-list --left-right --count develop...origin/develop
conda env list
conda run -n python311 python --version      # 3.11.x 이어야 함
conda run -n python311 python -c "import numpy, pandas, pytest, openpyxl; print(numpy.__version__, pandas.__version__, pytest.__version__, openpyxl.__version__)"
```
- **파이썬:** 이 PC의 기본 `python`은 3.14다(F0-pre). 이 작업의 python·pip·pytest 명령은 **모두 팀 conda 환경 `python311`로** 돌린다 — `conda run -n python311 python …`. 아래 표·부록에 `python`이라고 적힌 곳도 모두 이 뜻이다. 환경이 없거나 3.11이 아니거나 `conda`가 안 되면 멈추고 보고한다.
- **Git Bash 경로 변환:** `git show origin/develop:.gitignore`처럼 `:` 뒤가 `.`으로 시작하면 경로가 바뀌어 실패한다 → `MSYS_NO_PATHCONV=1 git show …`.
- 2026-10-28 F0-pre 보고서(`docs/dev/reports/F0-pre_report.md`)의 상태 `[확인]`: 로컬 `develop`이 원격보다 27커밋 뒤(앞선 커밋 0). 원격에 gitlink 없음, README 충돌 표시 없음(F0-나 해소). 작업트리: 수정 `README.md`·`utils/README.md`·`docs/decisions.md`·`.vscode/settings.json` / 추적 안 됨 `.obsidian/`·`docs/dev/`·`진행 현황 및 계획 정리/`. 이 중 `README.md`·`docs/decisions.md`·`.vscode/settings.json`을 원격도 바꿔 `pull --ff-only`가 막힌다 → 2절 순서로 푼다.
- **위 상태와 다르면**(새 변경 파일, 로컬 앞선 커밋, 원격 추가 변경으로 1-5와 다른 파일이 겹침) 2절을 하지 말고 멈추고 보고한다.

## 2. develop 최신화 · 이슈 · 브랜치 (이 순서 그대로. 한 단계라도 기대와 다르면 멈추고 보고)
```bash
# 2-1 로컬 변경 백업 (리포 밖)
B="$HOME/bongsu_F0_backup_20261028"; mkdir -p "$B"
cp README.md "$B/README.md"; cp utils/README.md "$B/utils_README.md"
cp docs/decisions.md "$B/decisions.md"; cp .vscode/settings.json "$B/settings.json"
git diff HEAD -- README.md utils/README.md > "$B/readme_local.diff"
wc -l "$B"/*          # log에 붙임

# 2-2 원격과 겹치는 로컬 변경 되돌리기 (백업은 2-1에 있음)
git restore README.md utils/README.md docs/decisions.md .vscode/settings.json
git status --porcelain       # 기대: ?? .obsidian/ · ?? docs/dev/ · ?? "진행 현황 및 계획 정리/" 만

# 2-3 최신화
git pull --ff-only origin develop        # 실패하면 멈추고 보고(강제 병합·rebase·stash 금지)
git log --oneline -1                     # a05b019 또는 그 뒤 원격 커밋

# 2-4 개인 편집기 설정 되살리기 (원격 .gitignore의 .vscode/* 로 이제 무시됨)
cp "$B/settings.json" .vscode/settings.json
git check-ignore -v .vscode/settings.json   # 기대: .gitignore:…:.vscode/*

# 2-5 브랜치
git switch -c feature/tension-scaffold

# 2-6 이슈 (README 5절: 작업 전에 이슈)
#   본문 파일 "$B/issue_F0.md"를 .github/ISSUE_TEMPLATE/feature.md 양식(배경·범위·완료 조건 등)으로 쓴다:
#   배경 = 이 프롬프트 0절, 범위 = 3~8절 목록, 하지 않을 것 = 13절, 완료 조건 = 10절 표를 체크박스로.
gh issue create --title "[CHORE] 긴장도 코드화 뼈대(F0)" --label chore --body-file "$B/issue_F0.md"
#   나온 이슈 번호를 보고서 머리와 11절 PR 본문에 쓴다
```
- `README.md`·`utils/README.md`의 로컬 변경은 버리고 원격 본을 쓴다(사용자 결정 10-28 · 백업은 `$B`). `docs/decisions.md`는 8절에서 백업본과 원격 본을 합친다.

## 3. 만들 파일·폴더
| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | 부록 A 블록을 **글자 그대로** |
| `utils/tension/__init__.py` | 부록 B 그대로 |
| `scripts/README.md` | 한 줄: `계산 스크립트 — build_events.py(F1), run_tension.py(F2·F4). 로컬 원자료를 읽으므로 Streamlit 앱에서 import하지 않는다.` |
| `tests/__init__.py` | 빈 파일 |
| `tests/fixtures/.gitkeep` | 빈 파일 |
| `tests/test_smoke.py` | 부록 C 그대로 |
| `pytest.ini` | 부록 D 그대로 |
| `data/tension/.gitkeep` | 빈 파일 (결과 CSV 폴더 — 커밋 대상) |
| `docs/dev/reports/.gitkeep` | 빈 파일 |
| `docs/tension/` 결정 문서 사본 | 4절 |

`utils/__init__.py`는 만들지 않는다(기존 `utils/helpers.py` 구조 유지 — 암묵적 네임스페이스 패키지로 `import utils.tension`이 된다). 팀 기존 코드 `홈.py`·`pages/`·`utils/helpers.py`·`utils/build_db.py`·`utils/build_erd.py`·`db/`는 건드리지 않는다.

## 4. 결정 문서 사본 → `docs/tension/` (복사만, 원본 유지, 내용 수정 금지)
| 원본 (`진행 현황 및 계획 정리/`) | 사본 |
|---|---|
| `긴장도_산출식_정리_v1_2026-10-27.md` | `docs/tension/산출식_정리.md` |
| `인수인계_v0.1.3_통합세션_2026-10-27.md` | `docs/tension/인수인계_v0.1.4.md` |
| `채점_v0_결과_2026-10-28.md` | `docs/tension/채점_v0_결과.md` |
| `단계5_값확정_결정자료_2026-10-28.md` | `docs/tension/단계5_값확정_결정자료.md` |
| `인계_단계5_to_통합세션_2026-10-28.md` | `docs/tension/인계_단계5.md` |
| `S1_하한_완화_결정자료_2026-10-27.md` | `docs/tension/S1_하한_완화_결정자료.md` |
| `S2_사건점수_묶음_결정자료_2026-10-27.md` | `docs/tension/S2_사건점수_묶음_결정자료.md` |
| `S3_척도_단계_표시_결정자료_2026-10-27.md` | `docs/tension/S3_척도_단계_표시_결정자료.md` |
| `감쇠_표시_단계유예_조사_2026-10-27.md` | `docs/tension/감쇠_표시_단계유예_조사.md` |
복사 뒤 각 파일 바이트 크기가 원본과 같은지 확인해 보고서에 표로 적는다(`cmp` 또는 `wc -c`). 문서 안 경로(`진행 현황 및 계획 정리\…`)는 고치지 않는다.

## 5. `.gitignore` — 파일 맨 끝에 아래 블록을 추가 (기존 줄은 그대로)
```gitignore

# --- 긴장도 코드화 (2026-10-28, F0) ---
# 로컬 작업 폴더: 재현 스크립트·백업·중간 CSV (결정 문서 정본은 docs/tension/ 사본 — U8 10-28)
진행 현황 및 계획 정리/
# 사건표는 로컬 원자료에서 만든 입력 — 깃에 올리지 않음(D1). 결과 CSV·유형판정표·GPR 월별은 올림
data/tension/events_*.csv
# 밑줄로 시작하는 중간 파일(기존 data/processed/_* 규칙과 같은 방식)
data/tension/_*
```
확인:
```bash
git check-ignore -v "진행 현황 및 계획 정리/긴장도_산출식_정리_v1_2026-10-27.md"
git check-ignore -v data/tension/events_기본.csv
git check-ignore -v data/raw/processed || true      # 기존 규칙으로 무시돼야 함
git check-ignore data/tension/일별_기본.csv && echo "잘못: 결과 CSV가 무시됨" || echo "정상: 결과 CSV는 추적 대상"
```
주의: 기존 `.gitignore`에 `*.json`이 있다(키 파일 차단). 앞으로 JSON 결과물은 만들지 않는다(CSV로).

## 6. `requirements.txt` — 버전 고정·추가
1. 원격 본은 이미 ASCII(UTF-8 호환)다(F0-pre). 인코딩 변환은 하지 않는다. `file requirements.txt`로 확인만 하고 보고서에 적는다.
2. 바꾸는 줄:
   - `pandas>=2.0.0` → `pandas==<python311 환경의 설치 버전>`
   - `numpy==2.4.6` → 환경 버전과 다르면 **바꾸지 말고** 보고서 5절에 적는다(같으면 그대로).
   - 맨 끝에 `pytest==<환경 버전>`, `openpyxl==<환경 버전>` 추가(F1 `build_events.py`가 xlsx를 읽음). 환경에 없으면 추가하지 말고 멈추고 보고(`pip install` 금지).
   - 나머지 줄(원격에서 추가된 `python-docx>=1.1.0` 포함)은 그대로.
3. 확인: `conda run -n python311 python -m pip install -r requirements.txt --dry-run` 이 오류 없이 끝나야 한다(출력 마지막 5줄을 log에).

## 7. `config.py` — 파라미터 추가
- 기존 줄(`HALF_LIFE_DAYS`, `DEFAULT_PERIOD_MONTHS`, `DB_PATH`)은 **값을 바꾸지 않는다**. `HALF_LIFE_DAYS` 주석만 `# 긴장도 감쇠 반감기 (일) — ADR-006`으로 바꾼다(ADR-001: 이름은 "위험도"가 아니라 "긴장도").
- 파일 끝(“# 3. API 및 기타 설정” 블록 뒤)에 부록 E 블록을 **글자 그대로** 붙인다. 값은 ADR 확정값이다 — 하나라도 바꾸지 않는다. `END_DATE = None`(U3)과 `TREND_DAYS`·`TREND_PCT_MIN` = 14·50(U11)도 10-28 사용자 결정값이다.

## 8. 작업트리의 남의 변경 처리 ← 결정 U2 (10-28) · F0-pre 반영
- `docs/decisions.md`: 원격 본(팀 기록 "2026-10-22 ERD v4…"·"2026-10-22 증감률…" 두 절)과 로컬 ADR(백업 `$B/decisions.md`)을 **내용 수정 없이 이어 붙여** 별도 커밋 `docs: ADR 갱신 반영(v0.1.4까지)`. 순서 = 로컬 ADR 전체 → `---` → 원격 팀 기록 두 절. 아래 스크립트를 `$B/merge_decisions.py`로 저장해 `conda run -n python311 python "$B/merge_decisions.py"`로 실행:
```python
from pathlib import Path
B = Path.home() / "bongsu_F0_backup_20261028"
local = (B / "decisions.md").read_text(encoding="utf-8")
remote_path = Path("docs/decisions.md")                 # pull 뒤 = 원격 본
remote = remote_path.read_text(encoding="utf-8")
team = remote[remote.index("## 2026-10-22 ERD v4"):].rstrip("\n")
merged = local.rstrip("\n") + "\n\n---\n\n" + team + "\n"
for src in (local, remote):
    missing = [l for l in src.splitlines() if l.strip() and l not in merged]
    assert not missing, missing[:3]
remote_path.write_text(merged, encoding="utf-8", newline="")
print(len(local.splitlines()), len(remote.splitlines()), len(merged.splitlines()))
```
  출력 세 숫자를 보고서에 적는다(로컬 줄 수 + 팀 기록 줄 수 + 2 안팎이어야 함). assert가 실패하면 멈추고 보고.
- `.vscode/settings.json`: 2-4에서 되살린 개인 설정 — 이제 `.gitignore`로 무시된다. 스테이징하지 않는다.
- 추적 안 되는 `.obsidian/`(사용자 편집기 폴더): 스테이징하지 않는다. `.gitignore`에도 넣지 않는다.
- 추적 안 되는 `진행 현황 및 계획 정리/`: 5절 `.gitignore`로 빠진다(D4). 스테이징하지 않는다.

## 9. 커밋 (한 커밋 한 목적, 이 순서)
1. `chore: 긴장도 코드화 뼈대와 Claude Code 규칙 추가` — CLAUDE.md, utils/tension, scripts, tests, pytest.ini, data/tension/.gitkeep, docs/dev/**(이 프롬프트·대응표·reports/.gitkeep ·진행기록.md — U2: 이 커밋에 포함), .gitignore
2. `chore: requirements 버전 고정·pytest·openpyxl 추가`
3. `chore: config.py에 긴장도 파라미터 추가`
4. `docs: 긴장도 결정 문서 사본을 docs/tension에 추가`
5. (U2) `docs: ADR 갱신 반영(v0.1.4까지)`
6. `docs: F0 보고서` — 보고서 두 파일(`F0_report.md`·`F0_log.md`)만

매 커밋 전 `git diff --cached --stat` 확인: `data/raw`, `진행 현황 및 계획 정리`, `.env`, `*.json`이 있으면 안 된다.

## 10. 검산 (완료 조건 — 모두 통과해야 "완료")
| # | 명령 | 기대 |
|---|---|---|
| 1 | `python -c "import utils.tension as t; print(t.__doc__.splitlines()[0])"` | 오류 없이 첫 줄 출력 |
| 2 | `python -m pytest -q` | 모두 통과(부록 C 테스트) |
| 3 | `python -c "import config; print(config.BASE_PERIOD, config.STAGE_QUANTILES, config.KILL_EVENTS)"` | `(2010, 2019) (0.7, 0.9, 0.95, 0.98) ('A7-0098', 'A7-0100')` |
| 4 | 5절 `git check-ignore` 네 줄 | 위 설명대로 |
| 5 | `file requirements.txt` | UTF-8 (또는 ASCII) text |
| 6 | 6절 `pip install --dry-run` | 오류 없음 |
| 7 | 4절 사본 크기 대조 | 9개 모두 같음 |
| 8 | `git log --oneline develop..HEAD` (11-1 병합 전에) | 9절 커밋 목록 |
| 9 | `git status --porcelain` | `?? .obsidian/` 하나만(`.vscode/settings.json`·`진행 현황 및 계획 정리/`는 무시돼 안 보임) |
| 10 | `head -1 CLAUDE.md` · `grep -c "^## 8. 참고 위치" CLAUDE.md` | `# CLAUDE.md — 봉수(烽燧) Team-Project · Claude Code 작업 규칙` · `1` |
| 12 | 8절 합치기 스크립트 출력 | 세 숫자, assert 통과 |
| 13 | `git check-ignore -v .vscode/settings.json` | `.vscode/*` 규칙으로 무시 |
| 11 | `ls scripts/README.md tests/__init__.py tests/fixtures/.gitkeep pytest.ini data/tension/.gitkeep docs/dev/reports/.gitkeep` | 6개 모두 출력("No such file" 없음) |

## 11. 동기화·푸시·PR ← 결정 F0-가 · 이슈·PR 규칙 (10-28)
```bash
# 11-1 PR 전 develop 동기화 (README 5절)
git fetch origin
git merge origin/develop          # "Already up to date" 또는 병합 커밋. 충돌 나면:
#   git merge --abort  → 직접 해결하지 말고 멈추고 보고
conda run -n python311 python -m pytest -q     # 병합 뒤 다시 통과 확인
# 11-2 푸시
git push -u origin feature/tension-scaffold
# 11-3 draft PR — 본문 "$B/pr_F0.md"를 .github/pull_request_template.md 양식으로 쓴다
#   (요약 · 관련 이슈 "closes #<2-6 이슈 번호>" · 변경 사항 = 9절 커밋 목록 · 테스트 = 10절 결과 · 체크리스트)
gh pr create --draft --base develop --label chore --title "[CHORE] 긴장도 코드화 뼈대(F0)" --body-file "$B/pr_F0.md"
```
병합하지 않는다. PR 링크를 보고서 머리에 적는다. `gh`가 실패하면 PR 본문을 보고서 7절에 적고 멈춘다.

## 12. 보고서 — `docs/dev/reports/F0_report.md`(요약) + `F0_log.md`(전체)
`CLAUDE.md` 7절 양식. log에는 1·2절 점검 출력, 8절 스크립트 출력, 10절 표의 실제 출력, 11절 출력을 모두 넣는다. report 1절은 10절 표 13행을 ✓/✗로.

## 13. 하지 않는 것
- 계산 코드(`io.py`·`core.py`·`charts.py`), 결과 CSV, 그림 — F1~F4
- `README.md` 수정(폴더 구조 갱신은 F7, 6절 SQLite 문구도 F7 — U12)
- `docs/decisions.md` 내용 수정(8절 이어 붙이기만), `docs/tension/` 사본 내용 수정
- `data/raw/**`, `진행 현황 및 계획 정리/**` 수정
- `develop`·`main`에 직접 커밋·푸시, force push, rebase, stash
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정

---

## 부록 A — `CLAUDE.md` (리포 루트, 글자 그대로)

````markdown
# CLAUDE.md — 봉수(烽燧) Team-Project · Claude Code 작업 규칙

이 리포는 KDT 팀 프로젝트 "봉수"(한반도 군사 긴장도 대시보드, Streamlit)다. Claude Code는 **작업 프롬프트 한 장(`docs/dev/tasks/F<n>_*.md`)을 받아 그것만 수행**한다. 설계·규칙 결정은 구현 메인 세션(별도 Claude 채팅)과 사용자 몫이다.

## 1. 매 세션 시작 순서
1. 받은 작업 프롬프트를 끝까지 읽는다. 프롬프트에 없는 일은 하지 않는다.
2. 이 파일과 `docs/dev/식_함수_대응표.md`(계산 작업일 때)를 읽는다.
3. `git status` · `git branch --show-current` · `git fetch origin`. 작업트리에 내가 만들지 않은 변경이 있으면 **건드리지 않고** 보고서에 적는다.
4. python은 **팀 conda 환경 `python311`로만** 돌린다: `conda run -n python311 python …`(이 PC 기본 `python`은 3.14 — 쓰지 않는다). 버전(3.11.x)과 numpy·pandas 버전을 보고서에 적는다. 환경이 없으면 멈추고 보고.
5. 프롬프트가 정한 브랜치를 프롬프트가 정한 기준 브랜치에서 만든다(F0은 최신 `develop`: `git pull --ff-only origin develop` → `git switch -c feature/<이름>`. F1부터도 앞 기능 PR이 `develop`에 병합된 뒤 최신 `develop`에서 만든다 — U4. 앞 PR이 병합 전이면 시작하지 말고 멈춘다).
6. 같은 리포 폴더에서 다른 Claude Code 세션이 돌고 있으면 시작하지 않는다(폴더 하나 = 체크아웃 브랜치 하나. 병렬 실행은 하지 않는다 — U1).
7. 이슈(README 5절): 프롬프트가 이슈 번호를 주지 않으면 작업 시작 전에 `gh issue create`로 만든다 — 제목 `[말머리] 요약`(FEAT·FIX·DOCS·REFACTOR·CHORE), 라벨은 같은 이름 소문자(`feat`·`fix`·`docs`·`refactor`·`chore`), 본문은 `.github/ISSUE_TEMPLATE/feature.md` 양식. 번호를 보고서에 적는다.

## 2. 구조와 경계
```
config.py                 # 파라미터(값의 근거 = docs/decisions.md ADR 번호). 함수는 인자로 받고 기본값만 config에서
홈.py · pages/            # Streamlit 화면(팀원 코드) — 프롬프트가 지시할 때만 수정
utils/helpers.py · utils/build_db.py · utils/build_erd.py · db/schema.sql   # 팀 기존 코드(화면 공통·DB) — 프롬프트가 지시할 때만 수정
utils/tension/
  io.py                   # 사건표·유형판정표·결과 CSV 로드/검증. 결측·중복은 0점이 아니라 제외 + 기록(ADR-004)
  core.py                 # 식 ①~⑰. 순수 함수(입력 DataFrame → 출력 DataFrame). Streamlit·파일 경로 모름
  charts.py               # Plotly 그림. Streamlit 없이 HTML 저장 가능해야 함
scripts/                  # build_events.py(로컬 원자료 → 사건표), run_tension.py(사건표 → 결과 CSV)
tests/                    # pytest. fixtures/ = v0.1.4 기준값·작은 합성 사건표
data/raw/                 # 로컬 원자료 — 깃 제외, 읽기만
data/tension/             # 결과 CSV·유형판정표 사본·GPR 월별 — 커밋. 사건표(events_*.csv)는 깃 제외
docs/decisions.md         # ADR — 구현 메인 소유
docs/tension/             # 산출식·결정 문서 — 구현 메인 소유
docs/dev/tasks/           # 작업 프롬프트(구현 메인이 씀) / docs/dev/reports/ 보고서(Claude Code가 씀)
docs/dev/진행기록.md       # 단계 6 진행 기록 — 구현 메인 소유, 읽기만
진행 현황 및 계획 정리/      # 로컬 작업 폴더 — 깃 제외, 읽기만. v0.1.4 기준 구현·검산 파일이 여기 있다
```

## 3. 하지 않는 것 (어기면 작업 무효)
- **규칙·설계 변경 금지:** 식, 파라미터 값, 묶음 구성, 판정 순서, 반올림 방식, CSV 열 이름·순서. 기준 구현과 다르게 하고 싶으면 **고치지 말고** 보고서 4절에 적는다. 결과가 안 맞으면 기준값을 고치지 말고 원인을 보고한다.
- `data/raw/**`, `진행 현황 및 계획 정리/**` 수정·커밋.
- `docs/decisions.md`, `docs/tension/**`, `docs/dev/tasks/**`, `docs/dev/진행기록.md`, `docs/dev/식_함수_대응표.md` 내용 수정(프롬프트가 복사를 지시할 때만 복사).
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정(프롬프트가 지시할 때만), 프롬프트에 없는 의존성 추가·`pip install`.
- `main`·`develop`에 직접 커밋·푸시, force push, 히스토리 재작성(rebase 포함), stash, PR 병합.
- `.env`, `secrets/`, 키 파일, `*.json` 커밋. JSON 결과물을 만들지 않는다(CSV로).

## 4. 코드 규칙
- 함수·변수 이름은 영어, CSV 열·묶음·문구는 한국어 그대로(예: `T_원값`, `핵·미사일`, `2거 · 하강 중(판정 1거)` — 가운뎃점은 U+00B7).
- `core.py` 함수 docstring 첫 줄에 식 번호: `"""⑨ T 구간 단계 — 기준기간 T의 70·90·95·98분위를 반올림한 정수로 판정."""`
- 반올림은 기준 구현과 같게(`np.round` 짝수 반올림, `np.quantile` 기본 linear). 정확히 x.5인 분위는 경고(요약 CSV `경계_x.5_주의` 행 — 일별 CSV에 열을 더하지 않는다).
- CSV 읽기·쓰기 모두 `encoding='utf-8-sig'`(U13 — 기준 CSV와 같음. 읽기는 BOM이 있든 없든 됨: v0.1.4 사건표·일별은 BOM 있음, 유형판정표는 없음). 날짜 `YYYY-MM-DD`, 일별 결과 `round(3)`.
- 경로는 `pathlib`로 리포 루트 기준. 한국어 폴더 이름은 따옴표로 감싼다.
- Windows에서 돈다: 줄바꿈·인코딩 차이로 diff가 커지지 않게 한다. Git Bash에서 `git show <브랜치>:.<경로>`처럼 `:` 뒤가 `.`으로 시작하면 `MSYS_NO_PATHCONV=1`을 붙인다.

## 5. 테스트·검산
- 테스트: `conda run -n python311 python -m pytest -q`
- 계산 작업은 프롬프트의 v0.1.4 대조 검산을 반드시 돌리고 명령·출력 요약을 보고서에 붙인다. **검산 없는 "완료" 보고는 통과되지 않는다.**

## 6. 깃
- 브랜치 `feature/<이름>`(프롬프트가 지정). PR 대상 `develop`.
- 커밋 말머리(팀 README): `feat` `fix` `docs` `refactor` `style` `test` `chore` + `: ` + 한국어 요약 50자 이내. 한 커밋 한 목적.
- 커밋 전 `git diff --cached --stat`로 `data/raw`·`진행 현황 및 계획 정리`·`.env`·`*.json`이 없는지 확인.
- 구현 메인이 바꾼 문서(`docs/dev/tasks/F<n>_*.md`·`docs/dev/진행기록.md`·`docs/dev/식_함수_대응표.md`·`docs/decisions.md`·`docs/tension/**`)가 작업트리에 변경으로 있으면, 그 기능 브랜치의 **첫 커밋** `docs: F<n> 작업 프롬프트·설계 문서 반영`으로 내용을 고치지 않고 커밋한다(U2). `.vscode/`는 스테이징하지 않는다.
- PR 전 동기화(README 5절): `git fetch origin` → `git merge origin/develop` → 테스트 다시. 충돌 나면 `git merge --abort` 하고 멈추고 보고(직접 해결 금지).
- 푸시·PR: `git push -u origin feature/<이름>` → `gh pr create --draft --base develop --label <말머리 소문자>`. 본문은 `.github/pull_request_template.md` 양식, 관련 이슈에 `closes #<번호>`. `gh`가 실패하면 PR 본문을 보고서 7절에 적는다. **병합하지 않는다**(F0-가).

## 7. 보고서 — 두 파일 (10-28 사용자 결정)
- `docs/dev/reports/F<n>_report.md` = **요약, 60줄 이내.** 구현 메인이 읽는 파일이다. 명령 출력을 붙이지 않는다.
- `docs/dev/reports/F<n>_log.md` = 실행한 명령과 출력 전부. 구현 메인이 필요할 때만 찾아본다. report의 각 항목은 log의 절 번호(L1, L2 …)를 가리킨다.
```markdown
# F<n> 보고서 — <기능 이름>
- 결과: 완료 / 일부 / 멈춤(이유 한 줄)
- 날짜 · 브랜치 · 이슈(번호) · 커밋(해시 + 메시지) · PR(링크 또는 "만들지 않음")
- 환경: python / numpy / pandas
## 1. 완료 조건 (프롬프트 표의 # · ✓/✗ · 한 줄 근거 · log 절)
## 2. 막힌 것 · 질문 (구현 메인이 답할 것 — 없으면 "없음")
## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것 (제안만 — 없으면 "없음")
## 4. 바뀐 파일 (경로 · 한 줄) · 작업트리에 남긴 변경
```
log 양식: `# F<n> 실행 로그` 아래 프롬프트 절 순서로 `## L1 …`, `## L2 …`를 두고 명령과 출력을 그대로 적는다. PR을 못 만들면 PR 본문 초안도 log 끝에 둔다.
보고서 두 파일을 커밋한 뒤 세션을 끝낸다. 다음 기능은 새 세션에서 새 프롬프트로.

## 8. 참고 위치
- 산출식(수식 ①~⑰): `docs/tension/산출식_정리.md` 1A절 · 식↔함수 대응: `docs/dev/식_함수_대응표.md`
- v0.1.4 기준값: `docs/tension/인수인계_v0.1.4.md` 3.2절
- 기준 구현: `진행 현황 및 계획 정리/v0.1_시험/S3/s3_core.py`, `…/v0.1.4/compute_v014.py`, 독립 구현 `…/단계5/lib5.py`
- 검산 기준 파일: `…/v0.1.4/사건표_v014_기본.csv`·`_확장.csv`·`일별_v014_*.csv`·`요약_v014.csv`, 유형판정표 `…/단계5/V1_물리사건_유형판정표.csv`
````

## 부록 B — `utils/tension/__init__.py`
```python
"""봉수 긴장도 계산 패키지 (v0.1.4 이식).

모듈(예정):
    io      — 사건표·유형판정표·결과 CSV 로드와 검증 (F1)
    core    — 산출식 ①~⑰, 순수 함수 (F2)
    charts  — Plotly 그림 (F4)

규칙의 근거는 docs/decisions.md(ADR), 수식은 docs/tension/산출식_정리.md 1A절.
파라미터 값은 config.py에 있고, 함수는 인자로 받는다.
"""

__all__: list[str] = []
```

## 부록 C — `tests/test_smoke.py`
```python
"""F0 뼈대 확인 — 계산 테스트는 F3에서."""
import importlib

import config


def test_import_package():
    mod = importlib.import_module("utils.tension")
    assert mod.__doc__


def test_config_values_match_adr():
    assert config.HALF_LIFE_DAYS == 14
    assert config.BASE_PERIOD == (2010, 2019)
    assert config.STAGE_QUANTILES == (0.70, 0.90, 0.95, 0.98)
    assert (config.RELIEF_C, config.RELIEF_CAP) == (0.1, 0.5)
    assert config.PHYS_FLOOR == {"3거": 3, "4거": 7, "풍선3거": 6}
    assert config.E5_FLOOR == {"3거": 4, "4거": 10}
    assert config.KILL_EVENTS == ("A7-0098", "A7-0100")
    assert config.EVENT_FLOOR_ICBM_S == 7.5
    assert config.STEP_DOWN_DAYS == 7 and config.DISPLAY_MA_DAYS == 7
    assert len(config.CRISIS_LIST) == 10


def test_half_life_definition():
    lam = 2 ** (-1 / config.HALF_LIFE_DAYS)
    assert abs(lam ** config.HALF_LIFE_DAYS - 0.5) < 1e-12
```

## 부록 D — `pytest.ini`
```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -q
```

## 부록 E — `config.py` 끝에 붙일 블록
```python

# 4. 긴장도 계산 파라미터 (utils/tension) — 값의 근거는 docs/decisions.md ADR 번호
#    함수는 이 값을 인자 기본값으로만 쓴다. 값을 바꾸면 모델 버전을 올리고 ADR에 기록한다.
TENSION_MODEL_VERSION = "v0.1.4"                 # ADR-018 확정판
CALC_START_DATE = "2010-01-01"                   # 계산 시작일(R 시작값 0)
END_DATE = None                                  # U3(10-28): None = 실행일. 회귀 검산은 "2026-10-27"로 넘겨 호출
BASE_PERIOD = (2010, 2019)                       # ADR-003 기준기간(평소값·T 구간)
BUNDLES_BASE = ("핵·미사일", "군사 과시", "위협 언어·교리")   # ADR-010 상승 묶음(기본) — s3_core.py 6행 UP3
BUNDLES_EXT = BUNDLES_BASE + ("제재·압박",)                # ADR-013 확장 시나리오 — compute_v014.py 63행
BUNDLE_RELIEF = "완화"                            # ADR-008·009 (F2만)
BUNDLE_PHYS = "물리 충돌"                          # ADR-007
BUNDLE_E5 = "북러 밀착"                            # ADR-014 (하한 대상 행만; "북러(표시만)"은 계산 제외)
STAGE_QUANTILES = (0.70, 0.90, 0.95, 0.98)       # ADR-018 2·3·4·5거 시작 분위(반올림 정수로 판정)
RELIEF_C = 0.1                                   # ADR-008 완화 세기 c
RELIEF_CAP = 0.5                                 # ADR-008 완화 상한 κ
F2_FIELD_FACTOR = {"정치·군사": 1.0, "경제·인도": 0.2, "사회문화": 0.2}  # ADR-015 — 사건표 생성 때 S에 곱함(core는 안 씀)
HALF_GAUSS_SIGMA = 10                            # ADR-006·014 전용 하한 원점수 exp(-k²/(2σ²))
FLOOR_WINDOW = 30                                # ADR-006·014 전용 하한 창(일)
PHYS_FLOOR = {"3거": 3, "4거": 7, "풍선3거": 6}   # ADR-007 풍선 뺀 A3·A7: ρ≥3 → 3거, ρ≥7 → 4거 / 오물풍선(A3, 사건명 Balloon): ρ≥6 → 3거
TYPE4_FLOOR_STAGE = 4                            # ADR-007 1-1 4거 유형 사건 당일
KILL_EVENTS = ("A7-0098", "A7-0100")             # ADR-007 사망·침몰 당일 5거(천안함·연평도)
KILL_FLOOR_STAGE = 5
E5_FLOOR = {"3거": 4, "4거": 10}                  # ADR-014 E5: ρ≥4 → 3거, ρ≥10 → 4거
EVENT_FLOOR_ICBM_S = 7.5                         # ADR-018 사건 하한: A1 또는 A2 S≥7.5(ICBM) 당일
EVENT_FLOOR_STAGE = 3
STEP_DOWN_DAYS = 7                               # ADR-006 하강: 더 낮은 판정 7일 → 한 단계
DISPLAY_MA_DAYS = 7                              # ADR-006 표시선 = 7일 후행 이동평균
PROVISIONAL_DAYS = 6                             # ADR-006 최근 6일 "잠정"
TREND_DAYS = 14                                  # U11 10-28 확정 — 14일 변화
TREND_PCT_MIN = 50                               # U11 10-28 확정 — 14일 전 표시값 50 미만이면 % 숨김
A2_DATA_END = "2024-11-05"                       # ADR-011a(A2 항목) 안 10-27 사용자 결정 — A2 자료 마지막 날(이후 "자료 없음" 표시)
CRISIS_LIST = (                                  # 내부 위기 목록 10건(검산·게이지 눈금용) — s3_core.py 9~11행 CR과 같음 [확인]
    ("천안함", "2010-03-26", "물리"),
    ("연평도", "2010-11-23", "물리"),
    ("3차 핵", "2013-02-12", "상승"),
    ("목함지뢰", "2015-08-04", "물리"),
    ("4차 핵", "2016-01-06", "상승"),
    ("6차 핵", "2017-09-03", "상승"),
    ("판문점 정상회담", "2018-04-27", "완화"),
    ("2022-11 집중발사", "2022-11-02", "상승"),
    ("2024-06 북러조약", "2024-06-19", "북러"),
    ("2026-09 DMZ 지뢰", "2026-09-21", "물리"),
)
CRISIS_WINDOW_DAYS = 14                          # 위기 단계·게이지 눈금 = 위기일부터 14일 안 최댓값
TENSION_DATA_DIR = "data/tension"                # 결과 CSV 폴더(커밋)
TYPE4_TABLE_PATH = "data/tension/물리사건_유형판정표.csv"   # 유형판정표 사본(F1에서 복사, 커밋)
```
