# F1 작업 프롬프트 — 입력 로더(io.py)·사건표 생성(build_events.py)

작성 2026-10-29 · 구현 메인(채팅 ②) → Claude Code · 브랜치 `feature/tension-io`(최신 `develop`에서 새로) · PR 대상 `develop`
상태: **실행** (2026-10-29 사용자 확인 — 범위 = 원자료 한 번에 · 제외기록 깃 제외 · io 중복 규칙 그대로 · 입력 파일 기록 넣기)
권장 모델·노력: Opus 5.5 · 중간

> Claude Code에게: 이 파일을 끝까지 읽고 그대로 수행한다. 여기 없는 일은 하지 않는다. 판단이 필요하면 고치지 말고 보고서 2절에 적고 멈춘다.
> **python:** `C:/Users/money/anaconda3/envs/python311/python.exe` (아래 `<py>`). `conda run`은 쓰지 않는다. **`$B`** = `$HOME/bongsu_F1_20261029`(셸이 새로 열리면 다시 정의).
> 금지: `rebase`·`stash`·`reset --hard`·`push --force`·`pip install`, `develop`·`main` 직접 커밋, PR 병합·ready 전환, `data/raw/**`·`진행 현황 및 계획 정리/**` 수정, 기준 스크립트(`s2lib.py`·`team.py`·`build_v013_input.py`·`build_v014_input.py`) **import** — 읽고 옮기기만 한다.

---

## 0. 목표와 정해진 것
- **목표:** ① `utils/tension/io.py` — 사건표·유형판정표를 읽고 검증하는 함수, CSV 쓰기 함수. ② `scripts/build_events.py` — **로컬 원자료(`data/raw/긴장도_산출식_세부_기준/`)에서 한 번에** 사건표 기본·확장과 제외기록을 만든다. ③ 유형판정표 사본을 `data/tension/`에 둔다. ④ 만든 사건표가 v0.1.4 사건표(기본 720행·확장 941행)와 같음을 검산한다.
- **왜 "한 번에"인가:** v0.1.4 사건표는 원래 3단계로 만들어졌다(`S2/s2lib.build_x` → `v0.1.3/build_v013_input.py` → `v0.1.4/build_v014_input.py`). 리포 코드가 깃 제외 작업 폴더의 중간 CSV를 입력으로 받지 않도록 세 단계의 규칙을 하나로 합친다(규칙은 바꾸지 않는다).
- **구현 메인이 미리 확인한 것 `[확인 10-29]`:** 3절 표대로 현재 원자료에서 한 번에 만들면 v0.1.4 기본·확장 사건표와 사건ID·날짜·요소·묶음·사건명·행 순서가 모두 같고, S는 엑셀 수식 값의 부동소수 표기 차이(예 `6.8999999999999995` vs `6.9`)뿐이다(34행, 차 < 1e-15). 그래서 S는 값 차이 < 1e-9로 판정한다.
- **기준 구현과 다르게 하는 것(구현 메인 결정 — 결과는 같음):**
  1. 계산 기간 끝(`--end`)을 모든 요소에 적용(기준은 C5·A4·A6에만 적용. 2026-10-27 뒤 날짜 행은 지금 없음).
  2. 엑셀 찾기 = "파일 이름 패턴 + 그 시트가 있는 파일이 **정확히 1개**". 기준 `team.sheet`는 패턴의 첫 파일을 집어서 `*C2_*`가 C1 파일(`…C1_34건_…_C2_전처리기준…`)에 걸린다.
  3. A6 시트 이름 `01_A6_17건_점수`(팀 파일이 v0.2로 바뀜. 기준 `build_x`는 `01_A6_9건_점수`).
  4. 제외기록에 ⑤⑥⑦(날짜 없음·기존 제외 규칙·사용여부 N)을 더 적는다(ADR-004 "제외 + 기록"). 기준 v0.1.3 기록의 ①③④는 그대로.
- 원자료 폴더 사실 `[확인 10-29]`: A1·A3·A4·A7 시트에는 `사용여부` 열이 없다. A4는 날짜 없는 행 18개. 요소 F2 점수표의 `분야보정`은 `config.F2_FIELD_FACTOR`와 668행 모두 일치.

## 1. 시작 점검 · develop 최신화 · 브랜치 · 이슈 (이 순서. 기대와 다르면 멈추고 보고)
```bash
git status --porcelain
#   기대(순서 무관): " M docs/decisions.md", " M docs/dev/식_함수_대응표.md", " M docs/dev/진행기록.md",
#                   " M docs/tension/산출식_정리.md", "?? docs/dev/tasks/F1_io.md", "?? .obsidian/"
git branch --show-current          # 기대: feature/tension-scaffold
git fetch origin
git log --oneline -1 origin/develop   # 기대: 9e7ed0d Merge pull request #15 … (또는 그 뒤 커밋 — 그러면 log에 적고 계속)
git rev-list --left-right --count feature/tension-scaffold...origin/develop   # 기대: 0	1 (병합 커밋 하나만 원격에 더 있음)

# 1-1 구현 메인이 고친 문서 백업(리포 밖)
B="$HOME/bongsu_F1_20261029"; mkdir -p "$B/docs"
for f in docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md docs/dev/tasks/F1_io.md; do
  mkdir -p "$B/docs/$(dirname "$f")"; cp "$f" "$B/docs/$f"; done
git diff --stat > "$B/docs_diff_stat.txt"; cat "$B/docs_diff_stat.txt"

# 1-2 되돌리고 develop으로
git restore docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md
git switch develop
git pull --ff-only origin develop        # 실패하면 멈추고 보고
git log --oneline -1                     # origin/develop과 같아야 함

# 1-3 백업 되살리기 → 브랜치
for f in docs/decisions.md docs/dev/식_함수_대응표.md docs/dev/진행기록.md docs/tension/산출식_정리.md docs/dev/tasks/F1_io.md; do cp "$B/docs/$f" "$f"; done
git status --porcelain                   # 1절 첫 줄 기대와 같아야 함
git switch -c feature/tension-io

# 1-4 이슈: 본문 "$B/issue_F1.md"를 .github/ISSUE_TEMPLATE/feature.md 양식으로(배경 = 0절, 범위 = 2~5절 목록, 하지 않을 것 = 11절, 완료 조건 = 7절 표를 체크박스로)
gh issue create --title "[FEAT] 긴장도 입력 로더·사건표 생성(F1)" --label feat --body-file "$B/issue_F1.md"
<py> --version; <py> -c "import numpy, pandas, openpyxl; print(numpy.__version__, pandas.__version__, openpyxl.__version__)"
```

## 2. `utils/tension/io.py` — 계약 (이름·서명 그대로)
모듈 docstring 첫 줄: `"""사건표·유형판정표 읽기·검증과 CSV 쓰기 (F1). 파일 경로만 받고 Streamlit을 모른다."""`
```python
EVENT_COLUMNS = ("사건ID", "date", "요소", "묶음", "S", "사건명")
KNOWN_BUNDLES = ("핵·미사일", "군사 과시", "위협 언어·교리", "제재·압박", "물리 충돌", "북러 밀착", "북러(표시만)", "완화")
EXCLUDED_COLUMNS = EVENT_COLUMNS + ("사유",)
TYPE4_COLUMNS = ("사건ID", "date", "요소", "S", "사건명", "판정유형", "4거유형", "봉수원뜻", "판정근거(팀 요약 원문 문구)", "비고")

def read_csv_kr(path, **kwargs) -> pd.DataFrame          # pd.read_csv(path, encoding="utf-8-sig", **kwargs)
def write_csv(df, path, index=False) -> None              # 상위 폴더 만들기, encoding="utf-8-sig", lineterminator="\n"
def load_events(path) -> tuple[pd.DataFrame, pd.DataFrame]  # (사건표, 제외기록)
def load_type4_table(path) -> pd.DataFrame
def type4_event_ids(table) -> frozenset[str]              # 4거유형 == "Y"
def check_type4_against_events(table, events) -> pd.DataFrame   # 문제 행(빈 표면 문제 없음)
```
- `load_events` 규칙
  1. 모든 열을 문자열로 읽는다(`dtype=str`, `keep_default_na=False`). 열 이름·순서가 `EVENT_COLUMNS`와 다르면 `ValueError`(구조 오류는 제외가 아니라 실패).
  2. 아래 행은 **0점으로 두지 않고 빼서** 제외기록(열 `EXCLUDED_COLUMNS`, 원래 문자열 그대로 + `사유`)에 남긴다(ADR-004): `사건ID`·`요소`·`묶음` 빈칸 → `빈칸: <열>` / `date`가 `%Y-%m-%d`로 안 읽힘 → `날짜 형식` / `S`가 숫자가 아님(빈칸 포함) → `S 숫자 아님` / `묶음`이 `KNOWN_BUNDLES`에 없음 → `묶음 모름: <값>`. **S = 0은 정상 행**이다(v0.1.4에 E5 0점 2행).
  3. 중복: 6개 열이 모두 같은 행은 첫 행만 남기고 나머지를 `중복 행`으로 기록. 같은 `사건ID`인데 내용이 다르면 `ValueError`(어느 쪽이 맞는지 코드가 정하지 않는다).
  4. 반환 사건표: `date` = datetime64(시각 없음), `S` = float64, 나머지 문자열. `date`·`사건ID` 순 정렬(`kind="mergesort"`), 인덱스 0부터. 날짜 범위로 거르지 않는다(계산 기간 밖 처리는 core 몫).
- `load_type4_table`: `read_csv_kr`(판정표는 BOM 없음 — 그래도 같은 함수). 열 이름·순서가 `TYPE4_COLUMNS`와 다르면, `4거유형`(공백 제거·대문자)이 Y/N 밖이면, `사건ID`가 중복이면 `ValueError`. `date`는 datetime64.
- `check_type4_against_events`: 열 `사건ID, 문제`. 문제 = `사건표에 없음` / `날짜 다름(판정표 …, 사건표 …)` / `요소가 A3·A7 아님`.
- pandas 3.0의 기본 문자열 dtype(`str`)에서도 같게 동작해야 한다(`object` dtype을 가정하지 않는다).

## 3. `scripts/build_events.py` — 원자료 → 사건표 (규칙 표 그대로)
- 맨 위에서 리포 루트를 `sys.path`에 넣고(`Path(__file__).resolve().parents[1]`) `config`·`utils.tension.io`를 쓴다. `진행 현황 및 계획 정리/` 아래 파일은 읽지 않고, 코드·주석·docstring에 그 폴더 이름도 쓰지 않는다(기준 위치는 `v0.1_시험/S2/s2lib.py build_x()`처럼 적는다).
- 인자: `--raw-dir`(기본 `data/raw/긴장도_산출식_세부_기준`) · `--out-dir`(기본 `config.TENSION_DATA_DIR`) · `--start`(기본 `config.CALC_START_DATE`) · `--end`(기본 `config.END_DATE`, None이면 실행일). 출력: `<out-dir>/events_기본.csv` · `events_확장.csv` · `events_제외기록.csv` · `events_입력파일.csv`(넷 다 `.gitignore`의 `data/tension/events_*.csv`로 깃 제외).
- 함수 `build_events(raw_dir, start, end) -> tuple[base, ext, excluded]`와 `main()`으로 나눈다(F3에서 테스트할 수 있게).
- **엑셀 읽기**(기준 `S2/team.py`의 `sheet()` 이식): `<raw-dir>/*/<패턴>`의 `.xlsx` 중 그 시트가 있는 파일이 정확히 1개여야 한다(0개·2개 이상이면 파일 목록을 출력하고 멈춤). `openpyxl.load_workbook(f, data_only=True, read_only=True)`, 첫 행 = 열 이름(`str`), 첫 열이 비어 있는 행은 버림(기록 안 함). 쓴 파일 이름을 출력한다.
- **행 만들기**(기준 `build_x`의 `add()`): 날짜 = `pd.to_datetime(str(값)[:10], errors="coerce")`를 **한 값씩, 형식 지정 없이**(기준과 같게) · S = `float(점수 열)` · 사건명 = `str(이름 열)[:60]`. 사용할 행(아래 (라))의 점수가 비었거나 숫자가 아니면 멈추고 보고(기준 코드도 여기서 실패한다 — C5는 ④로 기록).

| 요소 | 원자료(패턴 · 시트 또는 파일) | 사용여부 | 추가 제외 (기록 코드) | 날짜 열 | 점수 열 | 묶음 |
|---|---|---|---|---|---|---|
| A1 | `*A1_*` · `02_PRK6건_시험점수` | 열 없음 | — | 시작일 | 위력반영점수 | 핵·미사일 |
| A2 | `*A2_*` · `01_294건_적용본` | Y만 (N → ③) | — | 시작일 | 시험 점수 | 핵·미사일 |
| B1 | `*B1_*` · `B1_사건별시험` | Y만 (N → ⑦) | `중복연계_표시 == "A2 동일 사건 명시"` (⑥) | 시작일 | 시험점수 | 핵·미사일 |
| A3 | `*A3_*` · `01_Y62_사건판정` | 열 없음 | `A3-0059` (①, 대표 A7-0120) | 시작일 | 사건시험점수 | 물리 충돌 |
| A7 | `*A7_*` · `A7_사건별_맥락검토` | 열 없음 | — | 시작일 | 기존 점수 | 물리 충돌 |
| A4 | `*A4_*` · `01_39건_점수시험` | 열 없음 | — | 시작일 | 사건시험점수 | 군사 과시 |
| A5 | `*A5_*` · `01_사건별117건` | Y만 (⑦) | — | 시작일 | 사건 시험점수 | 군사 과시 |
| A6 | `*A6_*` · `01_A6_17건_점수` | Y만 (⑦) | — | 시작일 | 시험점수 | 군사 과시 |
| B4 | `*B4_*` · `B4_41건_점수시험` | Y만 (⑦) | `태세방향 == "완화"` (⑥) | 시작일 | 시험점수 | 위협 언어·교리 |
| C1 | `*C1_*` · `C1_전건_재검토` | Y만 (⑦) | — | **날짜** | v0.2 점수 | 위협 언어·교리 |
| C2 | `*C2_*` · `C2_사건별_v03비교` | Y만 (⑦) | `사건ID == "C2-0035"` (⑥ 9·19 군사합의 체결, 완화) | 시작일 | v0.2 점수 | 위협 언어·교리 |
| C3 | `*C3_v0.7*` · `사건별_66건_시험` | Y만 (⑦) | `사건ID ∈ {C3-0050, C3-0019, C3-0046, C3-0063}` (⑥ 같은 회담) · `협의축 == "북러"` (⑥ E5가 대표) | 시작일 | 시험점수 | 위협 언어·교리 |
| E5 | 파일 `E/E5_점수표_v2_2026-10-27.csv` | 없음(전부) | — | 시작일 | S | `기준선대상 == "Y"` → 북러 밀착, 그 밖 → 북러(표시만) |
| F2 | 파일 `F/F2_점수표_v4_2026-10-27.csv` | Y만 (⑦) | `사건ID`가 `F/F2_연도별회담_정제.csv`에 없음 (⑥) | 시작일 | S_보정 | 완화 |
| C5 (확장만) | `*C5_*` · `C5_282건_사건별시험` | Y이고 시험점수 있음 (아니면 ④) | — | 시작일 | 시험점수 | 제재·압박 |

- "열 없음" 요소에 `사용여부` 열이 생겼으면 멈추고 보고한다(새 규칙이 필요함). CSV는 `read_csv_kr(..., dtype=str)`.
- **적용 순서:** (가) 날짜가 읽히고 `start ≤ date ≤ end`인 행만 다룬다 — 날짜 없음은 ⑤로 기록(사용여부 N 행은 제외), 기간 밖은 기록하지 않는다. (나) 사용여부 N → ③·④·⑦. (다) 추가 제외 → ①·⑥. (라) 남은 행 = 사건표.
- **기본** = C5를 뺀 전부, **확장** = 기본 + C5. 둘 다 `date`·`사건ID` 순(`kind="mergesort"`), 열 `EVENT_COLUMNS`, `date`는 `YYYY-MM-DD` 문자열로 `write_csv`.
- **제외기록**(`events_제외기록.csv`) 열 = `사건ID, date, 요소, S, 대표ID, 사유`(v0.1.3 `제외기록_v013.csv`와 같음). 사유 문구:
  - ① `① A3–A7 같은 사건(2024-10-15 도로 폭파) — A7 대표, 계산 제외(0점 아님)`, 대표ID `A7-0120`
  - ③ `③ 같은 날 1회(팀 사용여부 N): ` + `제외사유`, 대표ID = `제외사유`에서 정규식 `(A2-\d{4}) 유지`로 찾은 값(없으면 빈칸), S = 시험 점수
  - ④ `④ 팀 사용여부 N: ` + `제외사유`, S 빈칸(확장에만 해당)
  - ⑤ `⑤ 날짜 없음(일별 반영 보류)` · ⑥ `⑥ 기존 규칙: <위 표의 괄호 설명>` · ⑦ `⑦ 팀 사용여부 N: ` + (`제외사유` 열이 있으면 그 값)
- **φ 대조**(요소 F2, 결과는 바꾸지 않음): 점수표 전 행에서 `분야보정 == config.F2_FIELD_FACTOR[분야군]`이고 `|S × 분야보정 − S_보정| < 1e-9`인지 확인해 `φ 대조 통과 <행 수>`를 출력. 하나라도 어긋나면 멈추고 보고.
- **입력 파일 기록**(`events_입력파일.csv`, 사용자 10-29 — 다음 계산에서 결과가 바뀐 이유를 찾기 위함. 결과에는 영향 없음): 이번 실행에서 읽은 파일마다 한 행. 열 = `요소, 파일, 크기, SHA256` — `파일`은 `--raw-dir` 기준 상대 경로(`/` 구분), `크기`는 바이트, `SHA256`은 `hashlib.sha256`으로 파일 전체를 읽어 낸 16진수 소문자. 행 = 엑셀 13개(A1~A7·B1·B4·C1·C2·C3·C5) + CSV 3개(E5 점수표 · F2 점수표 · F2 정제 목록) = 16행, `요소`·`파일` 순 정렬. 실행 시각은 넣지 않는다(같은 입력이면 같은 파일이 나오게).
- 끝에 출력: 쓴 파일 이름(엑셀 13개·CSV 3개), `(요소, 묶음)`별 행 수·S 합, `기본 <n>행 / 확장 <n>행 / 제외기록 <n>행`, 사유 코드별 개수.

## 4. 유형판정표 사본 (D1 — 커밋)
```bash
cp "진행 현황 및 계획 정리/v0.1_시험/단계5/V1_물리사건_유형판정표.csv" data/tension/물리사건_유형판정표.csv
cmp "진행 현황 및 계획 정리/v0.1_시험/단계5/V1_물리사건_유형판정표.csv" data/tension/물리사건_유형판정표.csv && echo same
```
바이트 그대로 복사한다(다시 쓰지 않는다 — BOM 없음 유지). 경로는 `config.TYPE4_TABLE_PATH`와 같다.

## 5. `tests/test_io.py` — 작은 합성 자료(`tmp_path`)로
1. BOM 있는 파일과 없는 파일을 같은 내용으로 읽는다.
2. 열 순서가 다르거나 열이 빠지면 `ValueError`.
3. 날짜 형식 오류·S 빈칸·모르는 묶음·빈 사건ID 행은 빠지고 제외기록에 사유와 함께 남는다. S = 0 행은 남는다.
4. 6개 열이 같은 중복 행은 하나만 남고 기록된다. 같은 사건ID·다른 내용은 `ValueError`.
5. 반환 사건표가 `date`·`사건ID` 순이고 `date` dtype이 datetime64, `S`가 float64.
6. 판정표: 정상 로드와 Y 집합 / `4거유형` 값 오류 → `ValueError` / 사건ID 중복 → `ValueError` / `check_type4_against_events`가 "사건표에 없음"·"날짜 다름"을 찾는다.
7. `write_csv`: 파일이 BOM(`EF BB BF`)으로 시작하고 `\r\n`이 없으며, `read_csv_kr`로 다시 읽으면 같다.
원자료·기준 CSV가 필요한 테스트는 만들지 않는다(깃 밖 파일 — 회귀 테스트는 F3).

## 6. v0.1.4 대조 검산
부록 B 스크립트를 `$B/verify_events.py`로 저장하고 리포 루트에서 실행한다:
```bash
<py> scripts/build_events.py --end 2026-10-27
<py> "$B/verify_events.py"
```
- 맞지 않으면: **옮기다 생긴 실수**(기준 코드와 다르게 옮긴 곳)는 고치고 다시 돌린다. **3절 표(규칙)를 바꿔야만 맞는 경우**와 pandas 버전 차이로 보이는 경우는 고치지 말고, 다른 행 목록(최대 20행)을 log에 남기고 멈추고 보고한다.

## 7. 완료 조건 (모두 통과해야 "완료")
| # | 명령 | 기대 |
|---|---|---|
| 1 | 1절 점검 | 기대 상태와 같음 |
| 2 | `<py> -c "import utils.tension.io as m; print(m.EVENT_COLUMNS, len(m.KNOWN_BUNDLES))"` | `('사건ID', 'date', '요소', '묶음', 'S', '사건명') 8` |
| 3 | `<py> -m pytest -q` | 전부 통과(스모크 3 + test_io) |
| 4 | `<py> scripts/build_events.py --end 2026-10-27` | 오류 없음 · `φ 대조 통과 668` · `기본 720행 / 확장 941행` · `events_입력파일.csv` 16행(두 번 돌려도 바이트 같음 — `cmp`) |
| 5 | `git check-ignore -v data/tension/events_기본.csv data/tension/events_확장.csv data/tension/events_제외기록.csv data/tension/events_입력파일.csv` | 4개 모두 `events_*.csv` 규칙 |
| 6 | `<py> "$B/verify_events.py"` | 마지막 줄 `전체: 통과` |
| 7 | 4절 `cmp` | `same` |
| 8 | 아래 블록 8 | `정상` |
| 9 | 아래 블록 9 | 두 grep 모두 출력 없음 |
| 10 | `git log --oneline develop..HEAD` | 8절 커밋 순서 |
| 11 | 8절 금지 경로 검사(매 커밋 전) | 매번 `OK` |
| 12 | 마지막 `git status --porcelain` | `?? .obsidian/` 하나만 |

표 8·9의 명령(표 안에 두면 `|`가 깨지므로 여기에):
```bash
# 8
git check-ignore data/tension/물리사건_유형판정표.csv && echo 잘못 || echo 정상
# 9 — 기준 스크립트 import 없음 · 작업 폴더 이름 없음
grep -nE '^[[:space:]]*(import|from)[[:space:]]+(s2lib|team|build_v01)' scripts/build_events.py utils/tension/io.py
grep -n '진행 현황' scripts/build_events.py utils/tension/io.py
```

## 8. 커밋 (한 커밋 한 목적, 이 순서)
금지 경로 검사(각 커밋 전 그대로 실행):
```bash
git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_' && echo "금지경로 있음 — 멈춤" || echo "OK"
```
1. `docs: F1 작업 프롬프트·설계 문서 반영` — `docs/dev/tasks/F1_io.md`, `docs/dev/진행기록.md`, `docs/dev/식_함수_대응표.md`, `docs/decisions.md`, `docs/tension/산출식_정리.md`(내용 수정 없이 — U2)
2. `feat: 사건표·유형판정표 로더 io.py 추가` — `utils/tension/io.py`, `tests/test_io.py`
3. `feat: 원자료에서 사건표 만드는 build_events 추가` — `scripts/build_events.py`
4. `chore: 물리사건 유형판정표 사본 추가` — `data/tension/물리사건_유형판정표.csv`
5. `docs: F1 보고서` — `docs/dev/reports/F1_report.md`, `F1_log.md`

## 9. 동기화 · 푸시 · PR
```bash
git fetch origin
git merge origin/develop          # 충돌 나면 git merge --abort 하고 멈추고 보고
<py> -m pytest -q
git push -u origin feature/tension-io
# 본문 "$B/pr_F1.md" = .github/pull_request_template.md 양식(요약 · closes #<1-4 이슈> · 변경 = 8절 · 테스트 = 7절 결과 · 체크리스트)
gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 입력 로더·사건표 생성(F1)" --body-file "$B/pr_F1.md"
```
병합하지 않는다. 보고서 커밋(8절 5) 뒤 다시 푸시하고 끝낸다.

## 10. 보고서 (CLAUDE.md 7절 — 두 파일)
`F1_report.md`(60줄 이내): 1절 = 7절 표 12행 ✓/✗ · 2절 막힌 것 · 3절 기준과 다르게 한 것(0절 1~4 외에 더 있으면) · 4절 바뀐 파일. 사유 코드별 제외 수(①③④⑤⑥⑦)를 1절 6행 근거에 한 줄로.
`F1_log.md`: 1절 점검 출력, 4·6절 실행 출력 전부, pytest 출력, 커밋·푸시·PR 출력.

## 11. 하지 않는 것
- 계산 코드(`core.py`·`run_tension.py`·`charts.py`), 결과 CSV(일별·요약) — F2~F4
- `config.py`·`requirements.txt`·`CLAUDE.md`·`README.md` 수정, 의존성 추가
- 사건표·제외기록 커밋(깃 제외 파일), JSON 출력
- 규칙(3절 표·제외 순서·점수 열) 변경 — 이상하면 보고서 3절에 제안만
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정

---

## 부록 A. 기준 구현 위치 (읽기만 — `진행 현황 및 계획 정리/v0.1_시험/` 아래)
- `S2/s2lib.py` `build_x()`(241~300행) — 요소별 시트·열·거르기. 확정 옵션 = `S2/e5v2.py` 7행 `FIN = dict(c3='all', c2wan='keep', e5=True, c3nr='drop', c3dup='rules', c3weak='keep')` (그 밖의 인자는 기본값: `b1dup='team'`, `c3place='a'`, `f2raw=False`, `c3held=None`)
- `S2/team.py` `sheet()`(6~11행) — 엑셀 읽기
- `v0.1.3/build_v013_input.py` — ① A3-0059 · ③ A2 같은 날 1회 · ④ C5, 제외기록 문구
- `v0.1.4/build_v014_input.py` — A4·A6 보완(이제 팀 파일에 들어 있어 3절 표로 자연히 반영됨)
- 검산 기준: `v0.1.4/사건표_v014_기본.csv`·`_확장.csv`, `v0.1.3/제외기록_v013.csv`(① 1 · ③ 129 · ④ 2), 판정표 `단계5/V1_물리사건_유형판정표.csv`(37행, Y 16)

## 부록 B. `$B/verify_events.py` (글자 그대로 저장)
```python
"""F1 검산 — 리포 루트에서 실행. 새 사건표·제외기록·판정표 사본을 v0.1.4 기준과 대조."""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from utils.tension import io as tio

REF = ROOT / "진행 현황 및 계획 정리" / "v0.1_시험"
COLS = ["사건ID", "date", "요소", "묶음", "S", "사건명"]
KEYS = ["사건ID", "date", "요소", "묶음", "사건명"]
ok = True
for nm, ref, n in [("기본", "v0.1.4/사건표_v014_기본.csv", 720), ("확장", "v0.1.4/사건표_v014_확장.csv", 941)]:
    path = ROOT / "data" / "tension" / f"events_{nm}.csv"
    new = tio.read_csv_kr(path, dtype={"사건ID": str})
    old = tio.read_csv_kr(REF / ref, dtype={"사건ID": str})
    same_cols = list(new.columns) == COLS
    same_len = len(new) == len(old) == n
    same_keys = same_len and bool((new[KEYS].astype(str).to_numpy() == old[KEYS].astype(str).to_numpy()).all())
    sdiff = float((new["S"].astype(float) - old["S"].astype(float)).abs().max()) if same_len else float("nan")
    ev, exc = tio.load_events(path)
    r = same_cols and same_keys and sdiff < 1e-9 and len(exc) == 0 and len(ev) == n
    ok &= r
    print(nm, "| 열", same_cols, "| 행", len(new), len(old), "| 키·순서 동일", same_keys, "| S 최대차", sdiff, "| load 제외", len(exc), "→", "통과" if r else "실패")
    if same_len and not same_keys:
        bad = (new[KEYS].astype(str).to_numpy() != old[KEYS].astype(str).to_numpy()).any(axis=1)
        print(pd.concat([new[bad].head(20), old[bad].head(20)], axis=1).to_string())

x13 = tio.read_csv_kr(REF / "v0.1.3" / "제외기록_v013.csv", dtype=str)
xn = tio.read_csv_kr(ROOT / "data" / "tension" / "events_제외기록.csv", dtype=str, keep_default_na=False)
for code in ["①", "③", "④"]:
    a = x13[x13["사유"].str.startswith(code)]
    b = xn[xn["사유"].str.startswith(code)]
    r = set(a["사건ID"]) == set(b["사건ID"])
    if code == "③" and r:
        m = a.merge(b, on="사건ID", suffixes=("", "_새"))
        r = bool((m["대표ID"].fillna("") == m["대표ID_새"].fillna("")).all())
    ok &= r
    print(code, "v013", len(a), "새", len(b), "→", "동일" if r else f"다름 v013만 {sorted(set(a['사건ID']) - set(b['사건ID']))[:5]} 새만 {sorted(set(b['사건ID']) - set(a['사건ID']))[:5]}")
print("새 제외기록 사유 코드별:", xn["사유"].str[:1].value_counts().to_dict())

t = tio.load_type4_table(ROOT / "data" / "tension" / "물리사건_유형판정표.csv")
ids = tio.type4_event_ids(t)
ev, _ = tio.load_events(ROOT / "data" / "tension" / "events_기본.csv")
prob = tio.check_type4_against_events(t, ev)
r = len(t) == 37 and len(ids) == 16 and len(prob) == 0
ok &= r
print("판정표", len(t), "행 · Y", len(ids), "· 사건표 대조 문제", len(prob), "→", "통과" if r else "실패")
print("전체:", "통과" if ok else "실패")
sys.exit(0 if ok else 1)
```
