# F0 보고서 — 긴장도 코드화 뼈대·규칙
- 결과: **완료**(완료 조건 13개 통과). 단, python 실행 방법은 사용자 결정으로 바꿈(2절 1)
- 날짜 2026-10-28 · 브랜치 `feature/tension-scaffold` · 이슈 [#14](https://github.com/kjy700317-maker/Team-Project/issues/14) · PR [#15](https://github.com/kjy700317-maker/Team-Project/pull/15)(draft, 병합 안 함)
- 커밋: `71c5b36` chore: 긴장도 코드화 뼈대와 Claude Code 규칙 추가 · `2040539` chore: requirements 버전 고정·pytest·openpyxl 추가 · `a442c1a` chore: config.py에 긴장도 파라미터 추가 · `6f32c3e` docs: 긴장도 결정 문서 사본을 docs/tension에 추가 · `e4965be` docs: ADR 갱신 반영(v0.1.4까지) · (이 커밋) docs: F0 보고서
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 (`envs/python311/python.exe` 직접 호출)

## 1. 완료 조건
| # | | 근거 | log |
|---|---|---|---|
| 1 | ✓ | `봉수 긴장도 계산 패키지 (v0.1.4 이식).` (콘솔 cp949라 UTF-8로 재출력) | L10 |
| 2 | ✓ | 3 passed (병합 뒤 재실행도 통과) | L10·L11 |
| 3 | ✓ | `(2010, 2019) (0.7, 0.9, 0.95, 0.98) ('A7-0098', 'A7-0100')` | L10 |
| 4 | ✓ | 작업 폴더·사건표 무시, `data/raw/processed`는 `data/raw/*`로 무시, 결과 CSV는 추적 | L5 |
| 5 | ✓ | `ASCII text` | L6 |
| 6 | ✓ | dry-run 오류 없음(`Would install lxml-6.1.3 python-docx-1.2.0`) | L6 |
| 7 | ✓ | 9개 모두 바이트 크기 같음 + `cmp` 동일 | L4 |
| 8 | ✓ | 9절 커밋 1~5 순서대로(6 = 이 커밋) | L10 |
| 9 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만(커밋 전에는 보고서 2개도 보임) | L10 |
| 10 | ✓ | 첫 줄 일치 · `1` | L10 |
| 11 | ✓ | 6개 모두 있음 | L10 |
| 12 | ✓ | `224 23 246`, assert 통과(팀 기록 19줄 + 로컬 224 + 3) | L8 |
| 13 | ✓ | `.gitignore:253:.vscode/*` | L2·L10 |
추가 대조: CLAUDE.md·`__init__.py`·`test_smoke.py`·`pytest.ini`·config 부록 E가 프롬프트 부록과 글자 그대로 같음(L10)

## 2. 막힌 것 · 질문
1. **`conda run -n python311`은 이 PC에서 base(3.14.6)를 실행한다**(`sys.executable` = `anaconda3\python.exe`. conda 플러그인 로드 오류와 관련 있어 보임 — 추정). 사용자 결정(10-28)으로 `C:/Users/money/anaconda3/envs/python311/python.exe` 직접 호출로 진행. 그런데 **CLAUDE.md 1·5절은 `conda run` 방식**으로 적혀 있다(부록 A 그대로 넣음). F1 전에 문구를 고칠지는 구현 메인이 정해야 함.
2. python311 환경에 **pytest·openpyxl이 없어서** 사용자 허락을 받아 설치함(`pip install pytest==9.0.3 openpyxl==3.1.5` — 이전 점검에서 본 버전과 같게). 팀원 환경에도 설치가 필요함.
3. 원격 develop이 프롬프트 기대(27커밋)보다 2커밋 많았음(PR #13, README.md만 바뀜). 겹치는 파일 집합이 같아서 그대로 진행함(사용자 확인).

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
- `pandas==3.0.6`은 python311 환경 값이다(이전 점검의 3.0.3은 base 값).
- 커밋 1에 `docs/dev/**` 전체가 들어감: 프롬프트가 꼽은 파일 외에 `reports/F0-pre_report.md`·`tasks/F0-pre_원격점검.md`도 포함.
- 커밋 1~5 때 금지 경로 검사의 grep 패턴이 오류를 내서 검사가 돌지 않았다(제 실수). 커밋 뒤 `develop..HEAD` 전체로 다시 확인했고 금지 경로는 0건(L9).

## 4. 바뀐 파일 · 작업트리에 남긴 변경
- 새로 만듦: `CLAUDE.md`, `utils/tension/__init__.py`, `scripts/README.md`, `tests/{__init__.py,fixtures/.gitkeep,test_smoke.py}`, `pytest.ini`, `data/tension/.gitkeep`, `docs/dev/reports/.gitkeep`, `docs/tension/*.md`(9개 사본)
- 수정: `.gitignore`(끝에 블록 추가), `requirements.txt`(pandas 고정, pytest·openpyxl 추가), `config.py`(주석 1줄, 부록 E 추가), `docs/decisions.md`(이어 붙이기)
- 처음으로 추적됨: `docs/dev/` 문서들(프롬프트·대응표·진행기록·F0-pre)
- 로컬 변경 되돌림: `README.md`·`utils/README.md`(줄바꿈 차이뿐, `readme_local.diff` 0줄), `docs/decisions.md`(합쳐서 반영). 백업 `~/bongsu_F0_backup_20261028/`
- 작업트리에 남김: `.vscode/settings.json`(개인 설정, 무시됨), `.obsidian/`(추적 안 함), `진행 현황 및 계획 정리/`(무시됨)
- 환경: python311에 pytest 9.0.3·openpyxl 3.1.5와 의존 패키지 설치
