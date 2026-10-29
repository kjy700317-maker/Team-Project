# F2 검토 작업 프롬프트 — 계산 코어(PR #19) 독립 코드 리뷰 (U9)

작성 2026-10-29 · 구현 메인(채팅 ③) → **설계를 보지 않은 새 Claude Code 세션** · 브랜치 `feature/tension-core`(그대로 — 새 브랜치 없음) · PR [#19](https://github.com/kjy700317-maker/Team-Project/pull/19)(draft) · 이슈 #18
상태: **실행** (2026-10-29 사용자 확인 — 프롬프트 그대로)
권장 모델·노력: **Opus 5.5 · 높음**(계산 코어 검토 — 놓치면 화면 전체가 틀린다)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. **코드를 고치지 않는다 — 발견만 적는다.**
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). `conda run`은 쓰지 않는다. 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. **`$B`** = `$HOME/bongsu_F2review_20261029`(실험 스크립트는 모두 여기 — 리포 안에 만들지 않는다).
> **끝낼 때(사용자 10-29):** 세션 마지막 채팅 답은 **한국어로** 결과를 요약한다 — 결과 · 발견 개수(심각도별) · 가장 중요한 발견 3개 · 커밋·푸시 · 프롬프트와 다르게 한 것.
> 금지: 리포 파일 수정(1-3의 `CLAUDE.md` 한 줄과 6절 보고서 두 파일만 예외), `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, PR 병합·ready 전환·본문 수정, `develop`·`main` 직접 커밋, 파일 삭제(`rm` 대신 `$B`로 `mv`).

---

## 0. 목표와 읽는 범위 (치우치지 않게 하려는 것 — 꼭 지킨다)
- **목표:** `utils/tension/core.py`(289줄)·`scripts/run_tension.py`(47줄)가 **산출식 문서 `docs/tension/산출식_정리.md` 1A절(1A.1~1A.5)**의 식 ①~⑰을 정확히 구현했는지, 그리고 경계 조건·자료형·숨은 가정에서 틀릴 곳이 있는지 **독립적으로** 검토한다. 이 코드는 만든 쪽이 따로 v0.1.4 결과와 대조해 통과시켰다 — 그 검산을 다시 하는 것이 아니라 **그 검산이 못 잡는 것**(입력이 바뀌면 깨지는 곳, 문서와 코드의 어긋남, 앞으로 쓸 때의 함정)을 찾는 것이 일이다.
- **읽는 것:** 이 파일 · `CLAUDE.md`(자동) · `docs/tension/산출식_정리.md` **1A절만**(67행 `## 1A.`부터 `## 2.` 전까지) · `utils/tension/core.py` · `scripts/run_tension.py` · 입력을 이해하는 데 필요한 `config.py` · `utils/tension/io.py`.
- **읽지 않는 것:** `docs/dev/tasks/**`(구현 지시) · `docs/dev/reports/**`(이전 보고서) · `docs/dev/식_함수_대응표.md` · `docs/dev/진행기록.md` · `진행 현황 및 계획 정리/**`(기준 구현) · `docs/decisions.md` · 1A절 밖의 산출식 문서. 만든 쪽의 설명을 보면 같은 눈으로 보게 된다. 1-2 커밋에서 `git add`는 하되 내용은 열지 않는다.
- 판단이 서지 않는 것은 "질문"으로 적는다(추측으로 심각도를 올리지 않는다).

## 1. 시작 점검 · 문서 커밋 · CLAUDE.md (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F2review_20261029"; mkdir -p "$B"
git status --porcelain
#   기대(순서 무관 · 한글 경로가 "\354…"처럼 보여도 같은 것): " M docs/dev/진행기록.md", "?? docs/dev/tasks/F2_review.md", "?? .obsidian/"
git branch --show-current                    # 기대: feature/tension-core
git fetch origin
git status -sb | head -1                     # 기대: "## feature/tension-core...origin/feature/tension-core" (ahead/behind 없음)
git log --oneline -1                         # 기대: "… docs: F2-2 보고서"
gh pr view 19 --json state,isDraft,headRefName   # 기대: OPEN · true · feature/tension-core
git rev-list --left-right --count HEAD...origin/develop   # log에 적음(오른쪽 = develop에만 있는 커밋)
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest        # 기대: 14 passed
```
**1-2 커밋 1** — 구현 메인 문서(열지 않고 그대로 — U2):
```bash
git add docs/dev/tasks/F2_review.md docs/dev/진행기록.md
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
git commit -m "docs: F2 검토 작업 프롬프트·설계 문서 반영"
```
**1-3 커밋 2 — CLAUDE.md 한국어 요약 규칙**(사용자 10-29). 부록 A를 `$B/add_korean_summary.py`로 글자 그대로 저장하고 리포 루트에서:
```bash
PYTHONIOENCODING=utf-8 <py> "$B/add_korean_summary.py"   # 기대: "CLAUDE.md: 7절에 한국어 요약 규칙 1줄 넣음"
git diff --stat CLAUDE.md                                 # 기대: 1 file changed, 1 insertion(+)
git diff CLAUDE.md | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '   # 기대: "+**세션 마지막 채팅 답은 항상 한국어로**…" 한 줄
git add CLAUDE.md   # → 위 금지 경로 검사 → 커밋
git commit -m "docs: CLAUDE.md 마지막 답 한국어 요약 규칙"
```

## 2. 검토 항목 (모두 본다 · 항목마다 "문제 없음"도 한 줄 남긴다)
| # | 항목 | 볼 것 |
|---|---|---|
| R1 | 식 ↔ 코드 | 1A.2의 ②~⑰ 각각에 대응하는 함수를 찾아(docstring 첫 줄에 식 번호) **식과 같은 계산인지**. 첫날·시작값(③ R=0, ⑫ 첫날 L=J, ⑬ 처음 6일), 경계 부등호(≥·>·<), 반올림(⑨ ⌊x⌉와 짝수 반올림 — 1A.5), 분위수(1A.1 "선형 보간"), ⑭ 동점("≤"), ⑯ 50 조건, ⑰ 문구 |
| R2 | 문서 ↔ 코드 어긋남 | 1A의 글(1A.1 기호, 1A.3 표, 1A.5 주의)과 코드가 다른 곳. 예: 1A.2 ⑦은 φ_i를 식 안에 두는데 코드는 어디서 φ를 쓰는가(또는 안 쓰는가) · ⑮의 G가 시나리오에 따라 바뀌는가 · 일별 열 `완화할인`이 ⑦의 δ와 같은 값인가. **어느 쪽이 맞는지 판정하지 말고** 어긋남과 영향만 적는다 |
| R3 | 파라미터 | 숫자가 코드에 박혀 있지 않고 `config` 기본값으로 들어오는가. config 주석의 값과 1A의 값이 같은가(반감기 14, σ 10·창 30, 문턱 3·7·6·4·10·7.5, κ 0.5·c 0.1, 7일, 14일·50, 분위 0.70·0.90·0.95·0.98) |
| R4 | 경계 조건 | 아래를 `$B`에서 **합성 사건표로 실제로 돌려** 확인(결과는 log에): ① 사건 0행 ② 기준기간에 어떤 묶음 사건이 0건(B_g = 0 → 나누기) ③ 계산 기간 밖 날짜만 있는 사건 ④ 같은 날 여러 사건 ⑤ END가 기준기간 끝(2019-12-31)보다 이른 경우 ⑥ `calc_days(end=None)` ⑦ 시작일에 사건 1건(⑨ 분위가 0인 경우 포함) ⑧ ⑭ 동점이 많은 구간(T̄ = 0이 이어지는 2010년 초) ⑨ `step_down` 첫날이 높은 단계 ⑩ `type4_ids`가 비었을 때. "예외가 나는가 / 조용히 틀린 값이 나오는가 / 맞는가"로 적는다 |
| R5 | 자료형·pandas 3 | 정수 열 int64, bool 열 bool, 문자열 열, NaN이 생기는 곳(⑯·`완화할인`), `datetime64[us]`, `isin`·`reindex`·`np.select`에 Series를 넘기는 곳, 경고(`FutureWarning`·`RuntimeWarning`)가 나는 곳 — `<py> -W error::FutureWarning`로 한 번 돌려 본다 |
| R6 | 순수 함수·경계 | `core.py`가 파일·Streamlit·전역 상태를 모르는가, 입력 DataFrame을 바꾸지 않는가(돌리기 전후 `events.equals(사본)`), 같은 입력에 같은 출력 |
| R7 | `run_tension.py` | 경로(리포 루트 기준, 한국어 경로), 인코딩(utf-8-sig·LF), `--end` 잘못된 값일 때, 사건표가 없을 때 메시지, 반환 코드 |
| R8 | F3 테스트 제안 | 위에서 본 것 중 단위 테스트로 고정할 것(입력 · 기대값 · 왜) — 최대 15개. 이미 통과한 v0.1.4 회귀 대조와 겹치는 것은 빼고 **회귀가 못 잡는 것** 위주 |

- 실험은 `$B/*.py`에 쓰고 리포 루트에서 `PYTHONIOENCODING=utf-8 <py> "$B/<파일>.py"`로 돌린다(`sys.path`에 리포 루트를 넣고 `from utils.tension import core, io as tio`). 실제 사건표(`data/tension/events_*.csv`)는 읽어도 되지만 바꾸지 않는다.
- 심각도: **높음** = 지금 입력이나 앞으로 들어올 입력에서 1A와 다른 단계·값이 나옴(재현 명령 필수) · **중간** = 예외로 멈추거나, 문서와 코드가 달라 다음 사람이 틀리게 쓸 수 있음 · **낮음** = 읽기·유지보수 · **정보** = 질문·확인 요청.

## 3. 하지 않는 것
- 코드·테스트·문서 수정(1-3 한 줄 · 보고서 두 파일만 예외), 새 테스트 파일을 리포에 만들기(F3 몫 — R8은 제안만)
- v0.1.4 기준 CSV와의 전 열 대조 다시 하기(이미 통과 — 필요하면 한 열만 확인 용도로)
- 기준 구현·구현 지시·이전 보고서 읽기(0절)

## 4. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 기대 상태, 14 passed |
| 2 | 1-2·1-3 커밋 | 금지 경로 `OK`, CLAUDE.md +1줄 |
| 3 | R1~R8 | 항목마다 결과(발견 또는 "문제 없음" 한 줄) |
| 4 | R4 | 10가지 경계를 실제로 돌린 출력이 log에 있음 |
| 5 | 높음 발견 | 모두 재현 명령·출력 있음 |
| 6 | 리포 파일 | 1-3·보고서 말고 바뀐 파일 없음(`git status --porcelain`이 커밋 뒤 `?? .obsidian/` 하나만) |

## 5. 커밋 · 푸시
1. `docs: F2 검토 작업 프롬프트·설계 문서 반영`(1-2)  2. `docs: CLAUDE.md 마지막 답 한국어 요약 규칙`(1-3)  3. `docs: F2 검토 보고서`(6절 두 파일)
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
git push
gh pr view 19 --json state,isDraft    # 기대: OPEN · true (본문은 고치지 않는다)
```

## 6. 보고서 (두 파일)
`docs/dev/reports/F2_review.md`(**80줄 이내**):
```markdown
# F2 검토 보고서 — 계산 코어(PR #19) 독립 리뷰
- 결과: 완료 / 일부 / 멈춤(이유) · 날짜 · 브랜치 · 커밋 · 환경(python/numpy/pandas)
- 읽은 것: (0절 범위를 지켰는지 한 줄 — 더 읽은 것이 있으면 적는다)
## 1. 발견 (심각도 순)
| # | 심각도 | 위치(파일:행) | 식 | 내용 | 근거(log 절) | 제안 |
## 2. 항목별 결과 (R1~R8 한 줄씩 — 문제 없음도)
## 3. F3 테스트 제안 (R8 — 입력 · 기대 · 이유)
## 4. 질문 (구현 메인이 답할 것 — 없으면 "없음")
```
`docs/dev/reports/F2_review_log.md`: 1절 출력 · R4 실험 스크립트와 출력 전부 · R5 경고 출력 · 커밋·푸시 출력.

---

## 부록 A. `$B/add_korean_summary.py` (글자 그대로 저장)
```python
"""F2 검토 1-3 — CLAUDE.md 7절 끝 문장 다음 줄에 '마지막 채팅 답은 한국어 요약' 규칙 한 줄을 넣는다(사용자 10-29). 바이트로 넣어 줄바꿈을 그대로 둔다."""
from pathlib import Path

p = Path("CLAUDE.md")
b = p.read_bytes()
nl = b"\r\n" if b"\r\n" in b else b"\n"
anchor = "보고서 두 파일을 커밋한 뒤 세션을 끝낸다. 다음 기능은 새 세션에서 새 프롬프트로.".encode("utf-8") + nl
add = ("**세션 마지막 채팅 답은 항상 한국어로**(10-29 사용자): 결과(완료·일부·멈춤) · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것을 짧게 요약한다."
       .encode("utf-8") + nl)
assert b.count(anchor) == 1, f"기준 문장이 {b.count(anchor)}번 — 멈춤"
assert add not in b, "이미 들어 있음 — 멈춤"
p.write_bytes(b.replace(anchor, anchor + add))
print("CLAUDE.md: 7절에 한국어 요약 규칙 1줄 넣음")
```
