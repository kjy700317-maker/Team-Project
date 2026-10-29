# F6 작업 프롬프트 — 비교선 T_basic(⑮′) · GPR 한국 비교 · 반감기 민감도 · 유사 시기 주요 사건 (계산·결과·화면 통로)

작성 2026-10-29 · 구현 메인(채팅 ⑤) → Claude Code · 브랜치 **`feature/tension-compare`(PR #25 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행**(10-29 사용자 "지금 Claude Code로") — 10-29 사용자 결정 반영: T_basic = 상승 묶음 합 ÷ 평소 × 100 × (1 − δ)(정규화 효과만) · 화면은 설명 자리만 · `비교선_일별.csv` 별도 커밋 · GPR 원본 그대로 복사 + 월별 비교(순위% 두 선) + 판독문 1줄 새로 · 반감기 민감도 표 계산·커밋 · 유사 시기 "주요 사건" 통로 · 과거 유사 시기 카드는 만들지 않음(화면에 이미 있음) · 비교선 판독문 `NORMALIZATION_NOTE` = 부록 초안대로(10-29 사용자) · **담당 파일 원칙**(화면 `홈.py`·`pages/`는 고치지 않음 — 요청서 `docs/dev/requests/F6_화면요청.md`)
권장 모델·노력: **Opus 5.5 · 중간**(패치 적용 + 실행·커밋 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`(‑q 없이). **`$B`** = `$HOME/bongsu_F6_20261029`(`export B=…` — 2절 파이썬이 읽음).
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약(결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것).
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 1절에서 `commit-msg` 훅을 확인하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 8절 검사로 확인한다. 검사 패턴 `$AI`는 1절에서 정의(셸이 새로 열리면 다시 정의).
> **팀원 파일 중 이 작업이 바꾸는 것(사용자 10-29 — 데이터 통로·긴장도 절은 우리 몫):** `config.py` **맨 끝에 2줄**(긴장도 절 `HALF_LIFE_SENSITIVITY`·`GPR_PATH`) · `utils/loader.py` **맨 끝에 F6 블록**(함수 8개). 둘 다 부록 A 패치가 한다. 기존 줄은 바꾸지 않는다.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `git branch -d`·`push --delete`(브랜치 삭제는 사용자 몫), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정(GPR 파일은 **읽어서 복사만**), **`홈.py`·`pages/`·`utils/ui.py`·`utils/dummy.py`·`utils/real.py`·`utils/helpers.py`·`utils/build_*.py`·`db/`·`requirements.txt` 수정**, 부록 A 밖의 코드 수정, 결과 CSV 손 편집. 부록 A는 **글자 그대로**(2절 파이썬으로 잘라 저장 — md5 기대값과 다르면 다시).

---

## 0. 목표
- **⑮′ 비교선 T_basic**(`core.basic_index`): 상승 묶음 R 합 ÷ 기준기간 평균 × 100 × (1 − δ). 묶음 구성·완화 할인은 주 지수와 같게 두고 "묶음별 ÷ 평소값" 효과만 남긴다(왜 이 정의인가 = `docs/tension/산출식_변경이력.md` C18). `run_tension.py`가 `data/tension/비교선_일별.csv`(시나리오·날짜·T_basic·T_basic_표시7일)로 쓴다. **일별·요약·월별·연도별 CSV는 그대로**(열 계약·F3 회귀 바이트 비교 유지).
- **반감기 민감도**(`summary.half_life_table`): 반감기 7·14·21·30일(`config.HALF_LIFE_SENSITIVITY`)로 `daily_table(params={"half_life": h})`를 다시 돌려 T 구간(같은 규칙으로 다시 뽑음)·1~5거 %·14일과 단계 같은 날 %·한 단계 안 %·위기 10건 단계·현재를 `data/tension/반감기_민감도.csv`로. 하한 감쇠는 그대로(ADR-006 2번). 화면 문구 "반감기를 7·21·30일로 바꾼 결과도 함께 공개"의 근거.
- **GPR 한국 월별**: `진행 현황 및 계획 정리/v0.1_시험/채점_v0/입력_GPR_한국_월별.csv`를 **바이트 그대로** `data/tension/GPR_한국_월별.csv`로 복사(D1 — 커밋). `io.load_gpr_monthly`가 읽고 검증(형식·중복·빈 값은 멈춤).
- **화면 통로**(`screen.py` + `utils/loader.py` 끝 `load_tension_*` 8개 + `charts.py` 그림 2개): 비교선(표·요약·"묶음 정규화 효과" 그림) · 봉수 vs GPR 월별(순위% 두 선·요약·판독문 3줄) · 반감기 민감도 표·설명 문구 · 그달 주요 사건(유사 시기 카드용). 화면에 붙이는 일은 담당자(요청서).
- **테스트** `tests/test_compare.py`(20개 — 합성 자료 9 · 화면 통로 10 · run_tension 출력 1(regression)).
- 구현 메인 시험본 `[확인 10-29: python 3.13 · numpy 2.4.6 · pandas 3.0.6 · plotly 7.1.0 · streamlit 1.65.0]`: develop `04c5353` + 부록 A 패치(`git apply --check` 통과) → `run_tension --end 2026-10-29`의 기존 5개 결과 = 커밋된 결과와 **바이트 같음**, 새 파일 2개 md5 아래 3절 표, **107 passed**(F5까지 87 + 20), `-m "not regression"` 90 passed · 17 deselected, `-W error::FutureWarning` test_compare 20 passed. 값(기본): T_basic과 T 상관 0.9995 · 차 최대 22.4 / GPR 2010-01~2026-09 201달 피어슨 0.33 · 순위 상관 0.35 / 반감기 14일 행 = 요약과 같음.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
export B="$HOME/bongsu_F6_20261029"; mkdir -p "$B/docs"
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
git status --porcelain
#   기대(순서 무관, 한글은 "\352…" 꼴로 보일 수 있음):
#     " M docs/decisions.md" " M docs/dev/식_함수_대응표.md" " M docs/dev/진행기록.md" " M docs/tension/산출식_정리.md"
#     "?? docs/dev/requests/" "?? docs/dev/tasks/F6_compare.md" "?? docs/tension/산출식_변경이력.md" "?? .obsidian/"
git branch --show-current                          # 기대: feature/tension-merge-data 또는 develop(그 밖이면 멈춤)
test -x .git/hooks/commit-msg && echo "훅 있음" || echo "훅 없음 — 멈추고 보고"
git fetch origin
gh pr view 25 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop                # 기대: 04c5353(뒤에 커밋이 있으면 log에 적고 계속 — 2절 git apply --check가 실패하면 거기서 멈춤)

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 develop으로
DOCS="docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md docs/tension/산출식_변경이력.md docs/dev/tasks/F6_compare.md docs/dev/requests/F5_화면요청.md docs/dev/requests/F6_화면요청.md"
for f in $DOCS; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git restore docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md
git switch develop                                  # 이미 develop이면 그대로
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in $DOCS; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-compare
# 1-3 이슈: 본문 "$B/issue_F6.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 0절 목록, 완료 조건 = 6절) — AI 표기 없이
grep -inE "$AI" "$B/issue_F6.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 비교선 T_basic·GPR 비교·반감기 민감도(F6)" --label feat --body-file "$B/issue_F6.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest, plotly, streamlit, docx; print(numpy.__version__, pandas.__version__, pytest.__version__, plotly.__version__, streamlit.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 87 passed(F5까지)
```
**커밋 1** `docs: F6 작업 프롬프트·설계 문서 반영` — 위 `$DOCS` 8개(내용 수정 없이 — U2. F5 화면 요청서도 여기서 처음 커밋). 8절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B | grep -inE "$AI" || echo OK`.

## 2. 패치 적용 (부록 A)
```bash
PYTHONIOENCODING=utf-8 <py> - <<'EOF'
import os, re, pathlib
t = pathlib.Path("docs/dev/tasks/F6_compare.md").read_text(encoding="utf-8")
m = re.search(r"<!-- F6\.patch 시작 -->\n```diff\n(.*?)```\n<!-- F6\.patch 끝 -->", t, re.S)
pathlib.Path(os.environ["B"], "f6.patch").write_bytes(m.group(1).encode("utf-8"))
print("저장:", len(m.group(1).splitlines()), "줄")
EOF
md5sum "$B/f6.patch"                               # 기대: 6b6685f1c51776f99133773b57720b6b (646줄)
git apply --check "$B/f6.patch" && echo "적용 가능" || echo "적용 불가 — 멈추고 보고(손으로 고치지 않음)"
git apply "$B/f6.patch"
git hash-object config.py utils/tension/core.py utils/tension/io.py utils/tension/summary.py scripts/run_tension.py utils/tension/screen.py utils/tension/charts.py utils/loader.py tests/test_compare.py
#   기대(순서대로):
#     config.py                 7e7f2b511a48395b5638828e048e1c7f6a544c72
#     utils/tension/core.py     be6c54fcf3564229bf32ea51709183372c6e5c1a
#     utils/tension/io.py       0e473714f86dd844c919792fb665679cd620629d
#     utils/tension/summary.py  8b3634adc8a7d691e960a5d6c58d0913aff3f27b
#     scripts/run_tension.py    ffec26773b1167c69163a7003f1b4cc1ee49e402
#     utils/tension/screen.py   c10033ddf4ae29488659d4989eaa252c5b9c2d0e
#     utils/tension/charts.py   e9eb7df4796309fb1944f56a742a4dd499359b80
#     utils/loader.py           258ca59779ddb67ddbbd08ae522a90339d8a1fed
#     tests/test_compare.py     eb34713b1661734a88b70ca28affe89bff5fae03
#   하나라도 다르면 멈추고 보고
git diff config.py utils/loader.py | grep -E '^-[^-]' && echo "팀원 파일 기존 줄이 바뀜 — 멈춤" || echo "기존 줄 그대로(끝에 더한 줄만)"
git diff --stat                                    # 기대: 8개 파일 수정(+ tests/test_compare.py는 ?? 새 파일)
```

## 3. GPR 복사 · 결과 다시 만들기
```bash
cp "진행 현황 및 계획 정리/v0.1_시험/채점_v0/입력_GPR_한국_월별.csv" data/tension/GPR_한국_월별.csv
md5sum data/tension/GPR_한국_월별.csv              # 기대: 81081a43a3e8d6215685fb4521a49c52(원본과 같아야 함 — cmp로도 확인)
cmp "진행 현황 및 계획 정리/v0.1_시험/채점_v0/입력_GPR_한국_월별.csv" data/tension/GPR_한국_월별.csv && echo "원본과 같음"
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --end 2026-10-29
#   기대 마지막 줄: "쓴 파일: …비교선_일별.csv · 반감기_민감도.csv(반감기 [7, 14, 21, 30]일)"
#   끝날은 커밋된 결과와 같은 2026-10-29로 고정(비교선·일별 날짜가 같아야 화면 통로가 읽음)
git status --porcelain data/tension
#   기대: 기존 결과(일별_기본·일별_확장·요약·월별·연도별)는 줄 없음(바뀌지 않음) · 새 파일 3개 "??"(GPR_한국_월별·비교선_일별·반감기_민감도)
md5sum data/tension/비교선_일별.csv data/tension/반감기_민감도.csv
#   기대: 704053ceea621623091bb32be4050562  비교선_일별.csv
#         af13c6f9e9e7c83c7ec0d7b55054c90a  반감기_민감도.csv
#   다르면: 파일을 고치지 말고 차이를 log에 남기고 멈추고 보고(버전 차이로 보이면 그렇게 적음)
PYTHONIOENCODING=utf-8 <py> -c "import pandas as pd; t = pd.read_csv('data/tension/반감기_민감도.csv', encoding='utf-8-sig'); print(t.iloc[:, :12].to_string())"
#   기대(기본 14일 행): 115/256/315/378 · 48.4 · 22.2 · 11.9 · 9.5 · 8.0 · 749 · 100.0 · 100.0
```
| 파일 | 내용 | 커밋 |
|---|---|---|
| `data/tension/GPR_한국_월별.csv` | GPRC_KOR 월별 2010-01~2026-09(201달), 원본 그대로 | ○ (D1) |
| `data/tension/비교선_일별.csv` | 시나리오·날짜·T_basic·T_basic_표시7일, 기본·확장 각 6,146일 | ○ |
| `data/tension/반감기_민감도.csv` | 기본·확장 × 반감기 7·14·21·30일 = 8행, 열 22개(시나리오·반감기·T 구간·1~5거%·T원값 최대·같은 날%·한 단계 안%·위기 10건·현재) | ○ |

## 4. 테스트
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_compare.py                    # 기대: 20 passed
PYTHONIOENCODING=utf-8 <py> -m pytest                                          # 기대: 107 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"                      # 기대: 90 passed, 17 deselected
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest tests/test_compare.py   # 기대: 20 passed(우리 코드 경고 0)
```
- AppTest(`test_app_smoke.py`)는 화면을 고치지 않았으므로 그대로 통과해야 한다. 실패하면 화면 코드를 고치지 말고 예외 원문 전부를 log에 남기고 멈추고 보고.
- 그 밖에 기대와 다르면 테스트도 코드도 고치지 말고 실패 출력 전부를 log에 남기고 멈추고 보고한다.

**커밋 2~6**(4절 통과 뒤, 8절 순서)

## 5. 하지 않는 것
- 화면(`홈.py`·`pages/`)·`utils/ui.py`·`dummy.py`·`real.py` 수정, `utils/loader.py`·`config.py`의 기존 줄 수정(담당 파일 원칙 — 화면에 붙이는 일은 요청서로)
- 일별·요약·월별·연도별 CSV의 열 추가·이름 변경, `tests/fixtures/` 수정, 기존 테스트 수정
- GPR 원본 고치기·다른 판본 내려받기(인터넷), 결과 CSV 손 편집, 원격·로컬 브랜치 삭제
- 부록과 다른 함수·테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절)

## 6. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | PR #25 MERGED, 훅 있음, 87 passed, 버전 적음 |
| 2 | 1-2·1-3 | 새 브랜치 `feature/tension-compare`, 이슈 번호 |
| 3 | 2절 | 패치 md5 같음, `git apply --check` 통과, hash 9개 같음, 팀원 파일 기존 줄 그대로 |
| 4 | 3절 | GPR = 원본(cmp), 기존 결과 5개 안 바뀜, 새 파일 md5 2개 같음, 14일 행 기대대로 |
| 5 | 4절 | 20 / 107 passed · not regression 90/17 · FutureWarning 0 |
| 6 | 커밋 | 8절 순서 6개 + 보고서 |
| 7 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 8 | AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |
| 9 | 마지막 status | `?? .obsidian/` 하나만 |

## 7. 참고 — 화면 담당께 갈 것
`docs/dev/requests/F6_화면요청.md`(구현 메인 작성, 커밋 1에 들어감)를 사용자가 박성인 님께 전달한다. PR 본문 끝에 "화면 연결은 요청서 F5·F6"과 "PR #25 사후 확인 요청"(요청서 4절) 한 줄씩.

## 8. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_(제외기록|입력파일)|_check/|\.html$|\.tgz$' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F6 작업 프롬프트·설계 문서 반영` — 1절 `$DOCS` 8개
2. `feat: 비교선 T_basic(⑮′)·반감기 민감도 계산` — `utils/tension/core.py` · `utils/tension/summary.py` · `scripts/run_tension.py` · `config.py`
3. `feat: GPR 한국 월별 읽기·사본` — `utils/tension/io.py` · `data/tension/GPR_한국_월별.csv`
4. `feat: 화면 통로에 비교선·GPR·민감도·월 사건 추가` — `utils/tension/screen.py` · `utils/tension/charts.py` · `utils/loader.py`
5. `chore: 비교선·반감기 민감도 결과 CSV` — `data/tension/비교선_일별.csv` · `data/tension/반감기_민감도.csv`
6. `test: 비교선·GPR·민감도 테스트` — `tests/test_compare.py`
7. `docs: F6 보고서` — `docs/dev/reports/F6_report.md` · `F6_log.md`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 107 passed
git log --format='%h %an' origin/develop..HEAD                                   # 작성자 목록을 log에 남김
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고" || echo "OK"
git push -u origin feature/tension-compare
# 본문 "$B/pr_F6.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 0절 목록 · 테스트 = 6절 결과(107 passed)
#   · 체크리스트 아래에 팀원 안내 세 줄:
#     "화면 파일(홈.py·pages/)은 바꾸지 않았습니다. config.py 끝 2줄과 utils/loader.py 끝 함수 8개(load_tension_basic 등)만 더했습니다."
#     "화면 연결은 docs/dev/requests/F5_화면요청.md·F6_화면요청.md에 정리했습니다(F5 요청서도 이 PR에서 처음 올라갑니다)."
#     "PR #25가 리뷰 없이 병합되어, 그때 우리가 고친 팀원 파일 4개(README 1줄·.gitignore 1줄·config.py·홈.py) 사후 확인을 부탁드립니다(F6 요청서 4절)."
grep -inE "$AI" "$B/pr_F6.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 비교선 T_basic·GPR 비교·반감기 민감도(F6)" --body-file "$B/pr_F6.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 9. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F6_report.md`(60줄 이내): 1절 = 6절 표 9행 ✓/✗ · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일(팀원 파일 2개는 "끝에 더한 줄만"으로 구분).
`docs/dev/reports/F6_log.md`: 1~4절 출력 전부(패치 md5·hash, run_tension 출력, md5, 민감도 표, 테스트 결과), 작성자 목록, 커밋·푸시·PR 출력.

---

## 부록 A. `$B/f6.patch` (2절 파이썬으로 잘라 저장 — 글자 그대로, md5 `6b6685f1c51776f99133773b57720b6b`)
대상: `config.py`(끝 2줄) · `utils/tension/core.py`(⑮′ `basic_index`) · `utils/tension/io.py`(`GPR_COLUMNS`·`load_gpr_monthly`) · `utils/tension/summary.py`(`HALF_LIFE_COLUMNS`·`half_life_table`) · `scripts/run_tension.py`(비교선·민감도 출력) · `utils/tension/screen.py`(판독문·문구 상수 + 통로 함수 9개) · `utils/tension/charts.py`(`normalization_figure`·`gpr_figure`) · `utils/loader.py`(끝 F6 블록) · `tests/test_compare.py`(새 파일).

<!-- F6.patch 시작 -->
```diff
diff --git a/config.py b/config.py
index 6624f6c..7e7f2b5 100644
--- a/config.py
+++ b/config.py
@@ -85,3 +85,5 @@ CRISIS_LIST = (                                  # 내부 위기 목록 10건(
 CRISIS_WINDOW_DAYS = 14                          # 위기 단계·게이지 눈금 = 위기일부터 14일 안 최댓값
 TENSION_DATA_DIR = "data/tension"                # 결과 CSV 폴더(커밋)
 TYPE4_TABLE_PATH = "data/tension/물리사건_유형판정표.csv"   # 유형판정표 사본(F1에서 복사, 커밋)
+HALF_LIFE_SENSITIVITY = (7, 14, 21, 30)          # ADR-006 1번 — 반감기 민감도(공개용 표, 단계 판정은 HALF_LIFE_DAYS). 하한 감쇠는 그대로
+GPR_PATH = "data/tension/GPR_한국_월별.csv"        # ADR-002 GPR 한국(GPRC_KOR) 월별 — 비교 지수만. 채점_v0 입력 그대로 복사(F6)
diff --git a/scripts/run_tension.py b/scripts/run_tension.py
index d69d3af..ffec267 100644
--- a/scripts/run_tension.py
+++ b/scripts/run_tension.py
@@ -1,6 +1,7 @@
-"""긴장도 계산(F4) — 사건표 → 결과 CSV(일별·요약·월별·연도별) + 추이 그림(선택).
+"""긴장도 계산(F4·F6) — 사건표 → 결과 CSV(일별·요약·월별·연도별·비교선·반감기 민감도) + 추이 그림(선택).
 
 기본: data/tension/events_기본.csv·_확장.csv → data/tension/일별_기본.csv·일별_확장.csv·요약.csv·월별.csv·연도별.csv
++ 비교선_일별.csv(⑮′ T_basic, F6) · 반감기_민감도.csv(config.HALF_LIFE_SENSITIVITY, F6)
 (결과 CSV는 커밋 — D1). 끝날 기본값은 config.END_DATE(None = 실행일, U3). 회귀 검산은 --end 2026-10-27.
 
 사용: python scripts/run_tension.py [--end YYYY-MM-DD] [--events-dir DIR] [--out DIR] [--scenario 기본 확장] [--figure DIR]
@@ -15,6 +16,8 @@ from pathlib import Path
 ROOT = Path(__file__).resolve().parents[1]
 sys.path.insert(0, str(ROOT))
 
+import pandas as pd  # noqa: E402
+
 import config  # noqa: E402
 from utils.tension import core  # noqa: E402
 from utils.tension import io as tio  # noqa: E402
@@ -44,6 +47,7 @@ def _run(end, events_dir, out_dir, names, figure_dir) -> None:
     days = core.calc_days(config.CALC_START_DATE, end)
     print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")
     results = []
+    extras = {}   # F6: 시나리오 → (비교선 T_basic Series, 반감기 민감도 표)
     for name in names:
         label, bundles = SCENARIOS[name]
         path = events_dir / f"events_{name}.csv"
@@ -57,6 +61,12 @@ def _run(end, events_dir, out_dir, names, figure_dir) -> None:
         daily, info = core.daily_table(events, days, bundles, type4)
         vals = sm.summary_values(daily, info, days, bundles, input_name=path.name, n_type4=len(type4))
         results.append((name, label, events, excluded, daily, info, vals))
+        basic = core.basic_index(info["components"], bundles, core.base_mask(days))
+        runs = {config.HALF_LIFE_DAYS: (daily, info)}
+        for h in config.HALF_LIFE_SENSITIVITY:   # 반감기만 바꾼 계산 — config는 그대로, params로(F2-3)
+            if h != config.HALF_LIFE_DAYS:
+                runs[h] = core.daily_table(events, days, bundles, type4, {"half_life": h})
+        extras[name] = (basic, sm.half_life_table(dict(sorted(runs.items())), config.HALF_LIFE_DAYS))
     # 모든 시나리오가 계산된 뒤에만 쓴다(중간에 멈추면 아무 파일도 바꾸지 않음)
     for name, label, events, excluded, daily, info, vals in results:
         out = out_dir / f"일별_{name}.csv"
@@ -71,6 +81,15 @@ def _run(end, events_dir, out_dir, names, figure_dir) -> None:
     tio.write_csv(sm.period_tables(dailies, "월"), out_dir / "월별.csv")
     tio.write_csv(sm.period_tables(dailies, "연"), out_dir / "연도별.csv")
     print(f"  쓴 파일: {out_dir / '요약.csv'} · 월별.csv · 연도별.csv")
+    lines = [pd.DataFrame({"시나리오": name, "날짜": basic.index.strftime("%Y-%m-%d"),
+                           "T_basic": basic.round(3).to_numpy(),
+                           "T_basic_표시7일": core.display_ma(basic).round(3).to_numpy()})
+             for name, (basic, _) in extras.items()]
+    tio.write_csv(pd.concat(lines, ignore_index=True), out_dir / "비교선_일별.csv")
+    sens = [t.assign(시나리오=name) for name, (_, t) in extras.items()]
+    sens = pd.concat(sens, ignore_index=True)
+    tio.write_csv(sens[["시나리오", *[c for c in sens.columns if c != "시나리오"]]], out_dir / "반감기_민감도.csv")
+    print(f"  쓴 파일: {out_dir / '비교선_일별.csv'} · 반감기_민감도.csv(반감기 {list(config.HALF_LIFE_SENSITIVITY)}일)")
     if figure_dir is not None:
         from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
         for name, label, _, _, daily, info, _ in results:
diff --git a/tests/test_compare.py b/tests/test_compare.py
new file mode 100644
index 0000000..eb34713
--- /dev/null
+++ b/tests/test_compare.py
@@ -0,0 +1,204 @@
+"""F6 테스트 — 비교선 T_basic(⑮′) · GPR 읽기·비교 · 반감기 민감도 · 유사 시기 주요 사건 · 그림.
+
+합성 자료 테스트는 사건표 없이 돈다. 화면 통로 테스트는 커밋된 결과(data/tension)를 읽는다(test_screen.py와 같음).
+run_tension 출력 테스트는 사건표가 필요해 regression 표시.
+"""
+import subprocess
+import sys
+
+import numpy as np
+import pandas as pd
+import plotly.graph_objects as go
+import pytest
+
+import config
+from tests.test_core import base_events, ev
+from utils.tension import charts, core, io as tio, screen, summary as sm
+
+ROOT = screen.ROOT
+DATA = ROOT / config.TENSION_DATA_DIR
+DAYS = core.calc_days("2010-01-01", "2020-12-31")
+MASK = core.base_mask(DAYS)
+
+
+# ⑮′ 비교선
+def test_basic_index_equals_T_when_baselines_equal():
+    """묶음 평소값이 모두 같으면 정규화 효과가 없다 → T_basic = T(정의 확인)."""
+    rows = []
+    for y in range(2010, 2021):
+        for m in range(1, 13):
+            d = f"{y}-{m:02d}-01"
+            for i, (b, e) in enumerate([("핵·미사일", "A2"), ("군사 과시", "A4"), ("위협 언어·교리", "C1")]):
+                rows.append((f"{e}-{y}{m:02d}", d, e, b, 2.0 + (m % 3), "합성"))
+            rows.append((f"F2-{y}{m:02d}", d, "F2", "완화", 1.0, "합성"))
+    comp, B = core.tension_components(ev(rows), DAYS, config.BUNDLES_BASE)
+    assert B[list(config.BUNDLES_BASE)].nunique() == 1
+    tb = core.basic_index(comp, config.BUNDLES_BASE, MASK)
+    assert float((tb - comp["T"]).abs().max()) < 1e-9
+
+
+def test_basic_index_formula_and_relief():
+    comp, _ = core.tension_components(base_events(), DAYS, config.BUNDLES_BASE)
+    R = sum(comp[f"R_{b}"] for b in config.BUNDLES_BASE)
+    expect = 100 * R / R[MASK].mean() * (1 - comp["delta"])
+    tb = core.basic_index(comp, config.BUNDLES_BASE, MASK)
+    assert float((tb - expect).abs().max()) < 1e-12
+    assert abs(float((100 * R / R[MASK].mean())[MASK].mean()) - 100) < 1e-9   # 할인 전 기준기간 평균 = 100
+    assert (tb >= 0).all()
+
+
+def test_basic_index_stops_when_base_zero():
+    comp, _ = core.tension_components(base_events(), DAYS, config.BUNDLES_BASE)
+    zero = comp.copy()
+    for b in config.BUNDLES_BASE:
+        zero[f"R_{b}"] = 0.0
+    with pytest.raises(ValueError, match="0 이하"):
+        core.basic_index(zero, config.BUNDLES_BASE, MASK)
+
+
+# 반감기 민감도(집계)
+def test_half_life_table_rows_and_ref():
+    events = base_events()
+    runs = {h: core.daily_table(events, DAYS, config.BUNDLES_BASE, frozenset(), {"half_life": h, "kill_ids": ()}) for h in (7, 14, 30)}
+    crises = config.CRISIS_LIST[:6]                                  # 합성 기간(~2020) 안의 위기만
+    t = sm.half_life_table(runs, 14, crises)
+    assert list(t.columns[:len(sm.HALF_LIFE_COLUMNS)]) == list(sm.HALF_LIFE_COLUMNS)
+    assert list(t.columns[len(sm.HALF_LIFE_COLUMNS):]) == [n for n, _, _ in crises] + ["현재"]
+    assert t["반감기"].tolist() == [7, 14, 30]
+    ref = t.set_index("반감기").loc[14]
+    assert ref["기준 반감기와 단계 같은 날%"] == 100.0 and ref["한 단계 안%"] == 100.0
+    assert t[[f"{k}거%" for k in range(1, 6)]].sum(axis=1).between(99.8, 100.2).all()
+    with pytest.raises(ValueError, match="기준 반감기"):
+        sm.half_life_table({7: runs[7]}, 14, crises)
+
+
+# GPR 읽기
+def _gpr_file(tmp_path, lines, header="month,GPRC_KOR,GPRHC_KOR"):
+    p = tmp_path / "gpr.csv"
+    p.write_text("\n".join([header, *lines]) + "\n", encoding="utf-8-sig")
+    return p
+
+
+def test_load_gpr_monthly_ok(tmp_path):
+    g = tio.load_gpr_monthly(_gpr_file(tmp_path, ["2010-02,0.2,0.3", "2010-01,0.1,0.2"]))
+    assert list(g.columns) == ["연월", "GPR"] and g["연월"].tolist() == ["2010-01", "2010-02"]
+    assert g["GPR"].tolist() == [0.1, 0.2]
+
+
+@pytest.mark.parametrize("lines, header, msg", [
+    (["2010-1,0.1,0.2"], "month,GPRC_KOR,GPRHC_KOR", "형식"),
+    (["2010-01,0.1,0.2", "2010-01,0.2,0.2"], "month,GPRC_KOR,GPRHC_KOR", "중복"),
+    (["2010-01,,0.2"], "month,GPRC_KOR,GPRHC_KOR", "빈 값"),
+    (["2010-01,0.1"], "month,GPRC_KOR", "열 이름"),
+])
+def test_load_gpr_monthly_stops(tmp_path, lines, header, msg):
+    with pytest.raises(ValueError, match=msg):
+        tio.load_gpr_monthly(_gpr_file(tmp_path, lines, header))
+
+
+def test_gpr_file_is_committed_copy():
+    """data/tension/GPR_한국_월별.csv = 채점 v0 입력 그대로(2010-01~2026-09, 201달)."""
+    g = screen.gpr_monthly()
+    assert g["연월"].iloc[0] == "2010-01" and len(g) >= 201
+    assert g.set_index("연월").loc["2026-09", "GPR"] == pytest.approx(0.2808381915092468, abs=1e-15)
+
+
+# 화면 통로(커밋된 결과)
+@pytest.mark.parametrize("scenario", ["기본", "확장"])
+def test_basic_line_matches_daily(scenario):
+    b = screen.basic_line(scenario)
+    d = screen.daily_raw(scenario)
+    assert len(b) == len(d) and b["날짜"].tolist() == list(d.index)
+    assert list(b.columns) == ["날짜", "T_원값", "T_표시7일", "T_basic", "T_basic_표시7일", "차이_표시7일"]
+    assert (b["T_basic"] >= 0).all()
+    st = screen.basic_stats(scenario).set_index("항목")["값"]
+    assert float(st["주 지수(T)와 상관"]) > 0.99            # 10-29: 상승 묶음 평소값이 비슷해 정규화 효과가 작음
+
+
+@pytest.mark.parametrize("scenario", ["기본", "확장"])
+def test_gpr_compare(scenario):
+    t = screen.gpr_compare(scenario)
+    assert list(t.columns) == ["연월", "봉수_T평균", "GPR", "봉수_순위%", "GPR_순위%", "순위차"]
+    assert t["연월"].is_monotonic_increasing and t["연월"].iloc[0] == "2010-01"
+    assert t["연월"].iloc[-1] == screen.gpr_monthly()["연월"].iloc[-1]
+    for c in ("봉수_순위%", "GPR_순위%"):
+        assert t[c].between(0, 100).all()
+    m = screen.monthly(scenario).set_index("연월")["T_평균"]
+    assert (t.set_index("연월")["봉수_T평균"] == m.loc[t["연월"]]).all()
+    st = screen.gpr_stats(scenario).set_index("항목")["값"]
+    assert st["달 수"] == str(len(t)) and -1 <= float(st["피어슨 상관"]) <= 1
+
+
+def test_gpr_2018_note_direction():
+    """판독문 셋째 줄(2018 정상회담기 GPR 높음·봉수 낮음)이 지금 결과와 맞는지."""
+    t = screen.gpr_compare("기본").set_index("연월")
+    y2018 = t.loc["2018-03":"2018-10"]
+    assert (y2018["순위차"] < 0).all()
+    assert len(screen.GPR_NOTES) == 3 and screen.GPR_NOTES[:2] == screen.READING_NOTES[2:4]
+
+
+@pytest.mark.parametrize("scenario", ["기본", "확장"])
+def test_half_life_screen_table(scenario):
+    t = screen.half_life_table(scenario)
+    assert t["반감기"].tolist() == list(config.HALF_LIFE_SENSITIVITY)
+    ref = t.set_index("반감기").loc[config.HALF_LIFE_DAYS]
+    s = screen.summary()[screen.SUMMARY_COLUMN[scenario]]
+    assert ref["T구간(2·3·4·5거 시작)"] == s["T구간(2·3·4·5거 시작)"]
+    for k in range(1, 6):
+        assert float(ref[f"{k}거%"]) == float(s[f"{k}거%"])
+    for name, _, _ in config.CRISIS_LIST:
+        assert int(ref[name]) == int(s[name])
+    assert "7·21·30일" in screen.HALF_LIFE_NOTE[-1]
+
+
+def test_month_events():
+    e = screen.month_events("2017-09")
+    assert list(e.columns) == ["날짜", "사건ID", "요소", "묶음", "구분", "S", "주체국", "사건명"]
+    assert len(e) == 3 and e["S"].is_monotonic_decreasing
+    assert e["사건ID"].iloc[0] == "A1-2058"                          # 6차 핵실험
+    assert (e["날짜"].dt.strftime("%Y-%m") == "2017-09").all()
+    assert set(screen.month_events("2010-03", top=10)["구분"]) <= {"상승", "완화(할인)", "하한 대상", "표시만"}
+    assert screen.month_events("2009-01").empty
+
+
+# 그림
+def test_figures(tmp_path):
+    f1 = screen.normalization_figure("기본")
+    f2 = screen.gpr_figure("기본")
+    assert isinstance(f1, go.Figure) and isinstance(f2, go.Figure)
+    assert [t.name for t in f1.data] == ["주 지수(묶음별 평소 대비) 7일 평균", "비교선 T_basic(단순 합) 7일 평균",
+                                         "차이(T_basic − 주 지수)"]
+    assert [t.name for t in f2.data] == ["봉수 월평균 T 순위%", "GPR 한국 순위%"]
+    assert list(f2.layout.yaxis.range) == [0, 100]
+    for name, fig in (("norm", f1), ("gpr", f2)):
+        assert charts.save_html(fig, tmp_path / f"{name}.html").stat().st_size > 1000
+
+
+# run_tension 출력(사건표 필요)
+@pytest.mark.regression
+def test_run_tension_writes_f6_files(tmp_path):
+    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", "2026-10-27", "--out", str(tmp_path)],
+                       cwd=ROOT, capture_output=True)
+    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
+    b = tio.read_csv_kr(tmp_path / "비교선_일별.csv")
+    assert list(b.columns) == ["시나리오", "날짜", "T_basic", "T_basic_표시7일"]
+    assert b.groupby("시나리오").size().to_dict() == {"기본": 6144, "확장": 6144}
+    raw = (tmp_path / "비교선_일별.csv").read_bytes()
+    assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
+    h = tio.read_csv_kr(tmp_path / "반감기_민감도.csv")
+    assert list(h.columns[:2]) == ["시나리오", "반감기"] and len(h) == 2 * len(config.HALF_LIFE_SENSITIVITY)
+    # 반감기 14일 행 = v0.1.4 요약(회귀 기준)과 같은 1~5거%·위기 단계
+    ref = tio.read_csv_kr(ROOT / "tests" / "fixtures" / "v014_요약.csv", index_col=0, dtype=str, keep_default_na=False)
+    for scenario, col in screen.SUMMARY_COLUMN.items():
+        r = h[(h["시나리오"] == scenario) & (h["반감기"] == config.HALF_LIFE_DAYS)].iloc[0]
+        assert r["T구간(2·3·4·5거 시작)"] == ref.loc["T구간(2·3·4·5거 시작)", col]
+        assert all(float(r[f"{k}거%"]) == float(ref.loc[f"{k}거%", col]) for k in range(1, 6))
+        assert all(int(r[n]) == int(ref.loc[n, col]) for n, _, _ in config.CRISIS_LIST)
+    # 비교선 = 사건표로 다시 계산한 ⑮′(기본, 3자리 반올림 안)
+    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
+    days = core.calc_days(config.CALC_START_DATE, "2026-10-27")
+    events, _ = tio.load_events(DATA / "events_기본.csv")
+    _, info = core.daily_table(events, days, config.BUNDLES_BASE, type4)
+    tb = core.basic_index(info["components"], config.BUNDLES_BASE, core.base_mask(days))
+    got = b[b["시나리오"] == "기본"]["T_basic"].to_numpy()
+    assert float(np.abs(got - tb.to_numpy()).max()) <= 0.0005 + 1e-9
diff --git a/utils/loader.py b/utils/loader.py
index f68be80..258ca59 100644
--- a/utils/loader.py
+++ b/utils/loader.py
@@ -84,3 +84,45 @@ def load_tension_contrib(day=None, scenario="기본", top=10):  # 점수 구성
 @st.cache_data
 def load_tension_figure(scenario="기본"):  # 추이 그림(Plotly) — st.plotly_chart(load_tension_figure())
     return tension_screen.figure(scenario)
+
+
+# ===== [F6 추가 · 긴장도 담당] 비교선 T_basic · GPR 비교 · 반감기 민감도 · 유사 시기 주요 사건 (utils/tension/screen.py) =====
+# 위 함수는 그대로 둔다. 화면에 붙이는 일은 화면 담당자께 요청(docs/dev/requests/F6_화면요청.md).
+@st.cache_data
+def load_tension_basic(scenario="기본"):  # 비교선 — 날짜·T_원값·T_표시7일·T_basic·T_basic_표시7일·차이_표시7일(설명 자리용)
+    return tension_screen.basic_line(scenario)
+
+
+@st.cache_data
+def load_tension_basic_stats(scenario="기본"):  # 비교선 요약 — 항목·값(상관·차이·상승 묶음 평소값)
+    return tension_screen.basic_stats(scenario)
+
+
+@st.cache_data
+def load_tension_normalization_figure(scenario="기본"):  # 묶음 정규화 효과 그림(Plotly)
+    return tension_screen.normalization_figure(scenario)
+
+
+@st.cache_data
+def load_tension_gpr(scenario="기본"):  # 봉수 vs GPR 월별 — 연월·봉수_T평균·GPR·봉수_순위%·GPR_순위%·순위차
+    return tension_screen.gpr_compare(scenario)
+
+
+@st.cache_data
+def load_tension_gpr_stats(scenario="기본"):  # GPR 비교 요약 — 항목·값(비교 기간·달 수·피어슨·순위 상관)
+    return tension_screen.gpr_stats(scenario)
+
+
+@st.cache_data
+def load_tension_gpr_figure(scenario="기본"):  # GPR 비교 그림(Plotly, 순위% 두 선)
+    return tension_screen.gpr_figure(scenario)
+
+
+@st.cache_data
+def load_tension_half_life(scenario="기본"):  # 반감기 민감도 — 반감기 7·14·21·30일 행(T 구간·1~5거%·같은 날%·위기 10건·현재)
+    return tension_screen.half_life_table(scenario)
+
+
+@st.cache_data
+def load_tension_month_events(month, scenario="기본", top=3):  # 그달 주요 사건(유사 시기 카드) — month = "YYYY-MM"
+    return tension_screen.month_events(month, scenario, top)
diff --git a/utils/tension/charts.py b/utils/tension/charts.py
index 7c139e7..e9eb7df 100644
--- a/utils/tension/charts.py
+++ b/utils/tension/charts.py
@@ -1,7 +1,8 @@
-"""긴장도 그림 (F4) — Plotly Figure를 돌려준다. Streamlit을 모른다(화면은 st.plotly_chart(fig)로 올림, 단독은 save_html).
+"""긴장도 그림 (F4·F6) — Plotly Figure를 돌려준다. Streamlit을 모른다(화면은 st.plotly_chart(fig)로 올림, 단독은 save_html).
 
 추이 그림(사용자 10-29): 위 = T 구간 가로 띠 + 표시선(7일 평균)·원값 + 위기 세로선 + A2 자료 끝 빗금,
 아래 = 단계_최종 색 띠(하한·하강 유예로 T 띠보다 높은 날이 보이게).
+F6(사용자 10-29): 묶음 정규화 효과(주 지수 vs 비교선 T_basic, 7일 평균) · GPR 비교(월별 순위% 두 선).
 """
 from pathlib import Path
 
@@ -81,6 +82,51 @@ def trend_figure(daily, cuts, *, compare=None, compare_name="확장(C5 포함) 7
     return fig
 
 
+def normalization_figure(line, *, title=None, height=420) -> go.Figure:
+    """(그림) 묶음 정규화 효과 — line = screen.basic_line() 표(날짜·T_표시7일·T_basic_표시7일·차이_표시7일).
+
+    주 지수(묶음마다 평소로 나눔)와 비교선 T_basic(단순 합, 완화 할인은 같음)을 7일 평균으로 겹치고, 아래에 차이를 그린다.
+    """
+    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.06)
+    x = line["날짜"]
+    fig.add_trace(go.Scatter(x=x, y=line["T_표시7일"], mode="lines", line=dict(color=LINE_MAIN, width=1.4),
+                             name="주 지수(묶음별 평소 대비) 7일 평균",
+                             hovertemplate="%{x|%Y-%m-%d} %{y:.1f}<extra>주 지수</extra>"), row=1, col=1)
+    fig.add_trace(go.Scatter(x=x, y=line["T_basic_표시7일"], mode="lines", line=dict(color=LINE_COMPARE, width=1, dash="dash"),
+                             name="비교선 T_basic(단순 합) 7일 평균",
+                             hovertemplate="%{x|%Y-%m-%d} %{y:.1f}<extra>T_basic</extra>"), row=1, col=1)
+    fig.add_trace(go.Scatter(x=x, y=line["차이_표시7일"], mode="lines", line=dict(color=INK, width=0.8),
+                             name="차이(T_basic − 주 지수)", hovertemplate="%{x|%Y-%m-%d} %{y:+.1f}<extra>차이</extra>"),
+                  row=2, col=1)
+    fig.add_hline(y=0, line=dict(color=INK, width=0.5, dash="dot"), row=2, col=1)
+    fig.update_yaxes(title_text="평소 = 100", rangemode="tozero", row=1, col=1)
+    fig.update_yaxes(title_text="차이", row=2, col=1)
+    fig.update_layout(height=height, title=title, hovermode="x unified", plot_bgcolor="white",
+                      margin=dict(l=10, r=10, t=90 if title else 50, b=10),
+                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
+    return fig
+
+
+def gpr_figure(table, *, title=None, height=380) -> go.Figure:
+    """(그림) GPR 비교 — table = screen.gpr_compare() 표(연월·봉수_T평균·GPR·봉수_순위%·GPR_순위%).
+
+    두 지수의 단위가 달라 각자 비교 기간 안 백분위 순위(0~100)로 같은 축에 그린다(사용자 10-29). 원값은 마우스를 올리면 보인다.
+    """
+    x = pd.to_datetime(table["연월"] + "-01")
+    fig = go.Figure()
+    fig.add_trace(go.Scatter(x=x, y=table["봉수_순위%"], mode="lines", line=dict(color=LINE_MAIN, width=1.4),
+                             name="봉수 월평균 T 순위%", customdata=table["봉수_T평균"].round(1),
+                             hovertemplate="%{x|%Y-%m} 순위 %{y:.0f}% · 월평균 T %{customdata}<extra>봉수</extra>"))
+    fig.add_trace(go.Scatter(x=x, y=table["GPR_순위%"], mode="lines", line=dict(color=LINE_COMPARE, width=1.2, dash="dash"),
+                             name="GPR 한국 순위%", customdata=table["GPR"].round(3),
+                             hovertemplate="%{x|%Y-%m} 순위 %{y:.0f}% · GPR %{customdata}%<extra>GPR</extra>"))
+    fig.update_yaxes(range=[0, 100], title_text="비교 기간 안 순위(%)")
+    fig.update_layout(height=height, title=title, hovermode="x unified", plot_bgcolor="white",
+                      margin=dict(l=10, r=10, t=90 if title else 50, b=10),
+                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
+    return fig
+
+
 def save_html(fig, path) -> Path:
     """(그림) HTML 파일로 저장 — Streamlit 없이 확인용. plotly.js는 CDN(인터넷 필요, 파일 작음)."""
     path = Path(path)
diff --git a/utils/tension/core.py b/utils/tension/core.py
index 5e0cab7..be6c54f 100644
--- a/utils/tension/core.py
+++ b/utils/tension/core.py
@@ -1,6 +1,6 @@
 """긴장도 계산 코어 — 산출식 ①~⑰(docs/tension/산출식_정리.md 1A.2절). 순수 함수: DataFrame·Series → DataFrame·Series.
 
-F2-1 = ②~⑧·⑩, F2-2 = ⑨·⑪~⑰. 입력 사건표는 io.load_events()가 돌려준 표(date datetime64·S float64),
+F2-1 = ②~⑧·⑩, F2-2 = ⑨·⑪~⑰, F6 = ⑮′(비교선 T_basic). 입력 사건표는 io.load_events()가 돌려준 표(date datetime64·S float64),
 반환 Series·DataFrame의 인덱스는 calc_days()의 날짜. config 값은 인자 기본값으로만 쓴다.
 """
 import bisect
@@ -244,6 +244,19 @@ def raw_gauge(comp, bundles) -> pd.Series:
     return sum(comp[f"R_{b}"] for b in bundles)
 
 
+def basic_index(comp, bundles, mask) -> pd.Series:
+    """⑮′ 비교선 T_basic — 상승 묶음 R의 합 ÷ 기준기간 평균 × 100 × (1 − δ). 묶음별 ÷B_g(정규화)만 뺀 T(사용자 10-29).
+
+    comp = tension_components()의 표(R_<묶음>·delta), mask = base_mask(days). 완화 할인 δ와 묶음 구성은 주 지수와 같다.
+    기준기간 평균이 0 이하이면 멈춘다(ValueError — 자료 이상, F2-3과 같은 규칙).
+    """
+    R = raw_gauge(comp, bundles)
+    base = float(R[mask].mean())
+    if not base > 0:
+        raise ValueError(f"비교선 T_basic: 기준기간 상승 묶음 R 합의 평균이 {base:g} - 0 이하(기준기간 사건 없음)")
+    return 100 * R / base * (1 - comp["delta"])
+
+
 def crisis_window_max(x, crises=config.CRISIS_LIST, window_days=config.CRISIS_WINDOW_DAYS) -> pd.Series:
     """⑮ 위기 눈금 — 위기일 t_c부터 t_c + 14일까지 x의 최댓값(x = 원점수_게이지면 게이지 눈금, 단계_최종이면 위기 단계)."""
     out = {}
diff --git a/utils/tension/io.py b/utils/tension/io.py
index 2f30b74..0e47371 100644
--- a/utils/tension/io.py
+++ b/utils/tension/io.py
@@ -14,6 +14,7 @@ TYPE4_COLUMNS = ("사건ID", "date", "요소", "S", "사건명", "판정유형",
 
 DATE_FORMAT = "%Y-%m-%d"
 TYPE4_ELEMENTS = ("A3", "A7")
+GPR_COLUMNS = ("month", "GPRC_KOR", "GPRHC_KOR")   # 채점_v0 입력_GPR_한국_월별.csv 그대로(F6)
 
 
 def read_csv_kr(path, **kwargs) -> pd.DataFrame:
@@ -117,3 +118,23 @@ def check_type4_against_events(table, events) -> pd.DataFrame:
         if r["요소"] not in TYPE4_ELEMENTS:
             problems.append((eid, "요소가 A3·A7 아님"))
     return pd.DataFrame(problems, columns=["사건ID", "문제"])
+
+
+def load_gpr_monthly(path) -> pd.DataFrame:
+    """GPR 한국 월별(F6)을 읽고 검증한다. 반환 = 열 `연월`(YYYY-MM 글자)·`GPR`(GPRC_KOR, 기사 비율 %), 연월 순.
+
+    비교 지수로만 쓴다(ADR-002). 열 이름·순서가 다르거나, 연월 형식·중복·빈 값·숫자 아님이 있으면 ValueError(빈 달을 0으로 두지 않음).
+    """
+    raw = read_csv_kr(path, dtype=str, keep_default_na=False)
+    _check_columns(raw, GPR_COLUMNS, path)
+    month = raw["month"].str.strip()
+    bad = ~month.str.fullmatch(r"\d{4}-(0[1-9]|1[0-2])")
+    if bad.any():
+        raise ValueError(f"{path}: month 형식(YYYY-MM)이 아님 — {list(month[bad][:10])}")
+    if month.duplicated().any():
+        raise ValueError(f"{path}: month 중복 — {sorted(set(month[month.duplicated()]))[:10]}")
+    value = pd.to_numeric(raw["GPRC_KOR"].str.strip(), errors="coerce")
+    if value.isna().any():
+        raise ValueError(f"{path}: GPRC_KOR 빈 값·숫자 아님 — {list(month[value.isna()][:10])}")
+    out = pd.DataFrame({"연월": month, "GPR": value.astype("float64")})
+    return out.sort_values("연월", kind="mergesort").reset_index(drop=True)
diff --git a/utils/tension/screen.py b/utils/tension/screen.py
index 17cf9d5..c10033d 100644
--- a/utils/tension/screen.py
+++ b/utils/tension/screen.py
@@ -4,6 +4,8 @@
 화면 이름 열을 더하고, 화면에서만 쓰는 값(지속일수·상위% 숨김·완화 할인 δ·사건별 남은 점수)을 만든다.
 10-29 사용자 결정: 평소대비 = 7일 표시값(원값은 `평소대비_원값`) · 상위 %는 첫 365일 숨김 · 점수 구성 = 묶음별 + 사건별 10건 ·
 주체국을 못 붙이면 "미상" · 완화 할인은 실제 δ · 시나리오는 기본이 주, 확장은 추이 그림 점선.
+F6(10-29 사용자): 비교선 T_basic(⑮′ — 정규화 효과만, 설명 자리용) · GPR 한국 월별 비교(순위% 두 선) · 반감기 민감도 표 ·
+반감기 설명 문구 · 유사 시기 그달 주요 사건.
 """
 from functools import lru_cache
 from pathlib import Path
@@ -37,6 +39,24 @@ READING_NOTES = ("기본점수·묶음 가중을 ±50% 흔들어도 일별 단
                  "방향 쌍 63~69% 일치(내부 대조용, 출처: Crisis Group).",
                  "북미 정상외교·국내 정치 사건은 지수 밖 — 완화는 남북 회담만.",
                  "반복 발사·정책 문서처럼 국제 보도는 적지만 군사 신호가 큰 달은 봉수가 GPR보다 높다(행동 vs 관심).")
+# F6 — GPR 비교 판독문 3줄(앞 2줄은 위 READING_NOTES와 같은 문구, 셋째 줄은 10-29 사용자 결정)
+GPR_NOTE_2018 = ("2018년 정상회담기에는 GPR이 높고 봉수가 낮다 — GPR은 보도량(관심)을, "
+                 "봉수는 남북 회담에 따른 완화(행동)를 반영한다(설계상 차이).")
+GPR_NOTES = (READING_NOTES[2], READING_NOTES[3], GPR_NOTE_2018)
+# F6 — 비교선 판독문 1줄(설명 자리 "묶음 정규화 효과" 그림 아래, 사용자 확인 대기 문구)
+NORMALIZATION_NOTE = ("묶음마다 평소로 나눈 우리 방식과 단순 합(묶음 구분 없이 더함)의 차이는 지금 자료에서 작다 — "
+                      "상승 묶음의 평소값이 비슷하기 때문이다. 물리 충돌·북러 밀착은 단순 합에 묻히지 않도록 하한으로 따로 반영한다.")
+GPR_SOURCE = ("GPR 한국 = GPRC_KOR(Caldara & Iacoviello, 한국 관련 지정학 위험 기사 비율 %, 월별). "
+              "비교 지수로만 씀(가중치를 맞추지 않음). 출처 matteoiacoviello.com/gpr.htm")
+# F6 — 반감기 설명 문구(docs/tension/감쇠_표시_단계유예_조사.md 4절 그대로, ADR-006 5번)
+HALF_LIFE_NOTE = (
+    "봉수는 기록된 사건의 영향을 \"반감기 14일\"로 셉니다. 사건 점수는 14일마다 절반이 되어 30일 뒤 약 23%, "
+    "60일 뒤 약 5%가 남습니다. 14일은 두 가지를 근거로 골랐습니다.",
+    "① 통일부 남북관계연표에서 큰 도발(핵실험·ICBM·물리 충돌 18건) 뒤 그 사건을 직접 언급한 기록이 줄어드는 속도를 쟀습니다. "
+    "추정 반감기는 약 15일이고 95% 구간은 12~62일입니다.",
+    "② 분쟁 사건 연구에서 한 사건의 영향이 이어지는 기간은 대체로 수일~수주로 보고됩니다.",
+    "이 값은 \"앞으로 며칠 위험하다\"는 예측이 아니라, 지나간 사건을 얼마나 오래 세는지에 대한 설계 선택입니다. "
+    "반감기를 7·21·30일로 바꾼 결과도 함께 공개합니다.")
 
 
 def _check(scenario):
@@ -195,3 +215,102 @@ def figure(scenario="기본", data_dir=DATA_DIR):
     from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
     compare = daily_raw("확장", data_dir) if scenario == "기본" else None
     return charts.trend_figure(daily_raw(scenario, data_dir), cuts(scenario, data_dir), compare=compare)
+
+
+# ===== F6 — 비교선 T_basic · GPR 비교 · 반감기 민감도 · 유사 시기 주요 사건 =====
+def _by_scenario(fname, scenario, data_dir):
+    _check(scenario)
+    t = tio.read_csv_kr(Path(data_dir) / fname)
+    return t[t["시나리오"] == scenario].drop(columns="시나리오").reset_index(drop=True)
+
+
+def basic_line(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
+    """(화면) 비교선 — 날짜 · T_원값 · T_표시7일(주 지수) · T_basic · T_basic_표시7일 · 차이_표시7일(T_basic − 주 지수, 7일 평균).
+
+    T_basic = 상승 묶음 R 합 ÷ 기준기간 평균 × 100 × (1 − δ)(⑮′) — 묶음별 정규화만 뺀 값(사용자 10-29). 설명 자리(산출 방법)용.
+    """
+    b = _by_scenario("비교선_일별.csv", scenario, data_dir)
+    b["날짜"] = pd.to_datetime(b["날짜"])
+    d = daily_raw(scenario, data_dir)[["T_원값", "T_표시7일"]].reset_index()
+    if len(b) != len(d) or not b["날짜"].equals(d["날짜"]):
+        raise ValueError(f"비교선_일별.csv와 일별_{scenario}.csv의 날짜가 다름 — run_tension.py로 함께 다시 만든다")
+    out = d.merge(b, on="날짜")
+    out["차이_표시7일"] = (out["T_basic_표시7일"] - out["T_표시7일"]).round(3)
+    return out
+
+
+def basic_stats(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
+    """(화면) 비교선 요약 — 항목·값: 주 지수와 상관(일별 원값) · 차이 최대·중앙(원값 절댓값) · 상승 묶음 평소값(요약.csv B_)."""
+    b = basic_line(scenario, data_dir)
+    diff = (b["T_basic"] - b["T_원값"]).abs()
+    s = summary(data_dir)[SUMMARY_COLUMN[scenario]]
+    base = " · ".join(f"{g} {float(s['B_' + g]):.2f}" for g in SCENARIOS[scenario])
+    return pd.DataFrame({"항목": ["주 지수(T)와 상관", "차이 최대(원값)", "차이 중앙(원값)", "상승 묶음 평소값"],
+                         "값": [f"{b['T_basic'].corr(b['T_원값']):.4f}", f"{diff.max():.1f}", f"{diff.median():.1f}", base]})
+
+
+def gpr_monthly(path=None) -> pd.DataFrame:
+    """(화면) GPR 한국 월별 원본 — 연월 · GPR(GPRC_KOR %). path 기본 = config.GPR_PATH."""
+    return tio.load_gpr_monthly(ROOT / config.GPR_PATH if path is None else path)
+
+
+def _pct_rank(x) -> pd.Series:
+    """(보조) 백분위 순위 0~100 — 채점 v0 s3_GPR_비교.py와 같은 rank(pct=True) × 100(같은 값은 평균 순위)."""
+    return x.rank(pct=True) * 100
+
+
+def gpr_compare(scenario="기본", data_dir=DATA_DIR, gpr_path=None) -> pd.DataFrame:
+    """(화면) 봉수 vs GPR 월별 — 연월 · 봉수_T평균(월별.csv T_평균) · GPR · 봉수_순위% · GPR_순위% · 순위차(봉수 − GPR).
+
+    두 자료가 다 있는 달만(GPR 끝 달까지). 순위는 그 비교 기간 안 백분위(0~100, 사용자 10-29 — 순위% 두 선).
+    """
+    m = monthly(scenario, data_dir)[["연월", "T_평균"]].rename(columns={"T_평균": "봉수_T평균"})
+    t = m.merge(gpr_monthly(gpr_path), on="연월", how="inner")
+    t["봉수_순위%"] = _pct_rank(t["봉수_T평균"]).round(1)
+    t["GPR_순위%"] = _pct_rank(t["GPR"]).round(1)
+    t["순위차"] = (t["봉수_순위%"] - t["GPR_순위%"]).round(1)
+    return t
+
+
+def gpr_stats(scenario="기본", data_dir=DATA_DIR, gpr_path=None) -> pd.DataFrame:
+    """(화면) 봉수 vs GPR 요약 — 항목·값: 비교 기간 · 달 수 · 피어슨 상관 · 순위 상관(스피어만 = 순위의 피어슨)."""
+    t = gpr_compare(scenario, data_dir, gpr_path)
+    pearson = t["봉수_T평균"].corr(t["GPR"])
+    spearman = t["봉수_T평균"].rank().corr(t["GPR"].rank())
+    return pd.DataFrame({"항목": ["비교 기간", "달 수", "피어슨 상관", "순위 상관"],
+                         "값": [f"{t['연월'].iloc[0]} ~ {t['연월'].iloc[-1]}", str(len(t)), f"{pearson:.2f}", f"{spearman:.2f}"]})
+
+
+def half_life_table(scenario="기본", data_dir=DATA_DIR) -> pd.DataFrame:
+    """(화면) 반감기 민감도 — 반감기_민감도.csv의 그 시나리오(반감기 7·14·21·30일 행, 열은 summary.half_life_table)."""
+    return _by_scenario("반감기_민감도.csv", scenario, data_dir)
+
+
+def month_events(month, scenario="기본", top=3, data_dir=DATA_DIR) -> pd.DataFrame:
+    """(화면) 그달 주요 사건 — month = 'YYYY-MM'. 그달 사건을 점수 S 큰 순으로 top건(같으면 늦은 날 먼저).
+
+    열 = 날짜 · 사건ID · 요소 · 묶음 · 구분(상승 / 완화(할인) / 하한 대상 / 표시만) · S · 주체국 · 사건명.
+    과거 유사 시기 카드의 "주요 사건"(개발 계획 2.3, 사용자 10-29)용. 사건표에 출처 열은 없다.
+    """
+    _check(scenario)
+    events, _ = tio.load_events(Path(data_dir) / f"events_{scenario}.csv")
+    ev = events[events["date"].dt.strftime("%Y-%m") == str(month)].copy()
+    bundles = list(SCENARIOS[scenario])
+    ev["구분"] = ev["묶음"].map(lambda b: "상승" if b in bundles else KIND.get(b, "그 밖"))
+    actors = _actor_map()
+    ev["주체국"] = ev["사건ID"].map(lambda k: actors.get(k, UNKNOWN_ACTOR))
+    ev = ev.sort_values(["S", "date"], ascending=[False, False]).head(top)
+    ev = ev.rename(columns={"date": "날짜"})[["날짜", "사건ID", "요소", "묶음", "구분", "S", "주체국", "사건명"]]
+    return ev.reset_index(drop=True)
+
+
+def normalization_figure(scenario="기본", data_dir=DATA_DIR):
+    """(화면) 묶음 정규화 효과 그림 — charts.normalization_figure(주 지수 vs T_basic, 7일 평균)."""
+    from utils.tension import charts
+    return charts.normalization_figure(basic_line(scenario, data_dir))
+
+
+def gpr_figure(scenario="기본", data_dir=DATA_DIR, gpr_path=None):
+    """(화면) GPR 비교 그림 — charts.gpr_figure(순위% 두 선)."""
+    from utils.tension import charts
+    return charts.gpr_figure(gpr_compare(scenario, data_dir, gpr_path))
diff --git a/utils/tension/summary.py b/utils/tension/summary.py
index a8c72f7..8b3634a 100644
--- a/utils/tension/summary.py
+++ b/utils/tension/summary.py
@@ -12,6 +12,8 @@ from utils.tension import core
 PERIOD_COLUMNS = ("일수", "T_평균", "T표시_최고", "원점수_평균", "단계_최고", "단계_평균",
                   "1거일", "2거일", "3거일", "4거일", "5거일")
 SUMMARY_NOTE = "A2 자료 {end}까지 — 그 뒤 미사일·ICBM 사건 하한 없음"
+HALF_LIFE_COLUMNS = ("반감기", "T구간(2·3·4·5거 시작)", "1거%", "2거%", "3거%", "4거%", "5거%", "T원값 최대",
+                     "기준 반감기와 단계 같은 날%", "한 단계 안%")   # + 위기 10건 단계 + 현재 (F6)
 
 
 def stage_streak(L, min_stage=4) -> pd.Series:
@@ -97,3 +99,28 @@ def summary_table(columns) -> pd.DataFrame:
     out = pd.DataFrame(rows).set_index("시나리오").T
     out.columns.name = None
     return out
+
+
+def half_life_table(runs, ref, crises=config.CRISIS_LIST) -> pd.DataFrame:
+    """(집계) 반감기 민감도(F6) — runs = {반감기(일): (일별 표, info)}(순서 유지), ref = 기준 반감기(14).
+
+    행 = 반감기 하나. 열 = HALF_LIFE_COLUMNS + 위기 10건(14일 안 최고 단계) + `현재`(마지막 날 화면 단계 문구).
+    T 구간은 반감기마다 같은 규칙(⑨)으로 다시 뽑은 값이다. 하한(물리·E5)의 감쇠는 바꾸지 않는다(ADR-006 2번).
+    """
+    if ref not in runs:
+        raise ValueError(f"기준 반감기 {ref}일이 runs에 없음: {list(runs)}")
+    L_ref = runs[ref][0]["단계_최종"].astype("int64")
+    rows = []
+    for h, (daily, info) in runs.items():
+        L = daily["단계_최종"].astype("int64")
+        if not L.index.equals(L_ref.index):
+            raise ValueError(f"반감기 {h}일 결과의 날짜가 기준과 다름")
+        stages = core.crisis_window_max(L, crises)
+        rows.append({"반감기": int(h), "T구간(2·3·4·5거 시작)": "/".join(f"{x:g}" for x in info["cuts"]),
+                     **{f"{k}거%": round((L == k).mean() * 100, 1) for k in range(1, 6)},
+                     "T원값 최대": round(float(daily["T_원값"].max())),
+                     "기준 반감기와 단계 같은 날%": round((L == L_ref).mean() * 100, 1),
+                     "한 단계 안%": round(((L - L_ref).abs() <= 1).mean() * 100, 1),
+                     **{name: int(stages[name]) for name, _, _ in crises},
+                     "현재": daily["화면_단계문구"].iloc[-1]})
+    return pd.DataFrame(rows)
```
<!-- F6.patch 끝 -->
