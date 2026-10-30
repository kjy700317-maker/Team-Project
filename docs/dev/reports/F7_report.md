# F7 보고서 — 긴장도 산출식·운영 문서 · README 4·6절 · F2 검토 발견 10 정리
- 결과: 완료
- 날짜 2026-10-30 · 브랜치 `feature/tension-docs`(최신 develop `2c853ed`에서) · 이슈 #28
- 커밋: `805f9cb` docs: F7 작업 프롬프트·설계 문서 반영 · `e7b55b1` refactor: 오물풍선 단어·A2 문구 config로, 문턱 4개 검사 · `42947f2` test: T 구간 문턱 4개 검사·config 상수 테스트 · `1d21028` docs: README 폴더 구조·화면 데이터 설명 갱신 · (이 보고서) docs: F7 보고서
- PR: https://github.com/kjy700317-maker/Team-Project/pull/29 (draft, 병합하지 않음)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6 (pytest 9.0.3 · plotly 7.1.0 · streamlit 1.65.0)

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | PR #27 MERGED, 훅 있음, 시작 107 passed, 버전 적음, 문서 md5 8개 같음 | L1 |
| 2 | ✓ | `feature/tension-docs` 생성, 이슈 #28 | L1 |
| 3 | ✓ | 패치 md5 `92b3edf6…`(118줄)·`c9c236f8…`(49줄) 같음, apply --check 통과, hash 3개 같음 | L2 |
| 4 | ✓ | 114 passed · not regression 97/17 deselected · FutureWarning 40 passed | L2 |
| 5 | ✓ | 결과 7개 cmp 같음, md5 기대와 같음, `data/` 변경 없음 | L2 |
| 6 | ✓(주석) | README 두 hunk(-52,25 / -145,7)·11 추가 2 삭제 맞음. 단 최종 hash가 기대 `e2f25ba`와 다름(아래 3절) | L3 |
| 7 | ✓ | 커밋 5개 순서대로 | L4 |
| 8 | ✓ | 매 커밋 전 금지 경로 검사 `OK` | L4 |
| 9 | ✓ | 이슈 본문·커밋 메시지·PR 본문(올리기 전·후) `OK` | L4 |
| 10 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | L4 |

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
- develop이 프롬프트 기준 `7951bb0`보다 앞선 `2c853ed`("Update README.md", money2082)였다. 이 커밋이 README 12~18행(팀원 표 이원희 줄)·마지막 줄을 바꿔서 `README.md` 최종 hash가 기대 `e2f25ba…`와 다른 `c509beb…`이다. `7951bb0`의 README에 패치를 적용하면 `e2f25ba…`가 나와(L3) 패치 자체는 정확하고, 차이는 4·6절 밖의 상류 변경 때문이다. 프롬프트 1절 "뒤에 커밋이 있으면 계속"에 따라 진행.
- 그 밖에 프롬프트와 다르게 한 것 없음.

## 4. 바뀐 파일
- `docs/tension/산출식.md`·`운영.md`(신규) · `docs/decisions.md`·`docs/dev/진행기록.md`·`식_함수_대응표.md`·`docs/tension/산출식_정리.md`·`인수인계_v0.1.4.md`·`docs/dev/지시서_구현_메인_채팅6.md`·`docs/dev/tasks/F7_docs.md` — 구현 메인 문서(내용 수정 없이 커밋)
- `config.py` — 긴장도 절에 `BALLOON_KEYWORD`·`A2_NOTE` 2줄
- `utils/tension/core.py` — 상수 2개 삭제·config 참조·`_require_four_cuts`
- `tests/test_core.py` — 테스트 7개 추가
- `README.md` — 4·6절만
- `docs/dev/reports/F7_report.md`·`F7_log.md`
- 작업트리에 남긴 변경: `?? .obsidian/`(내 것 아님)
