# F9 작업 프롬프트 — 단계 6 마무리 문서 반영 (커밋 안 된 구현 메인 문서 4개 + 이 프롬프트)

작성 2026-10-30 · 구현 메인(채팅 ⑧) → Claude Code · 브랜치 **`feature/tension-docs-sync`(최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행** — 이 세션은 PR을 draft로 올리고 병합하지 않는다(병합은 사용자 몫)
권장 모델·노력: **Sonnet 5.5 · 중간**(문서를 그대로 커밋하는 작업 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F9_20261030`(리포 밖 작업 폴더).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 검사한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **이 작업은 문서만이다.** 코드(`utils/`·`scripts/`·`tests/`·`config.py`·`홈.py`·`pages/`)·`data/`·`README.md`는 한 줄도 바꾸지 않는다.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`·`git rm`(지울 일은 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, `.obsidian/` 스테이징, 아래 5개 문서의 **내용 수정**(CLAUDE.md 3·6절 U2 — 고치지 않고 그대로 커밋), `git commit <경로>` 꼴(항상 `git add <경로>` 뒤 `git commit -m`).

---

## 0. 목표
- 단계 6(앱 연결) 마무리로, 작업트리에 커밋 안 된 채 남은 구현 메인 문서를 **내용 그대로** develop에 올린다. 팀원이 develop에서 ADR-019(가정 바꿔 보기)·F8 화면 요청서 확정본·진행기록 최신본을 볼 수 있게 하는 것이 목적이다.
- 올리는 파일 5개 (모두 `docs/` 아래):
  | 파일 | 작업트리 상태 | 내용 |
  |---|---|---|
  | `docs/decisions.md` | ` M` | ADR-019 요약표 한 줄(본문은 F8 PR로 이미 들어감) |
  | `docs/dev/requests/F8_화면요청.md` | ` M` | 박성인 님께 보낸 F8 화면 요청서 **확정본**(초안을 덮어씀) |
  | `docs/dev/진행기록.md` | ` M` | 10-30 결정·검토 행(F7c·F8·채팅 ⑧) |
  | `docs/dev/지시서_구현_메인_채팅8.md` | `??` | 채팅 ⑧ 인계 지시서 |
  | `docs/dev/tasks/F9_docs_sync.md` | `??` | 이 프롬프트 |
- **코드·결과 CSV·테스트는 바뀌지 않는다.** develop `9c5a3fa`에서 pytest 137 passed가 그대로여야 하고, 이 브랜치의 develop 대비 변경 파일은 `docs/` 아래 7개(문서 5 + 보고서 2)뿐이어야 한다.

## 1. 시작 점검 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F9_20261030"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/decisions.md" " M docs/dev/requests/F8_화면요청.md" " M docs/dev/진행기록.md"
#     "?? docs/dev/지시서_구현_메인_채팅8.md" "?? docs/dev/tasks/F9_docs_sync.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 3절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: develop (그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git config --get core.autocrlf                     # log에 남김(true 예상)
git fetch origin
git log --oneline -3 origin/develop                # 기대: 맨 위 9c5a3fa
git log --oneline -1                               # 기대: 9c5a3fa
gh pr list --state open --json number,title,headRefName,author   # log에 남김(판단 없이)

# 1-1 구현 메인 문서 백업(리포 밖) → md5 확인
DOCS="docs/decisions.md docs/dev/requests/F8_화면요청.md docs/dev/진행기록.md docs/dev/지시서_구현_메인_채팅8.md"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표 (다르면 멈추고 보고)
```
1-1 `md5sum` 기대 — 줄바꿈은 Windows 체크아웃 때문에 CRLF/LF 어느 쪽이든 **`tr -d '\r' < 파일 | md5sum`**으로 같게 본다(아래 값은 CR을 뺀 md5):
```
ca85bf6c7cac65a8fd3e859365ae3673  docs/dev/진행기록.md
ab9fca53fcdbb9291d8bd2a2032907f1  docs/decisions.md
4c25996ed710e6fdbfdabbc27db7d582  docs/dev/requests/F8_화면요청.md
73b3e31ff3353ab73ca8bf25235155f9  docs/dev/지시서_구현_메인_채팅8.md
```
(이 프롬프트 자신은 md5를 적지 않는다.)

```bash
# 1-2 origin/develop이 9c5a3fa보다 앞서 있을 때만:
#   git diff --name-only 9c5a3fa origin/develop      # log에 남김
#   위 목록에 $DOCS의 네 경로가 있으면 → 멈추고 보고(구현 메인이 문서를 다시 맞춘다)
#   없으면 → git pull --ff-only origin develop       # 실패하면 멈추고 보고. 성공 뒤 1-1 md5를 다시 확인
git status --porcelain                             # 맨 위 기대와 같아야 함
git switch -c feature/tension-docs-sync
# 1-3 이슈: 본문 "$B/issue_F9.md" = .github/ISSUE_TEMPLATE/feature.md 양식
#   (배경 = 0절 첫 줄 · 범위 = 0절 표의 5개 파일, 하지 않는 것 = 코드·데이터·README · 완료 조건 = 4절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F9.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[DOCS] 단계 6 마무리 — 구현 메인 문서 반영(F9)" --label docs --body-file "$B/issue_F9.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 137 passed
```

## 2. 커밋
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: 단계 6 마무리 문서 반영` — 아래 다섯 경로를 하나씩 `git add`(와일드카드·`git add .`·`-A` 금지)
   ```bash
   git add docs/decisions.md docs/dev/requests/F8_화면요청.md docs/dev/진행기록.md docs/dev/지시서_구현_메인_채팅8.md docs/dev/tasks/F9_docs_sync.md
   git diff --cached --stat                         # 기대: 정확히 5 files (.obsidian·코드·data 없음)
   ```
   금지 경로 검사 `OK` 뒤 `git commit -m "docs: 단계 6 마무리 문서 반영"`. 커밋 뒤 확인:
   ```bash
   git log -1 --format=%B | grep -inE "$AI" && echo "AI 표기 있음 — 멈추고 보고" || echo "OK"
   for f in $DOCS; do echo "$(MSYS_NO_PATHCONV=1 git show HEAD:"$f" | tr -d '\r' | md5sum | cut -c1-32)  $f"; done   # 1-1 표와 같아야 함
   git status --porcelain                           # 기대: "?? .obsidian/" 하나만
   ```
2. `docs: F9 보고서` — `docs/dev/reports/F9_report.md` · `F9_log.md` (6절 · PR 생성 뒤 5절 순서대로)

## 3. 하지 않는 것
- 위 5개 문서의 내용 수정(줄바꿈 변환 포함 — `git add` 때 LF→CRLF 경고는 정상이니 그냥 둔다), 다른 문서·코드·`data/`·`README.md`·`tests/fixtures/` 수정
- `.obsidian/` 스테이징, `docs/dev/reports/F8_*` 등 이미 병합된 보고서 수정
- 원격·로컬 브랜치 삭제, PR 병합·ready 전환, 고치고 싶은 것은 고치지 말고 보고서 3절에 적기

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 브랜치 develop, 훅 있음, status가 기대와 같음, 137 passed, 버전·autocrlf 적음, 1-1 md5 4개 같음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-docs-sync`, 이슈 번호 |
| 3 | 커밋 1 | `--cached --stat`이 정확히 5 files, 금지 경로 검사 OK, `HEAD:` md5 4개가 1-1 표와 같음, 커밋 뒤 status = `?? .obsidian/` 하나 |
| 4 | 푸시 전 | `git merge origin/develop` 충돌 없음(있으면 abort·멈춤), 137 passed |
| 5 | 변경 범위 | `git diff --name-only origin/develop..HEAD`가 `docs/` 아래 7개(문서 5 + 보고서 2)뿐, 7개 밖 0 |
| 6 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문(올리기 전·후) 모두 `OK` |
| 7 | PR | draft, base `develop`, 라벨 `docs`, `closes #<이슈>`, 병합 안 함 |
| 8 | 마지막 status | `?? .obsidian/` 하나만 |

## 5. 푸시 · PR
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 137 passed
git diff --name-only origin/develop..HEAD                      # 이 시점(커밋 1만) 기대: docs/ 아래 5개
git diff --name-only origin/develop..HEAD | grep -v '^docs/' && echo "docs 밖 변경 있음 — 멈추고 보고" || echo "OK"
git log --format='%h %an' origin/develop..HEAD                 # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-docs-sync
# 본문 "$B/pr_F9.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> ·
#   요약 = 문서만 올리는 PR · 변경 = 0절 표의 5개 파일 한 줄씩 · 테스트 = 137 passed, develop 대비 변경이 docs/ 아래뿐 ·
#   체크리스트 아래에 팀원 안내 세 줄:
#     "이 PR은 문서만입니다 — 코드·결과 CSV·테스트는 바뀌지 않았습니다."
#     "develop에서 볼 수 있게 되는 것: ADR-019 요약표 행(가정 바꿔 보기), 박성인 님께 드린 F8 화면 요청서 확정본(docs/dev/requests/F8_화면요청.md), 진행기록 최신본."
#     "화면 작업은 요청서대로 최신 develop에서 새 브랜치를 만들어 주시면 됩니다(이 PR을 기다릴 필요 없음 — 계산 함수는 이미 develop에 있습니다)."
grep -inE "$AI" "$B/pr_F9.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label docs --title "[DOCS] 단계 6 마무리 — 구현 메인 문서 반영(F9)" --body-file "$B/pr_F9.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다).
**순서 정리:** 커밋 1 → 위 검사·push → PR 생성 → 보고서 두 파일을 쓰고(PR 링크 포함) **커밋 2** → 변경 범위 다시 확인(`git diff --name-only origin/develop..HEAD`가 docs/ 아래 7개, `git diff --name-only origin/develop..HEAD | grep -v '^docs/'`가 빔) → `git push` → 끝.

## 6. 보고서 (CLAUDE.md 7절 — 두 파일)
- `docs/dev/reports/F9_report.md` = 요약, **60줄 이내**, 명령 출력 없음. 양식:
  ```markdown
  # F9 보고서 — 단계 6 마무리 문서 반영
  - 결과: 완료 / 일부 / 멈춤(이유 한 줄)
  - 날짜 · 브랜치 · 이슈(번호) · 커밋(해시 + 메시지) · PR(링크)
  - 환경: python / numpy / pandas
  ## 1. 완료 조건 (4절 표의 # · ✓/✗ · 한 줄 근거 · log 절)
  ## 2. 막힌 것 · 질문 (구현 메인이 답할 것 — 없으면 "없음")
  ## 3. 프롬프트와 다르게 한 것 · 고치고 싶은 것 (제안만 — 없으면 "없음")
  ## 4. 바뀐 파일 (경로 · 한 줄) · 작업트리에 남긴 변경
  ```
- `docs/dev/reports/F9_log.md` = 실행한 명령과 출력 전부. `# F9 실행 로그` 아래 `## L1 시작 점검`(1절) · `## L2 커밋`(2절) · `## L3 푸시·PR`(5절)로 나누고 report의 각 항목이 절 번호를 가리키게 한다. PR을 못 만들면 PR 본문 초안을 log 끝에 둔다.
- 두 파일을 커밋한 뒤 세션을 끝낸다.
