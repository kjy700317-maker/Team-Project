# F0-fix 작업 프롬프트 — CLAUDE.md 적용 범위 한정·python 문구 (PR #15에 커밋 추가)

작성 2026-10-29 · 구현 메인 → Claude Code · 브랜치 `feature/tension-scaffold`(이미 있음, PR #15) · 새 브랜치를 만들지 않는다
상태: **실행**

> Claude Code에게: 이 파일만 보고 그대로 수행한다. 판단이 필요하면 고치지 말고 보고서에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). `conda run`은 쓰지 않는다.
> 금지: `rebase`·`stash`·`reset`·`push --force`·`pip install`, `develop`·`main` 직접 커밋, PR 병합·ready 전환, 2절 밖의 CLAUDE.md 수정.

## 왜
팀원도 이 리포에서 Claude Code를 쓴다(사용자 10-29). PR #15가 병합되면 팀원의 Claude Code도 `CLAUDE.md`를 읽는다. 그래서 ① 규칙을 긴장도 작업에만 적용되게 한정하고, ② PC마다 다른 python 경로를 CLAUDE.md에서 빼서 작업 프롬프트가 지정하게 한다.

## 1. 시작 점검
```bash
git status --porcelain        # 기대: " M docs/dev/진행기록.md", "?? docs/dev/tasks/F0-fix_CLAUDE범위.md", "?? .obsidian/" 만
git branch --show-current     # 기대: feature/tension-scaffold
git fetch origin
git rev-list --left-right --count feature/tension-scaffold...origin/feature/tension-scaffold   # 기대: 0	0
```
기대와 다르면 멈추고 보고한다.

## 2. CLAUDE.md 수정 — 아래 스크립트로만 (3곳, 글자 그대로)
아래를 리포 밖 `~/bongsu_F0fix_20261029/fix_claude_md.py`로 저장하고 `<py> ~/bongsu_F0fix_20261029/fix_claude_md.py`로 실행한다. 바꿀 문장이 정확히 한 번씩 있어야 하며, 아니면 아무것도 쓰지 않고 멈춘다.
```python
from pathlib import Path
p = Path("CLAUDE.md")
t = p.read_text(encoding="utf-8")
R = [
 ("설계·규칙 결정은 구현 메인 세션(별도 Claude 채팅)과 사용자 몫이다.\n",
  "설계·규칙 결정은 구현 메인 세션(별도 Claude 채팅)과 사용자 몫이다.\n\n"
  "> **적용 범위:** 이 파일의 규칙은 `docs/dev/tasks/`의 작업 프롬프트로 하는 **긴장도 계산 코드화 작업**(`utils/tension/`·`scripts/`·`tests/`·`data/tension/`·`docs/dev/`·`docs/tension/`)에만 적용한다. "
  "그 밖의 작업(화면 `홈.py`·`pages/`, DB `utils/build_*.py`·`db/`, 전처리 데이터 등)은 팀 `README.md`의 협업 규칙을 따르고, 이 파일의 1·3·5~7절은 적용하지 않는다. "
  "다만 3절의 보안 규칙(`.env`·키·`*.json` 커밋 금지, `main` 직접 푸시 금지)은 모든 작업에 적용한다.\n"),
 ("4. python은 **팀 conda 환경 `python311`로만** 돌린다: `conda run -n python311 python …`(이 PC 기본 `python`은 3.14 — 쓰지 않는다). 버전(3.11.x)과 numpy·pandas 버전을 보고서에 적는다. 환경이 없으면 멈추고 보고.",
  "4. python은 **팀 conda 환경 `python311`의 `python.exe`를 경로로 직접 호출**한다. 경로는 PC마다 다르므로 **작업 프롬프트 머리에 적힌 경로**를 쓴다(`conda run`은 PC에 따라 base 환경을 잡을 수 있어 쓰지 않는다). 버전(3.11.x)과 numpy·pandas 버전을 보고서에 적는다. 경로가 없거나 3.11이 아니면 멈추고 보고."),
 ("- 테스트: `conda run -n python311 python -m pytest -q`",
  "- 테스트: `<작업 프롬프트가 지정한 python.exe> -m pytest -q`"),
]
for old, new in R:
    n = t.count(old)
    assert n == 1, (n, old[:40])
for old, new in R:
    t = t.replace(old, new)
p.write_text(t, encoding="utf-8", newline="")
print("ok", len(t.splitlines()))
```
확인:
```bash
grep -n "적용 범위" CLAUDE.md          # 1줄
grep -c "conda run" CLAUDE.md          # 1 (4번 항목 안의 "쓰지 않는다" 설명만)
<py> -m pytest -q                      # 3 passed
```

## 3. 커밋 (이 순서)
금지 경로 검사(각 커밋 전, 그대로 실행):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `git add docs/dev/진행기록.md docs/dev/tasks/F0-fix_CLAUDE범위.md` → `docs: F0-fix 작업 프롬프트·진행기록 반영`
2. `git add CLAUDE.md` → `docs: CLAUDE.md 적용 범위 한정·python 경로 문구 수정`
3. (5절 보고서 쓴 뒤) `git add docs/dev/reports/F0-fix_report.md docs/dev/reports/F0-fix_log.md` → `docs: F0-fix 보고서`

## 4. 동기화·푸시·PR 코멘트
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
<py> -m pytest -q
git push origin feature/tension-scaffold
```
PR #15에 코멘트를 단다. 본문 파일 `~/bongsu_F0fix_20261029/pr_comment.md`:
```
F0-fix 커밋 추가 (2026-10-29)
- CLAUDE.md: 맨 위에 적용 범위 문구 추가 — 이 규칙은 docs/dev/tasks 작업 프롬프트로 하는 긴장도 코드화 작업에만 적용. 화면·DB·전처리 등 다른 작업은 팀 README 규칙을 따름(보안 규칙은 공통).
- CLAUDE.md: python 실행 경로를 작업 프롬프트가 지정하도록 변경(PC마다 경로가 다름).

팀원 확인 부탁: 이 PR은 requirements.txt를 바꿉니다 — pandas `>=2.0.0` → `==3.0.6`, `pytest==9.0.3`·`openpyxl==3.1.5` 추가. 병합 뒤 `pip install -r requirements.txt`를 다시 해 주세요(pandas 3.0으로 올라가므로 기존 코드 동작을 한 번 확인 부탁드립니다).
```
`gh pr comment 15 --body-file ~/bongsu_F0fix_20261029/pr_comment.md`. PR을 ready로 바꾸거나 병합하지 않는다.

## 5. 보고서 (CLAUDE.md 7절 양식, 두 파일)
`docs/dev/reports/F0-fix_report.md`(요약 30줄 이내 — 완료 조건 표: 1절 점검 · 2절 스크립트 ok · grep 2개 · pytest · 커밋 3개 · 푸시 · 코멘트 링크) + `F0-fix_log.md`(명령 출력 전부). 커밋 3 뒤 다시 푸시하고 끝낸다.
