# F2-2 작업 프롬프트 — 계산 코어 2c(구간·판정·하강 ⑨⑪⑫)·2d(표시·문구 ⑬~⑰ + 일별 CSV) · run_tension.py 최소판

작성 2026-10-29 · 구현 메인(채팅 ③) → Claude Code · 브랜치 `feature/tension-core`(**F2-1에 이어서** — 새 브랜치·develop 전환 없음) · PR [#19](https://github.com/kjy700317-maker/Team-Project/pull/19)(draft)에 이어 커밋 · 이슈 #18
상태: **실행** (2026-10-29 사용자 확인 — 프롬프트 그대로 · 요약 지표 함수는 F4 · `run_tension.py` 최소판 출력은 깃 제외 폴더 `data/tension/_check/`)
권장 모델·노력: **Opus 5.5 · 높음**(지시서 v2: F2는 높음)

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). `conda run`은 쓰지 않는다. 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. **`$B`** = `$HOME/bongsu_F2-2_20261029`(셸이 새로 열리면 다시 정의).
> **테스트 명령은 `<py> -m pytest`**(‑q 없이 — `pytest.ini`의 `addopts = -q`와 겹치면 요약 줄이 사라진다, F2-1 보고서 3절 4).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, `config.py`·`io.py`·`build_events.py`·`tests/**` 수정, **F2-1 함수 15개의 본문·서명 수정**, 기준 스크립트(`s3_core.py`·`compute_v014.py`·`lib5.py`) **import** — 읽고 옮기기만 한다.

---

## 0. 목표
- `utils/tension/core.py`에 **식 ⑨·⑪·⑫(2c)와 ⑬~⑰ + 식 번호 밖 열(2d)**, 일별 결과 조립 `daily_table`을 더한다(공개 함수 16개 → 모두 31개). F2-1 함수는 그대로 쓴다.
- `scripts/run_tension.py` **최소판**(경로 고정, 인자는 `--end` 하나): 사건표 2개 → **`data/tension/_check/`**`일별_기본.csv`·`일별_확장.csv`(깃 제외 — `.gitignore`의 `data/tension/_*`, 사용자 10-29). 요약 지표 함수·요약·연도별 CSV, 입력·출력 인자, 커밋할 결과 위치는 **F4**(사용자 10-29).
- 시작 단계(사용자 10-29): 판정표 사본을 다시 체크아웃해 작업트리도 LF로(1-1), `CLAUDE.md` 5절 테스트 명령의 `-q` 중복 제거(1-4).
- **통과 기준(6절 검산, 지시서 0절 완료 기준 포함):** 기본·확장 모두 v0.1.4 `일별_v014_*.csv`와 **열 이름·순서 같음**, `단계_최종` 다른 날 0, 실수 열 |차| < 0.001, 정수·참거짓·문자열 열 완전 일치 · `요약_v014.csv`의 T 구간(115/256/315/378 · 확장 110/237/314/374)·반올림 전 분위·1~5거 %·바뀜/년·위기 10건 단계와 게이지 눈금·연도 지표·현재 값과 문구 일치 · END를 늘려도 과거 값 그대로 · `run_tension.py`가 쓴 파일도 같은 검사 통과.
- **구현 메인이 미리 확인한 것 `[확인 10-29]`:** 2·3절 계약대로 만든 간이 구현(리포 밖, python 3.10 · numpy 2.2.6 · pandas 2.3.3)으로 부록 B 검산이 기본·확장 모두 `전체: 통과`. 실수 열 최대차 0.0005(기준 CSV 셋째 자리 반올림 폭), `run_tension.py`가 쓴 두 파일은 기준 CSV와 **바이트까지 같았다**(pandas 3.0.6에서는 다를 수 있어 바이트 같음은 참고로만 본다).
- 기준 구현(읽기만, `진행 현황 및 계획 정리/v0.1_시험/` 아래): `S3/s3_core.py`(`stage`·`step_down`·`run` 63~79행·`metrics`) · `v0.1.4/compute_v014.py`(`compute` 21~60행 — 열 조립). 식 = `docs/tension/산출식_정리.md` 1A.2절, 대응 = `docs/dev/식_함수_대응표.md` 1·2·3·5절. 핵심 줄은 부록 A.

## 1. 시작 점검 · 판정표 다시 받기 · 문서 커밋 · develop 맞추기 · CLAUDE.md (이 순서. 기대와 다르면 멈추고 보고)
```bash
B="$HOME/bongsu_F2-2_20261029"; mkdir -p "$B"
git status --porcelain
#   기대(순서 무관 · 한글 경로가 "\354…"처럼 보여도 같은 것):
#   " M docs/dev/진행기록.md", " M docs/dev/식_함수_대응표.md", "?? docs/dev/tasks/F2-2_core.md", "?? .obsidian/"
git branch --show-current                    # 기대: feature/tension-core
git status -sb | head -1                     # 기대: "## feature/tension-core...origin/feature/tension-core" (ahead/behind 없음)
git log --oneline -1                         # 기대: "… docs: F2-1 보고서"
gh pr view 19 --json state,isDraft,headRefName   # 기대: OPEN · true · feature/tension-core
PYTHONIOENCODING=utf-8 <py> --version
PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
```

**1-1 판정표 사본 다시 체크아웃**(사용자 10-29 — F2-1 보고서 2절 1: 작업트리만 CRLF)
```bash
rm data/tension/물리사건_유형판정표.csv
git restore data/tension/물리사건_유형판정표.csv
git ls-files --eol data/tension/물리사건_유형판정표.csv   # 기대: i/lf  w/lf  attr/text eol=lf
git status --porcelain                                    # 1절 첫 기대와 같음(판정표가 보이지 않아야 함)
```

**1-2 커밋 1** — 구현 메인 문서(내용 수정 없이 — U2). 8절 금지 경로 검사 뒤:
```bash
git add docs/dev/tasks/F2-2_core.md docs/dev/진행기록.md docs/dev/식_함수_대응표.md
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
git commit -m "docs: F2-2 작업 프롬프트·설계 문서 반영"
```

**1-3 develop 맞추기**(인계 ② → ③: 시작 전 merge)
```bash
git fetch origin
git rev-list --left-right --count HEAD...origin/develop   # 오른쪽 = develop에만 있는 커밋 수(log에 적음)
# 오른쪽이 0이면 merge를 건너뛴다. 0보다 크면:
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고(직접 해결 금지)
PYTHONIOENCODING=utf-8 <py> -m pytest   # 기대: 14 passed
```

**1-4 커밋 2 — CLAUDE.md 테스트 명령**(사용자 10-29: 그 줄만 바꾸는 스크립트로). 부록 C를 `$B/fix_claude_md.py`로 글자 그대로 저장하고 리포 루트에서:
```bash
PYTHONIOENCODING=utf-8 <py> "$B/fix_claude_md.py"      # 기대: "CLAUDE.md: 테스트 명령 1곳 바꿈"
git diff --stat CLAUDE.md                               # 기대: 1 file changed, 1 insertion(+), 1 deletion(-)
git diff CLAUDE.md | grep -E '^[-+][^-+]'               # 기대: 두 줄(-q 있는 줄 / 없는 줄)만
git add CLAUDE.md   # → 8절 금지 경로 검사 → 커밋
git commit -m "docs: CLAUDE.md 테스트 명령 -q 중복 제거"
```

## 2. `utils/tension/core.py`에 더할 것 — 계약 (이름·서명·순서 그대로)
- import에 표준 라이브러리 `bisect`만 더한다(⑭). 그 밖은 F2-1과 같다: `numpy`·`pandas`·`config`만, Streamlit·파일 경로·`io` 모듈·scipy 금지, **`config` 값은 인자 기본값으로만**.
- 함수 docstring 첫 줄은 식 번호 또는 `(보조)`로 시작한다. 반환 Series·DataFrame 인덱스는 입력과 같다(`days`).
- 모듈 상수(F2-2 부분 맨 위):
  - `A2_NOTE = "A2 자료 없음({end}까지)"` (주석 `# 일별 CSV A2자료 열 문구 — compute_v014.py`)
  - `DAILY_HEAD = ("T_원값", "T_표시7일", "잠정")`
  - `DAILY_TAIL = ("완화할인", "원점수_게이지", "단계_T", "하한_물리", "물리_4거유형일", "하한_E5", "하한_사건", "단계_판정", "단계_최종", "그날까지_상위%", "A2자료", "화면_단계문구", "변화14_표시", "변화율14_표시")`

**2c — ⑨⑪⑫**

| 함수 (서명) | docstring 첫 줄 | 규칙 (기준 구현) |
|---|---|---|
| `stage_cuts(T, mask, quantiles=config.STAGE_QUANTILES) -> tuple[np.ndarray, np.ndarray]` | `⑨ T 구간 — 기준기간 T의 70·90·95·98분위를 반올림한 정수 문턱 θ와 반올림 전 분위.` | `q = np.quantile(T[mask], quantiles)`(기본 linear) → `return np.round(q, 0), q`(**(문턱, 반올림 전) 순서**, `np.round` 짝수 반올림 그대로) |
| `cuts_half_warning(q) -> bool` | `⑨ 반올림 경계 — 반올림 전 분위 중 하나라도 정확히 x.5면 True(짝수 반올림 주의, 1A.5).` | `bool(any(abs(v - np.floor(v) - 0.5) < 1e-9 for v in q))`(`compute_v014` 요약 `경계_x.5_주의`) |
| `stage_from_index(T, cuts) -> pd.Series` | `⑨ T 구간 단계 L^T — 1 + #{j : T ≥ θ_j} (1~5거).` | `c1, c2, c3, c4 = cuts` · `np.select([T >= c4, T >= c3, T >= c2, T >= c1], [5, 4, 3, 2], 1)`(`s3_core.stage`) · int64 |
| `judge(*levels) -> pd.Series` | `⑪ 판정 J — 단계_T와 하한들 중 가장 높은 단계.` | `pd.concat(levels, axis=1).max(axis=1).astype("int64")` |
| `step_down(J, n=config.STEP_DOWN_DAYS) -> pd.Series` | `⑫ 최종 단계 L — 판정이 같거나 높으면 즉시 따라가고, 낮은 날이 n일 쌓이면 한 단계 내림(첫날 L = J).` | **파이썬 루프 그대로**(`s3_core.step_down`): `cur = J.iloc[0]`, `below = 0` · `r >= cur`이면 `cur, below = r, 0` · 아니면 `below += 1`, `below >= n`이면 `cur, below = cur - 1, 0` · `out[i] = cur` · int64 |

**2d — ⑬~⑰ · 식 번호 밖 열 · 조립**

| 함수 (서명) | docstring 첫 줄 | 규칙 (기준 구현) |
|---|---|---|
| `display_ma(T, window=config.DISPLAY_MA_DAYS) -> pd.Series` | `⑬ 표시선 T̄ — 7일 후행 이동평균(처음 6일은 있는 날만 평균).` | `T.rolling(window, min_periods=1).mean()` |
| `cumulative_top_pct(T_bar) -> pd.Series` | `⑭ 그날까지 상위% — 100 − 100 · #{s ≤ t : T̄_s ≤ T̄_t} / #{s ≤ t}.` | **`bisect` 누적 그대로**: 앞에서부터 `bisect.insort(srt, v)` → `bisect.bisect_right(srt, v) / len(srt) * 100`을 모아 `100 − 배열`. 벡터화 `rank`·정렬 한 번으로 바꾸지 않는다(동점 처리 — 대응표 ⑭) |
| `raw_gauge(comp, bundles) -> pd.Series` | `⑮ 원점수 게이지 R^합 — 상승 묶음 R_g의 합(확장이면 제재·압박 포함).` | `comp` = `tension_components`의 첫 반환. `sum(comp[f"R_{b}"] for b in bundles)`(**bundles 순서로 더함**) |
| `crisis_window_max(x, crises=config.CRISIS_LIST, window_days=config.CRISIS_WINDOW_DAYS) -> pd.Series` | `⑮ 위기 눈금 — 위기일 t_c부터 t_c + 14일까지 x의 최댓값(x = 원점수_게이지면 게이지 눈금, 단계_최종이면 위기 단계).` | 위기마다 `t = pd.Timestamp(날짜)` → `x.loc[t:t + pd.Timedelta(days=window_days)].max()`(양 끝 포함 — `metrics`·요약 게이지와 같음). 인덱스 = 위기 이름(목록 순서) |
| `trend(T_bar, days=config.TREND_DAYS, pct_min=config.TREND_PCT_MIN) -> pd.DataFrame` | `⑯ 추세 — Δ = T̄_t − T̄_t−14, 변화율 = 100 · Δ / T̄_t−14 (T̄_t−14 ≥ 50일 때만, 그 밖 NaN).` | `prev = T_bar.shift(days)` · `chg = T_bar - prev` · `pct = np.where(prev >= pct_min, chg / prev * 100, np.nan)` · 열 `변화14_표시`·`변화율14_표시`(이름 고정) |
| `stage_label(L, J) -> pd.Series` | `⑰ 단계 카드 문구 — L > J면 "L거 · 하강 중(판정 J거)", 그 밖 "L거".` | `f"{l}거 · 하강 중(판정 {j}거)" if j < l else f"{l}거"` — **가운뎃점 U+00B7**, 띄어쓰기 그대로 |
| `provisional(days, n=config.PROVISIONAL_DAYS) -> pd.Series` | `(보조) 잠정 — 마지막 날 − n일보다 뒤인 날(최근 6일) True.` | `days > days[-1] - pd.Timedelta(days=n)` |
| `a2_note(days, a2_end=config.A2_DATA_END) -> pd.Series` | `(보조) A2자료 — a2_end보다 뒤인 날 "A2 자료 없음(a2_end까지)", 그 밖 빈 문자열.` | `np.where(days > pd.Timestamp(a2_end), A2_NOTE.format(end=a2_end), "")` |
| `relief_display(T, Tg) -> pd.Series` | `(보조) 완화할인 열 — 1 − T / mean(T_g), mean = 0인 날 0 (δ와 다름 — 대응표 2절).` | `(1 - T / Tg.mean(axis=1).replace(0, np.nan)).fillna(0)` — **`Tg.mean(axis=1)` 그대로**(`rising_index`·`delta`로 바꾸지 않는다. T⁺ = 0인 날 δ > 0이어도 0으로 적히는 기준 정의 — 회귀 일치를 위해 이식) |
| `daily_columns(bundles) -> list[str]` | `(보조) 일별 CSV 열 순서 — 인덱스(날짜) 빼고 기본 20열·확장 21열.` | `[*DAILY_HEAD, *[f"Tg_{b}" for b in bundles], *DAILY_TAIL]` |
| `daily_table(events, days, bundles, type4_ids) -> tuple[pd.DataFrame, dict]` | `②~⑰ 일별 결과 — 사건표에서 일별 CSV의 모든 열(반올림 전)과 계산 정보를 한 번에.` | 아래 순서 |

`daily_table` 순서(파라미터는 각 함수의 config 기본값 — 값을 바꾼 계산은 개별 함수를 직접 부른다):
1. `comp, B = tension_components(events, days, bundles)` · `T = comp["T"]` · `Tg = comp[[f"Tg_{b}" for b in bundles]]`
2. `cuts, q = stage_cuts(T, base_mask(days))` → `LT = stage_from_index(T, cuts)` (**T는 한 번만 계산** — 기준 구현은 `run`을 두 번 부르지만 T는 구간과 무관, 대응표 ⑨)
3. `fp = floor_physical(events, days, type4_ids)` · `fe = floor_e5(events, days)` · `fs = floor_event(events, days)` → `J = judge(LT, fp, fe, fs)` → `L = step_down(J)`
4. `T_bar = display_ma(T)` · `tr = trend(T_bar)`
5. 열 값: `T_원값`=T · `T_표시7일`=T_bar · `잠정`=`provisional(days)` · `Tg_<묶음>`=Tg · `완화할인`=`relief_display(T, Tg)` · `원점수_게이지`=`raw_gauge(comp, bundles)` · `단계_T`=LT · `하한_물리`=fp · `물리_4거유형일`=`type4_days(events, days, type4_ids)` · `하한_E5`=fe · `하한_사건`=fs · `단계_판정`=J · `단계_최종`=L · `그날까지_상위%`=`cumulative_top_pct(T_bar)` · `A2자료`=`a2_note(days)` · `화면_단계문구`=`stage_label(L, J)` · `변화14_표시`·`변화율14_표시`=tr
6. `daily = pd.DataFrame(…, index=days)[daily_columns(bundles)]`, `daily.index.name = "날짜"`. 반올림하지 않는다(쓸 때 `round(3)` — 3절).
7. 반환 `info` 키(영어 그대로): `"B"`(평소값 Series) · `"cuts"`(문턱) · `"quantiles_raw"`(반올림 전) · `"half_warning"`(`cuts_half_warning(q)`) · `"components"`(comp)
- 자료형: 정수 열(`단계_T`·`하한_*`·`단계_판정`·`단계_최종`) int64, `잠정`·`물리_4거유형일` bool.
- 기준 구현과 다르게 하고 싶은 곳(벡터화, 이름, 완화할인 정의 등)은 **고치지 말고** 보고서 3절에 적는다.

## 3. `scripts/run_tension.py` — 최소판 (새 파일)
- 모듈 docstring 첫 줄: `"""긴장도 계산 최소판(F2-2) — data/tension/events_기본.csv·_확장.csv → data/tension/_check/일별_기본.csv·일별_확장.csv.`, 다음 단락에 "경로는 고정. 출력은 깃 제외 폴더 _check(.gitignore data/tension/_*) — 검산용(사용자 10-29). 입력·시나리오·출력 폴더 인자, 커밋할 결과 위치, 요약·연도별 CSV는 F4에서 정한다"와 사용법 `python scripts/run_tension.py [--end YYYY-MM-DD]`(기본 `config.END_DATE` — None이면 실행일).
- 머리는 `build_events.py`와 같은 방식: `ROOT = Path(__file__).resolve().parents[1]`, `sys.path.insert(0, str(ROOT))`, 그 뒤 `import config` · `from utils.tension import core` · `from utils.tension import io as tio`(`# noqa: E402`).
- `SCENARIOS = (("기본", config.BUNDLES_BASE), ("확장", config.BUNDLES_EXT))` · `OUT_DIR = ROOT / config.TENSION_DATA_DIR / "_check"`(주석 `# F2-2 검산용 — 깃 제외. 커밋할 결과 위치는 F4`). config에 더하지 않는다. `main(argv=None) -> int` + `if __name__ == "__main__": sys.exit(main())`.
- 인자는 `--end` 하나(`argparse`, 기본 `config.END_DATE`).
- 흐름: 판정표 `tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))` → `days = core.calc_days(config.CALC_START_DATE, args.end)` → 시나리오마다 `tio.load_events(ROOT / config.TENSION_DATA_DIR / f"events_{이름}.csv")` → `core.daily_table(...)` → **`tio.write_csv(daily.round(3), OUT_DIR / f"일별_{이름}.csv", index=True)`**(utf-8-sig·LF·인덱스 이름 `날짜` — U13. `write_csv`가 폴더를 만든다).
- 출력(표준 출력, 한 줄씩): 계산 기간·일수·`config.TENSION_MODEL_VERSION` / 시나리오마다 사건 행 수·load 제외 수·T구간(`f"{v:g}"`를 `/`로)·반올림 전(`.2f`)·마지막 날 `화면_단계문구`·쓴 파일 경로 / `info["half_warning"]`가 True면 경고 한 줄 "T 구간 분위가 정확히 x.5 — 짝수 반올림 결과를 사람이 확인(산출식 1A.5)".
- `data/tension/_check/`는 깃 제외라 `git status`에 보이지 않는다(5-6에서 확인). 커밋하지 않는다(커밋할 결과는 F4 — D1).

## 4. 하지 않는 것
- 요약·연도별 CSV, 요약 지표 계산 함수(사용자 10-29 — F4), 입력·출력 인자·커밋할 결과 위치(F4) · 새 테스트 파일(F3) · 그림(F4) · T_basic ⑮′(F6) · 결과 CSV 커밋(F4) · JSON 출력
- F2-1 함수 15개 수정, `config.py`·`utils/tension/io.py`·`scripts/build_events.py`·`tests/**`·`README.md`·`requirements.txt` 수정(`CLAUDE.md`는 1-4의 한 곳만)
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정

## 5. 확인 명령
```bash
# 5-1 import·docstring 번호 — 기대: 31개(F2-1 15 + F2-2 16), 첫 줄이 식 번호 또는 (보조)로 시작
PYTHONIOENCODING=utf-8 <py> -c "import inspect, utils.tension.core as c; fs=[(n,f) for n,f in inspect.getmembers(c, inspect.isfunction) if f.__module__==c.__name__ and not n.startswith('_')]; [print(n, '|', (f.__doc__ or '').splitlines()[0]) for n,f in fs]; print(len(fs))"
# 5-2 금지 사용 없음 — 주석 줄은 보지 않는다(F2-1 보고서 3절 1). 두 줄 모두 출력 없음
grep -nE '^[^#]*(streamlit|scipy|lfilter|\.ewm\(|\.rank\(|read_csv|to_csv|open\(|Path\()' utils/tension/core.py
grep -nE '^[[:space:]]*(import|from)[[:space:]]+(s3_core|compute_v01|lib5|streamlit|scipy)' utils/tension/core.py scripts/run_tension.py
# 5-3 import 목록 — 기대: bisect, numpy, pandas, config 네 줄
grep -nE '^(import|from) ' utils/tension/core.py
# 5-4 테스트 — 기대: 14 passed(이번에 테스트를 더하지 않음)
PYTHONIOENCODING=utf-8 <py> -m pytest
# 5-5 도움말 — 기대: --end 하나
PYTHONIOENCODING=utf-8 <py> scripts/run_tension.py --help
# 5-6 (6절 검산 뒤) 출력 폴더가 깃 제외인지 — 기대: .gitignore의 data/tension/_* 규칙이 두 파일 모두에 나옴
git check-ignore -v data/tension/_check/일별_기본.csv data/tension/_check/일별_확장.csv
```

## 6. v0.1.4 대조 검산
부록 B를 `$B/verify_core_2cd.py`로 **글자 그대로** 저장하고 리포 루트에서:
```bash
PYTHONIOENCODING=utf-8 <py> "$B/verify_core_2cd.py"
```
- 입력은 F1이 만든 `data/tension/events_기본.csv`·`_확장.csv`(로컬, 깃 제외)와 판정표 사본. 없으면 `PYTHONIOENCODING=utf-8 <py> scripts/build_events.py --end 2026-10-27`로 다시 만든다(log에 적음).
- 검산이 `scripts/run_tension.py --end 2026-10-27`을 직접 실행해 `data/tension/_check/일별_*.csv`를 쓰고 그 파일을 읽어 대조한다(3절 — 깃 제외).
- 맞지 않으면: **옮기다 생긴 실수**는 고치고 다시 돌린다. **2절 규칙을 바꿔야만 맞는 경우**와 pandas 버전 차이로 보이는 경우(예: bool 열 반올림·문자열 자료형)는 고치지 말고, 다른 날 목록(최대 20일, 날짜·새 값·기준 값)을 log에 남기고 멈추고 보고한다. 기준값(일별·요약 CSV)은 고치지 않는다.
- 2c만 먼저 확인하고 싶으면 `daily_table` 전에 `stage_cuts`·`judge`·`step_down`으로 `단계_T`·`단계_판정`·`단계_최종`을 기준 CSV와 비교해도 된다(방법 자유 — log에 적음). 커밋 전 마지막 검산은 반드시 부록 B 전체.

## 7. 완료 조건 (모두 통과해야 "완료")
| # | 항목 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 기대 상태(PR #19 OPEN·draft 포함) |
| 2 | 1-1 판정표 | `i/lf  w/lf  attr/text eol=lf`, status에 안 보임 |
| 3 | 1-3 develop 맞추기 | merge 했거나 건너뜀(오른쪽 0), 충돌 없음, 14 passed |
| 4 | 1-4 CLAUDE.md | 1곳만 바뀜(diff 1+/1−) |
| 5 | 5-1 | 공개 함수 31개, 첫 줄 규칙 지킴 |
| 6 | 5-2·5-3 | grep 두 개 출력 없음, import 네 줄 |
| 7 | 5-4·5-5·5-6 | 14 passed · `--end`만 · 두 파일 모두 `data/tension/_*` 규칙으로 제외 |
| 8 | 6절 검산 | 마지막 줄 `전체: 통과` |
| 9 | 커밋 목록 `git log --oneline origin/develop..HEAD` | F2-1 커밋 5개 + 8절 순서(merge 커밋이 있으면 그 자리) |
| 10 | 8절 금지 경로 검사(매 커밋 전) | 매번 `OK` |
| 11 | 마지막 `git status --porcelain` | `?? .obsidian/` 하나만 |

## 8. 커밋 (한 커밋 한 목적, 이 순서)
금지 경로 검사(각 커밋 전 그대로 — 이번부터 `일별_`도 막는다: 결과 CSV 커밋은 F4. `_check/`는 깃 제외라 원래 안 잡힘):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F2-2 작업 프롬프트·설계 문서 반영` — 1-2
2. (1-3에서 merge 했으면 merge 커밋 — 기본 메시지 그대로)
3. `docs: CLAUDE.md 테스트 명령 -q 중복 제거` — 1-4
4. `feat: 계산 코어 2c 구간·판정·하강(⑨⑪⑫)` — `utils/tension/core.py`(`import bisect`는 2d 커밋에서 더해도 된다)
5. `feat: 계산 코어 2d 표시·문구·일별 조립(⑬~⑰)` — `utils/tension/core.py`
6. `feat: 긴장도 계산 최소판 run_tension.py` — `scripts/run_tension.py`
7. `docs: F2-2 보고서` — `docs/dev/reports/F2-2_report.md`, `F2-2_log.md`
- 4·5·6을 나누려면 2c까지 쓰고 2c 부분을 확인한 뒤 커밋, 2d를 더한 뒤 커밋, `run_tension.py`를 쓰고 부록 B 전체를 돌린 뒤 커밋한다(순서만 지키면 방법은 자유. 4·5 커밋 시점의 확인 방법은 log에 적음).

## 9. 동기화 · 푸시 · PR (새 PR을 만들지 않는다 — #19에 이어서)
```bash
git fetch origin
git merge origin/develop          # 1-3 뒤 develop이 또 바뀌었을 때만 무엇이 들어옴. 충돌 나면 git merge --abort 하고 멈추고 보고
PYTHONIOENCODING=utf-8 <py> -m pytest
git push
# PR #19 본문 갱신: 지금 본문을 "$B/pr_F2_old.md"로 받고(gh pr view 19 --json body -q .body > "$B/pr_F2_old.md"),
#   요약 첫 줄을 "F2-1(②~⑧·⑩)·F2-2(⑨·⑪~⑰·일별 CSV·run_tension.py 최소판)까지 — F2 검토(U9) 뒤 ready·병합"으로,
#   변경 사항에 8절 3~6, 테스트에 7절 결과(6절 검산 숫자 요약)를 더한 "$B/pr_F2.md"로
gh pr edit 19 --body-file "$B/pr_F2.md"
gh pr view 19 --json state,isDraft    # 기대: OPEN · true
```
병합·ready 전환하지 않는다. 보고서 커밋 뒤 다시 `git push` 하고 끝낸다.

## 10. 보고서 (CLAUDE.md 7절 — 두 파일)
`docs/dev/reports/F2-2_report.md`(60줄 이내): 1절 = 7절 표 11행 ✓/✗ · 6절 검산 숫자 요약 한 줄씩(시나리오별 T 구간·실수 열 최대차·다른 칸 0인 열 수·1~5거 %·현재 문구·run_tension 파일 검사·바이트 같음(참고)) · 작업트리에 남긴 것에 `data/tension/_check/`(깃 제외) 적기 · 2절 막힌 것 · 3절 기준과 다르게 한 것·고치고 싶은 것(완화할인 열 정의를 기준 그대로 옮겼다는 한 줄 포함 — 바꿀 의견이 있으면 함께) · 4절 바뀐 파일·작업트리에 남긴 것.
`docs/dev/reports/F2-2_log.md`: 1절 점검 출력, 1-1~1-4·5·6절 출력 전부, 커밋·푸시·PR 출력.

---

## 부록 A. 기준 구현 핵심 줄 (`진행 현황 및 계획 정리/v0.1_시험/` — 읽기만)
```python
# S3/s3_core.py
def stage(T, cuts):
    c1, c2, c3, c4 = cuts
    return pd.Series(np.select([T >= c4, T >= c3, T >= c2, T >= c1], [5, 4, 3, 2], 1), index=T.index)
def step_down(raw, n=7):
    out = np.empty(len(raw), int); cur = raw.iloc[0]; below = 0
    for i, r in enumerate(raw.values):
        if r >= cur: cur, below = r, 0
        else:
            below += 1
            if below >= n: cur, below = cur-1, 0
        out[i] = cur
# run: Rsum = sum(R[b] for b in bundles); P = DataFrame({'단계_T', '하한_E5', '하한_물리', '하한_사건'}); raw = P.max(axis=1)
#      T7 = T.rolling(7, min_periods=1).mean(); 최종 = step_down(raw)
# metrics: 위기 단계 = df.loc[t : t + 14일, '최종'].max()
# v0.1.4/compute_v014.py — compute
q = np.quantile(d0['T'][bm], [.7, .9, .95, .98]); cuts = tuple(np.round(q, 0))
for v in d['T7'].values: bisect.insort(srt, v); pe.append(bisect.bisect_right(srt, v) / len(srt) * 100)
# '잠정': d.index > DAYS[-1] - 6일 · '완화할인': 1 - d['T'] / Tg.mean(axis=1).replace(0, nan) → fillna(0)
# '그날까지_상위%': 100 - pe · 'A2자료': np.where(d.index > 2024-11-05, 'A2 자료 없음(2024-11-05까지)', '')
out['화면_단계문구'] = [f'{f}거 · 하강 중(판정 {j}거)' if j < f else f'{f}거' for f, j in zip(out['단계_최종'], out['단계_판정'])]
out['변화14_표시'] = out['T_표시7일'] - out['T_표시7일'].shift(14)
out['변화율14_표시'] = np.where(out['T_표시7일'].shift(14) >= 50, out['변화14_표시'] / out['T_표시7일'].shift(14) * 100, np.nan)
# 게이지 눈금 = d.loc[t : t + 14일, 'R합'].max() · '경계_x.5_주의' = any(abs(v - floor(v) - .5) < 1e-9 for v in q)
# 쓰기: out.round(3).rename_axis('날짜').to_csv(…, encoding='utf-8-sig')
```

## 부록 B. `$B/verify_core_2cd.py` (글자 그대로 저장)
```python
"""F2-2 검산(2c·2d) — 리포 루트에서 실행. core.daily_table과 run_tension.py 출력을 v0.1.4 일별·요약 CSV와 대조."""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
import config
from utils.tension import core, io as tio

REF = ROOT / "진행 현황 및 계획 정리" / "v0.1_시험" / "v0.1.4"
END = "2026-10-27"
TOL = 0.001
INT_COLS = ["단계_T", "하한_물리", "하한_E5", "하한_사건", "단계_판정", "단계_최종"]
BOOL_COLS = ["잠정", "물리_4거유형일"]
STR_COLS = ["A2자료", "화면_단계문구"]
summary = tio.read_csv_kr(REF / "요약_v014.csv", index_col=0)
type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
days = core.calc_days(config.CALC_START_DATE, END)
NY = len(days) / 365.25
ok = len(days) == 6144
print("python", sys.version.split()[0], "· numpy", np.__version__, "· pandas", pd.__version__)
print("계산 기간", days[0].date(), "~", days[-1].date(), len(days), "일")


def check(label, cond):
    global ok
    ok &= bool(cond)
    print(f"  {label} {'✓' if cond else '✗'}")


def diff_cells(new, ref, tol):
    """열마다 다른 칸 수와 실수 최대차. 실수 = |차| ≥ tol 또는 NaN 위치 다름 · 정수·참거짓 = 값 다름 · 문자열 = 빈칸을 ''로 보고 다름."""
    rows = []
    for c in ref.columns:
        a, b = new[c], ref[c]
        if c in INT_COLS:
            n, m = int((a.to_numpy("int64") != b.to_numpy("int64")).sum()), None
        elif c in BOOL_COLS:
            n, m = int((a.to_numpy(bool) != b.to_numpy(bool)).sum()), None
        elif c in STR_COLS:
            n, m = int((a.fillna("").astype(str).to_numpy() != b.fillna("").astype(str).to_numpy()).sum()), None
        else:
            av, bv = a.to_numpy(float), b.to_numpy(float)
            na = np.isnan(av) != np.isnan(bv)
            d = np.abs(np.nan_to_num(av) - np.nan_to_num(bv))
            n, m = int((na | (d >= tol)).sum()), float(d.max())
        rows.append((c, n, m))
    return rows


def report(rows):
    for c, n, m in rows:
        check(f"{c}: 다른 칸 {n}" + (f" · 최대차 {m:.6f}" if m is not None else ""), n == 0)


results = {}
for nm, col, bundles in [("기본", "기본", config.BUNDLES_BASE), ("확장", "확장(C5 포함)", config.BUNDLES_EXT)]:
    ev, exc = tio.load_events(ROOT / "data" / "tension" / f"events_{nm}.csv")
    ref = tio.read_csv_kr(REF / f"일별_v014_{nm}.csv", index_col=0, parse_dates=True)
    s = summary[col]
    print(f"\n[{nm}] 사건 {len(ev)}행 · load 제외 {len(exc)}")
    daily, info = core.daily_table(ev, days, bundles, type4)
    results[nm] = daily

    # --- 형식: 열 이름·순서, 날짜, 자료형
    check(f"열 {len(daily.columns)}개 — 이름·순서가 기준과 같음", list(daily.columns) == list(ref.columns))
    check("날짜 인덱스 같음 · 이름 '날짜'", daily.index.equals(days) and np.array_equal(daily.index.to_numpy(), ref.index.to_numpy()) and daily.index.name == "날짜")
    check("정수 열 int64 · 참거짓 열 bool", all(daily[c].dtype == "int64" for c in INT_COLS) and all(daily[c].dtype == bool for c in BOOL_COLS))

    # --- 2c·2d: 일별 전 열 (0절 완료 기준 포함)
    rows = diff_cells(daily, ref, TOL)
    report(rows)
    d = dict((c, (n, m)) for c, n, m in rows)
    check(f"[0절] 단계_최종 다른 날 {d['단계_최종'][0]} · T_원값 최대차 {d['T_원값'][1]:.6f} < 0.001", d["단계_최종"][0] == 0 and d["T_원값"][1] < 0.001)

    # --- 요약 값
    L = daily["단계_최종"]
    check(f"T구간 {'/'.join(f'{v:g}' for v in info['cuts'])} (기준 {s['T구간(2·3·4·5거 시작)']})", "/".join(f"{v:g}" for v in info["cuts"]) == s["T구간(2·3·4·5거 시작)"])
    check(f"T구간 반올림 전 {'/'.join(f'{v:.2f}' for v in info['quantiles_raw'])} (기준 {s['T구간_반올림전']})", "/".join(f"{v:.2f}" for v in info["quantiles_raw"]) == s["T구간_반올림전"])
    check(f"경계_x.5_주의 {info['half_warning']} (기준 {s['경계_x.5_주의']})", str(info["half_warning"]) == s["경계_x.5_주의"])
    for k in range(1, 6):
        v = round((L == k).mean() * 100, 1)
        check(f"{k}거% {v} (기준 {s[f'{k}거%']})", v == float(s[f"{k}거%"]))
    v = round((L.diff().fillna(0) != 0).sum() / NY, 1)
    check(f"바뀜/년 {v} (기준 {s['바뀜/년']})", v == float(s["바뀜/년"]))
    cs = core.crisis_window_max(L)
    gm = core.crisis_window_max(daily["원점수_게이지"])
    for name, _, _ in config.CRISIS_LIST:
        check(f"위기 {name}: 단계 {int(cs[name])} (기준 {s[name]}) · 게이지 {round(float(gm[name]), 1)} (기준 {s['게이지_' + name]})",
              int(cs[name]) == int(s[name]) and round(float(gm[name]), 1) == float(s["게이지_" + name]))
    yr = {"2018 평균단계": round(L.loc["2018"].mean(), 2), "2018 3거이상일": int((L.loc["2018"] >= 3).sum()),
          "2021 평균단계": round(L.loc["2021"].mean(), 2), "2023 4거이상%": round((L.loc["2023"] >= 4).mean() * 100, 0),
          "2023 5거%": round((L.loc["2023"] == 5).mean() * 100, 0), "현재(10-27)": int(L.iloc[-1])}
    other = daily[["단계_T", "하한_물리", "하한_사건"]].max(axis=1)
    bm = core.base_mask(days)
    last = daily.iloc[-1]
    more = {"E5가 판정을 올린 날": int((daily["하한_E5"] > other).sum()),
            "원점수 기준기간 평균": round(daily["원점수_게이지"][bm].mean(), 2),
            "T원값 최대": round(daily["T_원값"].max()), "표시선 최대": round(daily["T_표시7일"].max()),
            "현재 표시(잠정)": round(last["T_표시7일"], 1), "현재 그날까지 상위%": round(last["그날까지_상위%"], 1),
            "현재 원점수": round(last["원점수_게이지"], 1), "현재 14일 변화": round(last["변화14_표시"], 1)}
    for k, v in {**yr, **more}.items():
        check(f"{k} {v} (기준 {s[k]})", float(v) == float(s[k]))
    check(f"현재 화면 단계 '{last['화면_단계문구']}' (기준 '{s['현재 화면 단계']}')", last["화면_단계문구"] == s["현재 화면 단계"])

    # --- END를 늘려도 과거 값은 그대로(대응표 3절) — 잠정 열만 바뀜
    days2 = core.calc_days(config.CALC_START_DATE, "2026-11-10")
    d2, _ = core.daily_table(ev, days2, bundles, type4)
    same = d2.loc[days].drop(columns="잠정").equals(daily.drop(columns="잠정"))
    n_prov = int((d2.loc[days, "잠정"] != daily["잠정"]).sum())
    check(f"END 2026-11-10로 늘려도 2026-10-27까지 값 같음(잠정 뺌): {same} · 잠정이 바뀐 날 {n_prov} (기대 6)", same and n_prov == 6)

# --- run_tension.py 최소판: 파일로 쓴 결과
print("\n[run_tension.py --end 2026-10-27]")
r = subprocess.run([sys.executable, "scripts/run_tension.py", "--end", END], capture_output=True, text=True, encoding="utf-8")
print(r.stdout.rstrip())
if r.stderr.strip():
    print(r.stderr.rstrip())
check(f"종료 코드 {r.returncode}", r.returncode == 0)
for nm in ["기본", "확장"]:
    path = ROOT / config.TENSION_DATA_DIR / "_check" / f"일별_{nm}.csv"
    raw = path.read_bytes() if path.exists() else b""
    n_lines, has_bom, has_crlf = raw.count(b"\n"), raw.startswith(b"\xef\xbb\xbf"), b"\r\n" in raw
    check(f"{path.name}: BOM {has_bom} · CRLF {has_crlf} · 줄 수 {n_lines} (기대 True · False · 6145)", has_bom and not has_crlf and n_lines == 6145)
    got = tio.read_csv_kr(path, index_col=0, parse_dates=True)
    ref = tio.read_csv_kr(REF / f"일별_v014_{nm}.csv", index_col=0, parse_dates=True)
    check("  열·날짜가 기준 파일과 같음", list(got.columns) == list(ref.columns) and np.array_equal(got.index.to_numpy(), ref.index.to_numpy()) and got.index.name == "날짜")
    rows = diff_cells(got, ref, TOL + 1e-9)   # 둘 다 셋째 자리 반올림 — 반올림 경계에서 마지막 자리 1 차이(0.001)까지 허용
    bad = [(c, n) for c, n, _ in rows if n]
    exact = sum(int((got[c].fillna("").astype(str) != ref[c].fillna("").astype(str)).sum()) for c in ref.columns)
    check(f"  값: 허용 밖 다른 칸 {sum(n for _, n in bad)} {bad if bad else ''} · 글자까지 다른 칸 {exact}(참고)", not bad)
    print(f"  (참고) 기준 파일과 바이트까지 같음: {raw == (REF / f'일별_v014_{nm}.csv').read_bytes()}")

print("\n전체:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
```

## 부록 C. `$B/fix_claude_md.py` (글자 그대로 저장)
```python
"""F2-2 1-4 — CLAUDE.md 5절 테스트 명령에서 -q 하나만 뺀다(pytest.ini addopts에 이미 -q). 바이트로 바꿔 줄바꿈을 그대로 둔다."""
from pathlib import Path

p = Path("CLAUDE.md")
b = p.read_bytes()
old = "`<작업 프롬프트가 지정한 python.exe> -m pytest -q`".encode("utf-8")
new = "`<작업 프롬프트가 지정한 python.exe> -m pytest`".encode("utf-8")
n = b.count(old)
assert n == 1, f"바꿀 문자열이 {n}번 있음 — 멈춤"
p.write_bytes(b.replace(old, new))
print("CLAUDE.md: 테스트 명령 1곳 바꿈")
```
