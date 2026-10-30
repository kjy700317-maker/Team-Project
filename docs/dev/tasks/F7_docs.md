# F7 작업 프롬프트 — 긴장도 산출식·운영 문서 · README 4·6절 · F2 검토 발견 10 정리

작성 2026-10-29 · 구현 메인(채팅 ⑥) → Claude Code · 브랜치 **`feature/tension-docs`(PR #27 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행**(10-29 사용자 "F7 지금대로 진행해") — 10-29 사용자 결정 반영: `산출식.md` = 새 정리본(가) · 발견 10 = 작게 고침(가) · README 문구 = 초안대로 · 리뷰 = 받지 않고 병합(사용자 몫 — 이 세션은 PR을 draft로 올리고 병합하지 않는다)
권장 모델·노력: **Sonnet 5.5 · 중간**(문서 커밋 + 패치 적용 + 실행 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F7_20261029`(`export B=…` — 2절 파이썬이 읽음).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 6절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **팀원 파일 중 이 작업이 바꾸는 것:** `README.md` **4절(폴더 구조)·6절 1번 문장만**(사용자 10-29: 팀원 허락 받음 — 10-29 "이원희 줄만" 원칙의 예외). 4·6절 밖은 바꾸지 않는다. `config.py`는 긴장도 절(8절)에 2줄만 더한다(우리 몫). 화면(`홈.py`·`pages/`)은 건드리지 않는다.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`홈.py`·`pages/`·`utils/ui.py`·`utils/dummy.py`·`utils/real.py` 수정**, `data/tension/**` 결과 파일 수정, 기존 테스트 수정(새 테스트를 `tests/test_core.py` 끝에 더하는 것만 패치로).

---

## 0. 목표
- **문서 2개(구현 메인 작성, 커밋 1에 들어감):** `docs/tension/산출식.md`(지금 v0.1.4가 무엇인가: 식 ①~⑰·⑮′, 파라미터, 묶음, 단계, 결과 파일, 한계) · `docs/tension/운영.md`(사건이 바뀌었을 때 재계산·판정표 갱신·GPR 월 갱신·파라미터 변경 절차). 내용을 고치지 않고 그대로 커밋한다. 함께 올라가는 갱신: `인수인계_v0.1.4.md` 3.3절(재계산 절차) · `decisions.md` 보류 목록 15~18 · `식_함수_대응표.md` F7 주석 · `산출식_정리.md` 안내 한 줄 · `진행기록.md` · `지시서_구현_메인_채팅6.md`.
- **F2 검토 발견 10 정리(부록 A 패치):** `BALLOON_KEYWORD`·`A2_NOTE`를 `core.py`에서 `config.py`(긴장도 절)로 옮기고, T 구간 분위·문턱이 4개가 아니면 `ValueError`로 멈춘다(`stage_cuts`·`stage_from_index`). **식·값·결과는 바뀌지 않는다** — 결과 CSV 7개가 바이트까지 같아야 한다. 새 테스트 7개(`tests/test_core.py` 끝).
- **README 4절 폴더 구조·6절 1번 갱신(부록 B 패치):** 4절 트리에 우리 줄 추가(`data/tension`·`docs/tension`·`docs/dev`·`scripts`·`tests`·`utils/tension`·`.gitattributes`·`CLAUDE.md`·`pytest.ini`, `loader.py` 줄 끝에 `load_tension_*` 설명) · 6절 1번 문장 교체(`홈.py`는 SQLite와 `data/tension/` 결과 CSV를 읽음, 긴장도 계산은 `scripts/run_tension.py`로 로컬에서 돌려 결과 CSV 커밋).
- 구현 메인 시험본 `[확인 10-29: python 3.13 · numpy 2.4.6 · pandas 3.0.6 · plotly 7.1.0 · streamlit 1.65.0]`: develop `7951bb0` + 부록 패치 2개(`git apply --check` 통과) → **114 passed**(F6까지 107 + 7), `-m "not regression"` 97 passed · 17 deselected, `run_tension --end 2026-10-29` 결과 7개 = 커밋된 결과와 **바이트 같음**(3절 표).

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F7_20261029"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/decisions.md" " M docs/dev/식_함수_대응표.md" " M docs/dev/진행기록.md"
#     " M docs/tension/산출식_정리.md" " M docs/tension/인수인계_v0.1.4.md"
#     "?? docs/dev/지시서_구현_메인_채팅6.md" "?? docs/dev/tasks/F7_docs.md"
#     "?? docs/tension/산출식.md" "?? docs/tension/운영.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 4절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: feature/tension-compare 또는 develop(그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 27 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop                # 기대: 7951bb0(뒤에 커밋이 있으면 누구의 무엇인지 log에 적고 계속 — 2절 git apply --check가 실패하면 거기서 멈춤)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 develop으로
DOCS_M="docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md docs/tension/인수인계_v0.1.4.md"
DOCS_N="docs/dev/지시서_구현_메인_채팅6.md docs/dev/tasks/F7_docs.md docs/tension/산출식.md docs/tension/운영.md"
DOCS="$DOCS_M $DOCS_N"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표(F7_docs.md 제외 8개 — 내용이 다르면 멈추고 보고)
git restore $DOCS_M
git switch develop                                  # 이미 develop이면 그대로
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in $DOCS; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-docs
# 1-3 이슈: 본문 "$B/issue_F7.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 0절 목록, 완료 조건 = 5절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F7.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[DOCS] 긴장도 산출식·운영 문서와 README 갱신(F7)" --label docs --body-file "$B/issue_F7.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 107 passed(F6까지)
```
1-1 `md5sum` 기대(줄바꿈은 Windows 체크아웃 때문에 CRLF/LF 어느 쪽이든 **`tr -d '\r' < 파일 | md5sum`**으로 같게 본다 — 아래 값은 CR을 뺀 md5):

```
83538367d95f6708592a8ba5646158aa  docs/tension/산출식.md
d25475232b29f32b15d7a96c4324cd37  docs/tension/운영.md
09ed92ef71cf823dd31b77e3a423193f  docs/decisions.md
7a56fa7e79f4c23ef6ff2568632b16ed  docs/dev/식_함수_대응표.md
365af800758d94168047bd23da160a80  docs/dev/진행기록.md
5a8c81f6d52f1cd3461637dc9012a8f2  docs/tension/산출식_정리.md
96ad4cd4e6beb6ec6b6e6da53ca70d8b  docs/tension/인수인계_v0.1.4.md
c486e6bb58eb5d6eaefba208667bca4f  docs/dev/지시서_구현_메인_채팅6.md
```

(`md5sum`을 그대로 돌리면 CRLF 파일은 값이 다르게 나온다. 확인은 `for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done`로 한다. `F7_docs.md`(이 파일)는 자기 자신의 md5를 본문에 적을 수 없어 표에서 뺐다 — 나머지 8개만 대조한다.)

**커밋 1** `docs: F7 작업 프롬프트·설계 문서 반영` — 위 `$DOCS` 9개(내용 수정 없이 — U2). 6절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 발견 10 패치 적용 (부록 A) → 테스트 → 결과 바이트 확인
```bash
PYTHONIOENCODING=utf-8 <py> - <<'EOF2'
import os, re, pathlib
t = pathlib.Path("docs/dev/tasks/F7_docs.md").read_text(encoding="utf-8")
for tag, name in (("F7.code.patch", "f7_code.patch"), ("F7.readme.patch", "f7_readme.patch")):
    m = re.search(r"<!-- %s 시작 -->\n```diff\n(.*?)```\n<!-- %s 끝 -->" % (re.escape(tag), re.escape(tag)), t, re.S)
    pathlib.Path(os.environ["B"], name).write_bytes(m.group(1).encode("utf-8"))
    print("저장:", name, len(m.group(1).splitlines()), "줄")
EOF2
md5sum "$B/f7_code.patch" "$B/f7_readme.patch"
#   기대: 92b3edf69921c2b5c806b6a03c4b4197 (118줄) f7_code.patch / c9c236f818729b778312cbf2a6a478da (49줄) f7_readme.patch
git apply --check "$B/f7_code.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply --check "$B/f7_readme.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply "$B/f7_code.patch"                       # README 패치는 3절에서
git hash-object config.py utils/tension/core.py tests/test_core.py
#   기대(순서대로):
#     config.py              a4cb37a249992334221edc0291bbbae4d1f56457
#     utils/tension/core.py  d8b7b30d97f9ed70e13d54c763d709afc34664a0
#     tests/test_core.py     1a462a5859291a2efeeea5e215933867c205bac5
#   하나라도 다르면 멈추고 보고
git diff config.py utils/tension/core.py | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '   # 기대: 부록 A와 같은 줄만(config 2줄 추가 · core 상수 2개 삭제·함수 사용 2곳·보조 함수 1개·호출 2곳)
```
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest                                    # 기대: 114 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                # 기대: 97 passed, 17 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_core.py   # 기대: 전부 통과(우리 코드 경고 0)
mkdir -p "$B/after"
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --end 2026-10-29 --out "$B/after"
#   기대 마지막 줄: "쓴 파일: …비교선_일별.csv · 반감기_민감도.csv(반감기 [7, 14, 21, 30]일)"
for f in 일별_기본 일별_확장 요약 월별 연도별 비교선_일별 반감기_민감도; do cmp "$B/after/$f.csv" "data/tension/$f.csv" && echo "같음 $f" || echo "다름 $f — 멈추고 보고"; done
md5sum "$B/after/"*.csv
#   기대:
#     1363cb16cf991c8c3c79046d8a1ec998  일별_기본.csv
#     2b8d3cb21ee29ada655b271058cb7bf2  일별_확장.csv
#     c31fdbc3218819a524629ca6e2604093  요약.csv
#     dfa8f9950af7d4f291ffce60cda97035  월별.csv
#     f9b2841dfd67382caf3e01eb11de7121  연도별.csv
#     704053ceea621623091bb32be4050562  비교선_일별.csv
#     af13c6f9e9e7c83c7ec0d7b55054c90a  반감기_민감도.csv
git status --porcelain data/                       # 기대: 줄 없음(data/tension 결과는 건드리지 않았다 — 결과는 $B/after에만 썼다)
```
- 다르면: 파일도 코드도 고치지 말고 차이를 log에 남기고 멈추고 보고한다(버전 차이로 보이면 그렇게 적는다).
- `--end`를 반드시 `2026-10-29`로 고정한다(기본값은 실행일이라 커밋된 결과와 날짜가 달라진다).

**커밋 2** `refactor: 오물풍선 단어·A2 문구 config로, 문턱 4개 검사` — `config.py` · `utils/tension/core.py`
**커밋 3** `test: T 구간 문턱 4개 검사·config 상수 테스트` — `tests/test_core.py`

## 3. README 패치 적용 (부록 B) → 4·6절 안에서만 바뀌는지 확인
```bash
git apply "$B/f7_readme.patch"
git hash-object README.md                          # 기대: e2f25ba6d0fdb12fe73776db32925865d4ab5db7 — 다르면 멈추고 보고
git diff README.md | grep '^@@'                    # 기대 2줄: "@@ -52,25 +52,34 @@ Team-Project/" · "@@ -145,7 +154,7 @@ Team-Project/"  (4절 42~81행 · 6절 141~158행 안)
git diff --stat README.md                          # 기대: 1 file changed, 11 insertions(+), 2 deletions(-)
git diff README.md | grep -E '^-[^-]'              # 기대 2줄: "loader.py" 줄(끝에 설명 추가로 바뀜) · 6절 1번 문장 — 그 밖에 지운 줄이 있으면 멈춤
```
**커밋 4** `docs: README 폴더 구조·화면 데이터 설명 갱신` — `README.md`

## 4. 하지 않는 것
- 문서 2개·갱신된 설계 문서의 내용 수정(커밋 1은 그대로), 화면(`홈.py`·`pages/`)·`utils/ui.py`·`dummy.py`·`real.py`·`loader.py` 수정, `README.md` 4·6절 밖 수정(5절 협업 규칙 포함)
- `data/tension/` 결과·사건표·판정표 수정(검산 결과는 `$B/after`에만), 기존 테스트 수정, `tests/fixtures/` 수정
- 부록과 다른 코드·테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절), 원격·로컬 브랜치 삭제
- 커밋·PR·이슈 어디에도 AI 표기(`Co-Authored-By`, `Generated with`, 🤖, 세션 링크)를 넣지 않는다 — 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다.

## 5. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #27 MERGED, 훅 있음, 107 passed, 버전 적음, 1-1 md5 8개 같음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-docs`, 이슈 번호 |
| 3 | 2절 패치 | 두 패치 md5 같음, `git apply --check` 통과, hash 3개 같음 |
| 4 | 2절 테스트 | 114 passed · not regression 97/17 · FutureWarning 0 |
| 5 | 2절 결과 | `run_tension --end 2026-10-29` 결과 7개가 커밋된 결과와 바이트 같음, `data/` 변경 없음 |
| 6 | 3절 README | hash 같음, 변경이 4·6절 두 hunk 안, 지운 줄 2줄뿐 |
| 7 | 커밋 | 6절 순서 5개 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 10 | 마지막 status | `?? .obsidian/` 하나만 |

## 6. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F7 작업 프롬프트·설계 문서 반영` — 1절 `$DOCS` 9개
2. `refactor: 오물풍선 단어·A2 문구 config로, 문턱 4개 검사` — `config.py` · `utils/tension/core.py`
3. `test: T 구간 문턱 4개 검사·config 상수 테스트` — `tests/test_core.py`
4. `docs: README 폴더 구조·화면 데이터 설명 갱신` — `README.md`
5. `docs: F7 보고서` — `docs/dev/reports/F7_report.md` · `F7_log.md`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 114 passed
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-docs
# 본문 "$B/pr_F7.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 목록 · 테스트 = 5절 결과(114 passed, 결과 CSV 바이트 동일)
#   · 체크리스트 아래에 팀원 안내 세 줄:
#     "README는 4절(폴더 구조)과 6절 1번 문장만 고쳤습니다(팀원 허락 받음). 다른 절·다른 사람 줄은 그대로입니다."
#     "화면 파일(홈.py·pages/)은 바꾸지 않았습니다. 코드 변경은 config.py 긴장도 절 2줄과 utils/tension/core.py 정리뿐이며 계산 결과는 바이트까지 같습니다."
#     "산출식·운영 문서: docs/tension/산출식.md(지금 v0.1.4가 무엇인가) · docs/tension/운영.md(재계산 방법)."
grep -inE "$AI" "$B/pr_F7.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label docs --title "[DOCS] 긴장도 산출식·운영 문서와 README 갱신(F7)" --body-file "$B/pr_F7.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다). 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 7. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F7_report.md`(60줄 이내): 1절 = 5절 표 10행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일(`README.md`는 "4·6절만"으로 구분).
`docs/dev/reports/F7_log.md`: 1~3절 출력 전부(문서 md5, 패치 md5·hash, 테스트 결과, 결과 7개 cmp·md5, README hunk 확인), 작성자 목록, 커밋·푸시·PR 출력.
세션 마지막 채팅 답은 한국어로: 결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것.

---

## 부록 A. `$B/f7_code.patch` (2절 파이썬으로 잘라 저장 — 글자 그대로, md5 `92b3edf69921c2b5c806b6a03c4b4197`)
대상: `config.py`(긴장도 절에 `BALLOON_KEYWORD`·`A2_NOTE` 2줄) · `utils/tension/core.py`(상수 2개 삭제 → `config.` 참조, 보조 함수 `_require_four_cuts`, `stage_cuts`·`stage_from_index`에서 호출) · `tests/test_core.py`(끝에 테스트 7개).

<!-- F7.code.patch 시작 -->
```diff
diff --git a/config.py b/config.py
index 7e7f2b5..a4cb37a 100644
--- a/config.py
+++ b/config.py
@@ -58,6 +58,7 @@ F2_FIELD_FACTOR = {"정치·군사": 1.0, "경제·인도": 0.2, "사회문화":
 HALF_GAUSS_SIGMA = 10                            # ADR-006·014 전용 하한 원점수 exp(-k²/(2σ²))
 FLOOR_WINDOW = 30                                # ADR-006·014 전용 하한 창(일)
 PHYS_FLOOR = {"3거": 3, "4거": 7, "풍선3거": 6}   # ADR-007 풍선 뺀 A3·A7: ρ≥3 → 3거, ρ≥7 → 4거 / 오물풍선(A3, 사건명 Balloon): ρ≥6 → 3거
+BALLOON_KEYWORD = "Balloon"                   # ADR-007 2 오물풍선 = 물리 충돌의 A3 중 사건명에 이 단어(대소문자 무시)가 든 행
 TYPE4_FLOOR_STAGE = 4                            # ADR-007 1-1 4거 유형 사건 당일
 KILL_EVENTS = ("A7-0098", "A7-0100")             # ADR-007 사망·침몰 당일 5거(천안함·연평도)
 KILL_FLOOR_STAGE = 5
@@ -70,6 +71,7 @@ PROVISIONAL_DAYS = 6                             # ADR-006 최근 6일 "잠정"
 TREND_DAYS = 14                                  # U11 10-28 확정 — 14일 변화
 TREND_PCT_MIN = 50                               # U11 10-28 확정 — 14일 전 표시값 50 미만이면 % 숨김
 A2_DATA_END = "2024-11-05"                       # ADR-011a(A2 항목) 안 10-27 사용자 결정 — A2 자료 마지막 날(이후 "자료 없음" 표시)
+A2_NOTE = "A2 자료 없음({end}까지)"               # 일별 CSV `A2자료` 열 문구({end} = A2_DATA_END) — compute_v014.py와 같은 글자
 CRISIS_LIST = (                                  # 내부 위기 목록 10건(검산·게이지 눈금용) — s3_core.py 9~11행 CR과 같음 [확인]
     ("천안함", "2010-03-26", "물리"),
     ("연평도", "2010-11-23", "물리"),
diff --git a/tests/test_core.py b/tests/test_core.py
index 20d5435..1a462a5 100644
--- a/tests/test_core.py
+++ b/tests/test_core.py
@@ -253,3 +253,32 @@ def test_params_none_empty_and_unknown():
 
 def test_calc_days_end_none_is_today():
     assert core.calc_days("2026-01-01", None)[-1] == pd.Timestamp.today().normalize()
+
+
+# F7(F2 검토 발견 10) — 오물풍선 단어·A2 문구는 config, T 구간 문턱은 4개
+@pytest.mark.parametrize("n", [0, 3, 5])
+def test_stage_from_index_needs_four_cuts(n):
+    with pytest.raises(ValueError, match="4개"):
+        core.stage_from_index(pd.Series([1.0, 2.0]), tuple(range(1, n + 1)))
+
+
+@pytest.mark.parametrize("n", [3, 5])
+def test_stage_cuts_needs_four_quantiles(n):
+    with pytest.raises(ValueError, match="4개"):
+        core.stage_cuts(pd.Series([1.0, 2.0, 3.0]), np.array([True] * 3), quantiles=tuple(np.linspace(0.1, 0.9, n)))
+
+
+def test_daily_table_three_quantiles_stops():
+    e, days = base_events(), core.calc_days("2010-01-01", "2020-12-31")
+    with pytest.raises(ValueError, match="4개"):
+        core.daily_table(e, days, B3, set(), {**NOKILL, "quantiles": (0.7, 0.9, 0.95)})
+
+
+def test_balloon_keyword_and_a2_note_come_from_config(monkeypatch):
+    days = pd.date_range("2020-01-25", "2020-02-10")
+    e = ev([("A3-3", "2020-02-01", "A3", PHYS, 3.4, "Balloon launch")])
+    assert core.floor_physical(e, days, set(), kill_ids=())["2020-02-01"] == 1       # 풍선 1건 3.4 < 6
+    monkeypatch.setattr(config, "BALLOON_KEYWORD", "Kite")
+    assert core.floor_physical(e, days, set(), kill_ids=())["2020-02-01"] == 3       # 풍선으로 안 보면 일반 물리 ρ 3.4 ≥ 3
+    monkeypatch.setattr(config, "A2_NOTE", "자료 끝({end})")
+    assert core.a2_note(pd.DatetimeIndex(["2024-11-06"])).tolist() == ["자료 끝(2024-11-05)"]
diff --git a/utils/tension/core.py b/utils/tension/core.py
index be6c54f..d8b7b30 100644
--- a/utils/tension/core.py
+++ b/utils/tension/core.py
@@ -10,8 +10,6 @@ import pandas as pd
 
 import config
 
-BALLOON_KEYWORD = "Balloon"  # ADR-007 2 — 오물풍선 = A3 중 사건명에 Balloon
-
 
 def calc_days(start=config.CALC_START_DATE, end=config.END_DATE) -> pd.DatetimeIndex:
     """(보조) 𝒯 계산 기간 — start~end 하루 간격, end가 None이면 오늘."""
@@ -147,7 +145,7 @@ def floor_physical(events, days, type4_ids, kill_ids=config.KILL_EVENTS, thresho
     순서 그대로(s3_core.floors_s1 + compute_v014.floors_v014): ① 반가우스 판정 → ② 4거 유형일 max → ③ 사망·침몰일 덮어씀.
     """
     ph = events[events["묶음"] == bundle]
-    balloon = ph["요소"].eq("A3") & ph["사건명"].astype(str).str.contains(BALLOON_KEYWORD, case=False, na=False)
+    balloon = ph["요소"].eq("A3") & ph["사건명"].astype(str).str.contains(config.BALLOON_KEYWORD, case=False, na=False)
     rho_o = half_gauss_window(_day_sum(ph[~balloon], days), sigma, window).to_numpy()
     rho_b = half_gauss_window(_day_sum(ph[balloon], days), sigma, window).to_numpy()
     th = thresholds
@@ -179,14 +177,20 @@ def floor_event(events, days, icbm_s=config.EVENT_FLOOR_ICBM_S, stage=config.EVE
 
 # ---- F2-2: ⑨·⑪~⑰ · 일별 결과 조립 ----
 
-A2_NOTE = "A2 자료 없음({end}까지)"  # 일별 CSV A2자료 열 문구 — compute_v014.py
 DAILY_HEAD = ("T_원값", "T_표시7일", "잠정")
 DAILY_TAIL = ("완화할인", "원점수_게이지", "단계_T", "하한_물리", "물리_4거유형일", "하한_E5", "하한_사건", "단계_판정",
               "단계_최종", "그날까지_상위%", "A2자료", "화면_단계문구", "변화14_표시", "변화율14_표시")
 
+def _require_four_cuts(values, what) -> None:
+    """(보조) T 구간 문턱·분위는 정확히 4개(2·3·4·5거 시작) — 아니면 ValueError(F2 검토 발견 10, 자료 이상은 멈춤)."""
+    if len(values) != 4:
+        raise ValueError(f"{what}은 2·3·4·5거 시작 4개여야 함: {len(values)}개")
+
+
 def stage_cuts(T, mask, quantiles=config.STAGE_QUANTILES) -> tuple[np.ndarray, np.ndarray]:
     """⑨ T 구간 — 기준기간 T의 70·90·95·98분위를 반올림한 정수 문턱 θ와 반올림 전 분위."""
     # np.quantile 기본(linear) · np.round 짝수 반올림 그대로(compute_v014.compute — 대응표 ⑨)
+    _require_four_cuts(quantiles, "T 구간 분위")
     q = np.quantile(T[mask], quantiles)
     return np.round(q, 0), q
 
@@ -198,6 +202,7 @@ def cuts_half_warning(q) -> bool:
 
 def stage_from_index(T, cuts) -> pd.Series:
     """⑨ T 구간 단계 L^T — 1 + #{j : T ≥ θ_j} (1~5거)."""
+    _require_four_cuts(cuts, "T 구간 문턱")
     c1, c2, c3, c4 = cuts
     return pd.Series(np.select([T >= c4, T >= c3, T >= c2, T >= c1], [5, 4, 3, 2], 1).astype("int64"), index=T.index)
 
@@ -286,7 +291,7 @@ def provisional(days, n=config.PROVISIONAL_DAYS) -> pd.Series:
 
 def a2_note(days, a2_end=config.A2_DATA_END) -> pd.Series:
     """(보조) A2자료 — a2_end보다 뒤인 날 "A2 자료 없음(a2_end까지)", 그 밖 빈 문자열."""
-    return pd.Series(np.where(days > pd.Timestamp(a2_end), A2_NOTE.format(end=a2_end), ""), index=days)
+    return pd.Series(np.where(days > pd.Timestamp(a2_end), config.A2_NOTE.format(end=a2_end), ""), index=days)
 
 
 def relief_display(T, Tg) -> pd.Series:
```
<!-- F7.code.patch 끝 -->

## 부록 B. `$B/f7_readme.patch` (글자 그대로, md5 `c9c236f818729b778312cbf2a6a478da`)
대상: `README.md` 4절(폴더 구조)·6절 1번 문장만. 다른 절은 건드리지 않는다.

<!-- F7.readme.patch 시작 -->
```diff
diff --git a/README.md b/README.md
index c8c14c7..e2f25ba 100644
--- a/README.md
+++ b/README.md
@@ -52,25 +52,34 @@ Team-Project/
 ├── .streamlit/                  # 스트림릿 디자인 및 설정 파일 (.toml)
 ├── data/                        # 원본 및 샘플 데이터 파일 (.csv, SQLite 등)
 │   └── processed                   # 전처리 완료 CSV (A~F 카테고리 폴더 + 공통_국가코드,단위,참여국)
+│   └── tension                     # 긴장도 결과 CSV(일별·요약·월별·연도별·비교선·반감기 민감도)·사건표·유형판정표·GPR 월별 (커밋)
 ├── db/
 │   └── schema.sql                  # ERD v4 테이블 정의 (기준T, 데이터T, 보조T | FK, CHECK 포함)
 ├── docs/                        # 프로젝트 문서화 폴더
 │   └── decisions.md               # 설정값(가중치·기준선·기준기간 등)을 정한 근거 기록
+│   └── tension                    # 긴장도 산출식·운영·결정 문서 (산출식.md·운영.md·산출식_변경이력.md 등)
+│   └── dev                        # 긴장도 코드화 작업 기록 (작업 프롬프트·보고서·화면 요청서·진행기록)
 ├── pages/                       # 멀티페이지 화면 (파일명 앞 숫자 = 메뉴 순서)
 │   └── 1_긴장도_지수.py            # 현재 단계·평소대비·기준선 카드, 추이 그래프, 과거 유사 시기, 점수 구성
 │   └── 2_사건_기록.py              # 요소·기간별 사건 목록 검색
 │   └── 3_월별_연별.py              # 월별·연별 추이와 대표 사건 TOP5
 │   └── 4_보고서.py                 # 기준일을 골라 요약 보고서 보기·워드(.docx) 내려받기
+├── scripts/                     # 긴장도 계산 실행: build_events.py(원자료 → 사건표) · run_tension.py(사건표 → 결과 CSV)
+├── tests/                       # pytest — 긴장도 계산·화면 통로·화면 AppTest (fixtures = v0.1.4 기준값)
 ├── utils/                       # 공통 함수 및 전처리 모듈
 │   └── build_db.py                 # 1단계: processed CSV -> bongsu.db 통합 표 (사건, 수치, 참여국 등) + 검증
 │   └── build_erd.py                # 2단계: 통합 표 -> ERD v4 테이블 (사건_일단위, 지표값, 상세 13개) + 검증
 │   └── dummy.py                    # 결과 테이블과 같은 모양의 연습용 더미 데이터
 │   └── helpers.py                  # 초기 예시 함수 (현재 화면에서 안 씀)
-│   └── loader.py                   # 데이터 통로: USE_DUMMY에 따라 dummy 또는 real을 불러옴 (캐시 적용)
+│   └── loader.py                   # 데이터 통로: USE_DUMMY에 따라 dummy 또는 real을 불러옴 (캐시 적용) · 긴장도 실제 결과는 `load_tension_*`
 │   └── README.md                   # utils 폴더 설명
 │   └── real.py                     # 실제 사건 CSV → 원점수·평소대비·단계 계산 (결과_일별·월별·연별)
+│   └── tension/                    # 긴장도 계산 (io·core·summary·screen·charts)
 │   └── ui.py                       # 공통 화면 조각 (5단계 눈금 stage_scale)
 ├── .gitignore                   # 깃 제외 파일 목록 (보안 키, 대용량 파일 차단)
+├── .gitattributes               # 결과·기준 CSV 줄바꿈 LF 고정
+├── CLAUDE.md                    # Claude Code 작업 규칙 (긴장도 계산 코드화 작업에만 적용)
+├── pytest.ini                   # pytest 설정 (regression 표시)
 ├── 홈.py                        # 메인 실행 파일
 ├── SOURCES.md                   # 데이터·참고 자료 출처
 ├── config.py                    # 프로젝트 전역 설정값 모음 (반감기, 기준 기간 등)
@@ -145,7 +154,7 @@ Team-Project/
 - **인증키 및 환경변수 (`.env`, `secrets/`)**: BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 업로드하지 않으며, 배포 시 Streamlit `st.secrets`를 활용합니다. - 필요시 생성 예정 -
 
 ### 1. 수집과 화면 코드 분리
-- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`app.py`)은 오직 SQLite 데이터만 읽어 성능을 보장합니다.
+- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`홈.py`)은 SQLite 데이터와 `data/tension/` 결과 CSV만 읽어 성능을 보장합니다. 긴장도 계산은 `scripts/run_tension.py`로 로컬에서 돌려 결과 CSV를 커밋합니다.
 
 ### 2. 보안 및 인증키 관리
 - BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 깃허브에 업로드하지 않습니다 (`.gitignore` 필수 등록 및 Streamlit Cloud 배포 시 `st.secrets` 활용).
```
<!-- F7.readme.patch 끝 -->
