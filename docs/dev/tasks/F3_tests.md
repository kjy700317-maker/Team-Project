# F3 작업 프롬프트 — 테스트: 단위(test_core) · v0.1.4 회귀(test_regression) · 기준 파일(fixtures)

작성 2026-10-29 · 구현 메인(채팅 ③) → Claude Code · 브랜치 **`feature/tension-tests`(PR #19 병합 뒤 최신 `develop`에서 새로 — U4)** · PR 대상 `develop`
상태: **실행 대기 — PR #19 병합 뒤 실행**(10-29 사용자 결정 반영: 사건표 없으면 원인을 알리며 실패 · 기준 파일 = 요약 + v0.1.4 일별 2개 · AI 표기 금지. PR #19는 10-29 05:08 UTC 병합 확인 — 일반 merge 커밋 `041dda5`)
권장 모델·노력: **Opus 5.5 · 중간**(파일은 부록 그대로 저장 + 실행·커밋 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`. **`$B`** = `$HOME/bongsu_F3_20261029`.
> **끝낼 때(CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약.
> **AI 표기 금지(사용자 10-29, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 1-4 훅을 **첫 커밋 전에** 설치하고, 이슈·PR 본문과 푸시 전 커밋 메시지를 8절 검사로 확인한다. 검사 패턴 `$AI`는 1-3에서 정의(셸이 새로 열리면 다시 정의).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, **`utils/`·`scripts/`·`config.py` 수정**(테스트가 실패하면 코드를 고치지 말고 보고).

---

## 0. 목표
- 부록의 파일 5개를 리포에 **글자 그대로** 저장해 테스트를 고정한다. 모두 구현 메인이 리포 밖에서 F2-3까지 반영된 리포 코드로 돌려 통과시킨 것이다 `[확인 10-29: python 3.10 · numpy 2.2.6 · pandas 2.3.3 · pytest 9.2]`:
  - `tests/fixtures/` 기준 파일 3개(부록 A 스크립트로 복사 — 일별 2개는 바이트 그대로, 요약은 "완화 상한에 붙은 날" 빈칸만 272) + `tests/fixtures/README.md`(부록 B)
  - `pytest.ini`(부록 C — `markers`에 `regression` 추가)
  - `tests/test_core.py`(부록 D — 합성 자료 단위 테스트 33개: 식 ③⑩④~⑧⑨⑪⑫⑬⑭⑯⑰·보조 열·하한 규칙·ID 검사·조립과 F2-3 멈춤 규칙·params)
  - `tests/test_regression.py`(부록 E — v0.1.4 회귀 14개: 사건표 있는지 · 일별 전 열 · 0절 완료 기준 · 요약 값 전부 · END 연장 · run_tension 출력)
- **기대 결과:** `<py> -m pytest` → **61 passed**(기존 14 + 33 + 14). 사건표를 치우면 회귀는 **1 failed(원인·만드는 법 메시지) + 13 skipped**, `-m "not regression"` → 47 passed · 14 deselected.
- F2 검토 3절 테스트 제안 15개는 부록 D에 들어 있다(1~3·14는 F2-3 결정대로 "멈춤" 기대). 요약 지표는 F4가 함수로 만들기 전까지 `test_regression.py` 안에서 계산한다(F4에서 그 함수로 바꿀 예정).

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F3_20261029"; mkdir -p "$B/docs"
git status --porcelain
#   기대(순서 무관 · 한글 경로가 "\354…"처럼 보여도 같은 것): " M docs/dev/진행기록.md", "?? docs/dev/tasks/F3_tests.md", "?? .obsidian/"
git branch --show-current                          # 기대: feature/tension-core
git fetch origin
gh pr view 19 --json state,mergedAt                # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop

# 1-1 구현 메인 문서 백업(리포 밖) → 되돌리고 develop으로
for f in docs/dev/진행기록.md docs/dev/tasks/F3_tests.md; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git restore docs/dev/진행기록.md
git switch develop
git pull --ff-only origin develop                  # 실패하면 멈추고 보고
git log --oneline -1                               # origin/develop과 같아야 함
# 1-2 되살리기 → 브랜치
for f in docs/dev/진행기록.md docs/dev/tasks/F3_tests.md; do cp "$B/docs/$f" "$f"; done
git status --porcelain                             # 1절 첫 기대와 같아야 함
git switch -c feature/tension-tests
# 1-3 이슈: 본문 "$B/issue_F3.md" = .github/ISSUE_TEMPLATE/feature.md 양식(배경 = 0절, 범위 = 부록 파일 5개, 완료 조건 = 7절) — AI 표기 없이
AI='co-authored-by|generated with|claude-session|claude\.ai/code|claude\.com/claude-code|🤖'
grep -inE "$AI" "$B/issue_F3.md" && echo "AI 표기 있음 — 지우고 다시" || echo "OK"
gh issue create --title "[FEAT] 긴장도 단위·회귀 테스트(F3)" --label feat --body-file "$B/issue_F3.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas, pytest; print(numpy.__version__, pandas.__version__, pytest.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest              # 기대: 14 passed(F2까지)
ls data/tension/events_기본.csv data/tension/events_확장.csv   # 있어야 함 — 없으면 PYTHONIOENCODING=utf-8 <py> scripts/build_events.py --end 2026-10-27
```
**1-4 commit-msg 훅 설치 — 첫 커밋 전에**(사용자 10-29 AI 표기 금지 · 로컬 `.git/hooks/` — 리포에 커밋하지 않음). 부록 F를 `.git/hooks/commit-msg`로 글자 그대로 저장:
```bash
chmod +x .git/hooks/commit-msg
printf 'docs: 시험\n\n본문\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n' > "$B/msg_test.txt"
sh .git/hooks/commit-msg "$B/msg_test.txt" && cat "$B/msg_test.txt"   # 기대: "docs: 시험" · 빈 줄 · "본문"만 남음
git status --porcelain                                                # 훅은 .git 안이라 보이지 않음(1절 첫 기대와 같음)
```
**커밋 1** `docs: F3 작업 프롬프트·설계 문서 반영` — `docs/dev/tasks/F3_tests.md`, `docs/dev/진행기록.md`(내용 수정 없이 — U2). 8절 금지 경로 검사 뒤. 커밋 뒤 `git log -1 --format=%B`에 AI 표기가 없는지 확인(훅 작동 확인).

**1-5 커밋 2 — CLAUDE.md AI 표기 금지 규칙**(사용자 10-29). 부록 G를 `$B/add_no_ai_rule.py`로 저장하고 리포 루트에서:
```bash
PYTHONIOENCODING=utf-8 <py> "$B/add_no_ai_rule.py"     # 기대: "CLAUDE.md: 6절에 AI 표기 금지 규칙 1줄 넣음"
git diff --stat CLAUDE.md                               # 기대: 1 file changed, 1 insertion(+)
git add CLAUDE.md   # → 금지 경로 검사 → 커밋
git commit -m "docs: CLAUDE.md AI 표기 금지 규칙"
```
**1-6 PR #15·#17 본문 정리**(사용자 10-29 — 본문 끝 `🤖 Generated with Claude Code` 줄만 지움, 히스토리 영향 없음). 부록 H를 `$B/clean_pr_body.py`로 저장:
```bash
for n in 15 17; do
  gh pr view $n --json body -q .body > "$B/pr${n}_old.md"
  PYTHONIOENCODING=utf-8 <py> "$B/clean_pr_body.py" "$B/pr${n}_old.md" "$B/pr${n}_new.md"   # 기대: 지운 줄 1~2개
  diff "$B/pr${n}_old.md" "$B/pr${n}_new.md"                                               # AI 표기 줄(과 끝 빈 줄)만 빠짐
  gh pr edit $n --body-file "$B/pr${n}_new.md"
  gh pr view $n --json body -q .body | grep -inE "$AI" && echo "#$n 아직 있음 — 멈춤" || echo "#$n OK"
done
```

## 2. 기준 파일 (부록 A·B)
```bash
# 부록 A를 "$B/make_fixtures.py"로 글자 그대로 저장, 리포 루트에서
PYTHONIOENCODING=utf-8 <py> "$B/make_fixtures.py"     # 기대: v014_요약.csv 2051 · v014_일별_기본.csv 709627 · v014_일별_확장.csv 754704 바이트
# 부록 B를 tests/fixtures/README.md로 글자 그대로 저장
for n in 기본 확장; do cmp "tests/fixtures/v014_일별_$n.csv" "진행 현황 및 계획 정리/v0.1_시험/v0.1.4/일별_v014_$n.csv" && echo "$n 같음"; done
grep "완화 상한" tests/fixtures/v014_요약.csv          # 기대: 완화 상한에 붙은 날,272,272
git add tests/fixtures/ && git ls-files --eol tests/fixtures/*.csv   # 기대: 세 줄 모두 i/lf · attr/text eol=lf
```
**커밋 3** `test: v0.1.4 회귀 기준 파일(fixtures)` — `tests/fixtures/` 4개(`.gitkeep`은 그대로 둔다).

## 3. 테스트 파일 (부록 C·D·E)
부록 C → `pytest.ini`(덮어씀), 부록 D → `tests/test_core.py`, 부록 E → `tests/test_regression.py`. 셋 다 **글자 그대로**(코드 블록을 파이썬으로 잘라 저장해도 된다 — 줄 수를 log에 적음).
```bash
git diff pytest.ini | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '    # 기대: markers 두 줄만 +
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_core.py          # 기대: 33 passed
```
**커밋 4** `test: 계산 코어 단위 테스트(test_core)` — `tests/test_core.py`.

## 4. 회귀 · 전체 · 사건표 없음
```bash
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_regression.py    # 기대: 14 passed
PYTHONIOENCODING=utf-8 <py> -m pytest                             # 기대: 61 passed
PYTHONIOENCODING=utf-8 <py> -m pytest -m "not regression"         # 기대: 47 passed, 14 deselected
# 사건표가 없을 때(사용자 10-29: 원인을 알리며 실패) — rm이 아니라 mv로 치웠다가 되돌린다
mv data/tension/events_기본.csv "$B/"
PYTHONIOENCODING=utf-8 <py> -m pytest tests/test_regression.py -rs   # 기대: 1 failed, 13 skipped · 메시지 "회귀 테스트 입력 사건표가 없다: ['data/tension/events_기본.csv']" + 만들기·빼기 안내
mv "$B/events_기본.csv" data/tension/
PYTHONIOENCODING=utf-8 <py> -m pytest                             # 기대: 61 passed (되돌린 뒤)
PYTHONIOENCODING=utf-8 <py> -W error::FutureWarning -m pytest     # 기대: 61 passed(경고 0)
```
**커밋 5** `test: v0.1.4 회귀 테스트·regression 표시` — `tests/test_regression.py`, `pytest.ini`.
- 기대와 다르면(실패·개수 다름) 테스트도 코드도 고치지 말고, 실패 출력 전부를 log에 남기고 멈추고 보고한다(pandas 3.0에서만 다른 것으로 보이면 그렇게 적는다).

## 5. 하지 않는 것
- `utils/`·`scripts/`·`config.py`·`requirements.txt` 수정, 요약 지표 함수 만들기(F4), 결과 CSV 커밋(F4)
- 부록과 다른 테스트를 더하거나 빼기(고치고 싶은 것은 보고서 3절)

## 6. 확인 명령 (커밋 5 뒤)
```bash
git diff --stat origin/develop...HEAD -- tests pytest.ini     # tests/fixtures 4 · test_core · test_regression · pytest.ini
git status --porcelain                                        # 기대: "?? .obsidian/" 하나만
```

## 7. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 | PR #19 MERGED, 새 브랜치, 이슈 번호, 14 passed |
| 2 | 2절 | 일별 2개 원본과 바이트 같음, 요약 272, eol LF |
| 3 | 3절 | pytest.ini는 markers 두 줄만, test_core 33 passed |
| 4 | 4절 회귀 | 14 passed |
| 5 | 4절 전체 | 61 passed · not regression 47/14 · FutureWarning 경고 0 |
| 6 | 4절 사건표 없음 | 1 failed + 13 skipped, 메시지에 없는 파일·만드는 법, 되돌린 뒤 61 passed |
| 7 | 커밋 | 8절 순서 |
| 8 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 9 | 마지막 status | `?? .obsidian/` 하나만 |
| 10 | 1-4 훅 | 시험 메시지에서 AI 표기 줄이 지워짐, 커밋 1 메시지에 표기 없음 |
| 11 | 1-5 CLAUDE.md | +1줄 |
| 12 | 1-6 PR #15·#17 | 두 본문 모두 `OK` |
| 13 | 8절 AI 표기 검사 | 이슈 본문·커밋 메시지 전부·PR 본문 모두 `OK` |

## 8. 커밋 · 푸시 · PR
금지 경로 검사(각 커밋 전 — 이번에는 `tests/fixtures/v014_일별_*`가 들어가므로 `일별_`은 `data/tension/` 아래만 막는다):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|^data/tension/.*일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F3 작업 프롬프트·설계 문서 반영` 2. `docs: CLAUDE.md AI 표기 금지 규칙` 3. `test: v0.1.4 회귀 기준 파일(fixtures)` 4. `test: 계산 코어 단위 테스트(test_core)` 5. `test: v0.1.4 회귀 테스트·regression 표시` 6. `docs: F3 보고서`
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest    # 61 passed
git log --format=%B origin/develop..HEAD | grep -inE "$AI" && echo "커밋에 AI 표기 있음 — 멈추고 보고(히스토리 고치지 않음)" || echo "OK"
git push -u origin feature/tension-tests
# 본문 "$B/pr_F3.md" = .github/pull_request_template.md 양식 · closes #<1-3 이슈> · 변경 = 8절 2~4 · 테스트 = 7절 결과
#   · 체크리스트 아래에 "팀원 안내: 회귀 테스트는 로컬 사건표가 있어야 돈다 — 없으면 test_events_present가 만드는 법을 알리며 실패, 회귀만 빼려면 -m \"not regression\"" 한 줄
grep -inE "$AI" "$B/pr_F3.md" && echo "PR 본문에 AI 표기 있음 — 지우고 다시" || echo "OK"
gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 단위·회귀 테스트(F3)" --body-file "$B/pr_F3.md"
gh pr view --json body -q .body | grep -inE "$AI" && echo "올라간 PR 본문에 AI 표기 — gh pr edit로 지움" || echo "OK"
```
병합하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 9. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F3_report.md`(60줄 이내): 1절 = 7절 표 13행 ✓/✗ · 테스트 수 요약 · 2절 막힌 것 · 3절 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F3_log.md`: 1~4·6절 출력 전부(사건표 없음 실패 메시지 원문 포함), 커밋·푸시·PR 출력.

---

## 부록 A. `$B/make_fixtures.py` (글자 그대로 저장)
```python
"""F3 — v0.1.4 기준 파일을 tests/fixtures/로 복사한다(리포 루트에서). 요약의 빈칸 '완화 상한에 붙은 날'만 272로 채운다(대응표 4절)."""
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "진행 현황 및 계획 정리" / "v0.1_시험" / "v0.1.4"
DST = ROOT / "tests" / "fixtures"
DST.mkdir(parents=True, exist_ok=True)
for name in ("기본", "확장"):
    data = (SRC / f"일별_v014_{name}.csv").read_bytes()
    assert data.startswith(b"\xef\xbb\xbf") and b"\r\n" not in data, name
    (DST / f"v014_일별_{name}.csv").write_bytes(data)
data = (SRC / "요약_v014.csv").read_bytes()
old = "\n완화 상한에 붙은 날,,\n".encode("utf-8")
new = "\n완화 상한에 붙은 날,272,272\n".encode("utf-8")
assert data.count(old) == 1 and b"\r\n" not in data
(DST / "v014_요약.csv").write_bytes(data.replace(old, new))
for f in sorted(DST.glob("v014_*.csv")):
    print(f.name, f.stat().st_size, "바이트")
```

## 부록 B. `tests/fixtures/README.md` (글자 그대로 저장)
```markdown
# tests/fixtures — v0.1.4 회귀 기준 (F3, 2026-10-29)

- `v014_일별_기본.csv`·`v014_일별_확장.csv`: `진행 현황 및 계획 정리/v0.1_시험/v0.1.4/일별_v014_*.csv`를 바이트 그대로 복사(compute_v014.py 2026-10-28, ADR-018 확정판). 2010-01-01~2026-10-27, 6,144일.
- `v014_요약.csv`: `요약_v014.csv` 복사 + 빈칸 `완화 상한에 붙은 날`을 272로 채움(기준 구현 요약의 빈칸 — `docs/dev/식_함수_대응표.md` 4절).
- 이 파일들은 고치지 않는다. 규칙이 바뀌어 기준이 바뀌면(새 모델 버전) 새 파일(`v015_…`)을 더하고 ADR에 적는다.
- 회귀 테스트(`tests/test_regression.py`)는 로컬 사건표(`data/tension/events_*.csv`, 깃 제외)가 있어야 돈다. 없으면 `test_events_present`가 만드는 법을 알리며 실패한다(사용자 10-29). 회귀만 빼려면 `python -m pytest -m "not regression"`.
```

## 부록 C. `pytest.ini` (글자 그대로 — 덮어씀)
```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -q
markers =
    regression: v0.1.4 회귀 — 로컬 사건표(data/tension/events_*.csv) 필요, 없으면 실패. 빼려면 -m "not regression"
```

## 부록 D. `tests/test_core.py` (글자 그대로 저장)
```python
"""core.py 단위 테스트(F3) — 작은 합성 자료로 식 ②~⑰과 멈춤 규칙을 고정한다. 사건표·원자료 없이 돈다."""
import numpy as np
import pandas as pd
import pytest

import config
from utils.tension import core

DOT = "·"


def ev(rows):
    """(사건ID, date, 요소, 묶음, S, 사건명) 목록 → io.load_events와 같은 모양의 사건표."""
    df = pd.DataFrame(rows, columns=["사건ID", "date", "요소", "묶음", "S", "사건명"])
    df["date"] = pd.to_datetime(df["date"])
    df["S"] = df["S"].astype(float)
    return df


def s(values, start="2020-01-01"):
    return pd.Series(values, index=pd.date_range(start, periods=len(values), freq="D"), dtype=float)


def base_events(first_year=2010, last_year=2020):
    """기준기간을 채우는 합성 사건표 — 상승 3묶음·완화를 매달 1일에 한 건씩."""
    rows = []
    for y in range(first_year, last_year + 1):
        for m in range(1, 13):
            d = f"{y}-{m:02d}-01"
            for i, (b, e, sc) in enumerate([("핵·미사일", "A2", 5.0), ("군사 과시", "B2", 3.0),
                                            ("위협 언어·교리", "C1", 4.0), ("완화", "F2", 1.0)]):
                rows.append((f"{e}-{y}{m:02d}{i}", d, e, b, sc + (m % 3), "합성"))
    return ev(rows)


# ③ 감쇠
def test_decay_half_life():
    r = core.decay_cumulative(s([1.0] + [0.0] * 14))
    assert r.iloc[0] == 1.0
    assert abs(r.iloc[14] - 0.5) < 1e-12


def test_decay_accumulates_from_zero():
    lam = 2 ** (-1 / 14)
    r = core.decay_cumulative(s([1.0, 1.0]))
    assert r.tolist() == pytest.approx([1.0, 1.0 + lam], abs=1e-15)


# ⑩ 반가우스 창
def test_half_gauss_window_weights():
    r = core.half_gauss_window(s([1.0] + [0.0] * 30))
    assert r.iloc[0] == 1.0
    assert abs(r.iloc[10] - np.exp(-0.5)) < 1e-12
    assert abs(r.iloc[29] - np.exp(-841 / 200)) < 1e-15
    assert r.iloc[30] == 0.0


# ④~⑧
def test_relative_rising_relief_tension():
    idx = pd.date_range("2020-01-01", periods=1)
    R = pd.DataFrame({"a": [2.0], "b": [4.0]}, index=idx)
    Tg = core.relative_index(R, pd.Series({"a": 1.0, "b": 2.0}))
    assert Tg.iloc[0].tolist() == [200.0, 200.0]
    T_plus = core.rising_index(Tg)
    delta = core.relief_discount(pd.Series([10.0], index=idx), 1.0)
    assert (T_plus.iloc[0], delta.iloc[0]) == (200.0, 0.5)       # c·R/B = 1.0 → 상한 0.5
    assert core.tension_index(T_plus, delta).iloc[0] == 100.0


# ⑨ 구간
@pytest.mark.parametrize("values, cut, warn", [([114, 115], 114, True), ([115, 116], 116, True), ([115, 115.4], 115, False)])
def test_stage_cuts_round_half_even(values, cut, warn):
    T = pd.Series(values, dtype=float)
    cuts, q = core.stage_cuts(T, np.array([True] * len(values)), quantiles=(0.5, 0.5, 0.5, 0.5))
    assert cuts[0] == cut
    assert core.cuts_half_warning(q) is warn


def test_cuts_half_warning_float_tolerance():
    assert core.cuts_half_warning([256.49999999999997]) is True
    assert core.cuts_half_warning([256.4, 115.27]) is False


def test_stage_from_index_boundaries():
    T = pd.Series([114.999999999, 115, 255.99, 256, 315, 378, 1000, 0])
    assert core.stage_from_index(T, (115, 256, 315, 378)).tolist() == [1, 2, 2, 3, 4, 5, 5, 1]


# ⑪⑫
def test_judge_is_max():
    a, b, c, d = (pd.Series(x) for x in ([1, 3], [2, 1], [1, 1], [4, 1]))
    out = core.judge(a, b, c, d)
    assert out.tolist() == [4, 3] and out.dtype == "int64"


def test_step_down_one_stage_per_seven_days():
    L = core.step_down(pd.Series([5] + [1] * 30))
    assert L.tolist() == [5] * 7 + [4] * 7 + [3] * 7 + [2] * 7 + [1] * 3


def test_step_down_wait_continues_through_lower_judgement():
    J = pd.Series([3, 5, 1, 1, 1, 1, 1, 1, 4, 1])
    assert core.step_down(J).tolist() == [3, 5, 5, 5, 5, 5, 5, 5, 4, 4]


def test_step_down_rises_immediately_and_n_param():
    assert core.step_down(pd.Series([1, 3, 1, 1, 1, 1]), n=3).tolist() == [1, 3, 3, 3, 2, 2]


# ⑬⑭⑯⑰
def test_display_ma_first_days_partial():
    assert core.display_ma(s([7, 0, 0, 0, 0, 0, 0, 0])).tolist() == pytest.approx([7, 3.5, 7 / 3, 1.75, 1.4, 7 / 6, 1.0, 0.0])


def test_cumulative_top_pct_ties_are_le():
    assert core.cumulative_top_pct(s([0, 0, 0, 5, 5, 1])).tolist() == pytest.approx([0, 0, 0, 0, 0, 100 / 3])


@pytest.mark.parametrize("prev, pct_nan", [(50.0, False), (49.999, True)])
def test_trend_pct_min(prev, pct_nan):
    tr = core.trend(s([prev] + [0.0] * 13 + [60.0]))
    assert list(tr.columns) == ["변화14_표시", "변화율14_표시"]
    assert tr["변화14_표시"].iloc[14] == pytest.approx(60.0 - prev)
    assert bool(np.isnan(tr["변화율14_표시"].iloc[14])) is pct_nan
    if not pct_nan:
        assert tr["변화율14_표시"].iloc[14] == pytest.approx(20.0)


def test_stage_label_wording():
    out = core.stage_label(pd.Series([2, 3]), pd.Series([1, 3])).tolist()
    assert out == [f"2거 {DOT} 하강 중(판정 1거)", "3거"]


# 보조 열
def test_provisional_last_six_days():
    days = pd.date_range("2020-01-01", periods=10)
    assert core.provisional(days).tolist() == [False] * 4 + [True] * 6


def test_a2_note_after_end():
    out = core.a2_note(pd.DatetimeIndex(["2024-11-05", "2024-11-06"])).tolist()
    assert out == ["", "A2 자료 없음(2024-11-05까지)"]


def test_relief_display_zero_when_rising_zero():
    T = pd.Series([0.0, 50.0])
    Tg = pd.DataFrame({"a": [0.0, 100.0], "b": [0.0, 100.0]})
    assert core.relief_display(T, Tg).tolist() == [0.0, 0.5]


def test_raw_gauge_and_crisis_window():
    idx = pd.date_range("2020-01-01", periods=10)
    comp = pd.DataFrame({"R_a": np.arange(10.0), "R_b": np.ones(10)}, index=idx)
    g = core.raw_gauge(comp, ["a", "b"])
    assert g.tolist() == list(np.arange(10.0) + 1)
    m = core.crisis_window_max(g, crises=[("x", "2020-01-02", "")], window_days=3)
    assert m["x"] == 5.0                                            # 01-02~01-05 양 끝 포함


# ⑩ 하한
PHYS = "물리 충돌"


def test_floor_physical_rules():
    days = pd.date_range("2020-01-01", "2020-03-31")
    e = ev([("A3-1", "2020-01-05", "A3", PHYS, 3.0, "Trash balloon"), ("A3-2", "2020-01-05", "A3", PHYS, 3.2, "BALLOON"),
            ("A3-3", "2020-02-01", "A3", PHYS, 3.4, "Balloon launch"),
            ("A7-1", "2020-03-01", "A7", PHYS, 7.2, "포격")])
    fp = core.floor_physical(e, days, set(), kill_ids=())
    assert fp["2020-01-05"] == 3                                    # 풍선 같은 날 6.2 ≥ 6
    assert fp["2020-02-01"] == 1                                    # 풍선 1건 3.4
    assert (fp["2020-03-01":"2020-03-03"] == 4).all() and fp["2020-03-04"] == 3
    assert (fp["2020-03-04":"2020-03-14"] == 3).all() and fp["2020-03-15"] == 1


def test_floor_physical_type4_and_kill():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("A3-9", "2020-01-10", "A3", PHYS, 3.88, "침범"), ("A7-9", "2020-01-20", "A7", PHYS, 7.2, "침몰")])
    fp = core.floor_physical(e, days, {"A3-9", "A7-9"}, kill_ids=("A7-9",))
    assert fp["2020-01-10"] == 4 and fp["2020-01-11"] == 3        # 4거 유형일은 그날만 ≥ 4
    assert fp["2020-01-20"] == 5 and fp["2020-01-21"] == 4        # 사망·침몰일 5가 4거 유형보다 먼저
    assert core.type4_days(e, days, {"A3-9"}).sum() == 1


def test_floor_e5_and_event():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("E5-1", "2020-01-02", "E5", "북러 밀착", 4.0, "a"), ("E5-2", "2020-01-20", "E5", "북러 밀착", 10.0, "b"),
            ("A2-1", "2020-01-05", "A2", "핵·미사일", 7.5, "ICBM"), ("A2-2", "2020-01-06", "A2", "핵·미사일", 7.4999, "IRBM"),
            ("A1-1", "2020-01-07", "A1", "핵·미사일", 0.0, "핵실험")])
    fe = core.floor_e5(e, days)
    assert (fe["2020-01-02"], fe["2020-01-20"]) == (3, 4)
    fs = core.floor_event(e, days)
    assert (fs["2020-01-05"], fs["2020-01-06"], fs["2020-01-07"]) == (3, 1, 3)


def test_id_arguments_checked():
    days = pd.date_range("2020-01-01", "2020-01-31")
    e = ev([("A3-9", "2020-01-10", "A3", PHYS, 3.88, "침범")])
    with pytest.raises(TypeError):
        core.type4_days(e, days, "A3-9")
    with pytest.raises(TypeError):
        core.floor_physical(e, days, set(), kill_ids="A3-9")
    with pytest.raises(ValueError, match="A3-0"):
        core.type4_days(e, days, {"A3-0"})
    with pytest.raises(ValueError, match="사망"):
        core.floor_physical(e, days, set(), kill_ids=("A7-0",))


# 조립·멈춤 규칙 (F2-3)
B3 = config.BUNDLES_BASE
NOKILL = {"kill_ids": ()}


def test_daily_table_shape_and_purity():
    e = base_events()
    before = e.copy()
    days = core.calc_days("2010-01-01", "2020-12-31")
    d, info = core.daily_table(e, days, B3, set(), NOKILL)
    assert list(d.columns) == core.daily_columns(B3) and len(d.columns) == 20 and d.index.name == "날짜"
    assert all(d[c].dtype == "int64" for c in ["단계_T", "하한_물리", "하한_E5", "하한_사건", "단계_판정", "단계_최종"])
    assert d["잠정"].dtype == bool and d["물리_4거유형일"].dtype == bool
    assert e.equals(before)
    assert set(info) == {"B", "cuts", "quantiles_raw", "half_warning", "components", "params"}


@pytest.mark.parametrize("end", ["2019-12-30", "2015-06-30"])
def test_end_before_base_end_stops(end):
    with pytest.raises(ValueError, match="기준기간"):
        core.daily_table(base_events(), core.calc_days("2010-01-01", end), B3, set(), NOKILL)


def test_missing_relief_stops():
    e = base_events()
    with pytest.raises(ValueError, match="완화"):
        core.daily_table(e[e["묶음"] != "완화"], core.calc_days("2010-01-01", "2020-12-31"), B3, set(), NOKILL)


def test_first_cut_nonpositive_stops():
    with pytest.raises(ValueError, match="첫 문턱"):
        core.daily_table(base_events(2018, 2020), core.calc_days("2010-01-01", "2020-12-31"), B3, set(), NOKILL)


def test_params_none_empty_and_unknown():
    e, days = base_events(), core.calc_days("2010-01-01", "2020-12-31")
    d0, _ = core.daily_table(e, days, B3, set(), NOKILL)
    d1, _ = core.daily_table(e, days, B3, set(), {"kill_ids": (), "half_life": config.HALF_LIFE_DAYS})
    assert d0.equals(d1)
    d2, _ = core.daily_table(e, days, B3, set(), {"kill_ids": (), "half_life": 7})
    assert not d2["T_원값"].equals(d0["T_원값"])
    with pytest.raises(ValueError, match="halflife"):
        core.daily_table(e, days, B3, set(), {"halflife": 7})


def test_calc_days_end_none_is_today():
    assert core.calc_days("2026-01-01", None)[-1] == pd.Timestamp.today().normalize()
```

## 부록 E. `tests/test_regression.py` (글자 그대로 저장)
```python
"""v0.1.4 회귀(F3) — 로컬 사건표로 계산한 일별·요약이 tests/fixtures의 v0.1.4 기준과 같은지.

사건표(data/tension/events_*.csv)는 깃에 올리지 않으므로 없는 PC에서는 **실패**한다(사용자 10-29) — 실패 메시지에 만드는 법을 적는다.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import config
from utils.tension import core, io as tio

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
            f"  사건표는 깃에 올리지 않는다(D1). 원자료 {RAW_DIR.relative_to(ROOT).as_posix()}/ : {raw}\n"
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


@pytest.fixture(scope="module")
def summary():
    return tio.read_csv_kr(FIX / "v014_요약.csv", index_col=0)


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


def _summary_values(daily, info, days):
    """요약_v014.csv와 같은 이름의 값(F4 요약 함수가 생기기 전까지 테스트 안에서 계산)."""
    L = daily["단계_최종"]
    bm = core.base_mask(days)
    last = daily.iloc[-1]
    v = {"T구간(2·3·4·5거 시작)": "/".join(f"{x:g}" for x in info["cuts"]),
         "T구간_반올림전": "/".join(f"{x:.2f}" for x in info["quantiles_raw"]),
         "경계_x.5_주의": str(info["half_warning"]),
         **{f"B_{b}": round(float(x), 3) for b, x in info["B"].items()},
         **{f"{k}거%": round((L == k).mean() * 100, 1) for k in range(1, 6)},
         "바뀜/년": round((L.diff().fillna(0) != 0).sum() / (len(days) / 365.25), 1),
         "2018 평균단계": round(L.loc["2018"].mean(), 2), "2018 3거이상일": int((L.loc["2018"] >= 3).sum()),
         "2021 평균단계": round(L.loc["2021"].mean(), 2), "2023 4거이상%": round((L.loc["2023"] >= 4).mean() * 100, 0),
         "2023 5거%": round((L.loc["2023"] == 5).mean() * 100, 0), "현재(10-27)": int(L.iloc[-1]),
         "사건하한 날 수": int((daily["하한_사건"] == 3).sum()), "물리 4거유형 사건일 수": int(daily["물리_4거유형일"].sum()),
         "E5하한 3거↑ 날": int((daily["하한_E5"] >= 3).sum()),
         "E5가 판정을 올린 날": int((daily["하한_E5"] > daily[["단계_T", "하한_물리", "하한_사건"]].max(axis=1)).sum()),
         "물리하한 3거↑ 날": int((daily["하한_물리"] >= 3).sum()), "물리하한 4거↑ 날": int((daily["하한_물리"] >= 4).sum()),
         "물리하한 5거 날": int((daily["하한_물리"] == 5).sum()),
         "완화 상한에 붙은 날": int((info["components"]["delta"] >= config.RELIEF_CAP - 1e-12).sum()),
         "원점수 기준기간 평균": round(daily["원점수_게이지"][bm].mean(), 2),
         "T원값 최대": round(daily["T_원값"].max()), "표시선 최대": round(daily["T_표시7일"].max()),
         "현재 표시(잠정)": round(last["T_표시7일"], 1), "현재 그날까지 상위%": round(last["그날까지_상위%"], 1),
         "현재 원점수": round(last["원점수_게이지"], 1), "현재 14일 변화": round(last["변화14_표시"], 1),
         "현재 화면 단계": last["화면_단계문구"]}
    stages = core.crisis_window_max(L)
    marks = core.crisis_window_max(daily["원점수_게이지"])
    for name, _, _ in config.CRISIS_LIST:
        v[name] = int(stages[name])
        v[f"게이지_{name}"] = round(float(marks[name]), 1)
    return v


def _same(new, ref):
    return new == ref if isinstance(new, str) else float(new) == float(ref)


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


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_summary_matches_v014(computed, summary, name):
    r = computed["res"][name]
    got = _summary_values(r["daily"], r["info"], computed["days"])
    ref = summary[SCEN[name][0]]
    wrong = {k: (v, ref[k]) for k, v in got.items() if not _same(v, ref[k])}
    assert not wrong, f"요약 값이 다름(새 값, 기준): {wrong}"


@pytest.mark.parametrize("name", list(SCEN), ids=["base", "ext"])
def test_end_extension_keeps_past(computed, name):
    r, days = computed["res"][name], computed["days"]
    longer, _ = core.daily_table(r["events"], core.calc_days(config.CALC_START_DATE, "2026-11-10"), SCEN[name][1], computed["type4"])
    assert longer.loc[days].drop(columns="잠정").equals(r["daily"].drop(columns="잠정"))
    assert int((longer.loc[days, "잠정"] != r["daily"]["잠정"]).sum()) == config.PROVISIONAL_DAYS


def test_run_tension_output_matches_v014(computed):
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_tension.py"), "--end", END], cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
    for name in SCEN:
        out = ROOT / config.TENSION_DATA_DIR / "_check" / f"일별_{name}.csv"
        raw = out.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
        got = tio.read_csv_kr(out, index_col=0, parse_dates=True)
        assert list(got.columns) == list(_ref_daily(name).columns)
        assert not _diff_cells(got, _ref_daily(name), tol=0.001 + 1e-9)
```

## 부록 F. `.git/hooks/commit-msg` (글자 그대로 저장 — 리포에 커밋하지 않음)
```sh
#!/bin/sh
# 사용자 10-29: GitHub에 AI 생성 표기를 넣지 않는다 — 커밋 메시지에서 해당 줄을 지운다(F3에서 설치, 리포에 커밋하지 않음)
sed -i -E \
  -e '/^[Cc]o-[Aa]uthored-[Bb]y:.*([Cc]laude|anthropic\.com)/d' \
  -e '/[Gg]enerated with \[?[Cc]laude/d' \
  -e '/claude\.(ai|com)\/(code|claude-code)/d' \
  -e '/^Claude-Session:/d' \
  -e '/🤖/d' \
  "$1"
```

## 부록 G. `$B/add_no_ai_rule.py` (글자 그대로 저장)
```python
"""F3 1-5 — CLAUDE.md 6절 커밋 말머리 줄 다음에 AI 표기 금지 규칙 한 줄을 넣는다(사용자 10-29). 바이트로 넣어 줄바꿈을 그대로 둔다."""
from pathlib import Path

p = Path("CLAUDE.md")
b = p.read_bytes()
nl = b"\r\n" if b"\r\n" in b else b"\n"
anchor = "- 커밋 말머리(팀 README): `feat` `fix` `docs` `refactor` `style` `test` `chore` + `: ` + 한국어 요약 50자 이내. 한 커밋 한 목적.".encode("utf-8") + nl
add = ("- **AI 표기 금지(10-29 사용자, 절대):** 커밋 메시지·PR·이슈·코멘트 어디에도 `Co-Authored-By: Claude…`·`Generated with Claude Code`·`🤖`·claude.ai 세션 링크를 넣지 않는다. 로컬 `commit-msg` 훅이 커밋에서 지우고, 푸시·PR 전 검사로 다시 확인한다."
       .encode("utf-8") + nl)
assert b.count(anchor) == 1, f"기준 줄이 {b.count(anchor)}번 — 멈춤"
assert add not in b, "이미 들어 있음 — 멈춤"
p.write_bytes(b.replace(anchor, anchor + add))
print("CLAUDE.md: 6절에 AI 표기 금지 규칙 1줄 넣음")
```

## 부록 H. `$B/clean_pr_body.py` (글자 그대로 저장)
```python
"""F3 1-6 — PR 본문 파일에서 AI 생성 표기 줄을 지운다(사용자 10-29). 사용: python clean_pr_body.py <입력> <출력>"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
pat = re.compile(r"(🤖|generated with \[?claude|co-authored-by:.*(claude|anthropic\.com)|claude\.(ai|com)/(code|claude-code)|^claude-session:)", re.I)
lines = open(src, encoding="utf-8").read().splitlines()
kept = [ln for ln in lines if not pat.search(ln)]
while kept and not kept[-1].strip():
    kept.pop()
open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(kept) + "\n")
print(f"지운 줄 {len(lines) - len(kept)}개(끝 빈 줄 포함) → {dst}")
```
