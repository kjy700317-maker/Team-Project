# F6 실행 로그

## L1 시작 점검 · develop 최신화 · 브랜치 · 이슈

### L1-1 점검
```
$ git status --porcelain
 M docs/decisions.md
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
 M "docs/tension/\354\202\260\354\266\234\354\213\235_\354\240\225\353\246\254.md"
?? .obsidian/
?? docs/dev/requests/
?? docs/dev/tasks/F6_compare.md
?? "docs/tension/\354\202\260\354\266\234\354\213\235_\353\263\200\352\262\275\354\235\264\353\240\245.md"
$ git branch --show-current
feature/tension-merge-data
훅 있음
$ gh pr view 25
{"mergedAt":"2026-10-29T08:49:18Z","state":"MERGED"}
$ git log -1 origin/develop
04c5353 Merge pull request #25 from kjy700317-maker/feature/tension-merge-data
```

### L1-2 문서 백업 → develop pull → 되살리기 → 브랜치
```
백업 docs/decisions.md
백업 docs/dev/식_함수_대응표.md
백업 docs/dev/진행기록.md
백업 docs/tension/산출식_정리.md
백업 docs/tension/산출식_변경이력.md
백업 docs/dev/tasks/F6_compare.md
백업 docs/dev/requests/F5_화면요청.md
백업 docs/dev/requests/F6_화면요청.md
Switched to branch 'develop'
Your branch is behind 'origin/develop' by 23 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
From https://github.com/kjy700317-maker/Team-Project
 * branch            develop    -> FETCH_HEAD
Updating c691bf1..04c5353
Fast-forward
 .gitignore                                         |   1 +
 README.md                                          |   2 +-
 config.py                                          |  50 +-
 docs/dev/reports/F5_log.md                         | 309 +++++++++
 docs/dev/reports/F5_report.md                      |  34 +
 docs/dev/tasks/F5_merge_data.md                    | 709 +++++++++++++++++++++
 ...247\204\355\226\211\352\270\260\353\241\235.md" |  33 +-
 pages/.gitkeep                                     |   0
 ...36\245\353\217\204_\354\247\200\354\210\230.py" | 166 +++++
 ...02\254\352\261\264_\352\270\260\353\241\235.py" |  64 ++
 ...33\224\353\263\204_\354\227\260\353\263\204.py" |  71 +++
 "pages/4_\353\263\264\352\263\240\354\204\234.py"  | 410 ++++++++++++
 tests/test_app_smoke.py                            |  16 +
 tests/test_screen.py                               |  96 +++
 utils/dummy.py                                     |  62 ++
 utils/loader.py                                    |  86 +++
 utils/real.py                                      |  93 +++
 utils/tension/charts.py                            |  11 +-
 utils/tension/screen.py                            | 197 ++++++
 utils/ui.py                                        |  13 +
 "\355\231\210.py"                                  |  55 +-
 21 files changed, 2452 insertions(+), 26 deletions(-)
 create mode 100644 docs/dev/reports/F5_log.md
 create mode 100644 docs/dev/reports/F5_report.md
 create mode 100644 docs/dev/tasks/F5_merge_data.md
 delete mode 100644 pages/.gitkeep
 create mode 100644 "pages/1_\352\270\264\354\236\245\353\217\204_\354\247\200\354\210\230.py"
 create mode 100644 "pages/2_\354\202\254\352\261\264_\352\270\260\353\241\235.py"
 create mode 100644 "pages/3_\354\233\224\353\263\204_\354\227\260\353\263\204.py"
 create mode 100644 "pages/4_\353\263\264\352\263\240\354\204\234.py"
 create mode 100644 tests/test_app_smoke.py
 create mode 100644 tests/test_screen.py
 create mode 100644 utils/dummy.py
 create mode 100644 utils/loader.py
 create mode 100644 utils/real.py
 create mode 100644 utils/tension/screen.py
 create mode 100644 utils/ui.py
04c5353 Merge pull request #25 from kjy700317-maker/feature/tension-merge-data
 M docs/decisions.md
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
 M "docs/tension/\354\202\260\354\266\234\354\213\235_\354\240\225\353\246\254.md"
?? .obsidian/
?? docs/dev/requests/
?? docs/dev/tasks/F6_compare.md
?? "docs/tension/\354\202\260\354\266\234\354\213\235_\353\263\200\352\262\275\354\235\264\353\240\245.md"
Switched to a new branch 'feature/tension-compare'
```

### L1-3 이슈 · 환경
```
issue 본문 AI 검사: OK
https://github.com/kjy700317-maker/Team-Project/issues/26
Python 3.11.17
numpy 2.4.6 · pandas 3.0.6 · pytest 9.0.3 · plotly 7.1.0 · streamlit 1.65.0 (docx import 성공)
```

### L1-4 pytest(시작)
```
........................................................................ [ 82%]
...............                                                          [100%]
87 passed in 27.58s
```

### L1-5 커밋 1
```
금지경로 검사: OK
de9006a docs: F6 작업 프롬프트·설계 문서 반영 (8 files, +1370 −13)
AI 검사: OK
```

## L2 패치 적용
```
저장: 646 줄
6b6685f1c51776f99133773b57720b6b */c/Users/money/bongsu_F6_20261029/f6.patch
적용 가능
```

```
적용함
7e7f2b511a48395b5638828e048e1c7f6a544c72
be6c54fcf3564229bf32ea51709183372c6e5c1a
0e473714f86dd844c919792fb665679cd620629d
8b3634adc8a7d691e960a5d6c58d0913aff3f27b
ffec26773b1167c69163a7003f1b4cc1ee49e402
c10033ddf4ae29488659d4989eaa252c5b9c2d0e
e9eb7df4796309fb1944f56a742a4dd499359b80
258ca59779ddb67ddbbd08ae522a90339d8a1fed
eb34713b1661734a88b70ca28affe89bff5fae03
기존 줄 그대로(끝에 더한 줄만)
 config.py                |   2 +
 scripts/run_tension.py   |  21 ++++++++-
 utils/loader.py          |  42 +++++++++++++++++
 utils/tension/charts.py  |  48 ++++++++++++++++++-
 utils/tension/core.py    |  15 +++++-
 utils/tension/io.py      |  21 +++++++++
 utils/tension/screen.py  | 119 +++++++++++++++++++++++++++++++++++++++++++++++
 utils/tension/summary.py |  27 +++++++++++
 8 files changed, 292 insertions(+), 3 deletions(-)
 M config.py
 M scripts/run_tension.py
 M utils/loader.py
 M utils/tension/charts.py
 M utils/tension/core.py
 M utils/tension/io.py
 M utils/tension/screen.py
 M utils/tension/summary.py
?? .obsidian/
?? tests/test_compare.py
```

## L3 GPR 복사 · run_tension · md5 · 민감도 표
```
81081a43a3e8d6215685fb4521a49c52 *data/tension/GPR_한국_월별.csv
원본과 같음
계산 기간 2010-01-01 ~ 2026-10-29 · 6146일 · 모델 v0.1.4
[기본] 사건 720행 · load 제외 0 · T구간 115/256/315/378 · 마지막 날 1거
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\일별_기본.csv
[확장] 사건 941행 · load 제외 0 · T구간 110/237/314/374 · 마지막 날 1거
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\일별_확장.csv
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\요약.csv · 월별.csv · 연도별.csv
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\비교선_일별.csv · 반감기_민감도.csv(반감기 [7, 14, 21, 30]일)
?? "data/tension/GPR_\355\225\234\352\265\255_\354\233\224\353\263\204.csv"
?? "data/tension/\353\260\230\352\260\220\352\270\260_\353\257\274\352\260\220\353\217\204.csv"
?? "data/tension/\353\271\204\352\265\220\354\204\240_\354\235\274\353\263\204.csv"
704053ceea621623091bb32be4050562 *data/tension/비교선_일별.csv
af13c6f9e9e7c83c7ec0d7b55054c90a *data/tension/반감기_민감도.csv
  시나리오  반감기 T구간(2·3·4·5거 시작)   1거%   2거%   3거%   4거%  5거%  T원값 최대  기준 반감기와 단계 같은 날%  한 단계 안%  천안함
0   기본    7  117/273/350/449  42.8  23.7  13.7  10.9  8.8    1037              81.0     98.8    5
1   기본   14  115/256/315/378  48.4  22.2  11.9   9.5  8.0     749             100.0    100.0    5
2   기본   21  112/251/303/342  49.8  21.9  11.6   8.4  8.2     623              91.1    100.0    5
3   기본   30  108/245/287/323  49.9  22.1  12.2   7.4  8.4     545              84.8     98.9    5
4   확장    7  112/252/337/430  43.1  23.4  15.8   9.4  8.4     814              82.0     99.6    5
5   확장   14  110/237/314/374  47.5  22.9  14.0   8.2  7.4     624             100.0    100.0    5
6   확장   21  107/234/294/345  49.1  22.1  13.3   8.5  7.0     530              90.8     99.9    5
7   확장   30  104/230/279/326  49.0  23.0  12.4   9.1  6.5     467              83.8     99.4    5
['시나리오', '반감기', 'T구간(2·3·4·5거 시작)', '1거%', '2거%', '3거%', '4거%', '5거%', 'T원값 최대', '기준 반감기와 단계 같은 날%', '한 단계 안%', '천안함', '연평도', '3차 핵', '목함지뢰', '4차 핵', '6차 핵', '판문점 정상회담', '2022-11 집중발사', '2024-06 북러조약', '2026-09 DMZ 지뢰', '현재'] (8, 22)
```

## L4 테스트
```
$ pytest tests/test_compare.py
....................                                                     [100%]
20 passed in 10.13s
$ pytest
........................................................................ [ 67%]
...................................                                      [100%]
107 passed in 36.13s
$ pytest -m "not regression"
........................................................................ [ 80%]
..................                                                       [100%]
90 passed, 17 deselected in 25.60s
$ -W error::FutureWarning pytest tests/test_compare.py
....................                                                     [100%]
20 passed in 9.10s
```

## L5 커밋 2~6
```
 config.py                |  2 ++
 scripts/run_tension.py   | 21 ++++++++++++++++++++-
 utils/tension/core.py    | 15 ++++++++++++++-
 utils/tension/summary.py | 27 +++++++++++++++++++++++++++
 4 files changed, 63 insertions(+), 2 deletions(-)
OK
bd87a7c feat: 비교선 T_basic(⑮′)·반감기 민감도 계산
AI OK
 ...5\234\352\265\255_\354\233\224\353\263\204.csv" | 202 +++++++++++++++++++++
 utils/tension/io.py                                |  21 +++
 2 files changed, 223 insertions(+)
OK
a68826f feat: GPR 한국 월별 읽기·사본
AI OK
 utils/loader.py         |  42 +++++++++++++++++
 utils/tension/charts.py |  48 ++++++++++++++++++-
 utils/tension/screen.py | 119 ++++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 208 insertions(+), 1 deletion(-)
OK
ae0138a feat: 화면 통로에 비교선·GPR·민감도·월 사건 추가
AI OK
 ...0\260_\353\257\274\352\260\220\353\217\204.csv" |     9 +
 ...5\220\354\204\240_\354\235\274\353\263\204.csv" | 12293 +++++++++++++++++++
 2 files changed, 12302 insertions(+)
OK
736d27f chore: 비교선·반감기 민감도 결과 CSV
AI OK
 tests/test_compare.py | 204 ++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 204 insertions(+)
OK
9af6173 test: 비교선·GPR·민감도 테스트
AI OK
?? .obsidian/
```

## L6 동기화 · 작성자 · 푸시 · PR
```
$ git merge origin/develop
Already up to date.
$ pytest
107 passed in 33.95s
$ 작성자
9af6173 money2082
736d27f money2082
ae0138a money2082
a68826f money2082
bd87a7c money2082
de9006a money2082
OK
$ git push
remote: 
remote: Create a pull request for 'feature/tension-compare' on GitHub by visiting:        
remote:      https://github.com/kjy700317-maker/Team-Project/pull/new/feature/tension-compare        
remote: 
To https://github.com/kjy700317-maker/Team-Project.git
 * [new branch]      feature/tension-compare -> feature/tension-compare
branch 'feature/tension-compare' set up to track 'origin/feature/tension-compare'.
```

```
OK
Warning: 1 uncommitted change
https://github.com/kjy700317-maker/Team-Project/pull/27
OK
```

PR 본문(올린 것):

```
## 요약
- 긴장도 비교선 T_basic(⑮′), GPR 한국 월별 비교, 반감기 민감도 표를 계산·결과 CSV로 만들고, 화면 통로(screen.py·loader.py·charts.py)에 읽는 함수를 더했습니다. 기존 결과 CSV 5개(일별 2·요약·월별·연도별)는 바이트 그대로입니다.

## 관련 이슈
- closes #26

## 변경 사항
- ⑮′ 비교선 T_basic(`core.basic_index`): 상승 묶음 R 합 ÷ 기준기간 평균 × 100 × (1 − δ) → `data/tension/비교선_일별.csv`(기본·확장 각 6,146일)
- 반감기 민감도(`summary.half_life_table`): 반감기 7·14·21·30일 → `data/tension/반감기_민감도.csv`(8행 · 22열)
- GPR 한국 월별: 채점_v0 입력을 원본 그대로 복사(`data/tension/GPR_한국_월별.csv`, 2010-01~2026-09) + `io.load_gpr_monthly` 읽기·검증
- 화면 통로: `utils/tension/screen.py` 판독문·문구 상수와 통로 함수, `utils/loader.py` 끝 `load_tension_*` 8개, `utils/tension/charts.py` 그림 2개(`normalization_figure`·`gpr_figure`)
- `config.py` 끝 2줄(`HALF_LIFE_SENSITIVITY`·`GPR_PATH`)
- 테스트 `tests/test_compare.py` 20개

## 테스트
- `pytest`: 107 passed(F5까지 87 + 20)
- `pytest -m "not regression"`: 90 passed, 17 deselected
- `-W error::FutureWarning pytest tests/test_compare.py`: 20 passed
- `run_tension.py --end 2026-10-29`: 기존 결과 5개 변경 없음, 새 CSV 2개 md5 기대값과 같음

## 체크리스트
- [x] `.env` 등 민감 파일 커밋 안 함
- [x] 응답/데이터 스키마 변경 시 관련 문서 반영
- [x] (해당 시) 도메인 함정 확인

화면 파일(홈.py·pages/)은 바꾸지 않았습니다. config.py 끝 2줄과 utils/loader.py 끝 함수 8개(load_tension_basic 등)만 더했습니다.
화면 연결은 docs/dev/requests/F5_화면요청.md·F6_화면요청.md에 정리했습니다(F5 요청서도 이 PR에서 처음 올라갑니다).
PR #25가 리뷰 없이 병합되어, 그때 우리가 고친 팀원 파일 4개(README 1줄·.gitignore 1줄·config.py·홈.py) 사후 확인을 부탁드립니다(F6 요청서 4절).
```

