# F2-1 보고서 — 계산 코어 2a(상승·완화 ②~⑧)·2b(하한 ⑩)
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-core`(develop 869cfcb에서) · 이슈 #18(F2 전체 — F2-2도 사용)
- 커밋: `485b789 docs: F2-1 작업 프롬프트·설계 문서 반영` · `233e31c chore: 긴장도 CSV 줄바꿈 LF 고정(.gitattributes)` · `4ec4ddb feat: 계산 코어 2a 상승·완화 지수(②~⑧)` · `f348c35 feat: 계산 코어 2b 전용·사건 하한(⑩)` · `docs: F2-1 보고서`(이 파일)
- PR: https://github.com/kjy700317-maker/Team-Project/pull/19 (draft, 병합 안 함)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | 첫 시도는 PR #17 OPEN이라 멈춤(L0). 병합 뒤 다시: status·브랜치 기대대로, #17 MERGED, origin/develop 869cfcb, `0 1`, 백업→ff→되살리기 후 상태 같음 | L1 |
| 2 | ✓ | `attr/text eol=lf`, 다른 변경 없음. 단 작업트리 `w/crlf`(2절 1) | L3 |
| 3 | ✓ | 공개 함수 15개, 첫 줄 모두 식 번호 또는 `(보조)` | L5 |
| 4 | ✓ | grep 두 개 출력 없음(2b 커밋 전 기준 — 3절 1) | L5 |
| 5 | ✓ | 14 passed | L5 |
| 6 | ✓ | `전체: 통과`(exit 0) | L6 |
| 7 | ✓ | develop..HEAD = 8절 1~4(+ 보고서 커밋 5) | L8 |
| 8 | ✓ | 커밋 1~5 전 모두 `OK` | L8 |
| 9 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | L8 |

검산 숫자(기본·확장 같음, L6):
- B: 핵·미사일 2.553789 · 군사 과시 2.550744 · 위협 언어·교리 2.317696 · (확장) 제재·압박 3.257262 · 완화 0.757330 — 요약 셋째 자리와 모두 일치
- `T_원값`·`Tg_*` 최대 절대차 0.000500(기준 CSV 반올림 폭), 셋째 자리 다른 날 0
- 완화 상한에 붙은 날 272
- `하한_물리`·`하한_E5`·`하한_사건`·`물리_4거유형일` 다른 날 0 · 사건하한 18 · 4거유형 사건일 16 · E5 3거↑ 251 · 물리 3거↑ 441 · 4거↑ 106 · 5거 2

## 2. 막힌 것 · 질문
1. 3절 확인에서 `git ls-files --eol` 결과가 `i/lf  w/crlf  attr/text eol=lf`(기대 `w/lf`). 판정표 사본은 1-2 `git pull`(`.gitattributes` 전, autocrlf=true)로 CRLF로 체크아웃됐기 때문. 리포 blob은 LF, git status는 깨끗하고 pandas 읽기·검산에는 영향 없음. 작업트리를 LF로 맞추려면 `rm` 후 `git restore <파일>`로 다시 체크아웃하면 되지만, 프롬프트에 없어 하지 않았다 — 할지 구현 메인이 정해 주세요.

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
1. 커밋 3(2a)의 `decay_cumulative` 주석에 "ewm·lfilter"라는 단어가 있어 5-2 grep에 걸렸다(코드 사용 아님). 커밋 3이 이미 만들어졌고 히스토리 재작성은 금지라, 커밋 4에서 주석을 "벡터화하지 않는다"로 고쳤다 → 커밋 4에 2b 추가 말고 주석 한 줄 변경도 들어 있음.
2. 내부 보조 `_day_sum(rows, days)`를 더해 `daily_sums`·`floor_physical`·`floor_e5`가 같이 씀(`groupby("date")["S"].sum().reindex(days, fill_value=0.0)` 그대로). `floor_physical`의 4거 유형일 마스크는 `type4_days`를 다시 씀. 결과 영향 없음.
3. `isin`에는 `type4_ids`·`kill_ids`를 `list(...)`로 바꿔 넘김(frozenset 대비). 결과 영향 없음.
4. 알림: `pytest.ini`의 `addopts = -q`와 프롬프트의 `-q`가 겹쳐 `-qq`가 되어 `14 passed` 요약 줄이 안 나온다(점 14개만). 개수는 `-o addopts=`로 따로 확인해 log에 붙였다. 프롬프트 기대 문구를 고치거나 `addopts`를 비우는 걸 검토.
5. 알림: pandas 3.0에서 `calc_days()`·사건표 date가 모두 `datetime64[us]`. 검산·`isin`·`reindex`는 문제없었다.

## 4. 바뀐 파일
- `utils/tension/core.py` — 새 파일, 공개 함수 15개(②~⑧·⑩ + `calc_days`·`base_mask`), `BALLOON_KEYWORD`
- `.gitattributes` — 새 파일, `data/tension/*.csv`·`tests/fixtures/*.csv` `text eol=lf`
- `docs/dev/tasks/F2-1_core.md`·`docs/dev/진행기록.md`·`docs/dev/식_함수_대응표.md` — 구현 메인 문서, 내용 수정 없이 커밋
- `docs/dev/reports/F2-1_report.md`·`F2-1_log.md` — 이 보고서
- 작업트리에 남긴 변경: `?? .obsidian/`(건드리지 않음). 리포 밖 `$HOME/bongsu_F2-1_20261029/`(문서 백업·이슈·PR 본문·검산 스크립트·출력)
