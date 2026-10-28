# F2-1 작업 프롬프트 — 계산 코어 2a(상승·완화 ②~⑧)·2b(하한 ⑩)

작성 2026-10-29 · 구현 메인(채팅 ②) → Claude Code · 브랜치 `feature/tension-core`(최신 `develop`에서 새로 — F2-2도 이 브랜치에 이어서) · PR 대상 `develop`
상태: **실행** (2026-10-29 사용자 확인 — F2-1·F2-2 같은 브랜치 이어서 · 프롬프트 그대로) · 실행 조건: PR #17(F1)이 `develop`에 병합된 뒤(U4 — 1절에서 확인, 병합 전이면 멈춤)
권장 모델·노력: **Opus 5.5 · 높음**(지시서 v2: F2는 높음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). `conda run`은 쓰지 않는다. 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`(F1 보고서 3절 6 — 한글 출력 깨짐 방지). **`$B`** = `$HOME/bongsu_F2-1_20261029`(셸이 새로 열리면 다시 정의).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, `config.py`·`io.py`·`build_events.py` 수정, 기준 스크립트(`s3_core.py`·`compute_v014.py`·`lib5.py`) **import** — 읽고 옮기기만 한다.

---

## 0. 목표
- `utils/tension/core.py`를 새로 만들고 **식 ②~⑧(상승·완화 → T)과 ⑩(전용 하한 3종 + 4거 유형일)**만 옮긴다. ⑨·⑪~⑰(구간·판정·하강·표시·문구), 일별 CSV 조립, `scripts/run_tension.py`는 **F2-2**에서 한다.
- `.gitattributes`로 우리 CSV 줄바꿈을 LF로 고정한다(사용자 10-29 — F1 보고서 3절 7).
- 통과 기준(6절 검산): v0.1.4 `일별_v014_기본.csv`·`_확장.csv`의 `T_원값`·`Tg_*` 최대 절대차 < 0.001, `하한_물리`·`하한_E5`·`하한_사건`·`물리_4거유형일` 다른 날 0, `요약_v014.csv`의 평소값 B·하한 개수 일치, 완화 상한에 붙은 날 272(대응표 4절 — 기준 요약은 빈칸).
- **구현 메인이 미리 확인한 것 `[확인 10-29]`:** 2절 계약대로 만든 간이 구현(리포 밖)으로 부록 B 검산이 기본·확장 모두 `전체: 통과`(T·Tg 최대차 0.0005 = 기준 CSV 셋째 자리 반올림 폭). 사건표의 ICBM 14행은 S가 정확히 `7.5`로 저장돼 있어 `S >= 7.5` 판정에 부동소수 문제가 없다.
- 기준 구현(읽기만, `진행 현황 및 계획 정리/v0.1_시험/` 아래): `S3/s3_core.py`(`load`·`decay`·`conv`·`floors_s1`·`run` 63~79행) · `v0.1.4/compute_v014.py`(`floors_v014` 13~18행, `compute` 21~27행 — 사건 하한 `key`). 식 = `docs/tension/산출식_정리.md` 1A.2절, 대응 = `docs/dev/식_함수_대응표.md` 1·4·5절.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
git status --porcelain
#   기대(순서 무관): " M docs/dev/진행기록.md", " M docs/dev/식_함수_대응표.md", "?? docs/dev/tasks/F2-1_core.md", "?? .obsidian/"
git branch --show-current          # 기대: feature/tension-io
git fetch origin
gh pr view 17 --json state,mergedAt   # 기대: "state":"MERGED" — 아니면 멈춤(U4)
git log --oneline -1 origin/develop
git rev-list --left-right --count feature/tension-io...origin/develop   # 기대: 왼쪽 0 (오른쪽 숫자는 log에 적음)

# 1-1 구현 메인 문서 백업(리포 밖)
B="$HOME/bongsu_F2-1_20261029"; mkdir -p "$B/docs"
for f in docs/dev/진행기록.md docs/dev/식_함수_대응표.md docs/dev/tasks/F2-1_core.md; do mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git diff --stat > "$B/docs_diff_stat.txt"; cat "$B/docs_diff_stat.txt"

# 1-2 되돌리고 develop으로
git restore docs/dev/진행기록.md docs/dev/식_함수_대응표.md
git switch develop
git pull --ff-only origin develop        # 실패하면 멈추고 보고
git log --oneline -1                     # origin/develop과 같아야 함

# 1-3 백업 되살리기 → 브랜치
for f in docs/dev/진행기록.md docs/dev/식_함수_대응표.md docs/dev/tasks/F2-1_core.md; do cp "$B/docs/$f" "$f"; done
git status --porcelain                   # 1절 첫 줄 기대와 같아야 함
git switch -c feature/tension-core

# 1-4 이슈(F2 전체 — F2-2도 이 번호를 씀): 본문 "$B/issue_F2.md" = .github/ISSUE_TEMPLATE/feature.md 양식
#     (배경 = 0절 · 범위 = "F2-1: ②~⑧·⑩ / F2-2: ⑨·⑪~⑰·일별 CSV·run_tension.py" · 완료 조건 = 지시서 0절 완료 기준을 체크박스로)
gh issue create --title "[FEAT] 긴장도 계산 코어(F2)" --label feat --body-file "$B/issue_F2.md"
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
PYTHONIOENCODING=utf-8 <py> -m pytest -q   # 기대: 14 passed(F1까지)
```

## 2. `utils/tension/core.py` — 계약 (이름·서명·순서 그대로)
- 모듈 docstring 첫 줄: `"""긴장도 계산 코어 — 산출식 ①~⑰(docs/tension/산출식_정리.md 1A.2절). 순수 함수: DataFrame·Series → DataFrame·Series."""` 둘째 단락에 "F2-1 = ②~⑧·⑩, F2-2 = ⑨·⑪~⑰"을 적는다.
- import는 `numpy`·`pandas`·`config`만. Streamlit·파일 경로·`io` 모듈·scipy를 쓰지 않는다. **`config` 값은 인자 기본값으로만** 쓴다.
- 함수 docstring 첫 줄은 식 번호로 시작한다(CLAUDE.md 4절). 식 번호가 없는 보조 함수는 `(보조)`로 시작한다.
- 입력 `events` = `io.load_events()`가 돌려준 사건표(`date` datetime64·`S` float64·나머지 문자열). `days` = `calc_days()`의 `DatetimeIndex`. 반환 Series·DataFrame의 인덱스는 모두 `days`.

| 함수 (서명) | docstring 첫 줄 | 규칙 (기준 구현) |
|---|---|---|
| `calc_days(start=config.CALC_START_DATE, end=config.END_DATE) -> pd.DatetimeIndex` | `(보조) 𝒯 계산 기간 — start~end 하루 간격, end가 None이면 오늘.` | `pd.date_range(start, end, freq="D")`. end None → `pd.Timestamp.today().normalize()` |
| `base_mask(days, base_period=config.BASE_PERIOD) -> np.ndarray` | `(보조) 𝒯₀ 기준기간 — 연도가 base_period 안인 날 True.` | `(days.year >= a) & (days.year <= b)` |
| `daily_sums(events, days, bundles) -> pd.DataFrame` | `② 묶음별 일 합 — 묶음 g의 그날 사건 점수 합, 사건 없는 날 0.` | 열 = `bundles` 순서. 묶음별 `groupby("date")["S"].sum().reindex(days, fill_value=0.0)`(`s3_core.load`). `bundles`에 없는 묶음(예 `북러(표시만)`)은 읽지 않고, 기간 밖 날짜는 버린다 |
| `decay_cumulative(d, half_life=config.HALF_LIFE_DAYS) -> pd.Series` | `③ 감쇠 누적 — R_t = λ·R_t−1 + d_t, λ = 2^(−1/반감기), 시작값 0.` | **파이썬 루프 그대로**(`s3_core.decay`): `a = 2 ** (-1 / half_life)`, `acc = acc * a + v`. `ewm`·`lfilter`·누적곱 벡터화 금지(대응표 ③) |
| `baseline_means(R, mask) -> pd.Series` | `④ 평소값 — 기준기간 R의 평균(열마다).` | 열마다 `R[c][mask].mean()`, 인덱스 = R의 열 |
| `relative_index(R, B) -> pd.DataFrame` | `⑤ 평소 대비 — T_g = 100 · R_g / B_g.` | 열마다 `R[c] / B[c] * 100`(이 순서) |
| `rising_index(Tg) -> pd.Series` | `⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중).` | **열 순서대로 더한 뒤 열 수로 나눔**(`sum(Tg.values()) / len(bundles)`). `mean(axis=1)`을 쓰지 않는다 |
| `relief_discount(R_relief, B_relief, c=config.RELIEF_C, cap=config.RELIEF_CAP) -> pd.Series` | `⑦ 완화 할인 — δ = min(c · R완 / B완, κ).` | `np.minimum(c * R_relief / B_relief, cap)` → Series |
| `tension_index(T_plus, delta) -> pd.Series` | `⑧ 긴장도 — T = T⁺ · (1 − δ).` | `T_plus * (1 - delta)` |
| `tension_components(events, days, bundles, base_period=config.BASE_PERIOD, half_life=config.HALF_LIFE_DAYS, relief_c=config.RELIEF_C, relief_cap=config.RELIEF_CAP, relief_bundle=config.BUNDLE_RELIEF) -> tuple[pd.DataFrame, pd.Series]` | `②~⑧ 묶음 — 사건표에서 R·B·T_g·T⁺·δ·T를 한 번에.` | 대상 = `bundles` + `relief_bundle`(이 순서). 반환 ① DataFrame 열 = `R_<묶음>`(대상 순서) → `Tg_<묶음>`(bundles 순서) → `T_plus` → `delta` → `T` ② B Series(인덱스 = 대상 순서). 기준 구현은 `run`을 두 번 부르지만 T는 구간과 무관하므로 한 번 계산 |
| `half_gauss_window(d, sigma=config.HALF_GAUSS_SIGMA, window=config.FLOOR_WINDOW) -> pd.Series` | `⑩ 하한 원점수 — ρ_t = Σ_{k<창} exp(−k²/(2σ²)) · d_t−k (반가우스 σ10·30일).` | `w = np.exp(-np.arange(window) ** 2 / (2 * sigma ** 2))`, `np.convolve(d.to_numpy(float), w)[:len(d)]`(`s3_core.conv`). FFT·scipy 금지 |
| `type4_days(events, days, type4_ids) -> pd.Series` | `⑩ 물리 4거 유형 사건일 — 판정표 Y 사건의 사건표 날짜면 True.` | 사건표에서 `사건ID ∈ type4_ids`인 행의 `date`(판정표 date 아님 — 대응표 ⑩-b). 일별 CSV `물리_4거유형일` 열 |
| `floor_physical(events, days, type4_ids, kill_ids=config.KILL_EVENTS, thresholds=config.PHYS_FLOOR, type4_stage=config.TYPE4_FLOOR_STAGE, kill_stage=config.KILL_FLOOR_STAGE, bundle=config.BUNDLE_PHYS) -> pd.Series` | `⑩ 물리 하한 F^물 — 풍선 뺀 A3·A7 ρ≥3→3·≥7→4, 풍선 ρ≥6→3, 4거 유형일 ≥4, 사망·침몰일 5.` | **순서 그대로**(`floors_s1` + `floors_v014`): ① `묶음 == bundle` 행 중 풍선 = `요소 == "A3"`이고 `사건명`에 `BALLOON_KEYWORD`(대소문자 무시) → 풍선·비풍선 일 합을 따로 `half_gauss_window` → `np.select([ρo >= th["4거"], ρo >= th["3거"], ρb >= th["풍선3거"]], [4, 3, 3], 1)` ② 4거 유형일 `max(·, type4_stage)` ③ `사건ID ∈ kill_ids`인 사건표 날짜 `= kill_stage`(덮어씀). int64 |
| `floor_e5(events, days, thresholds=config.E5_FLOOR, bundle=config.BUNDLE_E5) -> pd.Series` | `⑩ E5 하한 F^E5 — 북러 밀착 ρ≥4→3, ≥10→4.` | `묶음 == bundle` 일 합 → `half_gauss_window` → `np.select([ρ >= th["4거"], ρ >= th["3거"]], [4, 3], 1)`. int64 |
| `floor_event(events, days, icbm_s=config.EVENT_FLOOR_ICBM_S, stage=config.EVENT_FLOOR_STAGE) -> pd.Series` | `⑩ 사건 하한 F^사 — 핵실험(A1) 또는 ICBM(A2, S ≥ 7.5) 당일 3거.` | `요소 == "A1"`이거나 (`요소 == "A2"`이고 `S >= icbm_s`)인 행의 날짜 → stage, 그 밖 1. int64 |

- 모듈 상수: `BALLOON_KEYWORD = "Balloon"`(주석 `# ADR-007 2 — 오물풍선 = A3 중 사건명에 Balloon`). config에 더하지 않는다.
- `floor_physical`의 `thresholds` 키 = `"3거"`·`"4거"`·`"풍선3거"`, `floor_e5`의 키 = `"3거"`·`"4거"`(config 그대로).
- 기준 구현과 다르게 하고 싶은 곳이 보이면(벡터화, 이름 등) **고치지 말고** 보고서 3절에 적는다.

## 3. `.gitattributes` (리포 루트, 새 파일 — 사용자 10-29)
```gitattributes
# 긴장도 코드화(F2-1, 2026-10-29): 결과·기준 CSV 줄바꿈을 LF로 고정 — core.autocrlf=true PC에서도 바이트 비교가 같게
data/tension/*.csv text eol=lf
tests/fixtures/*.csv text eol=lf
```
확인:
```bash
git add .gitattributes
git ls-files --eol data/tension/물리사건_유형판정표.csv   # 기대: i/lf  w/lf  attr/text eol=lf
git status --porcelain                                    # .gitattributes 말고 새로 바뀐 파일이 없어야 함
```
`git add --renormalize`는 하지 않는다(저장된 blob이 이미 LF — F1 보고서 3절 7).

## 4. 하지 않는 것 (F2-2 몫 포함)
- ⑨ 구간·⑪ 판정·⑫ 하강·⑬~⑰ 표시·문구, `완화할인` 열(2절 정의)·`원점수_게이지`·`잠정`·`A2자료` 열, 일별 CSV 조립, `scripts/run_tension.py` — **F2-2**
- 새 테스트 파일(F3), 결과 CSV 쓰기·커밋(F4), JSON 출력
- `config.py`·`utils/tension/io.py`·`scripts/build_events.py`·`CLAUDE.md`·`README.md`·`requirements.txt` 수정
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정

## 5. 확인 명령
```bash
# 5-1 import·docstring 번호
PYTHONIOENCODING=utf-8 <py> -c "import inspect, utils.tension.core as c; fs=[(n,f) for n,f in inspect.getmembers(c, inspect.isfunction) if f.__module__==c.__name__ and not n.startswith('_')]; [print(n, '|', (f.__doc__ or '').splitlines()[0]) for n,f in fs]; print(len(fs))"
#   기대: 2절 표의 공개 함수 15개(밑줄로 시작하는 내부 함수는 세지 않음 — 만들어도 됨), 첫 줄이 식 번호 또는 (보조)로 시작
# 5-2 금지 사용 없음
grep -nE "streamlit|scipy|lfilter|\.ewm\(|read_csv|to_csv|open\(|Path\(" utils/tension/core.py      # 출력 없음
grep -nE "^[[:space:]]*(import|from)[[:space:]]+(s3_core|compute_v01|lib5)" utils/tension/core.py  # 출력 없음
# 5-3 테스트
PYTHONIOENCODING=utf-8 <py> -m pytest -q      # 14 passed(이번에 테스트를 더하지 않음)
```

## 6. v0.1.4 대조 검산
부록 B를 `$B/verify_core_2ab.py`로 **글자 그대로** 저장하고 리포 루트에서:
```bash
PYTHONIOENCODING=utf-8 <py> "$B/verify_core_2ab.py"
```
- 입력은 F1이 만든 `data/tension/events_기본.csv`·`_확장.csv`(로컬, 깃 제외)와 판정표 사본. 없으면 `PYTHONIOENCODING=utf-8 <py> scripts/build_events.py --end 2026-10-27`로 다시 만든다(log에 적음).
- 맞지 않으면: **옮기다 생긴 실수**는 고치고 다시 돌린다. **2절 규칙을 바꿔야만 맞는 경우**와 pandas 버전 차이로 보이는 경우는 고치지 말고, 다른 날 목록(최대 20일, 날짜·새 값·기준 값)을 log에 남기고 멈추고 보고한다. 기준값(일별·요약 CSV)은 고치지 않는다.

## 7. 완료 조건 (모두 통과해야 "완료")
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 기대 상태(PR #17 MERGED 포함) |
| 2 | 3절 `.gitattributes` 확인 | `attr/text eol=lf`, 다른 변경 없음 |
| 3 | 5-1 | 공개 함수 15개, 첫 줄 규칙 지킴 |
| 4 | 5-2 | grep 두 개 출력 없음 |
| 5 | 5-3 | 14 passed |
| 6 | 6절 검산 | 마지막 줄 `전체: 통과` |
| 7 | 커밋 목록 `git log --oneline develop..HEAD` | 8절 순서 |
| 8 | 8절 금지 경로 검사(매 커밋 전) | 매번 `OK` |
| 9 | 마지막 `git status --porcelain` | `?? .obsidian/` 하나만 |

## 8. 커밋 (한 커밋 한 목적, 이 순서)
금지 경로 검사(각 커밋 전 그대로):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F2-1 작업 프롬프트·설계 문서 반영` — `docs/dev/tasks/F2-1_core.md`, `docs/dev/진행기록.md`, `docs/dev/식_함수_대응표.md`(내용 수정 없이 — U2)
2. `chore: 긴장도 CSV 줄바꿈 LF 고정(.gitattributes)` — `.gitattributes`
3. `feat: 계산 코어 2a 상승·완화 지수(②~⑧)` — `utils/tension/core.py`(2a 함수 + `calc_days`·`base_mask`)
4. `feat: 계산 코어 2b 전용·사건 하한(⑩)` — `utils/tension/core.py`(2b 함수 추가)
5. `docs: F2-1 보고서` — `docs/dev/reports/F2-1_report.md`, `F2-1_log.md`
- 3·4를 나누기 위해 2a 함수까지 쓰고 검산 2a 부분을 돌린 뒤 커밋하고, 2b를 더해 검산 전체를 돌린 뒤 커밋해도 된다(순서만 지키면 방법은 자유).

## 9. 동기화 · 푸시 · PR
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest -q
git push -u origin feature/tension-core
# 본문 "$B/pr_F2.md" = .github/pull_request_template.md 양식. 요약 첫 줄에 "F2-1(②~⑧·⑩)까지 — F2-2가 같은 브랜치에 이어서 커밋, F2 검토(U9) 뒤 병합"
#   · closes #<1-4 이슈> · 변경 = 8절 · 테스트 = 7절 결과
gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 계산 코어(F2)" --body-file "$B/pr_F2.md"
```
병합하지 않는다. 보고서 커밋 뒤 다시 푸시하고 끝낸다.

## 10. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F2-1_report.md`(60줄 이내): 1절 = 7절 표 9행 ✓/✗ · 6절 검산 숫자 요약 한 줄씩(시나리오별 B 4~5개 · T·Tg 최대차 · 상한 272 · 하한 다른 날) · 2절 막힌 것 · 3절 기준과 다르게 한 것·고치고 싶은 것 · 4절 바뀐 파일.
`docs/dev/reports/F2-1_log.md`: 1절 점검 출력, 3·5·6절 출력 전부, 커밋·푸시·PR 출력.

---

## 부록 A. 기준 구현 핵심 줄 (`진행 현황 및 계획 정리/v0.1_시험/` — 읽기만)
```python
# S3/s3_core.py
def decay(x, hl=14):
    a = 2**(-1/hl); r = np.zeros(len(x)); acc = 0.0
    for i, v in enumerate(x.values):
        acc = acc*a + v; r[i] = acc
_hg = np.exp(-np.arange(30)**2/200)
def conv(x): return pd.Series(np.convolve(x.values, _hg)[:len(x)], index=x.index)
# floors_s1: ph = 물리 충돌 행, bal = A3 & 사건명 contains 'Balloon'(case=False)
#   fp = np.select([Ro >= 7, Ro >= 3, Rb >= 6], [4, 3, 3], 1); kill 날짜 fp = 5
#   fe = np.select([Re >= 10, Re >= 4], [4, 3], 1)   (Re = 북러 밀착 일 합의 conv)
# run: R = decay(D[b]) for bundles + ['완화']; Bg = R[b][bm].mean(); Tg = R/Bg*100
#      disc = np.minimum(c*R['완화']/Bg['완화'], 0.5); T = sum(Tg.values())/len(bundles)*(1-disc)
# v0.1.4/compute_v014.py
# floors_v014: t4 = ev[사건ID ∈ type4].date.unique(); fp[t4] = max(fp, 4); 그 뒤 kill 날짜 = 5 (덮어씀)
# compute: key = ev[(요소 == 'A1') | ((요소 == 'A2') & (S >= 7.5))].date.unique(); ef = 1, ef[key] = 3
```

## 부록 B. `$B/verify_core_2ab.py` (글자 그대로 저장)
```python
"""F2-1 검산(2a·2b) — 리포 루트에서 실행. core 함수 결과를 v0.1.4 일별·요약 CSV와 대조."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
import config
from utils.tension import core, io as tio

REF = ROOT / "진행 현황 및 계획 정리" / "v0.1_시험" / "v0.1.4"
summary = tio.read_csv_kr(REF / "요약_v014.csv", index_col=0)
type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
days = core.calc_days("2010-01-01", "2026-10-27")
ok = len(days) == 6144
print("계산 기간", days[0].date(), "~", days[-1].date(), len(days), "일")

for nm, col, bundles in [("기본", "기본", config.BUNDLES_BASE), ("확장", "확장(C5 포함)", config.BUNDLES_EXT)]:
    ev, exc = tio.load_events(ROOT / "data" / "tension" / f"events_{nm}.csv")
    ref = tio.read_csv_kr(REF / f"일별_v014_{nm}.csv", index_col=0, parse_dates=True)
    s = summary[col]
    print(f"\n[{nm}] 사건 {len(ev)}행 · load 제외 {len(exc)} · 묶음 {bundles}")
    ok &= len(exc) == 0 and ref.index.equals(days)

    # --- 2a: ②~⑧
    comp, B = core.tension_components(ev, days, bundles)
    for b in list(bundles) + [config.BUNDLE_RELIEF]:
        r = round(float(B[b]), 3) == float(s[f"B_{b}"])
        ok &= r
        print(f"  B_{b} {B[b]:.6f} (기준 {s[f'B_{b}']}) {'✓' if r else '✗'}")
    for c_new, c_ref in [("T", "T_원값")] + [(f"Tg_{b}", f"Tg_{b}") for b in bundles]:
        d = (comp[c_new] - ref[c_ref]).abs()
        n3 = int((comp[c_new].round(3) != ref[c_ref]).sum())
        r = float(d.max()) < 0.001
        ok &= r
        print(f"  {c_ref}: 최대차 {d.max():.6f} · 셋째 자리 다른 날 {n3} {'✓' if r else '✗'}")
    cap_days = int((comp["delta"] >= config.RELIEF_CAP - 1e-12).sum())
    r = cap_days == 272
    ok &= r
    print(f"  완화 상한에 붙은 날 {cap_days} (기준 272 — 대응표 4절) {'✓' if r else '✗'}")

    # --- 2b: ⑩
    fp = core.floor_physical(ev, days, type4)
    fe = core.floor_e5(ev, days)
    fs = core.floor_event(ev, days)
    t4 = core.type4_days(ev, days, type4)
    for name, new, refcol in [("하한_물리", fp, "하한_물리"), ("하한_E5", fe, "하한_E5"), ("하한_사건", fs, "하한_사건"), ("물리_4거유형일", t4, "물리_4거유형일")]:
        n = int((new.to_numpy() != ref[refcol].to_numpy()).sum())
        r = n == 0
        ok &= r
        print(f"  {name}: 다른 날 {n} {'✓' if r else '✗'}")
    counts = {"사건하한 날 수": int((fs == 3).sum()), "물리 4거유형 사건일 수": int(t4.sum()), "E5하한 3거↑ 날": int((fe >= 3).sum()),
              "물리하한 3거↑ 날": int((fp >= 3).sum()), "물리하한 4거↑ 날": int((fp >= 4).sum()), "물리하한 5거 날": int((fp == 5).sum())}
    for k, v in counts.items():
        r = v == int(float(s[k]))
        ok &= r
        print(f"  {k} {v} (기준 {s[k]}) {'✓' if r else '✗'}")

print("\n전체:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
```
