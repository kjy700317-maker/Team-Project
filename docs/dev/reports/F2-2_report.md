# F2-2 보고서 — 계산 코어 2c(⑨⑪⑫)·2d(⑬~⑰ + 일별 CSV) · run_tension.py 최소판
- 결과: 완료
- 날짜 2026-10-29 · 브랜치 `feature/tension-core`(F2-1에 이어서) · 이슈 #18
- 커밋: `c183fa6 docs: F2-2 작업 프롬프트·설계 문서 반영` · `381d0e3 docs: CLAUDE.md 테스트 명령 -q 중복 제거` · `f1fd789 feat: 계산 코어 2c 구간·판정·하강(⑨⑪⑫)` · `9a16a00 feat: 계산 코어 2d 표시·문구·일별 조립(⑬~⑰)` · `84b39b6 feat: 긴장도 계산 최소판 run_tension.py` · `docs: F2-2 보고서`(이 파일). merge 커밋 없음(develop 쪽 0 — 1-3·9절 모두)
- PR: https://github.com/kjy700317-maker/Team-Project/pull/19 (draft 유지, 본문 갱신, 병합 안 함)
- 환경: python 3.11.17 / numpy 2.4.6 / pandas 3.0.6

## 1. 완료 조건
| # | ✓/✗ | 근거 | log |
|---|---|---|---|
| 1 | ✓ | status 4줄·브랜치·ahead/behind 없음·`f9b87e7 docs: F2-1 보고서`·PR #19 OPEN·draft | L1 |
| 2 | ✓ | `i/lf  w/lf  attr/text eol=lf`, status에 안 보임(`rm` 대신 백업 이동 — 3절 1) | L1-1 |
| 3 | ✓ | `6  0` → merge 건너뜀, 14 passed | L1-3 |
| 4 | ✓ | `1 file changed, 1 insertion(+), 1 deletion(-)`, -q 줄/없는 줄 두 줄(grep 정규식 — 3절 2) | L1-4 |
| 5 | ✓ | 공개 함수 31개, 첫 줄 모두 식 번호 또는 `(보조)` | L5 |
| 6 | ✓ | grep 두 개 출력 없음, import `bisect`·`numpy`·`pandas`·`config` 네 줄 | L5 |
| 7 | ✓ | 14 passed · `--end`만 · 두 파일 모두 `.gitignore:262:data/tension/_*` | L5 |
| 8 | ✓ | `전체: 통과`(exit 0) — 커밋 전·커밋 뒤 두 번, 출력 같음 | L6 |
| 9 | ✓ | develop..HEAD = F2-1 5개 + 8절 1·3·4·5·6(+ 보고서 7) | L9 |
| 10 | ✓ | 커밋 1~6 전 모두 `OK` | L1-2·L1-4·L2c·L8 |
| 11 | ✓ | 보고서 커밋 뒤 `?? .obsidian/` 하나만 | (커밋 뒤 확인) |

검산 숫자(L6):
- T 구간: 기본 115/256/315/378(반올림 전 115.27/256.48/314.82/377.91) · 확장 110/237/314/374(109.88/237.44/313.69/374.19), x.5 경고 둘 다 False
- 실수 열 최대차: 기본·확장 모든 실수 열 0.000500(기준 CSV 셋째 자리 반올림 폭)
- 다른 칸 0인 열: 기본 20/20 · 확장 21/21(정수·참거짓·문자열 완전 일치, `단계_최종` 다른 날 0)
- 1~5거 %: 기본 48.4/22.2/11.9/9.5/8.0 · 확장 47.4/22.9/14.0/8.2/7.4 · 바뀜/년 19.6 · 19.0 · 위기 10건 단계·게이지 눈금·연도 지표·현재 값 모두 일치
- 현재 문구: 기본 `2거 · 하강 중(판정 1거)` · 확장 `1거`
- END 2026-11-10: 2026-10-27까지 값 같음, `잠정`만 6일 바뀜(기본·확장)
- run_tension 파일 검사: 두 파일 BOM·LF·6145줄, 허용 밖 다른 칸 0, 글자까지 다른 칸 0
- 바이트 같음(참고): 기본·확장 모두 True — pandas 3.0.6에서도 기준 CSV와 바이트까지 같았다

## 2. 막힌 것 · 질문
없음

## 3. 기준 구현과 다르게 한 것 · 고치고 싶은 것
1. 1-1의 `rm data/tension/물리사건_유형판정표.csv`가 Claude Code 자동 모드 권한 검사에서 거부됨(되돌릴 수 없는 삭제로 분류). 추적 중·변경 없음을 확인하고 `rm` 대신 `$B/판정표_백업.csv`로 옮긴 뒤 `git restore` — 결과(`w/lf`, status 깨끗)는 같다. 다음 프롬프트에서 이런 단계는 `mv` 백업으로 적으면 막히지 않는다.
2. 1-4 기대 "`git diff CLAUDE.md | grep -E '^[-+][^-+]'` → 두 줄"이 출력 없음으로 나왔다. 바뀐 줄이 목록 `- 테스트:`로 시작해 diff 줄이 `--`·`+-`가 되어 정규식에 안 걸리기 때문. `grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '`로 두 줄(-q 있음/없음)만 바뀐 것을 확인해 log에 붙였다. 다음 프롬프트 정규식 검토.
3. 완화할인 열은 기준 정의(`1 − T / Tg.mean(axis=1)`, 분모 0이면 0)를 그대로 옮겼다(`relief_display`). 의견: 화면·설명에서 이 열을 "완화 할인 δ"로 쓸 거면 T⁺ = 0인 날(기본 35일) δ > 0인데 0으로 적히는 게 혼동을 줄 수 있다. F4에서 열 값을 `comp["delta"]`로 바꾸는 안을 검토(기준 CSV와 그 날들만 달라짐 — 회귀 기준을 바꾸는 결정이라 구현 메인 몫).
4. 작은 구현 선택(결과 영향 없음): `step_down`·`cumulative_top_pct`는 `to_numpy()`로 돌고, `stage_from_index`는 `np.select` 결과를 `int64`로 명시, `daily_table`은 `bundles`를 `list`로 받아 둠. `crisis_window_max` 반환 인덱스 = 위기 이름(목록 순서).
5. 알림: `run_tension.py`의 `--end` 도움말 문구와 `ArgumentParser` 설명은 프롬프트에 없는 문구라 내가 정했다(`계산 끝날 YYYY-MM-DD (기본: 실행일)`).

## 4. 바뀐 파일
- `utils/tension/core.py` — 2c 5개·2d 11개 함수(공개 31개), 상수 `A2_NOTE`·`DAILY_HEAD`·`DAILY_TAIL`, `import bisect`
- `scripts/run_tension.py` — 새 파일, 최소판(`--end` 하나 · 출력 `data/tension/_check/일별_기본.csv`·`일별_확장.csv`)
- `CLAUDE.md` — 5절 테스트 명령 `-q` 한 곳만 뺌
- `docs/dev/tasks/F2-2_core.md`·`docs/dev/진행기록.md`·`docs/dev/식_함수_대응표.md` — 구현 메인 문서, 내용 수정 없이 커밋
- `docs/dev/reports/F2-2_report.md`·`F2-2_log.md` — 이 보고서
- 작업트리에 남긴 것: `?? .obsidian/`(건드리지 않음) · `data/tension/_check/일별_기본.csv`·`일별_확장.csv`(깃 제외 — `run_tension.py` 출력). 리포 밖 `$HOME/bongsu_F2-2_20261029/`(검산·수정 스크립트, 출력, PR 본문, 판정표 백업)
