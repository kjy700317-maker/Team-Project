# F6 보고서 — 비교선 T_basic(⑮′) · GPR 한국 비교 · 반감기 민감도 · 유사 시기 주요 사건
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-compare`(최신 develop `04c5353`에서) · 이슈 #26
- 커밋: `de9006a` docs: F6 작업 프롬프트·설계 문서 반영 · `bd87a7c` feat: 비교선 T_basic(⑮′)·반감기 민감도 계산 · `a68826f` feat: GPR 한국 월별 읽기·사본 · `ae0138a` feat: 화면 통로에 비교선·GPR·민감도·월 사건 추가 · `736d27f` chore: 비교선·반감기 민감도 결과 CSV · `9af6173` test: 비교선·GPR·민감도 테스트 · (이 보고서) docs: F6 보고서
- PR: https://github.com/kjy700317-maker/Team-Project/pull/27 (draft, 병합하지 않음)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 (pytest 9.0.3 · plotly 7.1.0 · streamlit 1.65.0)

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | PR #25 MERGED, commit-msg 훅 있음, 시작 87 passed, 버전 위에 적음 | L1-1·L1-3·L1-4 |
| 2 | ✓ | develop ff `c691bf1→04c5353`, 문서 되살린 뒤 status 기대와 같음, `feature/tension-compare` 생성, 이슈 #26 | L1-2·L1-3 |
| 3 | ✓ | 패치 646줄 md5 `6b6685f1…` 같음, `git apply --check` 통과, hash 9개 모두 같음, config.py·loader.py 기존 줄 그대로 | L2 |
| 4 | ✓ | GPR cmp 원본과 같음(md5 `81081a43…`), 기존 결과 5개 변경 없음, 비교선 `704053ce…`·민감도 `af13c6f9…` 같음, 14일 행 115/256/315/378 · 48.4 · 22.2 · 11.9 · 9.5 · 8.0 · 749 · 100.0 · 100.0 | L3 |
| 5 | ✓ | test_compare 20 passed · 전체 107 passed · not regression 90 passed/17 deselected · FutureWarning 20 passed | L4 |
| 6 | ✓ | 8절 순서 커밋 6개 + 보고서 커밋 | L1-5·L5 |
| 7 | ✓ | 매 커밋 전 금지 경로 검사 `OK` | L1-5·L5 |
| 8 | ✓ | 이슈 본문·커밋 메시지 전부·PR 본문(올리기 전·후) 모두 `OK` | L1-3·L5·L6 |
| 9 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | (아래 4절) |

검산 숫자(기본): T구간 115/256/315/378, 마지막 날 1거 · 확장 110/237/314/374. 반감기 7/21/30일 T구간(기본) 117/273/350/449 · 112/251/303/342 · 108/245/287/323, 14일과 단계 같은 날 81.0 / 91.1 / 84.8%.

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
없음(부록 A 패치를 글자 그대로 적용).
- 참고: 1-1에서 `develop` pull 때 `docs/dev/진행기록.md`가 develop에서도 바뀌었으나, 프롬프트대로 백업본(구현 메인 작업트리 판본)을 되살려 커밋 1에 넣었다.

## 4. 바뀐 파일
- `docs/decisions.md` · `docs/dev/식_함수_대응표.md` · `docs/dev/진행기록.md` · `docs/tension/산출식_정리.md` · `docs/tension/산출식_변경이력.md`(새) · `docs/dev/tasks/F6_compare.md`(새) · `docs/dev/requests/F5_화면요청.md`·`F6_화면요청.md`(새) — 구현 메인 문서, 내용 수정 없이 커밋
- `utils/tension/core.py` — ⑮′ `basic_index`
- `utils/tension/summary.py` — `HALF_LIFE_COLUMNS`·`half_life_table`
- `scripts/run_tension.py` — 비교선·반감기 민감도 CSV 출력
- `utils/tension/io.py` — `GPR_COLUMNS`·`load_gpr_monthly`
- `utils/tension/screen.py` — 판독문·문구 상수 + 통로 함수
- `utils/tension/charts.py` — `normalization_figure`·`gpr_figure`
- `config.py`(팀원 파일) — **끝에 더한 줄만** 2줄(`HALF_LIFE_SENSITIVITY`·`GPR_PATH`)
- `utils/loader.py`(팀원 파일) — **끝에 더한 줄만**(F6 블록, `load_tension_*` 8개)
- `data/tension/GPR_한국_월별.csv`(새, 원본 바이트 그대로) · `비교선_일별.csv`(새) · `반감기_민감도.csv`(새)
- `tests/test_compare.py`(새, 20개)
- `docs/dev/reports/F6_report.md` · `F6_log.md`(새)
- 작업트리에 남긴 변경: `.obsidian/`(추적 안 함, 건드리지 않음)
