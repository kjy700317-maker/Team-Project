# F2-3 작업 프롬프트 — F2 검토 반영: 자료 이상 멈춤 · daily_table params · run_tension 입력 검사

작성 2026-10-29 · 구현 메인(채팅 ③) → Claude Code · 브랜치 `feature/tension-core`(이어서 — 새 브랜치 없음) · PR [#19](https://github.com/kjy700317-maker/Team-Project/pull/19)(draft) · 이슈 #18
상태: **실행** (2026-10-29 사용자 결정 — F2-3 수정 후 병합 · 자료 이상은 멈춤 · 이른 END 막음 · daily_table 파라미터 인자 추가)
권장 모델·노력: **Opus 5.5 · 중간**(변경은 부록 C 패치 그대로 적용 + 검산 — 설계 판단 없음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. 테스트는 `<py> -m pytest`. **`$B`** = `$HOME/bongsu_F2-3_20261029`.
> **끝낼 때(사용자 10-29, CLAUDE.md 7절):** 세션 마지막 채팅 답은 **한국어로** 결과 요약 — 결과 · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것.
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `rm`(지울 일이 있으면 `$B`로 `mv`), `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**`·`config.py`·`io.py`·`build_events.py`·`tests/**` 수정, **부록 C 밖의 코드 변경**.

---

## 0. 목표
- F2 검토(`docs/dev/reports/F2_review.md`)의 발견 중 사용자가 "고친 뒤 병합"으로 정한 것을 반영한다(10-29). 변경은 **부록 C 패치 그대로** — 구현 메인이 리포 밖 간이 구현에서 만들고 두 검산을 통과시킨 것이다 `[확인 10-29: python 3.10 · pandas 2.3.3]`.
- **지금 데이터의 결과는 바뀌지 않는다**: F2-2 검산(v0.1.4 대조)이 그대로 `전체: 통과`, 일별 CSV 바이트도 같아야 한다.
- 무엇이 바뀌나(자세히는 부록 A):
  1. **자료 이상 → 멈춤(ValueError):** 계산 기간이 기준기간 2010-01-01~2019-12-31을 다 담지 않음(이른 END·늦은 시작) · 평소값 B ≤ 0 또는 없음(기준기간 사건 0건, 완화 포함) · 첫 문턱 θ₁ ≤ 0 · 판정표 4거 유형·사망 사건ID가 사건표에 없음. ID 인자에 문자열 하나를 넘기면 TypeError (검토 발견 1·2·4·8)
  2. **`daily_table(…, params=None)`**: `PARAM_KEYS` 20개 중 바꿀 것만 dict로 넘김, 모르는 키는 ValueError, `info["params"]`. 이를 위해 `floor_physical`·`floor_e5`에 `sigma`·`window` 키워드 인자를 맨 뒤에 더함 (발견 3 — 사용자: 인자 통과 추가)
  3. docstring: ⑦ "S에 φ가 이미 곱해져 있음", `daily_table` "config는 import 때 묶임 — 바꾼 계산은 params로" (발견 3·12)
  4. **`run_tension.py`**: `--end` 형식 검사(YYYY-MM-DD 실제 날짜, 아니면 argparse 오류 rc 2) · 사건표 없음·판정표 대조(`io.check_type4_against_events`)·판정표 Y 0건·core의 ValueError를 `멈춤: …` 한 줄(stderr, rc 1)로 · 두 시나리오를 다 계산한 뒤에만 파일을 씀 · 출력 스트림 `errors="replace"`(cp949 콘솔) (발견 4·6·9)
- 공개 함수 수는 그대로 31개(새 함수는 밑줄 내부 함수 `_require_full_base`·`_require_ids`·`_pick`과 상수 `PARAM_KEYS`).
- 하지 않는 것: 발견 5·7·13(구현 메인이 `docs/tension/산출식_정리.md` 1A를 고침 — 이 브랜치 첫 커밋에 들어감), 10(F7), 11(F5), 테스트 추가(F3 — 검토 3절 제안은 F3 프롬프트로).

## 1. 시작 점검 · 문서 커밋 · develop 맞추기 (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F2-3_20261029"; mkdir -p "$B"
git status --porcelain
#   기대(순서 무관 · 한글 경로가 "\354…"처럼 보여도 같은 것):
#   " M docs/dev/진행기록.md", " M docs/tension/산출식_정리.md", "?? docs/dev/tasks/F2-3_fix.md", "?? .obsidian/"
git branch --show-current                    # 기대: feature/tension-core
git fetch origin
git status -sb | head -1                     # 기대: "## feature/tension-core...origin/feature/tension-core" (ahead/behind 없음)
git log --oneline -1                         # 기대: "… docs: F2 검토 보고서"
gh pr view 19 --json state,isDraft           # 기대: OPEN · true
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest        # 기대: 14 passed
```
**1-2 커밋 1** — 구현 메인 문서(내용 수정 없이 — U2):
```bash
git add docs/dev/tasks/F2-3_fix.md docs/dev/진행기록.md docs/tension/산출식_정리.md
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
git commit -m "docs: F2-3 작업 프롬프트·설계 문서 반영"
```
**1-3 develop 맞추기**
```bash
git rev-list --left-right --count HEAD...origin/develop   # 오른쪽 = develop에만 있는 커밋 수(log에 적음)
# 오른쪽이 0이면 건너뛴다. 0보다 크면:
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest   # 기대: 14 passed
```

## 2. 패치 적용
부록 C를 `$B/F2-3.diff`로 **글자 그대로** 저장(앞 공백·빈 줄 포함)하고 리포 루트에서:
```bash
git apply --check "$B/F2-3.diff" && git apply "$B/F2-3.diff"
#   --check가 실패하면 `git apply --check --ignore-whitespace`로 한 번 더. 그래도 실패하면 손으로 고치지 말고 멈추고 보고
git diff --stat      # 기대: utils/tension/core.py · scripts/run_tension.py 두 파일만
```

## 3. 확인 명령
```bash
# 3-1 공개 함수 — 기대: 31개, 첫 줄 식 번호 또는 (보조)
PYTHONIOENCODING=utf-8 <py> -c "import inspect, utils.tension.core as c; fs=[(n,f) for n,f in inspect.getmembers(c, inspect.isfunction) if f.__module__==c.__name__ and not n.startswith('_')]; [print(n, '|', (f.__doc__ or '').splitlines()[0]) for n,f in fs]; print(len(fs))"
# 3-2 금지 사용 — 두 줄 모두 출력 없음
grep -nE '^[^#]*(streamlit|scipy|lfilter|\.ewm\(|\.rank\(|read_csv|to_csv|open\(|Path\()' utils/tension/core.py
grep -nE '^[[:space:]]*(import|from)[[:space:]]+(s3_core|compute_v01|lib5|streamlit|scipy)' utils/tension/core.py scripts/run_tension.py
# 3-3 테스트 — 기대: 14 passed
PYTHONIOENCODING=utf-8 <py> -m pytest
# 3-4 도움말 — 기대: --end 하나
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --help
```

## 4. 검산 (둘 다 리포 루트에서)
```bash
# 4-1 값이 그대로인지 — F2-2 검산(v0.1.4 대조). "$HOME/bongsu_F2-2_20261029/verify_core_2cd.py"가 있으면 그것을,
#     없으면 docs/dev/tasks/F2-2_core.md 부록 B를 "$B/verify_core_2cd.py"로 글자 그대로 저장해 쓴다
PYTHONIOENCODING=utf-8 <py> "<그 파일>"          # 기대: 전체: 통과 · 바이트까지 같음 True(참고)
# 4-2 이번 변경 — 부록 B를 "$B/verify_F2-3.py"로 글자 그대로 저장
PYTHONIOENCODING=utf-8 <py> "$B/verify_F2-3.py"  # 기대: 전체: 통과
```
- 4-2는 `scripts/run_tension.py`를 여러 번 실행한다(멈추는 경우 + 정상 1번). 정상 실행이 `data/tension/_check/`를 다시 쓴다(깃 제외).
- 맞지 않으면 패치를 고치지 말고, 실패한 줄과 출력 전부를 log에 남기고 멈추고 보고한다(pandas 3.0에서만 다른 것으로 보이면 그렇게 적는다).

## 5. 완료 조건
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 기대 상태, 14 passed |
| 2 | 1-2·1-3 | 금지 경로 `OK`, merge 했거나 건너뜀 |
| 3 | 2절 패치 | 적용됨, 바뀐 파일 두 개 |
| 4 | 3-1·3-2 | 공개 31개 · grep 출력 없음 |
| 5 | 3-3·3-4 | 14 passed · `--end`만 |
| 6 | 4-1 | `전체: 통과`(값 그대로) |
| 7 | 4-2 | `전체: 통과` |
| 8 | 커밋 목록 `git log --oneline origin/develop..HEAD` | 이전 커밋 + 6절 순서 |
| 9 | 매 커밋 전 금지 경로 검사 | 매번 `OK` |
| 10 | 마지막 `git status --porcelain` | `?? .obsidian/` 하나만 |

## 6. 커밋 (이 순서)
1. `docs: F2-3 작업 프롬프트·설계 문서 반영`(1-2)
2. (1-3에서 merge 했으면 merge 커밋)
3. `fix: 계산 코어 자료 이상 멈춤·daily_table params` — `utils/tension/core.py`
4. `fix: run_tension 입력 검사·메시지` — `scripts/run_tension.py`
5. `docs: F2-3 보고서` — `docs/dev/reports/F2-3_report.md`, `F2-3_log.md`
- 3·4는 4절 검산이 모두 통과한 뒤 파일별로 `git add` → 금지 경로 검사 → 커밋.

## 7. 푸시 · PR
```bash
git fetch origin
git merge origin/develop          # 1-3 뒤 develop이 또 바뀌었을 때만. 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest
git push
gh pr view 19 --json body -q .body > "$B/pr_F2_old.md"
# "$B/pr_F2.md" = 지금 본문 + 요약 첫 줄을 "F2-1·F2-2·F2-3(검토 반영)까지 — 구현 메인 확인 뒤 ready·팀 리뷰·병합"으로,
#   변경 사항에 6절 3·4(부록 A 1~4 한 줄씩), 테스트에 4절 결과 한 줄씩을 더함
gh pr edit 19 --body-file "$B/pr_F2.md"
gh pr view 19 --json state,isDraft    # 기대: OPEN · true
```
병합·ready 전환하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 8. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F2-3_report.md`(60줄 이내): 1절 = 5절 표 10행 ✓/✗ · 4-1·4-2 결과 요약(값 그대로·바이트 같음 · 멈춤 경우 수 · params 키 20개 연결) · 2절 막힌 것 · 3절 프롬프트와 다르게 한 것 · 4절 바뀐 파일.
`docs/dev/reports/F2-3_log.md`: 1절 점검 출력, 2절 패치 적용 출력, 3·4절 출력 전부, 커밋·푸시·PR 출력.

---

## 부록 A. 패치 내용 요약 (부록 C를 읽는 길잡이 — 실제 변경은 부록 C)
| 위치 | 변경 | 검토 발견 |
|---|---|---|
| `core._require_full_base(days, base_period)` 새 내부 함수 | 계산 기간이 `base_period` 첫날~끝날을 다 담지 않으면 ValueError("…끝날짜는 2019-12-31 이후로") | 2 |
| `core._require_ids(events, ids, what)` 새 내부 함수 | `ids`가 str이면 TypeError, 사건표에 없는 ID가 있으면 ValueError — `type4_days`(4거 유형)·`floor_physical`(사망·침몰)에서 씀 | 4 |
| `core.relief_discount` docstring | 둘째 단락: S에 φ(ADR-015)가 이미 곱해져 있음 | 12 |
| `core.tension_components` | 처음에 `_require_full_base`, B 계산 뒤 `not B > 0`인 묶음이 있으면 ValueError(묶음 이름) | 1 |
| `core.floor_physical`·`floor_e5` | 키워드 인자 `sigma`·`window`(기본 config)를 맨 뒤에 더해 `half_gauss_window`에 넘김 | 3 |
| `core.PARAM_KEYS`·`_pick`·`daily_table(…, params=None)` | params 키 20개 → 각 함수 인자로, 모르는 키 ValueError, θ₁ ≤ 0이면 ValueError, `info["params"]` | 1·3·8 |
| `scripts/run_tension.py` | `_end_date`(argparse type) · `_run(end)`(판정표 Y 0건·사건표 없음·판정표 대조 → 멈춤, 두 시나리오 다 계산 뒤 쓰기) · `main`(스트림 `errors="replace"`, ValueError·TypeError·FileNotFoundError → `멈춤: …` rc 1) · 출력 문구 `—` → `-` | 4·6·9 |

## 부록 B. `$B/verify_F2-3.py` (글자 그대로 저장)
```python
"""F2-3 검산 — 리포 루트에서 실행. 자료 이상 검사(멈춤)·daily_table params·run_tension 입력 검사를 확인한다.
v0.1.4 대조(값이 그대로인지)는 F2-2 부록 B(verify_core_2cd.py)로 따로 돌린다."""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
import config
from utils.tension import core, io as tio

END = "2026-10-27"
ok = True
table = tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH)
type4 = tio.type4_event_ids(table)
ev, _ = tio.load_events(ROOT / "data" / "tension" / "events_기본.csv")
days = core.calc_days(config.CALC_START_DATE, END)
B3 = config.BUNDLES_BASE
print("python", sys.version.split()[0], "· numpy", np.__version__, "· pandas", pd.__version__)


def check(label, cond):
    global ok
    ok &= bool(cond)
    print(f"  {label} {'✓' if cond else '✗'}")


def raises(label, exc, fn, must_contain):
    try:
        fn()
    except exc as e:
        msg = str(e)
        check(f"{label} → {exc.__name__}: {msg[:110]}", must_contain in msg)
        return
    except Exception as e:  # noqa: BLE001
        check(f"{label} → 다른 예외 {type(e).__name__}: {e}", False)
        return
    check(f"{label} → 예외 없음", False)


print("\n[1] 자료 이상 → 멈춤")
raises("END 2019-12-30", ValueError, lambda: core.daily_table(ev, core.calc_days(config.CALC_START_DATE, "2019-12-30"), B3, type4), "기준기간")
d_ok, _ = core.daily_table(ev, core.calc_days(config.CALC_START_DATE, "2019-12-31"), B3, type4)
check(f"END 2019-12-31 → 계산됨({len(d_ok)}일)", len(d_ok) == 3652)
raises("시작 2010-01-02", ValueError, lambda: core.daily_table(ev, core.calc_days("2010-01-02", END), B3, type4), "기준기간")
raises("tension_components도 END 2019-12-30", ValueError, lambda: core.tension_components(ev, core.calc_days(config.CALC_START_DATE, "2019-12-30"), B3), "기준기간")
raises("완화 행 없음", ValueError, lambda: core.daily_table(ev[ev["묶음"] != "완화"], days, B3, type4), "완화")
no_nm = ev[~((ev["묶음"] == "핵·미사일") & (ev["date"] <= "2019-12-31"))]
raises("핵·미사일 기준기간 0건", ValueError, lambda: core.daily_table(no_nm, days, B3, type4), "핵·미사일")
raises("사건 0행", ValueError, lambda: core.daily_table(ev.iloc[0:0], days, B3, set()), "평소값")
late = ev[ev["date"] >= "2018-01-01"]
late_t4 = set(type4) & set(late["사건ID"])
raises("2018년부터만 사건(θ₁ = 0)", ValueError, lambda: core.daily_table(late, days, B3, late_t4), "첫 문턱")
no_kill = ev[ev["사건ID"] != "A7-0100"]
raises("사망 사건 A7-0100 없음(판정표 Y 검사와 따로)", ValueError, lambda: core.floor_physical(no_kill, days, set(type4) - {"A7-0100"}), "사망·침몰")
one = sorted(type4)[0]
raises(f"판정표 Y 사건 {one} 없음", ValueError, lambda: core.daily_table(ev[ev["사건ID"] != one], days, B3, type4), one)
raises("type4_ids가 문자열", TypeError, lambda: core.type4_days(ev, days, one), "문자열")
raises("kill_ids가 문자열", TypeError, lambda: core.floor_physical(ev, days, type4, kill_ids="A7-0098"), "문자열")
d_e, _ = core.daily_table(ev, days, B3, set())
check(f"type4_ids 빈 집합은 core에서 허용(4거 유형일 {int(d_e['물리_4거유형일'].sum())}일) — 멈춤은 run_tension", int(d_e["물리_4거유형일"].sum()) == 0)

print("\n[2] daily_table params")
d0, i0 = core.daily_table(ev, days, B3, type4)
d_none, _ = core.daily_table(ev, days, B3, type4, None)
d_empty, _ = core.daily_table(ev, days, B3, type4, {})
defaults = {"base_period": config.BASE_PERIOD, "half_life": config.HALF_LIFE_DAYS, "relief_c": config.RELIEF_C,
            "relief_cap": config.RELIEF_CAP, "quantiles": config.STAGE_QUANTILES, "sigma": config.HALF_GAUSS_SIGMA,
            "window": config.FLOOR_WINDOW, "phys_thresholds": config.PHYS_FLOOR, "type4_stage": config.TYPE4_FLOOR_STAGE,
            "kill_ids": config.KILL_EVENTS, "kill_stage": config.KILL_FLOOR_STAGE, "e5_thresholds": config.E5_FLOOR,
            "icbm_s": config.EVENT_FLOOR_ICBM_S, "event_stage": config.EVENT_FLOOR_STAGE, "step_days": config.STEP_DOWN_DAYS,
            "ma_days": config.DISPLAY_MA_DAYS, "provisional_days": config.PROVISIONAL_DAYS, "trend_days": config.TREND_DAYS,
            "trend_pct_min": config.TREND_PCT_MIN, "a2_end": config.A2_DATA_END}
check(f"PARAM_KEYS {len(core.PARAM_KEYS)}개 = 이 검산의 키와 같음", set(core.PARAM_KEYS) == set(defaults))
d_def, i_def = core.daily_table(ev, days, B3, type4, defaults)
check("params None · {} · config 값 그대로 → 기본 결과와 같음", d0.equals(d_none) and d0.equals(d_empty) and d0.equals(d_def))
check("info['params']에 넘긴 값", i0["params"] == {} and i_def["params"] == defaults)
raises("모르는 키", ValueError, lambda: core.daily_table(ev, days, B3, type4, {"halflife": 7}), "halflife")
alt = {"base_period": ((2011, 2019), ["T_원값"]), "half_life": (7, ["T_원값"]), "relief_c": (0.2, ["T_원값"]),
       "relief_cap": (0.3, ["T_원값"]), "quantiles": ((0.6, 0.9, 0.95, 0.98), ["단계_T"]), "sigma": (5, ["하한_물리", "하한_E5"]),
       "window": (10, ["하한_물리", "하한_E5"]), "phys_thresholds": ({"3거": 2, "4거": 7, "풍선3거": 6}, ["하한_물리"]),
       "type4_stage": (3, ["하한_물리"]), "kill_ids": (("A7-0098",), ["하한_물리"]), "kill_stage": (4, ["하한_물리"]),
       "e5_thresholds": ({"3거": 5, "4거": 10}, ["하한_E5"]), "icbm_s": (8.0, ["하한_사건"]), "event_stage": (2, ["하한_사건"]),
       "step_days": (3, ["단계_최종"]), "ma_days": (3, ["T_표시7일"]), "provisional_days": (3, ["잠정"]),
       "trend_days": (7, ["변화14_표시"]), "trend_pct_min": (100, ["변화율14_표시"]), "a2_end": ("2024-12-31", ["A2자료"])}
for key, (val, cols) in alt.items():
    d1, _ = core.daily_table(ev, days, B3, type4, {key: val})
    changed = [c for c in cols if not d1[c].equals(d0[c])]
    check(f"{key}={val!r} → 바뀐 열 {changed} (기대 {cols} 중 하나 이상) · 열 이름·순서 그대로", bool(changed) and list(d1.columns) == list(d0.columns))
comp2, _ = core.tension_components(ev, days, B3, relief_c=0.2)
d2, _ = core.daily_table(ev, days, B3, type4, {"relief_c": 0.2})
check("params relief_c=0.2의 T = tension_components(relief_c=0.2)의 T", d2["T_원값"].equals(comp2["T"]))
fp2 = core.floor_physical(ev, days, type4, sigma=5, window=10)
d3, _ = core.daily_table(ev, days, B3, type4, {"sigma": 5, "window": 10})
check("params sigma·window = floor_physical(sigma=5, window=10)", d3["하한_물리"].equals(fp2))

print("\n[3] run_tension.py 입력 검사")
outs = [ROOT / config.TENSION_DATA_DIR / "_check" / f"일별_{n}.csv" for n in ("기본", "확장")]
before = [o.stat().st_mtime_ns if o.exists() else None for o in outs]


def run(args, env_extra=None):
    env = dict(os.environ, **(env_extra or {}))
    r = subprocess.run([sys.executable, "scripts/run_tension.py", *args], capture_output=True, env=env)
    return r.returncode, r.stdout.decode(env.get("PYTHONIOENCODING", "utf-8"), "replace"), r.stderr.decode(env.get("PYTHONIOENCODING", "utf-8"), "replace")


for args, rc_want, word in [(["--end", "2019-12-30"], 1, "기준기간"), (["--end", "2026-13-01"], 2, "없는 날짜"),
                            (["--end", "abc"], 2, "형식"), (["--end", "20261027"], 2, "형식"), (["--end", "2026-10-27 13:00"], 2, "형식")]:
    rc, out, err = run(args)
    line = (err.strip().splitlines() or [""])[-1]
    check(f"{' '.join(args)} → rc {rc} (기대 {rc_want}) · {line[:90]}", rc == rc_want and word in err and "Traceback" not in err)
rc, out, err = run(["--end", "2019-12-30"], {"PYTHONIOENCODING": "cp949"})
check(f"cp949 출력에서 멈춤 메시지 → rc {rc} · UnicodeEncodeError 없음", rc == 1 and "UnicodeEncodeError" not in err and "Traceback" not in err)
after = [o.stat().st_mtime_ns if o.exists() else None for o in outs]
check("멈춘 실행은 _check 파일을 쓰지 않음(수정 시각 그대로)", before == after)
spec = importlib.util.spec_from_file_location("run_tension", ROOT / "scripts" / "run_tension.py")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
saved = config.TENSION_DATA_DIR
config.TENSION_DATA_DIR = "data/_없는폴더_F2-3"
try:
    rc = rt.main(["--end", END])
finally:
    config.TENSION_DATA_DIR = saved
check(f"사건표 없음 → main() 반환 {rc} (기대 1, 메시지 '사건표 없음'은 위 stderr)", rc == 1)
rc, out, err = run(["--end", END])
check(f"정상 --end {END} → rc {rc}", rc == 0 and "Traceback" not in err)

print("\n전체:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
```

## 부록 C. `$B/F2-3.diff` (글자 그대로 저장 — 앞 공백·빈 줄 포함)
```diff
--- a/utils/tension/core.py
+++ b/utils/tension/core.py
@@ -26,6 +26,26 @@
     return (days.year >= a) & (days.year <= b)
 
 
+def _require_full_base(days, base_period) -> None:
+    """(보조) 계산 기간이 기준기간 전체를 담는지 — 아니면 ValueError(사용자 10-29: 이른 END는 막는다)."""
+    a, b = base_period
+    first, last = pd.Timestamp(f"{a}-01-01"), pd.Timestamp(f"{b}-12-31")
+    if len(days) == 0 or days[0] > first or days[-1] < last:
+        span = f"{days[0]:%Y-%m-%d}~{days[-1]:%Y-%m-%d}" if len(days) else "빈 기간"
+        raise ValueError(f"계산 기간 {span}이 기준기간 {first:%Y-%m-%d}~{last:%Y-%m-%d}을 다 담지 않음 - 끝날짜는 {last:%Y-%m-%d} 이후로")
+
+
+def _require_ids(events, ids, what) -> list:
+    """(보조) ids가 사건ID 모음이고 모두 사건표에 있는지 — 아니면 TypeError·ValueError(사용자 10-29: 자료 이상은 멈춤)."""
+    if isinstance(ids, str):
+        raise TypeError(f"{what}: 문자열 하나가 아니라 사건ID 모음(set·tuple·list)으로 넘긴다")
+    ids = list(ids)
+    missing = sorted(set(ids) - set(events["사건ID"]))
+    if missing:
+        raise ValueError(f"{what}: 사건표에 없는 사건ID {missing[:10]}")
+    return ids
+
+
 def _day_sum(rows, days) -> pd.Series:
     """(보조) 행들의 그날 S 합, 사건 없는 날 0 — 기간 밖 날짜는 버린다(s3_core.load)."""
     return rows.groupby("date")["S"].sum().reindex(days, fill_value=0.0)
@@ -65,7 +85,10 @@
 
 
 def relief_discount(R_relief, B_relief, c=config.RELIEF_C, cap=config.RELIEF_CAP) -> pd.Series:
-    """⑦ 완화 할인 — δ = min(c · R완 / B완, κ)."""
+    """⑦ 완화 할인 — δ = min(c · R완 / B완, κ).
+
+    완화 사건의 S에는 분야 보정 φ(ADR-015)가 사건표를 만들 때 이미 곱해져 있다(build_events) — core는 φ를 모른다.
+    """
     return pd.Series(np.minimum(c * R_relief / B_relief, cap), index=R_relief.index)
 
 
@@ -84,9 +107,13 @@
     """
     bundles = list(bundles)
     targets = bundles + [relief_bundle]
+    _require_full_base(days, base_period)
     D = daily_sums(events, days, targets)
     R = pd.DataFrame({b: decay_cumulative(D[b], half_life) for b in targets}, index=days)
     B = baseline_means(R, base_mask(days, base_period))
+    bad = [b for b in targets if not B[b] > 0]
+    if bad:
+        raise ValueError(f"기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): {bad}")
     Tg = relative_index(R[bundles], B[bundles])
     T_plus = rising_index(Tg)
     delta = relief_discount(R[relief_bundle], B[relief_bundle], relief_c, relief_cap)
@@ -107,33 +134,36 @@
 def type4_days(events, days, type4_ids) -> pd.Series:
     """⑩ 물리 4거 유형 사건일 — 판정표 Y 사건의 사건표 날짜면 True."""
     # 날짜는 사건표에서 가져온다(판정표 date 아님 — 대응표 ⑩-b)
-    t4 = events.loc[events["사건ID"].isin(list(type4_ids)), "date"].unique()
+    ids = _require_ids(events, type4_ids, "4거 유형 사건(판정표 Y)")
+    t4 = events.loc[events["사건ID"].isin(ids), "date"].unique()
     return pd.Series(days.isin(t4), index=days)
 
 
 def floor_physical(events, days, type4_ids, kill_ids=config.KILL_EVENTS, thresholds=config.PHYS_FLOOR,
                    type4_stage=config.TYPE4_FLOOR_STAGE, kill_stage=config.KILL_FLOOR_STAGE,
-                   bundle=config.BUNDLE_PHYS) -> pd.Series:
+                   bundle=config.BUNDLE_PHYS, sigma=config.HALF_GAUSS_SIGMA, window=config.FLOOR_WINDOW) -> pd.Series:
     """⑩ 물리 하한 F^물 — 풍선 뺀 A3·A7 ρ≥3→3·≥7→4, 풍선 ρ≥6→3, 4거 유형일 ≥4, 사망·침몰일 5.
 
     순서 그대로(s3_core.floors_s1 + compute_v014.floors_v014): ① 반가우스 판정 → ② 4거 유형일 max → ③ 사망·침몰일 덮어씀.
     """
     ph = events[events["묶음"] == bundle]
     balloon = ph["요소"].eq("A3") & ph["사건명"].astype(str).str.contains(BALLOON_KEYWORD, case=False, na=False)
-    rho_o = half_gauss_window(_day_sum(ph[~balloon], days)).to_numpy()
-    rho_b = half_gauss_window(_day_sum(ph[balloon], days)).to_numpy()
+    rho_o = half_gauss_window(_day_sum(ph[~balloon], days), sigma, window).to_numpy()
+    rho_b = half_gauss_window(_day_sum(ph[balloon], days), sigma, window).to_numpy()
     th = thresholds
     fp = np.select([rho_o >= th["4거"], rho_o >= th["3거"], rho_b >= th["풍선3거"]], [4, 3, 3], 1)
     t4 = type4_days(events, days, type4_ids).to_numpy()
     fp[t4] = np.maximum(fp[t4], type4_stage)
-    kill = events.loc[events["사건ID"].isin(list(kill_ids)), "date"]
+    kill_ids = _require_ids(events, kill_ids, "사망·침몰 사건(KILL_EVENTS)")
+    kill = events.loc[events["사건ID"].isin(kill_ids), "date"]
     fp[days.isin(kill)] = kill_stage
     return pd.Series(fp.astype("int64"), index=days)
 
 
-def floor_e5(events, days, thresholds=config.E5_FLOOR, bundle=config.BUNDLE_E5) -> pd.Series:
+def floor_e5(events, days, thresholds=config.E5_FLOOR, bundle=config.BUNDLE_E5, sigma=config.HALF_GAUSS_SIGMA,
+             window=config.FLOOR_WINDOW) -> pd.Series:
     """⑩ E5 하한 F^E5 — 북러 밀착 ρ≥4→3, ≥10→4."""
-    rho = half_gauss_window(_day_sum(events[events["묶음"] == bundle], days)).to_numpy()
+    rho = half_gauss_window(_day_sum(events[events["묶음"] == bundle], days), sigma, window).to_numpy()
     th = thresholds
     fe = np.select([rho >= th["4거"], rho >= th["3거"]], [4, 3], 1)
     return pd.Series(fe.astype("int64"), index=days)
@@ -257,33 +287,58 @@
     return [*DAILY_HEAD, *[f"Tg_{b}" for b in bundles], *DAILY_TAIL]
 
 
-def daily_table(events, days, bundles, type4_ids) -> tuple[pd.DataFrame, dict]:
+# daily_table params 키 — 값을 바꾼 계산(민감도·비교선)은 config를 고치지 말고 이 키로 넘긴다(사용자 10-29)
+PARAM_KEYS = ("base_period", "half_life", "relief_c", "relief_cap", "quantiles", "sigma", "window",
+              "phys_thresholds", "type4_stage", "kill_ids", "kill_stage", "e5_thresholds", "icbm_s", "event_stage",
+              "step_days", "ma_days", "provisional_days", "trend_days", "trend_pct_min", "a2_end")
+
+
+def _pick(params, **argmap) -> dict:
+    """(보조) params에서 이 함수 인자에 해당하는 키만 골라 {인자: 값}."""
+    return {arg: params[key] for arg, key in argmap.items() if key in params}
+
+
+def daily_table(events, days, bundles, type4_ids, params=None) -> tuple[pd.DataFrame, dict]:
     """②~⑰ 일별 결과 — 사건표에서 일별 CSV의 모든 열(반올림 전)과 계산 정보를 한 번에.
 
-    파라미터는 각 함수의 config 기본값. 반올림하지 않는다(쓸 때 round(3)).
-    info = {"B": 평소값, "cuts": 문턱, "quantiles_raw": 반올림 전 분위, "half_warning": x.5 경고, "components": comp}.
+    params = PARAM_KEYS 중 바꿀 것만 담은 dict. 없는 키는 각 함수의 기본값(config). config 값은 import 때
+    함수 기본값으로 묶이므로 실행 중 config를 바꿔도 반영되지 않는다 — 바꾼 계산은 params로 넘긴다.
+    열 이름은 고정(trend_days를 바꿔도 `변화14_표시` 그대로). 반올림하지 않는다(쓸 때 round(3)).
+    기준기간이 다 들어 있지 않거나, 평소값 B ≤ 0, 첫 문턱 θ₁ ≤ 0, 판정표·사망 사건ID가 사건표에 없으면 멈춘다(ValueError).
+    info = {"B", "cuts", "quantiles_raw", "half_warning", "components", "params"(넘긴 params)}.
     """
+    p = dict(params or {})
+    unknown = sorted(set(p) - set(PARAM_KEYS))
+    if unknown:
+        raise ValueError(f"params에 모르는 키 {unknown} — 쓸 수 있는 키: {list(PARAM_KEYS)}")
     bundles = list(bundles)
-    comp, B = tension_components(events, days, bundles)
+    comp, B = tension_components(events, days, bundles, **_pick(p, base_period="base_period", half_life="half_life",
+                                                                 relief_c="relief_c", relief_cap="relief_cap"))
     T = comp["T"]
     Tg = comp[[f"Tg_{b}" for b in bundles]]
     # T는 한 번만 계산 — 구간과 무관(대응표 ⑨)
-    cuts, q = stage_cuts(T, base_mask(days))
+    cuts, q = stage_cuts(T, base_mask(days, **_pick(p, base_period="base_period")), **_pick(p, quantiles="quantiles"))
+    if not cuts[0] > 0:
+        raise ValueError(f"T 구간 첫 문턱(2거 시작)이 {cuts[0]:g} - 0 이하(기준기간 T가 대부분 0, 자료 부족)")
     LT = stage_from_index(T, cuts)
-    fp = floor_physical(events, days, type4_ids)
-    fe = floor_e5(events, days)
-    fs = floor_event(events, days)
+    gauss = _pick(p, sigma="sigma", window="window")
+    fp = floor_physical(events, days, type4_ids, **_pick(p, kill_ids="kill_ids", thresholds="phys_thresholds",
+                                                         type4_stage="type4_stage", kill_stage="kill_stage"), **gauss)
+    fe = floor_e5(events, days, **_pick(p, thresholds="e5_thresholds"), **gauss)
+    fs = floor_event(events, days, **_pick(p, icbm_s="icbm_s", stage="event_stage"))
     J = judge(LT, fp, fe, fs)
-    L = step_down(J)
-    T_bar = display_ma(T)
-    tr = trend(T_bar)
-    cols = {"T_원값": T, "T_표시7일": T_bar, "잠정": provisional(days),
+    L = step_down(J, **_pick(p, n="step_days"))
+    T_bar = display_ma(T, **_pick(p, window="ma_days"))
+    tr = trend(T_bar, **_pick(p, days="trend_days", pct_min="trend_pct_min"))
+    cols = {"T_원값": T, "T_표시7일": T_bar, "잠정": provisional(days, **_pick(p, n="provisional_days")),
             **{f"Tg_{b}": Tg[f"Tg_{b}"] for b in bundles},
             "완화할인": relief_display(T, Tg), "원점수_게이지": raw_gauge(comp, bundles), "단계_T": LT,
             "하한_물리": fp, "물리_4거유형일": type4_days(events, days, type4_ids), "하한_E5": fe, "하한_사건": fs,
-            "단계_판정": J, "단계_최종": L, "그날까지_상위%": cumulative_top_pct(T_bar), "A2자료": a2_note(days),
+            "단계_판정": J, "단계_최종": L, "그날까지_상위%": cumulative_top_pct(T_bar),
+            "A2자료": a2_note(days, **_pick(p, a2_end="a2_end")),
             "화면_단계문구": stage_label(L, J), "변화14_표시": tr["변화14_표시"], "변화율14_표시": tr["변화율14_표시"]}
     daily = pd.DataFrame(cols, index=days)[daily_columns(bundles)]
     daily.index.name = "날짜"
-    info = {"B": B, "cuts": cuts, "quantiles_raw": q, "half_warning": cuts_half_warning(q), "components": comp}
+    info = {"B": B, "cuts": cuts, "quantiles_raw": q, "half_warning": cuts_half_warning(q), "components": comp,
+            "params": p}
     return daily, info
--- a/scripts/run_tension.py
+++ b/scripts/run_tension.py
@@ -6,7 +6,9 @@
 사용: python scripts/run_tension.py [--end YYYY-MM-DD]   (기본 config.END_DATE — None이면 실행일)
 """
 import argparse
+import re
 import sys
+from datetime import datetime
 from pathlib import Path
 
 ROOT = Path(__file__).resolve().parents[1]
@@ -20,18 +22,37 @@
 OUT_DIR = ROOT / config.TENSION_DATA_DIR / "_check"  # F2-2 검산용 — 깃 제외. 커밋할 결과 위치는 F4
 
 
-def main(argv=None) -> int:
-    p = argparse.ArgumentParser(description="사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)")
-    p.add_argument("--end", default=config.END_DATE, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
-    args = p.parse_args(argv)
-
-    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
-    days = core.calc_days(config.CALC_START_DATE, args.end)
+def _end_date(text):
+    """--end 값 검사 — YYYY-MM-DD 형식의 실제 날짜만(F2 검토 9)."""
+    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
+        raise argparse.ArgumentTypeError(f"YYYY-MM-DD 형식이 아님: {text}")
+    try:
+        datetime.strptime(text, "%Y-%m-%d")
+    except ValueError:
+        raise argparse.ArgumentTypeError(f"없는 날짜: {text}") from None
+    return text
+
+
+def _run(end) -> None:
+    table = tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH)
+    type4 = tio.type4_event_ids(table)
+    if not type4:
+        raise ValueError("판정표에 4거 유형(Y) 사건이 없음")
+    days = core.calc_days(config.CALC_START_DATE, end)
     print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")
-
+    results = []
     for name, bundles in SCENARIOS:
-        events, excluded = tio.load_events(ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv")
+        path = ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv"
+        if not path.exists():
+            raise FileNotFoundError(f"사건표 없음: {path} - scripts/build_events.py로 먼저 만든다")
+        events, excluded = tio.load_events(path)
+        problems = tio.check_type4_against_events(table, events)
+        if len(problems):
+            listed = "; ".join(f"{r.사건ID} {r.문제}" for r in problems.head(10).itertuples())
+            raise ValueError(f"[{name}] 판정표와 사건표가 맞지 않음 {len(problems)}건: {listed}")
         daily, info = core.daily_table(events, days, bundles, type4)
+        results.append((name, events, excluded, daily, info))
+    for name, events, excluded, daily, info in results:   # 두 시나리오가 모두 계산된 뒤에만 쓴다
         out = OUT_DIR / f"일별_{name}.csv"
         tio.write_csv(daily.round(3), out, index=True)
         print(f"[{name}] 사건 {len(events)}행 · load 제외 {len(excluded)}")
@@ -39,7 +60,21 @@
         print(f"  마지막 날 화면 단계: {daily['화면_단계문구'].iloc[-1]}")
         print(f"  쓴 파일: {out}")
         if info["half_warning"]:
-            print("  경고: T 구간 분위가 정확히 x.5 — 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")
+            print("  경고: T 구간 분위가 정확히 x.5 - 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")
+
+
+def main(argv=None) -> int:
+    for stream in (sys.stdout, sys.stderr):   # cp949 콘솔에 없는 글자가 있어도 멈추지 않게(F2 검토 6)
+        if hasattr(stream, "reconfigure"):
+            stream.reconfigure(errors="replace")
+    p = argparse.ArgumentParser(description="사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)")
+    p.add_argument("--end", default=config.END_DATE, type=_end_date, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
+    args = p.parse_args(argv)
+    try:
+        _run(args.end)
+    except (ValueError, TypeError, FileNotFoundError) as e:
+        print(f"멈춤: {e}", file=sys.stderr)
+        return 1
     return 0
 
 
```
