# F8 작업 프롬프트 — 가정 바꿔 보기(슬라이더 재계산): 묶음 비중 ω + 재계산 통로

작성 2026-10-30 · 구현 메인(채팅 ⑦) → Claude Code · 브랜치 **`feature/tension-slider`(F7c PR 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행**(10-30 사용자 결정: 슬라이더 = 반감기·완화 c·κ·묶음 비중 ω · 단계 구간 다시 뽑기 · "공식 결과 아님"은 기본값과 다를 때만 · D1~D6 모두 권장안) — 이 세션은 PR을 draft로 올리고 병합하지 않는다(병합은 사용자 몫)
권장 모델·노력: **Sonnet 5.5 · 중간**(패치 적용 + 실행 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F8_20261030`(`export B=…` — 2절 파이썬이 읽음).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 5절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **바꾸는 파일:** 우리 몫 — `utils/tension/core.py` · `utils/tension/screen.py` · `utils/loader.py` **끝 블록에 함수 1개 더하기만** · `config.py` **8절 끝에 4줄 더하기만** · 새 테스트 `tests/test_recompute.py` · `README.md` **6절 1번 문장 1줄**(F7 때 팀원 허락 범위 4·6절 안). 화면(`홈.py`·`pages/`·`utils/ui.py`)은 건드리지 않는다 — 화면 연결은 박성인 님 몫(요청서 `docs/dev/requests/F8_화면요청.md`).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`·`git rm`(지울 일은 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`홈.py`·`pages/`·`utils/ui.py`·`utils/real.py`·`scripts/**` 수정**, `data/tension/**` 결과 파일 수정, 부록 밖의 코드·테스트·문서 변경, `git commit <경로>` 꼴(항상 `git add` 뒤 `git commit -m`).

---

## 0. 목표 (ADR-019 — 이 프롬프트 커밋 1에 들어가는 `docs/decisions.md`)
- **공식 결과는 그대로 결과 CSV.** 새 통로 `load_tension_recompute(half_life=None, relief_c=None, relief_cap=None, weights=None, scenario="기본")`만 커밋된 사건표로 `core.daily_table`을 다시 부른다(공식 결과 아님 — 모두 기본값이면 공식과 같음).
  - 돌려주는 것 = `(일별 표, 비교 표, 정보 dict)` — 일별 표는 `load_tension_daily()`와 **같은 열·자료형** · 비교 표는 열 `항목 · 공식 · 내 설정`(글자) 20행 · 정보 = `공식과_같음 · 설정 · 비중% · 구간 · 공식_구간 · 같은날% · 한단계안%`.
  - 범위(`config.SLIDER_*`, 8절 끝 4줄): 반감기 7~30일 · c 0~0.3 · κ 0~0.8 · 묶음 배수 0.5~2. 밖이면 ValueError. 단계 구간은 같은 규칙(ADR-018)으로 다시 뽑음.
- **⑥ 묶음 비중 ω:** `core.rising_index(Tg, weights)` = Σ(배수·T_g) ÷ Σ배수, **배수가 모두 같으면 지금 식(합 ÷ 개수) 그대로**(`core.bundle_weight_map`이 None을 돌려줌) → 공식 결과 바이트 동일. `core.PARAM_KEYS`에 `bundle_weights`(21개). `완화할인` 표시 열은 배수를 바꾼 계산만 가중 T⁺ 기준. 원점수 게이지·하한은 그대로.
- **결과 CSV는 바뀌지 않는다** — `run_tension --end 2026-10-29` 결과 7개가 바이트까지 같아야 한다. 새 테스트 20개(`tests/test_recompute.py`).
- 구현 메인 시험본 `[확인 10-30: PC .git 사본 develop fad8310 + F7c 결과(같은 코드) · python 3.13 · numpy 2.4.6 · pandas 3.0.6 · plotly 7.1.0 · streamlit 1.65.0, core.autocrlf=true 체크아웃에서도 git apply 통과·hash 같음]`: 부록 A 패치 → **137 passed**(117 + 새 20), `-m "not regression"` 120 passed · 17 deselected, `-W error::FutureWarning tests/test_screen.py tests/test_recompute.py` 32 passed, `run_tension --end 2026-10-29` 결과 7개 = 커밋된 결과와 **바이트 같음**, AppTest 5화면 통과.
- 숫자 예(끝날 2026-10-29, 기본): 기본값 → 구간 115/256/315/378 · 같은 날 100% / 반감기 21·c 0.2·κ 0.3 → 111/251/302/342 · 같은 날 90.8% / 핵·미사일 2배 → 비중 50·25·25% · 116/267/330/392 · 같은 날 83.0% · 한 단계 안 98.4%.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F8_20261030"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/decisions.md" " M docs/dev/진행기록.md" " M docs/dev/식_함수_대응표.md"
#     " M docs/tension/산출식.md" " M docs/tension/산출식_변경이력.md" " M docs/tension/운영.md"
#     "?? docs/dev/tasks/F8_slider_recompute.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 4절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: develop 또는 feature/tension-cleanup(10-30 사용자가 이 브랜치에서 pull해 62debbf에 있음) — 그 밖이면 멈춤
git log --oneline -1                               # feature/tension-cleanup이면 기대: 62debbf(병합 커밋). 어느 쪽이든 1-1에서 develop으로 옮긴다
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 35 --json state,mergedAt                # 기대: "state":"MERGED"(F7c) — 아니면 멈춤(U4)
git log --oneline -3 origin/develop                # 기대: 맨 위 62debbf(뒤에 커밋이 있으면 누구의 무엇인지 log에 적고 계속 — 2절 git apply --check가 실패하면 거기서 멈춤)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 최신 develop으로
DOCS_M="docs/decisions.md docs/dev/진행기록.md docs/dev/식_함수_대응표.md docs/tension/산출식.md docs/tension/산출식_변경이력.md docs/tension/운영.md"
DOCS_N="docs/dev/tasks/F8_slider_recompute.md"
DOCS="$DOCS_M $DOCS_N"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표(F8_slider_recompute.md 제외 6개 — 내용이 다르면 멈추고 보고)
git restore $DOCS_M
git switch develop                                  # 이미 develop이면 그대로
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in $DOCS; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-slider
# 1-3 이슈: 본문 "$B/issue_F8.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절 첫 줄, 범위 = 0절, 완료 조건 = 4절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F8.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 가정 바꿔 보기 — 슬라이더 재계산 통로·묶음 비중(F8)" --label feat --body-file "$B/issue_F8.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 117 passed(F7c까지)
```
1-1 `md5sum` 기대(CR을 뺀 md5 — `tr -d '\r' < 파일 | md5sum`):
```
7cc7920ae1500c4041d701087da12831  docs/decisions.md
de1c3f6fb082a85a5a4ada10d38bf0e1  docs/dev/진행기록.md
f91e8a1610a5205e17ff9fdf21e5784a  docs/dev/식_함수_대응표.md
da038d3b232b5f44ed430a2e2c3b3e24  docs/tension/산출식.md
c6137e7b65997e954593135c37aa8a72  docs/tension/산출식_변경이력.md
2a429e3ca6539ad0978931579c7b9fd0  docs/tension/운영.md
```

**커밋 1** `docs: F8 작업 프롬프트·설계 문서 반영` — 위 `$DOCS` 7개(내용 수정 없이 — U2). 5절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 패치 적용 (부록 A) → 테스트 → 결과 바이트 확인
```bash
PYTHONIOENCODING=utf-8 <py> - <<'EOF2'
import os, re, pathlib
t = pathlib.Path("docs/dev/tasks/F8_slider_recompute.md").read_text(encoding="utf-8")
m = re.search(r"<!-- F8.code.patch 시작 -->\n```diff\n(.*?)```\n<!-- F8.code.patch 끝 -->", t, re.S)
pathlib.Path(os.environ["B"], "f8_code.patch").write_bytes(m.group(1).encode("utf-8"))
print("저장: f8_code.patch", len(m.group(1).splitlines()), "줄")
EOF2
md5sum "$B/f8_code.patch"
#   기대: a4d344c062d84ac5221f2bb2c208f1da (361줄)
git apply --check "$B/f8_code.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply "$B/f8_code.patch"
git hash-object config.py utils/tension/core.py utils/tension/screen.py utils/loader.py README.md tests/test_recompute.py
#   기대(순서대로):
#     config.py               849f1beede8b1654dbb2021b30a9f77a64b19c57
#     utils/tension/core.py   7b5931e509ce7dbc45cc8699d958659c1bc85126
#     utils/tension/screen.py 1ab6c51cabed82c9eae53d175222a624e92dd539
#     utils/loader.py         7fd1a0fa84ebd1616761af4b90dd81d6fbb3a721
#     README.md               c087da6089c32f6f0f90f1a957540bfa07b3e930
#     tests/test_recompute.py 25ecdc9e9921d982b671ffd3e1842c50c62f2a5b
#   하나라도 다르면 멈추고 보고
git diff --stat                                    # 기대(새 파일 tests/test_recompute.py는 untracked라 안 나옴): 5 files changed, 138 insertions(+), 14 deletions(-)
git diff config.py utils/loader.py README.md | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '
#   기대: config.py는 SLIDER_ 4줄 더함만 · loader.py는 끝에 7줄 더함만 · README.md는 6절 1번 문장 1줄 바꿈
```
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest                                    # 기대: 137 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                # 기대: 120 passed, 17 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_screen.py tests/test_recompute.py   # 기대: 32 passed
mkdir -p "$B/after"
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --end 2026-10-29 --out "$B/after"
for f in 일별_기본 일별_확장 요약 월별 연도별 비교선_일별 반감기_민감도; do cmp "$B/after/$f.csv" "data/tension/$f.csv" && echo "같음 $f" || echo "다름 $f — 멈추고 보고"; done
git status --porcelain data/                       # 기대: 줄 없음(결과는 $B/after에만 썼다)
PYTHONIOENCODING=utf-8 <py> -c "
import time
from utils import loader
from utils.tension import screen
v, t, m = screen.recompute(); print(v.equals(screen.daily()), m['공식과_같음'], m['구간'], m['같은날%'])
v, t, m = screen.recompute(21, 0.2, 0.3); print(m['구간'], m['공식과_같음'], m['같은날%'])
t0 = time.time(); v, t, m = loader.load_tension_recompute(weights={'핵·미사일': 2}); s = time.time() - t0
print(m['비중%'], m['구간'], m['같은날%'], m['한단계안%'], len(t), list(t.columns), f'{s:.2f}초')
"
#   기대: True True (115, 256, 315, 378) 100.0
#         (111, 251, 302, 342) False 90.8
#         {'핵·미사일': 50.0, '군사 과시': 25.0, '위협 언어·교리': 25.0} (116, 267, 330, 392) 83.0 98.4 20 ['항목', '공식', '내 설정'] <초>   (초는 log에 적기만 — streamlit 경고 줄이 앞에 나와도 됨)
```
- 다르면: 파일도 코드도 고치지 말고 차이를 log에 남기고 멈추고 보고한다(버전 차이로 보이면 그렇게 적는다).
- `--end`를 반드시 `2026-10-29`로 고정한다.

**커밋 2** `feat: 묶음 비중과 가정 바꿔 보기 재계산 통로` — `utils/tension/core.py` · `utils/tension/screen.py` · `utils/loader.py` · `config.py`
**커밋 3** `test: 가정 바꿔 보기 재계산 테스트` — `tests/test_recompute.py`
**커밋 4** `docs: README 6절에 앱 안 재계산 예외 한 줄` — `README.md`

## 3. 하지 않는 것
- 문서 7개·설계 문서의 내용 수정(커밋 1은 그대로), 화면(`홈.py`·`pages/`)·`utils/ui.py`·`utils/real.py`·`scripts/**` 수정
- `config.py` 8절 끝 4줄 밖 수정, `utils/loader.py` 끝 블록 밖 수정, README 6절 1번 문장 밖 수정
- `data/tension/` 결과·사건표·판정표 수정(검산 결과는 `$B/after`에만), 기존 테스트 수정, `tests/fixtures/` 수정
- 부록과 다른 코드·테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절), 원격·로컬 브랜치 삭제

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | F7c PR MERGED, 훅 있음, 117 passed, 버전 적음, 1-1 md5 6개 같음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-slider`, 이슈 번호 |
| 3 | 2절 패치 | 패치 md5 같음, `git apply --check` 통과, hash 6개 같음, `--stat` 5 files · 138 insertions · 14 deletions, config·loader·README 바뀐 줄이 기대대로 |
| 4 | 2절 테스트 | 137 passed · not regression 120/17 · FutureWarning 32 passed |
| 5 | 2절 결과 | `run_tension --end 2026-10-29` 결과 7개가 커밋된 결과와 바이트 같음, `data/` 변경 없음 |
| 6 | 2절 재계산 확인 | 기본값 = 공식(True True 115/256/315/378 100.0) · 21/0.2/0.3 → 111/251/302/342 · 핵·미사일 2배 → 50·25·25 · 116/267/330/392 · 83.0 · 98.4 · 비교 표 20행 |
| 7 | 커밋 | 5절 순서 5개 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 10 | 마지막 status | `?? .obsidian/` 하나만 |

## 5. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F8 작업 프롬프트·설계 문서 반영` — 1절 `$DOCS` 7개
2. `feat: 묶음 비중과 가정 바꿔 보기 재계산 통로` — `utils/tension/core.py` · `utils/tension/screen.py` · `utils/loader.py` · `config.py`
3. `test: 가정 바꿔 보기 재계산 테스트` — `tests/test_recompute.py`
4. `docs: README 6절에 앱 안 재계산 예외 한 줄` — `README.md`
5. `docs: F8 보고서` — `docs/dev/reports/F8_report.md` · `F8_log.md`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 137 passed
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-slider
# 본문 "$B/pr_F8.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 · 테스트 = 2절 결과(137 passed, 결과 CSV 바이트 동일, AppTest 5화면)
#   · 체크리스트 아래에 팀원 안내 네 줄:
#     "긴장도 '가정 바꿔 보기'(슬라이더 재계산) 통로를 더했습니다: loader.load_tension_recompute(half_life, relief_c, relief_cap, weights, scenario) → (일별 표, 비교 표, 정보). 화면 연결은 박성인 님께 요청서(docs/dev/requests/F8_화면요청.md 확정본)로 따로 드립니다."
#     "공식 결과(결과 CSV·load_tension_* 기존 함수)는 그대로이고, 모두 기본값이면 재계산 결과가 공식 결과와 같습니다(테스트로 고정). 슬라이더 범위는 config.py 8절 끝 SLIDER_* 4줄입니다."
#     "README 6절 1번 문장에 '앱 안 재계산 예외(ADR-019)' 한 줄을 더했습니다. 화면 파일(홈.py·pages/·ui.py)은 바꾸지 않았습니다."
#     "결정 근거는 docs/decisions.md ADR-019, 산출식 변경 기록은 docs/tension/산출식_변경이력.md C22입니다."
grep -inE "$AI" "$B/pr_F8.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 가정 바꿔 보기 — 슬라이더 재계산 통로·묶음 비중(F8)" --body-file "$B/pr_F8.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다). 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 6. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F8_report.md`(60줄 이내): 1절 = 4절 표 10행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F8_log.md`: 1~2절 출력 전부(문서 md5, 패치 md5·hash, diff 줄, 테스트 결과, 결과 7개 cmp, 재계산 확인 출력과 걸린 시간), 작성자 목록, 커밋·푸시·PR 출력.

---

## 부록 A. `$B/f8_code.patch` (2절 파이썬으로 잘라 저장 — 글자 그대로, md5 `a4d344c062d84ac5221f2bb2c208f1da`, 361줄 · config·core·screen·loader·README + 새 tests/test_recompute.py, 모두 LF)

<!-- F8.code.patch 시작 -->
```diff
diff --git a/README.md b/README.md
index 8b7da2c..c087da6 100644
--- a/README.md
+++ b/README.md
@@ -153,7 +153,7 @@ Team-Project/
 - **인증키 및 환경변수 (`.env`, `secrets/`)**: BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 업로드하지 않으며, 배포 시 Streamlit `st.secrets`를 활용합니다. - 필요시 생성 예정 -
 
 ### 1. 수집과 화면 코드 분리
-- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`홈.py`)은 SQLite 데이터와 `data/tension/` 결과 CSV만 읽어 성능을 보장합니다. 긴장도 계산은 `scripts/run_tension.py`로 로컬에서 돌려 결과 CSV를 커밋합니다.
+- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`홈.py`)은 SQLite 데이터와 `data/tension/` 결과 CSV만 읽어 성능을 보장합니다. 긴장도 계산은 `scripts/run_tension.py`로 로컬에서 돌려 결과 CSV를 커밋합니다. 예외는 긴장도 "가정 바꿔 보기"(슬라이더) 한 곳으로, 커밋된 사건표로 앱 안에서 다시 계산하고 "공식 결과가 아님"으로 표시합니다(`docs/decisions.md` ADR-019).
 
 ### 2. 보안 및 인증키 관리
 - BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 깃허브에 업로드하지 않습니다 (`.gitignore` 필수 등록 및 Streamlit Cloud 배포 시 `st.secrets` 활용).
diff --git a/config.py b/config.py
index 6ba57f5..849f1be 100644
--- a/config.py
+++ b/config.py
@@ -79,3 +79,7 @@ TENSION_DATA_DIR = "data/tension"                # 결과 CSV 폴더(커밋)
 TYPE4_TABLE_PATH = "data/tension/물리사건_유형판정표.csv"   # 유형판정표 사본(F1에서 복사, 커밋)
 HALF_LIFE_SENSITIVITY = (7, 14, 21, 30)          # ADR-006 1번 — 반감기 민감도(공개용 표, 단계 판정은 HALF_LIFE_DAYS). 하한 감쇠는 그대로
 GPR_PATH = "data/tension/GPR_한국_월별.csv"        # ADR-002 GPR 한국(GPRC_KOR) 월별 — 비교 지수만. 채점_v0 입력 그대로 복사(F6)
+SLIDER_HALF_LIFE = (7, 30)                       # ADR-019 가정 바꿔 보기(F8) — 반감기(일) 슬라이더 범위(기본 = HALF_LIFE_DAYS)
+SLIDER_RELIEF_C = (0.0, 0.3)                     # ADR-019 완화 세기 c 범위(기본 = RELIEF_C)
+SLIDER_RELIEF_CAP = (0.0, 0.8)                   # ADR-019 완화 상한 κ 범위(기본 = RELIEF_CAP)
+SLIDER_WEIGHT = (0.5, 2.0)                       # ADR-019 묶음 비중 배수 범위(묶음마다, 기본 1배 = 동일 가중)
diff --git a/tests/test_recompute.py b/tests/test_recompute.py
new file mode 100644
index 0000000..25ecdc9
--- /dev/null
+++ b/tests/test_recompute.py
@@ -0,0 +1,88 @@
+"""가정 바꿔 보기(F8, ADR-019) 테스트 — 반감기·완화 c·κ·묶음 비중을 바꾼 재계산. 모두 기본값이면 공식 결과와 같아야 한다."""
+import numpy as np
+import pandas as pd
+import pytest
+
+import config
+from utils.tension import core, screen
+
+B3 = list(config.BUNDLES_BASE)
+
+
+@pytest.fixture(scope="module")
+def official():
+    return screen.daily("기본")
+
+
+@pytest.mark.parametrize("scenario", ["기본", "확장"])
+def test_default_equals_official(scenario):
+    view, table, meta = screen.recompute(scenario=scenario)
+    assert view.equals(screen.daily(scenario))                       # 열·값·자료형까지 공식 결과와 같음
+    assert meta["공식과_같음"] and meta["같은날%"] == 100.0 and meta["구간"] == screen.cuts(scenario)
+    assert (table["공식"] == table["내 설정"]).all()
+
+
+def test_equal_multipliers_are_default(official):
+    view, _, meta = screen.recompute(weights={b: 2 for b in B3})
+    assert view.equals(official) and meta["공식과_같음"]
+    assert meta["비중%"] == {b: 33.3 for b in B3}
+
+
+def test_core_equal_weights_take_current_path():
+    raw = screen.daily_raw("기본")
+    events, type4 = screen._recompute_inputs("기본", screen.DATA_DIR)
+    days = pd.DatetimeIndex(raw.index)
+    a, _ = core.daily_table(events, days, B3, type4)
+    b, _ = core.daily_table(events, days, B3, type4, {"bundle_weights": {x: 1.5 for x in B3}})
+    assert a.equals(b)                                                # 같은 배수 = 지금 경로(합 ÷ 개수) 그대로
+    assert "bundle_weights" in core.PARAM_KEYS
+
+
+def test_slider_values_recut_stages():
+    _, table, meta = screen.recompute(21, 0.2, 0.3)
+    assert meta["구간"] == (111, 251, 302, 342) and not meta["공식과_같음"]   # 10-30 측정값(ADR-018 규칙으로 다시 뽑음)
+    assert table.set_index("항목").loc["단계 구간(2·3·4·5거 시작)", "공식"] == "115/256/315/378"
+
+
+def test_weights_change_t_plus(official):
+    view, _, meta = screen.recompute(weights={"핵·미사일": 2})
+    assert meta["비중%"] == {"핵·미사일": 50.0, "군사 과시": 25.0, "위협 언어·교리": 25.0}
+    assert not meta["공식과_같음"] and meta["구간"] != screen.cuts("기본")
+    tg = view[[f"Tg_{b}" for b in B3]].to_numpy()
+    t_plus = (2 * tg[:, 0] + tg[:, 1] + tg[:, 2]) / 4                    # T⁺ = Σ(배수·T_g) ÷ Σ배수
+    T = t_plus * (1 - view["완화할인_δ"].to_numpy())
+    assert (np.abs(T - view["T_원값"].to_numpy()) <= 0.0006 * t_plus + 0.002).all()   # 반올림(3자리, δ×T⁺) 차이만
+    on = t_plus > 0                                                     # 완화할인 표시 열도 가중 T⁺ 기준
+    assert np.abs(view.loc[on, "완화할인"].to_numpy() - view.loc[on, "완화할인_δ"].to_numpy()).max() < 0.0011   # T⁺ > 0이면 δ와 같음
+    assert view["원점수_게이지"].equals(official["원점수_게이지"])          # 원점수 게이지(R 합)는 ω와 무관
+    assert view["하한_물리"].equals(official["하한_물리"])                  # 하한은 그대로
+
+
+def test_extended_scenario_weights():
+    _, _, meta = screen.recompute(weights={"제재·압박": 0.5}, scenario="확장")
+    assert meta["비중%"]["제재·압박"] == round(0.5 / 3.5 * 100, 1) and not meta["공식과_같음"]
+
+
+@pytest.mark.parametrize("kwargs", [
+    {"half_life": 6}, {"half_life": 31}, {"relief_c": -0.1}, {"relief_c": 0.31}, {"relief_cap": 0.81},
+    {"weights": {"핵·미사일": 0.4}}, {"weights": {"핵·미사일": 2.1}}, {"weights": {"제재·압박": 1}},
+    {"weights": {"없는 묶음": 1}}, {"scenario": "없음"}, {"half_life": float("nan")},
+])
+def test_out_of_range_stops(kwargs):
+    with pytest.raises(ValueError):
+        screen.recompute(**kwargs)
+
+
+def test_core_bundle_weights_checks():
+    assert core.bundle_weight_map(None, B3) is None and core.bundle_weight_map({"핵·미사일": 1}, B3) is None
+    assert core.bundle_weight_map({"핵·미사일": 2}, B3) == {"핵·미사일": 2.0, "군사 과시": 1.0, "위협 언어·교리": 1.0}
+    for bad in ({"없는 묶음": 1}, {"핵·미사일": 0}, {"핵·미사일": -1}, {"핵·미사일": float("inf")}):
+        with pytest.raises(ValueError):
+            core.bundle_weight_map(bad, B3)
+
+
+def test_loader_recompute_matches_screen():
+    from utils import loader
+    a = loader.load_tension_recompute(weights={"핵·미사일": 2})
+    b = screen.recompute(weights={"핵·미사일": 2})
+    assert a[0].equals(b[0]) and a[1].equals(b[1]) and a[2] == b[2]
diff --git a/utils/loader.py b/utils/loader.py
index 53d9220..7fd1a0f 100644
--- a/utils/loader.py
+++ b/utils/loader.py
@@ -97,3 +97,10 @@ def load_tension_month_events(month, scenario="기본", top=3):  # 그달 주요
 @st.cache_data
 def load_tension_events(scenario="기본"):  # 사건표 — 사건ID·date(날짜형)·요소·묶음·S·사건명 (지수에 들어간 사건 전부, 기본 720건·확장 941건)
     return tension_screen.events_table(scenario)
+
+
+# ===== [F8 추가 · 긴장도 담당] 가정 바꿔 보기(슬라이더 재계산) — 공식 결과 아님, 모두 기본값이면 공식과 같음(ADR-019) =====
+# 화면에 붙이는 일은 화면 담당자께 요청(docs/dev/requests/F8_화면요청.md). 범위·기본값 = config.SLIDER_* · HALF_LIFE_DAYS · RELIEF_C · RELIEF_CAP.
+@st.cache_data
+def load_tension_recompute(half_life=None, relief_c=None, relief_cap=None, weights=None, scenario="기본"):  # (일별 표, 비교 표, 정보 dict) — None = 기본값, weights = {묶음: 배수}, 범위 밖이면 ValueError
+    return tension_screen.recompute(half_life, relief_c, relief_cap, weights, scenario)
diff --git a/utils/tension/core.py b/utils/tension/core.py
index d8b7b30..7b5931e 100644
--- a/utils/tension/core.py
+++ b/utils/tension/core.py
@@ -76,10 +76,31 @@ def relative_index(R, B) -> pd.DataFrame:
     return pd.DataFrame({c: R[c] / B[c] * 100 for c in R.columns}, index=R.index)
 
 
-def rising_index(Tg) -> pd.Series:
-    """⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중)."""
-    # 기준 구현 sum(Tg.values()) / len(bundles) — 열 순서대로 더한 뒤 나눈다(mean(axis=1) 아님)
-    return sum(Tg[c] for c in Tg.columns) / len(Tg.columns)
+def bundle_weight_map(weights, bundles):
+    """(보조) ⑥ 묶음 비중(ADR-019) — {묶음: 배수} 검사. 빠진 묶음 = 1배. 배수가 모두 같으면 None(= 동일 가중, 지금 경로).
+
+    모르는 묶음·0 이하·숫자 아님은 멈춘다(ValueError). 슬라이더 범위(config.SLIDER_WEIGHT)는 화면 통로(screen)가 본다.
+    """
+    if weights is None:
+        return None
+    bundles = list(bundles)
+    unknown = sorted(set(weights) - set(bundles))
+    if unknown:
+        raise ValueError(f"bundle_weights에 상승 묶음이 아닌 키 {unknown} — 쓸 수 있는 묶음: {bundles}")
+    w = {b: float(weights.get(b, 1.0)) for b in bundles}
+    bad = [b for b, v in w.items() if not (np.isfinite(v) and v > 0)]
+    if bad:
+        raise ValueError(f"bundle_weights 배수는 0보다 큰 수여야 함: {bad}")
+    return None if len(set(w.values())) == 1 else w
+
+
+def rising_index(Tg, weights=None) -> pd.Series:
+    """⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중). weights = {묶음: 배수}면 가중 평균 Σ(배수·T_g) ÷ Σ배수(ADR-019)."""
+    w = bundle_weight_map(weights, Tg.columns)
+    if w is None:
+        # 기준 구현 sum(Tg.values()) / len(bundles) — 열 순서대로 더한 뒤 나눈다(mean(axis=1) 아님)
+        return sum(Tg[c] for c in Tg.columns) / len(Tg.columns)
+    return sum(Tg[c] * w[c] for c in Tg.columns) / sum(w[c] for c in Tg.columns)
 
 
 def relief_discount(R_relief, B_relief, c=config.RELIEF_C, cap=config.RELIEF_CAP) -> pd.Series:
@@ -97,10 +118,11 @@ def tension_index(T_plus, delta) -> pd.Series:
 
 def tension_components(events, days, bundles, base_period=config.BASE_PERIOD, half_life=config.HALF_LIFE_DAYS,
                        relief_c=config.RELIEF_C, relief_cap=config.RELIEF_CAP,
-                       relief_bundle=config.BUNDLE_RELIEF) -> tuple[pd.DataFrame, pd.Series]:
+                       relief_bundle=config.BUNDLE_RELIEF, bundle_weights=None) -> tuple[pd.DataFrame, pd.Series]:
     """②~⑧ 묶음 — 사건표에서 R·B·T_g·T⁺·δ·T를 한 번에.
 
     반환 = (열 R_<대상>·Tg_<묶음>·T_plus·delta·T 인 DataFrame, 평소값 B Series). 대상 = bundles + relief_bundle.
+    bundle_weights = {묶음: 배수}(ADR-019 — 앱의 가정 바꿔 보기). None이거나 모두 같으면 동일 가중.
     기준 구현은 run을 두 번 부르지만 T는 단계 구간과 무관하므로 한 번만 계산한다.
     """
     bundles = list(bundles)
@@ -113,7 +135,7 @@ def tension_components(events, days, bundles, base_period=config.BASE_PERIOD, ha
     if bad:
         raise ValueError(f"기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): {bad}")
     Tg = relative_index(R[bundles], B[bundles])
-    T_plus = rising_index(Tg)
+    T_plus = rising_index(Tg, bundle_weights)
     delta = relief_discount(R[relief_bundle], B[relief_bundle], relief_c, relief_cap)
     T = tension_index(T_plus, delta)
     comp = pd.concat([R.add_prefix("R_"), Tg.add_prefix("Tg_")], axis=1)
@@ -294,10 +316,11 @@ def a2_note(days, a2_end=config.A2_DATA_END) -> pd.Series:
     return pd.Series(np.where(days > pd.Timestamp(a2_end), config.A2_NOTE.format(end=a2_end), ""), index=days)
 
 
-def relief_display(T, Tg) -> pd.Series:
-    """(보조) 완화할인 열 — 1 − T / mean(T_g), mean = 0인 날 0 (δ와 다름 — 대응표 2절)."""
+def relief_display(T, Tg, T_plus=None) -> pd.Series:
+    """(보조) 완화할인 열 — 1 − T / mean(T_g), mean = 0인 날 0 (δ와 다름 — 대응표 2절). 묶음 비중을 바꾼 계산은 T_plus(가중 T⁺)로."""
     # 기준 구현 정의 그대로: T⁺ = 0인 날은 δ > 0이어도 0(회귀 일치를 위해 이식 — 대응표 2절 완화할인)
-    return (1 - T / Tg.mean(axis=1).replace(0, np.nan)).fillna(0)
+    denom = Tg.mean(axis=1) if T_plus is None else T_plus   # ADR-019: 동일 가중이면 지금 식 그대로(바이트 동일)
+    return (1 - T / denom.replace(0, np.nan)).fillna(0)
 
 
 def daily_columns(bundles) -> list[str]:
@@ -308,7 +331,8 @@ def daily_columns(bundles) -> list[str]:
 # daily_table params 키 — 값을 바꾼 계산(민감도·비교선)은 config를 고치지 말고 이 키로 넘긴다(사용자 10-29)
 PARAM_KEYS = ("base_period", "half_life", "relief_c", "relief_cap", "quantiles", "sigma", "window",
               "phys_thresholds", "type4_stage", "kill_ids", "kill_stage", "e5_thresholds", "icbm_s", "event_stage",
-              "step_days", "ma_days", "provisional_days", "trend_days", "trend_pct_min", "a2_end")
+              "step_days", "ma_days", "provisional_days", "trend_days", "trend_pct_min", "a2_end",
+              "bundle_weights")   # F8(ADR-019): 묶음 비중 {묶음: 배수} — 앱의 가정 바꿔 보기만 씀
 
 
 def _pick(params, **argmap) -> dict:
@@ -330,8 +354,10 @@ def daily_table(events, days, bundles, type4_ids, params=None) -> tuple[pd.DataF
     if unknown:
         raise ValueError(f"params에 모르는 키 {unknown} — 쓸 수 있는 키: {list(PARAM_KEYS)}")
     bundles = list(bundles)
+    weighted = bundle_weight_map(p.get("bundle_weights"), bundles) is not None   # 모르는 묶음·0 이하는 여기서 멈춤
     comp, B = tension_components(events, days, bundles, **_pick(p, base_period="base_period", half_life="half_life",
-                                                                 relief_c="relief_c", relief_cap="relief_cap"))
+                                                                 relief_c="relief_c", relief_cap="relief_cap",
+                                                                 bundle_weights="bundle_weights"))
     T = comp["T"]
     Tg = comp[[f"Tg_{b}" for b in bundles]]
     # T는 한 번만 계산 — 구간과 무관(대응표 ⑨)
@@ -350,7 +376,7 @@ def daily_table(events, days, bundles, type4_ids, params=None) -> tuple[pd.DataF
     tr = trend(T_bar, **_pick(p, days="trend_days", pct_min="trend_pct_min"))
     cols = {"T_원값": T, "T_표시7일": T_bar, "잠정": provisional(days, **_pick(p, n="provisional_days")),
             **{f"Tg_{b}": Tg[f"Tg_{b}"] for b in bundles},
-            "완화할인": relief_display(T, Tg), "원점수_게이지": raw_gauge(comp, bundles), "단계_T": LT,
+            "완화할인": relief_display(T, Tg, comp["T_plus"] if weighted else None), "원점수_게이지": raw_gauge(comp, bundles), "단계_T": LT,
             "하한_물리": fp, "물리_4거유형일": type4_days(events, days, type4_ids), "하한_E5": fe, "하한_사건": fs,
             "단계_판정": J, "단계_최종": L, "그날까지_상위%": cumulative_top_pct(T_bar),
             "A2자료": a2_note(days, **_pick(p, a2_end="a2_end")),
diff --git a/utils/tension/screen.py b/utils/tension/screen.py
index 08f9ca4..1ab6c51 100644
--- a/utils/tension/screen.py
+++ b/utils/tension/screen.py
@@ -6,7 +6,10 @@
 주체국을 못 붙이면 "미상" · 완화 할인은 실제 δ · 시나리오는 기본이 주, 확장은 추이 그림 점선.
 F6(10-29 사용자): 비교선 T_basic(⑮′ — 정규화 효과만, 설명 자리용) · GPR 한국 월별 비교(순위% 두 선) · 반감기 민감도 표 ·
 반감기 설명 문구 · 유사 시기 그달 주요 사건.
+F8(10-30 사용자, ADR-019): 가정 바꿔 보기 — 반감기·완화 c·κ·묶음 비중을 바꿔 사건표에서 다시 계산(`recompute`). 공식 결과는 여전히
+결과 CSV이고, 이 함수만 앱 안에서 계산한다(모두 기본값이면 공식 결과와 같음 — 테스트로 고정).
 """
+import io
 from functools import lru_cache
 from pathlib import Path
 
@@ -92,6 +95,11 @@ def daily(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
     단계이름 · 지속일수(4거 이상 며칠째) · 상위%_표시(첫 365일 NaN) · 완화할인_δ.
     """
     raw = daily_raw(scenario, data_dir)
+    return _screen_view(raw, relief_delta(scenario, raw.index, data_dir))
+
+
+def _screen_view(raw, delta) -> pd.DataFrame:
+    """(보조) 일별 결과 표(날짜 인덱스, 결과 CSV와 같은 모양) + 완화 할인 δ → 화면 일별 표(daily()와 같은 열)."""
     d = raw.reset_index()
     d["평소대비"] = d["T_표시7일"]
     d["평소대비_원값"] = d["T_원값"]
@@ -102,7 +110,7 @@ def daily(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
     top = d["그날까지_상위%"].astype(float).copy()
     top.iloc[:TOP_PCT_HIDE_DAYS] = np.nan
     d["상위%_표시"] = np.round(top, 1)   # 사용자 10-30: 요약.csv·그림 hover와 같은 반올림(np.round) — 화면 :.1f는 x.x5에서 달랐음(43.15 → 43.1)
-    d["완화할인_δ"] = relief_delta(scenario, raw.index, data_dir).round(3).to_numpy()
+    d["완화할인_δ"] = pd.Series(delta).round(3).to_numpy()
     return d
 
 
@@ -324,3 +332,82 @@ def gpr_figure(scenario="기본", data_dir=DATA_DIR, gpr_path=None):
     """(화면) GPR 비교 그림 — charts.gpr_figure(순위% 두 선)."""
     from utils.tension import charts
     return charts.gpr_figure(gpr_compare(scenario, data_dir, gpr_path))
+
+
+# ===== F8 가정 바꿔 보기(슬라이더 재계산, ADR-019) =====
+@lru_cache(maxsize=4)
+def _recompute_inputs(scenario, data_dir):
+    """(보조) 사건표·4거 유형 사건ID — 시나리오마다 한 번만 읽는다(함수 안에서 고치지 않음)."""
+    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
+    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
+    return events, type4
+
+
+def _in_range(name, value, bounds):
+    lo, hi = bounds
+    if not (np.isfinite(float(value)) and lo <= float(value) <= hi):
+        raise ValueError(f"{name} {value}은(는) 범위 {lo:g}~{hi:g} 밖")
+
+
+def _csv_roundtrip(daily) -> pd.DataFrame:
+    """(보조) 일별 결과를 결과 CSV와 같은 글자로 썼다가 다시 읽는다 — 화면 표의 값·자료형을 공식 결과(daily_raw)와 같게."""
+    buf = io.StringIO()
+    daily.round(3).to_csv(buf, index=True, lineterminator="\n")
+    buf.seek(0)
+    return pd.read_csv(buf, index_col=0, parse_dates=True)
+
+
+def _stage_pct(L, k):
+    return round((L == k).mean() * 100, 1)
+
+
+def recompute(half_life=None, relief_c=None, relief_cap=None, weights=None, scenario="기본", data_dir=DATA_DIR):
+    """(화면) 가정 바꿔 보기(F8) — 반감기·완화 세기 c·완화 상한 κ·묶음 비중을 바꿔 사건표에서 다시 계산한다(공식 결과 아님).
+
+    None = 기본값(config). weights = {묶음: 배수}(빠진 묶음 1배). 범위 = config.SLIDER_*(밖이면 ValueError).
+    단계 구간은 같은 규칙(⑨ 기준기간 70·90·95·98분위)으로 다시 뽑는다. 하한·하강 7일·기준기간·사건 점수 S는 그대로.
+    반환 = (일별 표 — daily()와 같은 열, 비교 표 — 열 항목·공식·내 설정(글자), 정보 dict). 모두 기본값이면 공식 결과와 같다.
+    """
+    _check(scenario)
+    bundles = list(SCENARIOS[scenario])
+    h = config.HALF_LIFE_DAYS if half_life is None else half_life
+    c = config.RELIEF_C if relief_c is None else relief_c
+    cap = config.RELIEF_CAP if relief_cap is None else relief_cap
+    _in_range("반감기(일)", h, config.SLIDER_HALF_LIFE)
+    _in_range("완화 세기 c", c, config.SLIDER_RELIEF_C)
+    _in_range("완화 상한 κ", cap, config.SLIDER_RELIEF_CAP)
+    mult = {b: 1.0 for b in bundles}
+    unknown = sorted(set(weights or {}) - set(bundles))
+    if unknown:
+        raise ValueError(f"묶음 비중에 {scenario} 상승 묶음이 아닌 키 {unknown} — 쓸 수 있는 묶음: {bundles}")
+    for b, v in (weights or {}).items():
+        _in_range(f"묶음 비중({b})", v, config.SLIDER_WEIGHT)
+        mult[b] = float(v)
+    w = core.bundle_weight_map(mult, bundles)   # 모두 같은 배수면 None(동일 가중 = 공식과 같은 계산)
+    params = {"half_life": h, "relief_c": c, "relief_cap": cap}
+    if w is not None:
+        params["bundle_weights"] = w
+    raw_off = daily_raw(scenario, data_dir)
+    events, type4 = _recompute_inputs(scenario, Path(data_dir))
+    mine, info = core.daily_table(events, pd.DatetimeIndex(raw_off.index), bundles, type4, params)
+    view = _screen_view(_csv_roundtrip(mine), info["components"]["delta"])
+    same = (h == config.HALF_LIFE_DAYS and c == config.RELIEF_C and cap == config.RELIEF_CAP and w is None)
+    L_off = raw_off["단계_최종"].astype("int64")
+    L = view["최종단계"].set_axis(L_off.index)
+    cuts_off, cuts_mine = cuts(scenario, data_dir), tuple(int(x) for x in info["cuts"])
+    same_pct, near_pct = round((L == L_off).mean() * 100, 1), round(((L - L_off).abs() <= 1).mean() * 100, 1)
+    s_off, s_mine = core.crisis_window_max(L_off), core.crisis_window_max(L)
+    rows = [("현재 단계", raw_off["화면_단계문구"].iloc[-1], view["화면_단계문구"].iloc[-1]),
+            ("평소 대비(7일)", f"{np.round(raw_off['T_표시7일'].iloc[-1], 1):.1f}", f"{np.round(view['T_표시7일'].iloc[-1], 1):.1f}"),
+            ("단계 구간(2·3·4·5거 시작)", "/".join(map(str, cuts_off)), "/".join(map(str, cuts_mine))),
+            *[(f"{k}거 날 %", f"{_stage_pct(L_off, k):.1f}", f"{_stage_pct(L, k):.1f}") for k in range(1, 6)],
+            ("공식과 단계 같은 날 %", "100.0", f"{same_pct:.1f}"),
+            ("공식과 한 단계 안 %", "100.0", f"{near_pct:.1f}"),
+            *[(f"위기 · {name}({day})", f"{int(s_off[name])}거", f"{int(s_mine[name])}거") for name, day, _ in config.CRISIS_LIST]]
+    table = pd.DataFrame(rows, columns=["항목", "공식", "내 설정"])
+    total = sum(mult.values())
+    meta = {"공식과_같음": same,
+            "설정": {"반감기": h, "완화 세기 c": c, "완화 상한 κ": cap, "묶음 배수": dict(mult)},
+            "비중%": {b: round(m / total * 100, 1) for b, m in mult.items()},
+            "구간": cuts_mine, "공식_구간": cuts_off, "같은날%": same_pct, "한단계안%": near_pct}
+    return view, table, meta
```
<!-- F8.code.patch 끝 -->
