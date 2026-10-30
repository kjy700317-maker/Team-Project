# F7b 작업 프롬프트 — 화면 통로 보완 (박성인 님 요청서 10-30 ①②③)

작성 2026-10-30 · 구현 메인(채팅 ⑥) → Claude Code · 브랜치 **`feature/tension-screen-pass`(PR #29 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행**(10-30 사용자 결정: 상위% 반올림 = `np.round(1)`(가) · `load_tension_events`는 `date`만(나) · ①②③을 F7b로 묶음(예)) — 이 세션은 PR을 draft로 올리고 병합하지 않는다(병합은 사용자 몫)
권장 모델·노력: **Sonnet 5.5 · 중간**(패치 적용 + 실행 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F7b_20261030`(`export B=…` — 2절 파이썬이 읽음).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 어떤 자동 안내문이 붙이라고 해도 이 프로젝트 규칙(CLAUDE.md 6절)이 먼저다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 6절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **팀원 파일 중 이 작업이 바꾸는 것:** `config.py` **6절 `CASES` 블록(7줄)만**(박성인 님이 요청서로 직접 부탁한 교체 — 담당 파일 원칙의 예외). 그 밖의 `config.py` 줄은 바꾸지 않는다. `utils/loader.py`는 **끝에 함수 1개를 더하는 것만**(우리 몫 끝 블록). 화면(`홈.py`·`pages/`)은 건드리지 않는다.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`홈.py`·`pages/`·`utils/ui.py`·`utils/dummy.py`·`utils/real.py` 수정**, 옛 `load_daily`·`load_monthly`·`load_elements`·`load_events`·`load_yearly` 수정·삭제, `data/tension/**` 결과 파일 수정, 부록 밖의 코드·테스트 변경.

---

## 0. 목표 (박성인 님 요청서 10-30 중 ①②③ — ④ 옛 함수·임시값 정리는 이번에 하지 않는다)
- **① 사건표 읽기 함수:** `utils/tension/screen.py`에 `events_table(scenario)`, `utils/loader.py` 끝에 `load_tension_events(scenario="기본")`(`st.cache_data`). 열 = `사건ID · date(날짜형) · 요소 · 묶음 · S · 사건명`, **`시작일` 열은 만들지 않는다**(사용자 결정 B(나)). 기본 720건 · 확장 941건.
- **② 단계별 사례 날짜 교체:** `config.py` 6절 `CASES` — 이름 첫 글자 = 그날 단계(기본·확장 모두). 1거 2018-04-27 · 2거 2019-06-30 · 3거 2013-02-12 · 4거 2015-08-04 · 5거 2017-09-03.
- **③ 상위% 표시 반올림:** `screen.daily`의 `상위%_표시`를 `np.round(…, 1)`로 — 요약.csv·그림 hover와 같은 규칙. 최신일 원값 43.15가 43.2로 나온다(화면 `:.1f`는 43.1이었음). 첫 365일은 그대로 NaN.
- **식·값·결과 CSV는 바뀌지 않는다** — 결과 CSV 7개가 바이트까지 같아야 한다. 새 테스트 3개 + 기존 테스트 1줄 수정(`tests/test_screen.py`, 부록 A 패치).
- 구현 메인 시험본 `[확인 10-30: python 3.13 · numpy 2.4.6 · pandas 3.0.6 · plotly 7.1.0 · streamlit 1.65.0]`: develop `899855e` + 부록 A 패치(`git apply --check` 통과) → **117 passed**(114 + 새 3), `-m "not regression"` 100 passed · 17 deselected, `-W error::FutureWarning tests/test_screen.py` 12 passed, `run_tension --end 2026-10-29` 결과 7개 = 커밋된 결과와 **바이트 같음**.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F7b_20261030"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/dev/진행기록.md" " M docs/dev/지시서_구현_메인_채팅6.md" " M docs/dev/requests/F5_화면요청.md"
#     "?? docs/dev/tasks/F7b_screen_pass.md" "?? .obsidian/"
#   (이 밖의 변경이 있으면 건드리지 않고 보고서 4절에 적는다 — 코드 파일이 바뀌어 있으면 멈춤)
git branch --show-current                          # 기대: develop (그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 29 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop                # 기대: 899855e(뒤에 커밋이 있으면 누구의 무엇인지 log에 적고 계속 — 2절 git apply --check가 실패하면 거기서 멈춤)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 최신 develop으로
DOCS_M="docs/dev/진행기록.md docs/dev/지시서_구현_메인_채팅6.md docs/dev/requests/F5_화면요청.md"
DOCS_N="docs/dev/tasks/F7b_screen_pass.md"
DOCS="$DOCS_M $DOCS_N"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
for f in $DOCS; do echo "$(tr -d '\r' < "$f" | md5sum | cut -c1-32)  $f"; done   # 기대: 아래 표(F7b_screen_pass.md 제외 3개 — 내용이 다르면 멈추고 보고)
git restore $DOCS_M
git switch develop                                  # 이미 develop이면 그대로
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in $DOCS; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-screen-pass
# 1-3 이슈: 본문 "$B/issue_F7b.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 0절 ①②③, 완료 조건 = 5절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F7b.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 화면 통로 보완 — 사건표 함수·사례 날짜·상위% 반올림(F7b)" --label feat --body-file "$B/issue_F7b.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 114 passed(F7까지)
```
1-1 `md5sum` 기대(줄바꿈은 Windows 체크아웃 때문에 CRLF/LF 어느 쪽이든 **`tr -d '\r' < 파일 | md5sum`**으로 같게 본다 — 아래 값은 CR을 뺀 md5):


```
6dbd8fe910169cf9d28e93a22965bb1a  docs/dev/진행기록.md
c5b084b517d374b894e3573c95b004ed  docs/dev/지시서_구현_메인_채팅6.md
60f40a468778c849c3722a0a6e322af5  docs/dev/requests/F5_화면요청.md
```

**커밋 1** `docs: F7b 작업 프롬프트·설계 문서 반영` — 위 `$DOCS` 4개(내용 수정 없이 — U2). 6절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 패치 적용 (부록 A) → 테스트 → 결과 바이트 확인
```bash
PYTHONIOENCODING=utf-8 <py> - <<'EOF2'
import os, re, pathlib
t = pathlib.Path("docs/dev/tasks/F7b_screen_pass.md").read_text(encoding="utf-8")
m = re.search(r"<!-- F7b.code.patch 시작 -->\n```diff\n(.*?)```\n<!-- F7b.code.patch 끝 -->", t, re.S)
pathlib.Path(os.environ["B"], "f7b_code.patch").write_bytes(m.group(1).encode("utf-8"))
print("저장: f7b_code.patch", len(m.group(1).splitlines()), "줄")
EOF2
md5sum "$B/f7b_code.patch"
#   기대: 5d931742ee3604a8457eaca0806b0a1d (117줄)
git apply --check "$B/f7b_code.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply "$B/f7b_code.patch"
git hash-object config.py utils/tension/screen.py utils/loader.py tests/test_screen.py
#   기대(순서대로):
#     config.py               38c356dedfc34a6b387676329376a070b18a6417
#     utils/tension/screen.py 08f9ca4118004cf9800270783c1794a9dd0f9627
#     utils/loader.py         30dd5c6dc81bc6e5555d1ea249ec66a37a2df798
#     tests/test_screen.py    d44a6a8587eaca0a621aa1c692c0ce72e6a23592
#   하나라도 다르면 멈추고 보고
git diff --stat                                    # 기대: 4 files changed, 56 insertions(+), 8 deletions(-)
git diff config.py | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '   # 기대: CASES 블록 안(첫 줄 주석 + 사례 5줄)만 — 6줄 지우고 6줄 더함
```
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest                                    # 기대: 117 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                # 기대: 100 passed, 17 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_screen.py   # 기대: 12 passed
mkdir -p "$B/after"
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --end 2026-10-29 --out "$B/after"
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
git status --porcelain data/                       # 기대: 줄 없음(결과는 $B/after에만 썼다)
PYTHONIOENCODING=utf-8 <py> -c "
from utils import loader
e = loader.load_tension_events(); print(len(e), list(e.columns), str(e['date'].dtype))
d = loader.load_tension_daily(); print(d['상위%_표시'].iloc[-1], f\"{d['상위%_표시'].iloc[-1]:.1f}\")
"
#   기대: 720 ['사건ID', 'date', '요소', '묶음', 'S', '사건명'] datetime64[ns] / 43.2 43.2   (streamlit 경고 줄이 앞에 나와도 됨)
```
- 다르면: 파일도 코드도 고치지 말고 차이를 log에 남기고 멈추고 보고한다(버전 차이로 보이면 그렇게 적는다).
- `--end`를 반드시 `2026-10-29`로 고정한다(기본값은 실행일이라 커밋된 결과와 날짜가 달라진다).

**커밋 2** `feat: 사건표 읽기 통로와 상위% 반올림` — `utils/tension/screen.py` · `utils/loader.py`
**커밋 3** `fix: 단계별 사례 날짜를 새 결과 기준으로 교체` — `config.py`
**커밋 4** `test: 사건표 함수·사례 단계·상위% 반올림 테스트` — `tests/test_screen.py`

## 3. 하지 않는 것
- 문서 4개·설계 문서의 내용 수정(커밋 1은 그대로), 화면(`홈.py`·`pages/`)·`utils/ui.py`·`dummy.py`·`real.py` 수정, 옛 `load_*`(`load_daily`·`load_monthly`·`load_elements`·`load_events`·`load_yearly`) 수정·삭제, `config.py` 6절 `CASES` 밖 수정(옛 임시값 `RAM_CUTS`·`RATIO_CUTS`·`WEIGHTS`·`WINDOW_DAYS`·`USE_DUMMY`도 지우지 않는다 — 이번 작업 아님)
- `data/tension/` 결과·사건표·판정표 수정(검산 결과는 `$B/after`에만), 기존 테스트 수정(부록 A가 바꾸는 한 줄 말고), `tests/fixtures/` 수정
- 부록과 다른 코드·테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절), 원격·로컬 브랜치 삭제, README 수정

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #29 MERGED, 훅 있음, 114 passed, 버전 적음, 1-1 md5 3개 같음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-screen-pass`, 이슈 번호 |
| 3 | 2절 패치 | 패치 md5 같음, `git apply --check` 통과, hash 4개 같음, `--stat` 4 files · 56 insertions · 8 deletions |
| 4 | 2절 테스트 | 117 passed · not regression 100/17 · FutureWarning 12 passed |
| 5 | 2절 결과 | `run_tension --end 2026-10-29` 결과 7개가 커밋된 결과와 바이트 같음, `data/` 변경 없음 |
| 6 | 2절 화면 통로 | 사건표 720건 · 열 6개 · `date` datetime64 · 상위%_표시 최신일 43.2 |
| 7 | 커밋 | 6절 순서 5개 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 10 | 마지막 status | `?? .obsidian/` 하나만 |

## 5. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F7b 작업 프롬프트·설계 문서 반영` — 1절 `$DOCS` 4개
2. `feat: 사건표 읽기 통로와 상위% 반올림` — `utils/tension/screen.py` · `utils/loader.py`
3. `fix: 단계별 사례 날짜를 새 결과 기준으로 교체` — `config.py`
4. `test: 사건표 함수·사례 단계·상위% 반올림 테스트` — `tests/test_screen.py`
5. `docs: F7b 보고서` — `docs/dev/reports/F7b_report.md` · `F7b_log.md`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 117 passed
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-screen-pass
# 본문 "$B/pr_F7b.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 ①②③ · 테스트 = 2절 결과(117 passed, 결과 CSV 바이트 동일)
#   · 체크리스트 아래에 팀원 안내 네 줄:
#     "박성인 님 요청서(10-30) ①②③을 처리했습니다. ④ 옛 함수·임시값 정리는 화면 PR이 병합된 뒤에 합니다."
#     "화면 파일(홈.py·pages/·ui.py)·real.py·dummy.py·옛 load_*는 바꾸지 않았습니다. config.py는 6절 CASES 블록(7줄)만 요청하신 교체안으로 바꿨습니다."
#     "load_tension_events(scenario=\"기본\")는 열이 사건ID·date(날짜형)·요소·묶음·S·사건명이고 시작일 열은 없습니다 — 시작일을 쓰는 곳은 date로 바꾸거나 load_tension_events().rename(columns={\"date\": \"시작일\"}) 한 줄이 필요합니다."
#     "상위%_표시는 요약·그림과 같은 반올림(소수 1자리)으로 미리 돌려줍니다 — 최신일 43.2."
grep -inE "$AI" "$B/pr_F7b.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 화면 통로 보완 — 사건표 함수·사례 날짜·상위% 반올림(F7b)" --body-file "$B/pr_F7b.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다(ready 전환도 하지 않는다 — 리뷰 여부와 병합은 사용자가 정한다). 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 6. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F7b_report.md`(60줄 이내): 1절 = 4절 표 10행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F7b_log.md`: 1~2절 출력 전부(문서 md5, 패치 md5·hash, 테스트 결과, 결과 7개 cmp·md5, 화면 통로 확인 출력), 작성자 목록, 커밋·푸시·PR 출력.

---

## 부록 A. `$B/f7b_code.patch` (2절 파이썬으로 잘라 저장 — 글자 그대로, md5 `5d931742ee3604a8457eaca0806b0a1d`)
대상: `config.py`(6절 `CASES` 블록) · `utils/tension/screen.py`(`events_table` 추가, `상위%_표시` 반올림) · `utils/loader.py`(끝에 `load_tension_events`) · `tests/test_screen.py`(1줄 수정 + 테스트 3개 추가).

<!-- F7b.code.patch 시작 -->
```diff
diff --git a/config.py b/config.py
index a4cb37a..38c356d 100644
--- a/config.py
+++ b/config.py
@@ -26,13 +26,13 @@ BASE_START = "2010-01-01"
 BASE_END = "2019-12-31"
 
 # ===== 6. [수정] 기준일 사례 (1페이지·보고서가 같이 씀, 두 곳에 있던 목록을 여기로 모음) =====
-CASES = {   # 보여 줄 이름: 날짜 (None = 최신, "pick" = 달력으로 직접) / 단계는 지금 임시 가중치로 계산한 값
+CASES = {   # 보여 줄 이름: 날짜 (None = 최신, "pick" = 달력으로 직접) / 단계는 긴장도 결과(data/tension 일별 `단계_최종`, 기본·확장 모두)로 확인한 값 — 이름 첫 글자 = 그날 단계
     "최신": None,
-    "1단계 평온 · 2019-06-30 판문점 남북미 회동": "2019-06-30",
-    "2단계 관심 · 2025-06-30": "2025-06-30",
-    "3단계 주의 · 2010-11-30 연평도 포격 1주 뒤": "2010-11-30",
-    "4단계 경계 · 2017-11-30 화성-15 발사 다음 날": "2017-11-30",
-    "5단계 심각 · 2017-09-15 6차 핵실험 12일 뒤": "2017-09-15",
+    "1거 평온 · 2018-04-27 판문점 정상회담": "2018-04-27",
+    "2거 관심 · 2019-06-30 판문점 남북미 회동": "2019-06-30",
+    "3거 주의 · 2013-02-12 3차 핵실험": "2013-02-12",
+    "4거 경계 · 2015-08-04 목함지뢰": "2015-08-04",
+    "5거 심각 · 2017-09-03 6차 핵실험": "2017-09-03",
     "직접 고르기": "pick",
 }
 
diff --git a/tests/test_screen.py b/tests/test_screen.py
index 0c3a1fb..d44a6a8 100644
--- a/tests/test_screen.py
+++ b/tests/test_screen.py
@@ -29,7 +29,7 @@ def test_streak_and_top_pct(d):
     i = int(np.argmax(on))                                                            # 처음 4거 이상인 날
     assert d["지속일수"].iloc[i] == 1
     assert d["상위%_표시"].iloc[:365].isna().all() and d["상위%_표시"].iloc[365:].notna().all()
-    assert d["상위%_표시"].iloc[365:].equals(d["그날까지_상위%"].iloc[365:].astype(float))
+    assert d["상위%_표시"].iloc[365:].equals(np.round(d["그날까지_상위%"].iloc[365:].astype(float), 1))   # 10-30: 요약·그림과 같은 반올림
 
 
 def test_relief_delta_matches_core(d):
@@ -94,3 +94,36 @@ def test_loader_functions_match_screen():
     t2, e2 = screen.contributions("2026-10-29")
     assert t1.equals(t2) and e1.equals(e2)
     assert callable(loader.load_daily) and callable(loader.load_monthly)                # 기존 함수 그대로
+
+
+def test_top_pct_display_matches_summary():
+    """상위%_표시 = 요약.csv·그림 hover와 같은 반올림 — 최신일 43.15는 화면에서 43.2(박성인 님 요청서 10-30 ③)."""
+    s = pd.read_csv(ROOT / "data" / "tension" / "요약.csv", encoding="utf-8-sig", index_col=0)
+    for scenario, col in (("기본", "기본"), ("확장", "확장(C5 포함)")):
+        d = screen.daily(scenario)
+        last = d["상위%_표시"].iloc[-1]
+        assert last == float(s.loc["현재 그날까지 상위%", col]) and f"{last:.1f}" == f"{float(s.loc['현재 그날까지 상위%', col]):.1f}"
+        assert (d["상위%_표시"].iloc[365:] == d["그날까지_상위%"].iloc[365:].astype(float).round(1)).all()
+    assert f"{screen.daily('기본')['상위%_표시'].iloc[-1]:.1f}" == "43.2"
+
+
+def test_events_table_and_loader():
+    from utils import loader
+    for scenario, n in (("기본", 720), ("확장", 941)):
+        ev = screen.events_table(scenario)
+        assert list(ev.columns) == ["사건ID", "date", "요소", "묶음", "S", "사건명"] and len(ev) == n
+        assert str(ev["date"].dtype).startswith("datetime64") and ev["사건ID"].is_unique
+        assert loader.load_tension_events(scenario).equals(ev)
+    assert loader.load_tension_events().equals(screen.events_table("기본"))
+    with pytest.raises(ValueError):
+        screen.events_table("다른것")
+
+
+def test_cases_match_stage_names():
+    """CASES 이름 첫 글자(몇 거) = 그날 최종 단계 — 기본·확장 모두(박성인 님 요청서 10-30 ②)."""
+    dates = [(k, v) for k, v in config.CASES.items() if v not in (None, "pick")]
+    assert [int(k[0]) for k, _ in dates] == [1, 2, 3, 4, 5]
+    for scenario in ("기본", "확장"):
+        d = screen.daily(scenario).set_index("날짜")
+        for name, day in dates:
+            assert int(d.loc[pd.Timestamp(day), "최종단계"]) == int(name[0]), (scenario, name)
diff --git a/utils/loader.py b/utils/loader.py
index 258ca59..30dd5c6 100644
--- a/utils/loader.py
+++ b/utils/loader.py
@@ -126,3 +126,8 @@ def load_tension_half_life(scenario="기본"):  # 반감기 민감도 — 반감
 @st.cache_data
 def load_tension_month_events(month, scenario="기본", top=3):  # 그달 주요 사건(유사 시기 카드) — month = "YYYY-MM"
     return tension_screen.month_events(month, scenario, top)
+
+
+@st.cache_data
+def load_tension_events(scenario="기본"):  # 사건표 — 사건ID·date(날짜형)·요소·묶음·S·사건명 (지수에 들어간 사건 전부, 기본 720건·확장 941건)
+    return tension_screen.events_table(scenario)
diff --git a/utils/tension/screen.py b/utils/tension/screen.py
index c10033d..08f9ca4 100644
--- a/utils/tension/screen.py
+++ b/utils/tension/screen.py
@@ -101,7 +101,7 @@ def daily(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
     d["지속일수"] = sm.stage_streak(d["최종단계"]).to_numpy()
     top = d["그날까지_상위%"].astype(float).copy()
     top.iloc[:TOP_PCT_HIDE_DAYS] = np.nan
-    d["상위%_표시"] = top
+    d["상위%_표시"] = np.round(top, 1)   # 사용자 10-30: 요약.csv·그림 hover와 같은 반올림(np.round) — 화면 :.1f는 x.x5에서 달랐음(43.15 → 43.1)
     d["완화할인_δ"] = relief_delta(scenario, raw.index, data_dir).round(3).to_numpy()
     return d
 
@@ -304,6 +304,16 @@ def month_events(month, scenario="기본", top=3, data_dir=DATA_DIR) -> pd.DataF
     return ev.reset_index(drop=True)
 
 
+def events_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
+    """(화면) 사건표 — 지수 계산에 들어간 사건 전부(기본 720건 · 확장 941건). 박성인 님 요청서 10-30 ①.
+
+    열 = 사건ID · date(날짜형) · 요소 · 묶음 · S · 사건명 — CSV 열 이름 그대로(화면 이름 열은 더하지 않는다). CSV 순서 그대로.
+    """
+    _check(scenario)
+    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
+    return events.reset_index(drop=True)
+
+
 def normalization_figure(scenario="기본", data_dir=DATA_DIR):
     """(화면) 묶음 정규화 효과 그림 — charts.normalization_figure(주 지수 vs T_basic, 7일 평균)."""
     from utils.tension import charts
```
<!-- F7b.code.patch 끝 -->
