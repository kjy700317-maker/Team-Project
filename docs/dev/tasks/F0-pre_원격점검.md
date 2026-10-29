# F0-pre 작업 프롬프트 — 원격 develop 점검 (읽기 전용)

작성 2026-10-28 · 구현 메인 → Claude Code · 브랜치 만들지 않음 · 커밋·푸시 없음
상태: **실행**

> Claude Code에게: 이 파일만 보고 그대로 수행한다(리포에 아직 `CLAUDE.md` 없음). **아무 파일도 고치지 않는다.** 예외는 보고서 파일 하나 `docs/dev/reports/F0-pre_report.md`(커밋하지 않음).
> 금지: `git pull`·`merge`·`switch`·`checkout`·`reset`·`stash`·`commit`·`push`, 이슈·PR·라벨 만들기, `pip install`. 명령이 실패하면 고치려 하지 말고 출력을 그대로 보고서에 적는다.

## 목적
F0(`docs/dev/tasks/F0_scaffold.md`)은 10-14 기준 원격을 가정하고 쓰였다. 팀 리포가 그 뒤 크게 바뀌었으므로(README 기준: `홈.py`, `utils/real.py`·`loader.py`·`build_db.py`, `db/schema.sql`, `pages/1~4`, `.vscode/settings.default.json`), F0이 손댈 파일의 **원격 최신 상태**와 **F0을 돌릴 때 막힐 곳**을 구현 메인이 알 수 있게 그대로 옮겨 적는다.

## 1. 명령 (순서대로, 각 출력 전부를 보고서 해당 칸에 붙임)
```bash
# 1-1 현재 상태
git status --porcelain
git branch -vv
python --version
python -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
python -c "import pytest; print(pytest.__version__)" || echo "pytest 없음"
python -c "import openpyxl; print(openpyxl.__version__)" || echo "openpyxl 없음"
python -c "import streamlit; print(streamlit.__version__)" || echo "streamlit 없음"
gh --version || echo "gh 없음"
gh auth status || echo "gh 로그인 안 됨"

# 1-2 원격 기록 받기 (작업트리는 안 바뀜)
git fetch origin
git log --oneline -15 origin/develop
git rev-list --left-right --count develop...origin/develop
git ls-remote --symref origin HEAD

# 1-3 원격 develop 파일 목록과 바뀐 것
git ls-tree -r --name-only origin/develop
git ls-tree origin/develop | grep 160000 || echo "gitlink 없음"
git diff --stat develop origin/develop

# 1-4 F0이 손댈 파일의 원격 내용
git show origin/develop:config.py
git show origin/develop:.gitignore
git show origin/develop:requirements.txt | file -
git show origin/develop:requirements.txt | iconv -f UTF-16 -t UTF-8 2>/dev/null || git show origin/develop:requirements.txt
git show origin/develop:.github/pull_request_template.md
git show origin/develop:utils/README.md || echo "없음"
git show origin/develop:README.md | grep -n -E "^(<<<<<<<|=======|>>>>>>>)" || echo "충돌 표시 없음"

# 1-5 F0의 pull --ff-only가 막힐지: 로컬에서 커밋 안 된 파일을 원격도 바꿨나
git diff --stat develop origin/develop -- docs/decisions.md .vscode/settings.json docs/dev config.py requirements.txt .gitignore
git ls-tree origin/develop -- .vscode/settings.json || true
git check-ignore -v .vscode/settings.json || echo "현재 로컬 .gitignore로는 무시 안 됨"

# 1-6 팀 이슈·PR·라벨 (읽기만)
gh label list || true
gh issue list --state all --limit 10 || true
gh pr list --state all --limit 10 || true
```

## 2. 보고서 `docs/dev/reports/F0-pre_report.md`
```markdown
# F0-pre 보고서 — 원격 develop 점검
- 날짜 · 실행 위치(브랜치) · 고친 파일: 없음(이 보고서만)
## 1-1 현재 상태
## 1-2 원격 기록
## 1-3 파일 목록·바뀐 것
## 1-4 F0이 손댈 파일의 원격 내용
## 1-5 pull --ff-only 막힘 여부 (판단: 막힘 / 안 막힘 + 근거 한 줄)
## 1-6 이슈·PR·라벨
## 막힌 것 · 이상한 것 (사실만, 고치는 방법 제안 금지)
```
보고서를 쓰고 끝낸다(커밋하지 않음).
