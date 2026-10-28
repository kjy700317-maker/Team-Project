# CLAUDE.md — 봉수(烽燧) Team-Project · Claude Code 작업 규칙

이 리포는 KDT 팀 프로젝트 "봉수"(한반도 군사 긴장도 대시보드, Streamlit)다. Claude Code는 **작업 프롬프트 한 장(`docs/dev/tasks/F<n>_*.md`)을 받아 그것만 수행**한다. 설계·규칙 결정은 구현 메인 세션(별도 Claude 채팅)과 사용자 몫이다.

> **적용 범위:** 이 파일의 규칙은 `docs/dev/tasks/`의 작업 프롬프트로 하는 **긴장도 계산 코드화 작업**(`utils/tension/`·`scripts/`·`tests/`·`data/tension/`·`docs/dev/`·`docs/tension/`)에만 적용한다. 그 밖의 작업(화면 `홈.py`·`pages/`, DB `utils/build_*.py`·`db/`, 전처리 데이터 등)은 팀 `README.md`의 협업 규칙을 따르고, 이 파일의 1·3·5~7절은 적용하지 않는다. 다만 3절의 보안 규칙(`.env`·키·`*.json` 커밋 금지, `main` 직접 푸시 금지)은 모든 작업에 적용한다.

## 1. 매 세션 시작 순서
1. 받은 작업 프롬프트를 끝까지 읽는다. 프롬프트에 없는 일은 하지 않는다.
2. 이 파일과 `docs/dev/식_함수_대응표.md`(계산 작업일 때)를 읽는다.
3. `git status` · `git branch --show-current` · `git fetch origin`. 작업트리에 내가 만들지 않은 변경이 있으면 **건드리지 않고** 보고서에 적는다.
4. python은 **팀 conda 환경 `python311`의 `python.exe`를 경로로 직접 호출**한다. 경로는 PC마다 다르므로 **작업 프롬프트 머리에 적힌 경로**를 쓴다(`conda run`은 PC에 따라 base 환경을 잡을 수 있어 쓰지 않는다). 버전(3.11.x)과 numpy·pandas 버전을 보고서에 적는다. 경로가 없거나 3.11이 아니면 멈추고 보고.
5. 프롬프트가 정한 브랜치를 프롬프트가 정한 기준 브랜치에서 만든다(F0은 최신 `develop`: `git pull --ff-only origin develop` → `git switch -c feature/<이름>`. F1부터도 앞 기능 PR이 `develop`에 병합된 뒤 최신 `develop`에서 만든다 — U4. 앞 PR이 병합 전이면 시작하지 말고 멈춘다).
6. 같은 리포 폴더에서 다른 Claude Code 세션이 돌고 있으면 시작하지 않는다(폴더 하나 = 체크아웃 브랜치 하나. 병렬 실행은 하지 않는다 — U1).
7. 이슈(README 5절): 프롬프트가 이슈 번호를 주지 않으면 작업 시작 전에 `gh issue create`로 만든다 — 제목 `[말머리] 요약`(FEAT·FIX·DOCS·REFACTOR·CHORE), 라벨은 같은 이름 소문자(`feat`·`fix`·`docs`·`refactor`·`chore`), 본문은 `.github/ISSUE_TEMPLATE/feature.md` 양식. 번호를 보고서에 적는다.

## 2. 구조와 경계
```
config.py                 # 파라미터(값의 근거 = docs/decisions.md ADR 번호). 함수는 인자로 받고 기본값만 config에서
홈.py · pages/            # Streamlit 화면(팀원 코드) — 프롬프트가 지시할 때만 수정
utils/helpers.py · utils/build_db.py · utils/build_erd.py · db/schema.sql   # 팀 기존 코드(화면 공통·DB) — 프롬프트가 지시할 때만 수정
utils/tension/
  io.py                   # 사건표·유형판정표·결과 CSV 로드/검증. 결측·중복은 0점이 아니라 제외 + 기록(ADR-004)
  core.py                 # 식 ①~⑰. 순수 함수(입력 DataFrame → 출력 DataFrame). Streamlit·파일 경로 모름
  charts.py               # Plotly 그림. Streamlit 없이 HTML 저장 가능해야 함
scripts/                  # build_events.py(로컬 원자료 → 사건표), run_tension.py(사건표 → 결과 CSV)
tests/                    # pytest. fixtures/ = v0.1.4 기준값·작은 합성 사건표
data/raw/                 # 로컬 원자료 — 깃 제외, 읽기만
data/tension/             # 결과 CSV·유형판정표 사본·GPR 월별 — 커밋. 사건표(events_*.csv)는 깃 제외
docs/decisions.md         # ADR — 구현 메인 소유
docs/tension/             # 산출식·결정 문서 — 구현 메인 소유
docs/dev/tasks/           # 작업 프롬프트(구현 메인이 씀) / docs/dev/reports/ 보고서(Claude Code가 씀)
docs/dev/진행기록.md       # 단계 6 진행 기록 — 구현 메인 소유, 읽기만
진행 현황 및 계획 정리/      # 로컬 작업 폴더 — 깃 제외, 읽기만. v0.1.4 기준 구현·검산 파일이 여기 있다
```

## 3. 하지 않는 것 (어기면 작업 무효)
- **규칙·설계 변경 금지:** 식, 파라미터 값, 묶음 구성, 판정 순서, 반올림 방식, CSV 열 이름·순서. 기준 구현과 다르게 하고 싶으면 **고치지 말고** 보고서 4절에 적는다. 결과가 안 맞으면 기준값을 고치지 말고 원인을 보고한다.
- `data/raw/**`, `진행 현황 및 계획 정리/**` 수정·커밋.
- `docs/decisions.md`, `docs/tension/**`, `docs/dev/tasks/**`, `docs/dev/진행기록.md`, `docs/dev/식_함수_대응표.md` 내용 수정(프롬프트가 복사를 지시할 때만 복사).
- 팀 기존 코드(`홈.py`·`pages/`·`utils/helpers.py`·`utils/build_*.py`·`db/`) 수정(프롬프트가 지시할 때만), 프롬프트에 없는 의존성 추가·`pip install`.
- `main`·`develop`에 직접 커밋·푸시, force push, 히스토리 재작성(rebase 포함), stash, PR 병합.
- `.env`, `secrets/`, 키 파일, `*.json` 커밋. JSON 결과물을 만들지 않는다(CSV로).

## 4. 코드 규칙
- 함수·변수 이름은 영어, CSV 열·묶음·문구는 한국어 그대로(예: `T_원값`, `핵·미사일`, `2거 · 하강 중(판정 1거)` — 가운뎃점은 U+00B7).
- `core.py` 함수 docstring 첫 줄에 식 번호: `"""⑨ T 구간 단계 — 기준기간 T의 70·90·95·98분위를 반올림한 정수로 판정."""`
- 반올림은 기준 구현과 같게(`np.round` 짝수 반올림, `np.quantile` 기본 linear). 정확히 x.5인 분위는 경고(요약 CSV `경계_x.5_주의` 행 — 일별 CSV에 열을 더하지 않는다).
- CSV 읽기·쓰기 모두 `encoding='utf-8-sig'`(U13 — 기준 CSV와 같음. 읽기는 BOM이 있든 없든 됨: v0.1.4 사건표·일별은 BOM 있음, 유형판정표는 없음). 날짜 `YYYY-MM-DD`, 일별 결과 `round(3)`.
- 경로는 `pathlib`로 리포 루트 기준. 한국어 폴더 이름은 따옴표로 감싼다.
- Windows에서 돈다: 줄바꿈·인코딩 차이로 diff가 커지지 않게 한다. Git Bash에서 `git show <브랜치>:.<경로>`처럼 `:` 뒤가 `.`으로 시작하면 `MSYS_NO_PATHCONV=1`을 붙인다.

## 5. 테스트·검산
- 테스트: `<작업 프롬프트가 지정한 python.exe> -m pytest -q`
- 계산 작업은 프롬프트의 v0.1.4 대조 검산을 반드시 돌리고 명령·출력 요약을 보고서에 붙인다. **검산 없는 "완료" 보고는 통과되지 않는다.**

## 6. 깃
- 브랜치 `feature/<이름>`(프롬프트가 지정). PR 대상 `develop`.
- 커밋 말머리(팀 README): `feat` `fix` `docs` `refactor` `style` `test` `chore` + `: ` + 한국어 요약 50자 이내. 한 커밋 한 목적.
- 커밋 전 `git diff --cached --stat`로 `data/raw`·`진행 현황 및 계획 정리`·`.env`·`*.json`이 없는지 확인.
- 구현 메인이 바꾼 문서(`docs/dev/tasks/F<n>_*.md`·`docs/dev/진행기록.md`·`docs/dev/식_함수_대응표.md`·`docs/decisions.md`·`docs/tension/**`)가 작업트리에 변경으로 있으면, 그 기능 브랜치의 **첫 커밋** `docs: F<n> 작업 프롬프트·설계 문서 반영`으로 내용을 고치지 않고 커밋한다(U2). `.vscode/`는 스테이징하지 않는다.
- PR 전 동기화(README 5절): `git fetch origin` → `git merge origin/develop` → 테스트 다시. 충돌 나면 `git merge --abort` 하고 멈추고 보고(직접 해결 금지).
- 푸시·PR: `git push -u origin feature/<이름>` → `gh pr create --draft --base develop --label <말머리 소문자>`. 본문은 `.github/pull_request_template.md` 양식, 관련 이슈에 `closes #<번호>`. `gh`가 실패하면 PR 본문을 보고서 7절에 적는다. **병합하지 않는다**(F0-가).

## 7. 보고서 — 두 파일 (10-28 사용자 결정)
- `docs/dev/reports/F<n>_report.md` = **요약, 60줄 이내.** 구현 메인이 읽는 파일이다. 명령 출력을 붙이지 않는다.
- `docs/dev/reports/F<n>_log.md` = 실행한 명령과 출력 전부. 구현 메인이 필요할 때만 찾아본다. report의 각 항목은 log의 절 번호(L1, L2 …)를 가리킨다.
```markdown
# F<n> 보고서 — <기능 이름>
- 결과: 완료 / 일부 / 멈춤(이유 한 줄)
- 날짜 · 브랜치 · 이슈(번호) · 커밋(해시 + 메시지) · PR(링크 또는 "만들지 않음")
- 환경: python / numpy / pandas
## 1. 완료 조건 (프롬프트 표의 # · ✓/✗ · 한 줄 근거 · log 절)
## 2. 막힌 것 · 질문 (구현 메인이 답할 것 — 없으면 "없음")
## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것 (제안만 — 없으면 "없음")
## 4. 바뀐 파일 (경로 · 한 줄) · 작업트리에 남긴 변경
```
log 양식: `# F<n> 실행 로그` 아래 프롬프트 절 순서로 `## L1 …`, `## L2 …`를 두고 명령과 출력을 그대로 적는다. PR을 못 만들면 PR 본문 초안도 log 끝에 둔다.
보고서 두 파일을 커밋한 뒤 세션을 끝낸다. 다음 기능은 새 세션에서 새 프롬프트로.

## 8. 참고 위치
- 산출식(수식 ①~⑰): `docs/tension/산출식_정리.md` 1A절 · 식↔함수 대응: `docs/dev/식_함수_대응표.md`
- v0.1.4 기준값: `docs/tension/인수인계_v0.1.4.md` 3.2절
- 기준 구현: `진행 현황 및 계획 정리/v0.1_시험/S3/s3_core.py`, `…/v0.1.4/compute_v014.py`, 독립 구현 `…/단계5/lib5.py`
- 검산 기준 파일: `…/v0.1.4/사건표_v014_기본.csv`·`_확장.csv`·`일별_v014_*.csv`·`요약_v014.csv`, 유형판정표 `…/단계5/V1_물리사건_유형판정표.csv`
