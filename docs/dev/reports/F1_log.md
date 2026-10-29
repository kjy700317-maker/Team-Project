# F1 실행 로그

## L1 시작 점검 · develop 최신화 · 브랜치 · 이슈
```
$ git status --porcelain
 M docs/decisions.md
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
 M "docs/tension/\354\202\260\354\266\234\354\213\235_\354\240\225\353\246\254.md"
?? .obsidian/
?? docs/dev/tasks/F1_io.md
$ git branch --show-current
feature/tension-scaffold
$ git fetch origin && git log --oneline -1 origin/develop
9e7ed0d Merge pull request #15 from kjy700317-maker/feature/tension-scaffold
$ git rev-list --left-right --count feature/tension-scaffold...origin/develop
0	1
$ (1-1 백업) git diff --stat
 docs/decisions.md                                  |  4 ++--
 ...10\230_\353\214\200\354\235\221\355\221\234.md" |  6 +++---
 ...247\204\355\226\211\352\270\260\353\241\235.md" | 23 +++++++++++++++-------
 ...66\234\354\213\235_\354\240\225\353\246\254.md" |  4 ++--
 4 files changed, 23 insertions(+), 14 deletions(-)
$ (1-2) git restore … && git switch develop && git pull --ff-only origin develop
Updating 064c655..9e7ed0d
Fast-forward  (32 files changed, 5647 insertions(+), 6 deletions(-))
$ git log --oneline -1
9e7ed0d Merge pull request #15 from kjy700317-maker/feature/tension-scaffold
$ (1-3 되살리기) git status --porcelain
 M docs/decisions.md
 M docs/dev/식_함수_대응표.md (quotepath 표기)
 M docs/dev/진행기록.md
 M docs/tension/산출식_정리.md
?? .obsidian/
?? docs/dev/tasks/F1_io.md
$ git switch -c feature/tension-io
Switched to a new branch 'feature/tension-io'
$ gh issue create --title "[FEAT] 긴장도 입력 로더·사건표 생성(F1)" --label feat --body-file "$B/issue_F1.md"
https://github.com/kjy700317-maker/Team-Project/issues/16
$ <py> --version ; <py> -c "import numpy, pandas, openpyxl; …"
Python 3.11.17
2.4.6 3.0.6 3.1.5
```

## L2 build_events.py 실행 (3절 · 7절 #4)
첫 실행은 콘솔 cp949로 한글이 깨져 출력만 다시 받음(`PYTHONIOENCODING=utf-8`). 결과 수치는 같음(기본 720 / 확장 941 / 제외기록 177).
```
$ PYTHONIOENCODING=utf-8 <py> scripts/build_events.py --end 2026-10-27
원자료 C:\Users\money\dev\Team-Project\data\raw\긴장도_산출식_세부_기준 · 기간 2010-01-01 ~ 2026-10-27
읽은 파일:
  A1: 봉수_A1_북한6건_위력세부기준_수정시험안_v0.4.xlsx [02_PRK6건_시험점수]
  A2: 봉수_A2_동일시작종료일_중복_사용여부N.xlsx [01_294건_적용본]
  B1: 봉수_B1_신형무기개발시험_31건_2기준_점수시험안_v0.2.xlsx [B1_사건별시험]
  A3: 봉수_A3_저강도물리도발_62건_사건별점수판정_시험안_v0.2.xlsx [01_Y62_사건판정]
  A7: 봉수_A7_125건_피해맥락_A2A3연계_민감도검토_v0.3.xlsx [A7_사건별_맥락검토]
  A4: 봉수_A4_군사훈련_50건_단일기준_점수시험안_v0.2.xlsx [01_39건_점수시험]
  A5: 봉수_A5_미전력자산전개_117건_2기준_점수시험안_v0.1.xlsx [01_사건별117건]
  A6: 봉수_A6_무기공개열병식_17건_2기준_점수시험안_v0.2.xlsx [01_A6_17건_점수]
  B4: 봉수_B4_41건_정책변화실질성_단일기준_점수시험안_v0.3.xlsx [B4_41건_점수시험]
  C1: 봉수_C1_34건_과대평가검토_C2_전처리기준_1차검토.xlsx [C1_전건_재검토]
  C2: 봉수_C2_53건_군사질서변화_긴장방향_기준비교_v0.3.xlsx [C2_사건별_v03비교]
  C3: 봉수_C3_v0.7_보류28건판정근거추가.xlsx [사건별_66건_시험]
  C5: 봉수_C5_v0.9_기타조치13건세부분류_판정규칙정리.xlsx [C5_282건_사건별시험]
  E5: E5_점수표_v2_2026-10-27.csv
  F2: F2_점수표_v4_2026-10-27.csv
  F2: F2_연도별회담_정제.csv
φ 대조 통과 668
               n       S합
요소 묶음                    
A1 핵·미사일       4    43.50
A2 핵·미사일     137   780.00
A3 물리 충돌      37   123.56
A4 군사 과시      30   123.60
A5 군사 과시     113   627.75
A6 군사 과시      17    49.05
A7 물리 충돌      31   202.50
B1 핵·미사일      28   146.50
B4 위협 언어·교리   40   216.50
C1 위협 언어·교리   55   305.25
C2 위협 언어·교리   34   188.50
C3 위협 언어·교리   37   199.50
C5 제재·압박     221  1124.75
E5 북러 밀착      24   166.50
   북러(표시만)    52   125.50
F2 완화         81   133.60
기본 720행 / 확장 941행 / 제외기록 177행
사유 코드별: {'①': 1, '③': 129, '④': 2, '⑤': 18, '⑥': 17, '⑦': 10}
쓴 파일: C:\Users\money\dev\Team-Project\data\tension/events_기본.csv · events_확장.csv · events_제외기록.csv · events_입력파일.csv
$ cmp <1회차 events_입력파일.csv> data/tension/events_입력파일.csv && echo inputs-same
inputs-same
$ wc -l data/tension/events_*.csv   (머리 1행 포함)
   721 events_기본.csv · 942 events_확장.csv · 178 events_제외기록.csv · 17 events_입력파일.csv
$ head -c 3 events_기본.csv | od -tx1 → ef bb bf ;  grep -c $'\r' → 0
```

## L3 유형판정표 사본 (4절 · 7절 #7)
```
$ cp ".../단계5/V1_물리사건_유형판정표.csv" data/tension/물리사건_유형판정표.csv
$ cmp ... && echo same
same
$ git cat-file blob HEAD:data/tension/물리사건_유형판정표.csv | cmp - <원본> && echo blob-same   (커밋 뒤)
blob-same
$ git config --show-origin core.autocrlf
file:C:/Program Files/Git/etc/gitconfig	true      (.gitattributes 없음)
```

## L4 v0.1.4 대조 검산 (6절 · 7절 #6)
```
$ PYTHONIOENCODING=utf-8 <py> "$B/verify_events.py"
기본 | 열 True | 행 720 720 | 키·순서 동일 True | S 최대차 0.0 | load 제외 0 → 통과
확장 | 열 True | 행 941 941 | 키·순서 동일 True | S 최대차 0.0 | load 제외 0 → 통과
① v013 1 새 1 → 동일
③ v013 129 새 129 → 동일
④ v013 2 새 2 → 동일
새 제외기록 사유 코드별: {'③': 129, '⑤': 18, '⑥': 17, '⑦': 10, '④': 2, '①': 1}
판정표 37 행 · Y 16 · 사건표 대조 문제 0 → 통과
전체: 통과
```

## L5 완료 조건 #2·#3·#5·#8·#9
```
### 2
('사건ID', 'date', '요소', '묶음', 'S', '사건명') 8
### 3
..............                                                           [100%]
=================================== PASSES ====================================
=========================== short test summary info ===========================
PASSED tests/test_io.py::test_bom_and_no_bom_read_same
PASSED tests/test_io.py::test_column_mismatch_raises[date,\uc0ac\uac74ID,\uc694\uc18c,\ubb36\uc74c,S,\uc0ac\uac74\uba85]
PASSED tests/test_io.py::test_column_mismatch_raises[\uc0ac\uac74ID,date,\uc694\uc18c,\ubb36\uc74c,S]
PASSED tests/test_io.py::test_invalid_rows_excluded_with_reason
PASSED tests/test_io.py::test_duplicates
PASSED tests/test_io.py::test_sorted_and_dtypes
PASSED tests/test_io.py::test_type4_load_and_ids
PASSED tests/test_io.py::test_type4_bad_flag_raises
PASSED tests/test_io.py::test_type4_duplicate_id_raises
PASSED tests/test_io.py::test_type4_against_events
PASSED tests/test_io.py::test_write_csv_bom_lf_roundtrip
PASSED tests/test_smoke.py::test_import_package
PASSED tests/test_smoke.py::test_config_values_match_adr
PASSED tests/test_smoke.py::test_half_life_definition
### 5
.gitignore:260:data/tension/events_*.csv	"data/tension/events_\352\270\260\353\263\270.csv"
.gitignore:260:data/tension/events_*.csv	"data/tension/events_\355\231\225\354\236\245.csv"
.gitignore:260:data/tension/events_*.csv	"data/tension/events_\354\240\234\354\231\270\352\270\260\353\241\235.csv"
.gitignore:260:data/tension/events_*.csv	"data/tension/events_\354\236\205\353\240\245\355\214\214\354\235\274.csv"
### 8
정상
### 9
(9 끝)
```

## L6 커밋 (8절 · 7절 #10·#11)
각 커밋 전 금지 경로 검사 `OK` 확인 후 커밋(OK가 아니면 커밋하지 않게 묶어 실행).
```
warning: in the working copy of 'docs/decisions.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/식_함수_대응표.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/진행기록.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/tension/산출식_정리.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/tasks/F1_io.md', LF will be replaced by CRLF the next time Git touches it
 docs/decisions.md           |   4 +-
 docs/dev/tasks/F1_io.md     | 262 ++++++++++++++++++++++++++++++++++++++++++++
 docs/dev/식_함수_대응표.md  |   6 +-
 docs/dev/진행기록.md        |  23 ++--
 docs/tension/산출식_정리.md |   4 +-
 5 files changed, 285 insertions(+), 14 deletions(-)
c1 OK
warning: in the working copy of 'tests/test_io.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'utils/tension/io.py', LF will be replaced by CRLF the next time Git touches it
 tests/test_io.py    | 125 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 utils/tension/io.py | 119 +++++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 244 insertions(+)
c2 OK
warning: in the working copy of 'scripts/build_events.py', LF will be replaced by CRLF the next time Git touches it
 scripts/build_events.py | 265 ++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 265 insertions(+)
c3 OK
warning: in the working copy of 'data/tension/물리사건_유형판정표.csv', LF will be replaced by CRLF the next time Git touches it
 data/tension/물리사건_유형판정표.csv | 38 ++++++++++++++++++++++++++++++++++++
 1 file changed, 38 insertions(+)
c4 OK
b2cc494 chore: 물리사건 유형판정표 사본 추가
2d9593a feat: 원자료에서 사건표 만드는 build_events 추가
5ea4a99 feat: 사건표·유형판정표 로더 io.py 추가
02a047d docs: F1 작업 프롬프트·설계 문서 반영
?? .obsidian/
```

## L7 동기화 · 푸시 · PR (9절)
```
Already up to date.
..............                                                           [100%]
remote: 
remote: Create a pull request for 'feature/tension-io' on GitHub by visiting:        
remote:      https://github.com/kjy700317-maker/Team-Project/pull/new/feature/tension-io        
remote: 
To https://github.com/kjy700317-maker/Team-Project.git
 * [new branch]      feature/tension-io -> feature/tension-io
branch 'feature/tension-io' set up to track 'origin/feature/tension-io'.
$ gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 입력 로더·사건표 생성(F1)" --body-file "$B/pr_F1.md"
Warning: 1 uncommitted change
https://github.com/kjy700317-maker/Team-Project/pull/17
```
