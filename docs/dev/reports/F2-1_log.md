# F2-1 실행 로그

python = `C:/Users/money/anaconda3/envs/python311/python.exe`(아래 `<py>`), 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. `$B` = `$HOME/bongsu_F2-1_20261029`.

## L0 첫 시도(멈춤) — PR #17 병합 전
```
$ gh pr view 17 --json state,mergedAt
{"mergedAt":null,"state":"OPEN"}
$ git rev-list --left-right --count feature/tension-io...origin/develop
5	0
```
U4에 따라 아무것도 바꾸지 않고 멈춤 → 사용자가 PR #17 병합 후 다시 시작.

## L1 시작 점검 · develop 최신화 · 브랜치 · 이슈
```
$ git status --porcelain
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2-1_core.md
$ git branch --show-current
feature/tension-io
$ git fetch origin
   9e7ed0d..869cfcb  develop    -> origin/develop
$ gh pr view 17 --json state,mergedAt
{"mergedAt":"2026-10-28T18:43:22Z","state":"MERGED"}
$ git log --oneline -1 origin/develop
869cfcb Merge pull request #17 from kjy700317-maker/feature/tension-io
$ git rev-list --left-right --count feature/tension-io...origin/develop
0	1
```
### 1-1 백업
```
$ cat "$B/docs_diff_stat.txt"
 ...5\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md" | 1 +
 "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"    | 8 ++++++--
 2 files changed, 7 insertions(+), 2 deletions(-)
```
### 1-2 · 1-3
```
$ git restore docs/dev/진행기록.md docs/dev/식_함수_대응표.md
$ git switch develop
Your branch is behind 'origin/develop' by 6 commits, and can be fast-forwarded.
$ git pull --ff-only origin develop
Updating 9e7ed0d..869cfcb
Fast-forward
 11 files changed, 1079 insertions(+), 14 deletions(-)
$ git log --oneline -1
869cfcb Merge pull request #17 from kjy700317-maker/feature/tension-io
(백업 되살리기)
$ git status --porcelain
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2-1_core.md
$ git switch -c feature/tension-core
Switched to a new branch 'feature/tension-core'
```
### 1-4 이슈 · 환경
본문 `$B/issue_F2.md`(배경·범위 F2-1/F2-2·완료 조건 = 지시서 0절 완료 기준 + F2-1·F2-2 검산).
```
$ gh issue create --title "[FEAT] 긴장도 계산 코어(F2)" --label feat --body-file "$B/issue_F2.md"
https://github.com/kjy700317-maker/Team-Project/issues/18
$ <py> --version
Python 3.11.17
$ <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
2.4.6 3.0.6
$ <py> -m pytest -q
..............                                                           [100%]
$ <py> -m pytest -q -o addopts=      # pytest.ini addopts=-q 와 겹쳐 -qq가 되어 요약 줄이 안 나와 개수 확인용으로 추가
14 passed in 1.94s
```

## L3 `.gitattributes`
```
$ cat .gitattributes
# 긴장도 코드화(F2-1, 2026-10-29): 결과·기준 CSV 줄바꿈을 LF로 고정 — core.autocrlf=true PC에서도 바이트 비교가 같게
data/tension/*.csv text eol=lf
tests/fixtures/*.csv text eol=lf
$ git add .gitattributes
$ git ls-files --eol data/tension/물리사건_유형판정표.csv
i/lf    w/crlf  attr/text eol=lf      	"data/tension/\353\254\274\353\246\254\354\202\254\352\261\264_\354\234\240\355\230\225\355\214\220\354\240\225\355\221\234.csv"
$ git status --porcelain
A  .gitattributes
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2-1_core.md
```
`w/crlf`: 이 파일은 1-2의 `git pull`(.gitattributes 전, autocrlf=true)로 체크아웃되어 작업트리가 CRLF. 다시 체크아웃하지 않고 그대로 둠(보고서 2절).
(커밋 1을 먼저 하려고 `git restore --staged .gitattributes` 후 커밋 1 → `git add .gitattributes` → 커밋 2)

## L5 확인 명령(2b 커밋 전)
```
$ 5-1
base_mask | (보조) 𝒯₀ 기준기간 — 연도가 base_period 안인 날 True.
baseline_means | ④ 평소값 — 기준기간 R의 평균(열마다).
calc_days | (보조) 𝒯 계산 기간 — start~end 하루 간격, end가 None이면 오늘.
daily_sums | ② 묶음별 일 합 — 묶음 g의 그날 사건 점수 합, 사건 없는 날 0.
decay_cumulative | ③ 감쇠 누적 — R_t = λ·R_t−1 + d_t, λ = 2^(−1/반감기), 시작값 0.
floor_e5 | ⑩ E5 하한 F^E5 — 북러 밀착 ρ≥4→3, ≥10→4.
floor_event | ⑩ 사건 하한 F^사 — 핵실험(A1) 또는 ICBM(A2, S ≥ 7.5) 당일 3거.
floor_physical | ⑩ 물리 하한 F^물 — 풍선 뺀 A3·A7 ρ≥3→3·≥7→4, 풍선 ρ≥6→3, 4거 유형일 ≥4, 사망·침몰일 5.
half_gauss_window | ⑩ 하한 원점수 — ρ_t = Σ_{k<창} exp(−k²/(2σ²)) · d_t−k (반가우스 σ10·30일).
relative_index | ⑤ 평소 대비 — T_g = 100 · R_g / B_g.
relief_discount | ⑦ 완화 할인 — δ = min(c · R완 / B완, κ).
rising_index | ⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중).
tension_components | ②~⑧ 묶음 — 사건표에서 R·B·T_g·T⁺·δ·T를 한 번에.
tension_index | ⑧ 긴장도 — T = T⁺ · (1 − δ).
type4_days | ⑩ 물리 4거 유형 사건일 — 판정표 Y 사건의 사건표 날짜면 True.
15
$ 5-2a
(exit 1)
$ 5-2b
(exit 1)
$ 5-3
..............                                                           [100%]
(exit 0)
14 passed in 4.04s
```
5-2a·5-2b exit 1 = grep 출력 없음.
2a 커밋(4ec4ddb) 전에 돌린 5-2a grep은 내 주석 한 줄에 걸렸다(아래). 커밋 3은 이미 만들어졌고 히스토리 재작성 금지라 커밋 4에서 주석 문구만 고침:
```
37:    # 기준 구현(s3_core.decay)과 같은 파이썬 루프 — ewm·lfilter로 바꾸지 않는다(대응표 ③)
→ 커밋 4: # 기준 구현(s3_core.decay)과 같은 파이썬 루프 — 벡터화하지 않는다(대응표 ③)
```

## L6 v0.1.4 대조 검산
`$B/verify_core_2ab.py` = 부록 B를 프롬프트 파일에서 그대로 뽑음(`sed -n 186,246p | diff -` → IDENTICAL). 입력 `data/tension/events_기본.csv`·`_확장.csv`는 F1 생성물이 있어 다시 만들지 않음.
### 6-1 2a 커밋 전(2b 함수 없음 — 기본 2a까지 출력 후 AttributeError)
```
계산 기간 2010-01-01 ~ 2026-10-27 6144 일

[기본] 사건 720행 · load 제외 0 · 묶음 ('핵·미사일', '군사 과시', '위협 언어·교리')
  B_핵·미사일 2.553789 (기준 2.554) ✓
  B_군사 과시 2.550744 (기준 2.551) ✓
  B_위협 언어·교리 2.317696 (기준 2.318) ✓
  B_완화 0.757330 (기준 0.757) ✓
  T_원값: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_핵·미사일: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_군사 과시: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_위협 언어·교리: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  완화 상한에 붙은 날 272 (기준 272 — 대응표 4절) ✓
Traceback (most recent call last):
  File "C:\Users\money\bongsu_F2-1_20261029\verify_core_2ab.py", line 44, in <module>
    fp = core.floor_physical(ev, days, type4)
         ^^^^^^^^^^^^^^^^^^^
AttributeError: module 'utils.tension.core' has no attribute 'floor_physical'
```
확장 2a 따로 확인(스크래치 명령):
```
[('핵·미사일', 2.554, '2.554'), ('군사 과시', 2.551, '2.551'), ('위협 언어·교리', 2.318, '2.318'), ('제재·압박', 3.257, '3.257'), ('완화', 0.757, '0.757')]
T 0.0004999841041524178
Tg_핵·미사일 0.0004998169336829505
Tg_군사 과시 0.000499798964151657
Tg_위협 언어·교리 0.0004997852449832862
Tg_제재·압박 0.0004999971927119873
cap 272
```
### 6-2 전체(2b 커밋 전)
```
$ <py> "$B/verify_core_2ab.py"
계산 기간 2010-01-01 ~ 2026-10-27 6144 일

[기본] 사건 720행 · load 제외 0 · 묶음 ('핵·미사일', '군사 과시', '위협 언어·교리')
  B_핵·미사일 2.553789 (기준 2.554) ✓
  B_군사 과시 2.550744 (기준 2.551) ✓
  B_위협 언어·교리 2.317696 (기준 2.318) ✓
  B_완화 0.757330 (기준 0.757) ✓
  T_원값: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_핵·미사일: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_군사 과시: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_위협 언어·교리: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  완화 상한에 붙은 날 272 (기준 272 — 대응표 4절) ✓
  하한_물리: 다른 날 0 ✓
  하한_E5: 다른 날 0 ✓
  하한_사건: 다른 날 0 ✓
  물리_4거유형일: 다른 날 0 ✓
  사건하한 날 수 18 (기준 18) ✓
  물리 4거유형 사건일 수 16 (기준 16) ✓
  E5하한 3거↑ 날 251 (기준 251) ✓
  물리하한 3거↑ 날 441 (기준 441) ✓
  물리하한 4거↑ 날 106 (기준 106) ✓
  물리하한 5거 날 2 (기준 2) ✓

[확장] 사건 941행 · load 제외 0 · 묶음 ('핵·미사일', '군사 과시', '위협 언어·교리', '제재·압박')
  B_핵·미사일 2.553789 (기준 2.554) ✓
  B_군사 과시 2.550744 (기준 2.551) ✓
  B_위협 언어·교리 2.317696 (기준 2.318) ✓
  B_제재·압박 3.257262 (기준 3.257) ✓
  B_완화 0.757330 (기준 0.757) ✓
  T_원값: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_핵·미사일: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_군사 과시: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_위협 언어·교리: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  Tg_제재·압박: 최대차 0.000500 · 셋째 자리 다른 날 0 ✓
  완화 상한에 붙은 날 272 (기준 272 — 대응표 4절) ✓
  하한_물리: 다른 날 0 ✓
  하한_E5: 다른 날 0 ✓
  하한_사건: 다른 날 0 ✓
  물리_4거유형일: 다른 날 0 ✓
  사건하한 날 수 18 (기준 18) ✓
  물리 4거유형 사건일 수 16 (기준 16) ✓
  E5하한 3거↑ 날 251 (기준 251) ✓
  물리하한 3거↑ 날 441 (기준 441) ✓
  물리하한 4거↑ 날 106 (기준 106) ✓
  물리하한 5거 날 2 (기준 2) ✓

전체: 통과
exit=0
```
보조 확인: `tension_components` 열 = `['R_핵·미사일', 'R_군사 과시', 'R_위협 언어·교리', 'R_완화', 'Tg_핵·미사일', 'Tg_군사 과시', 'Tg_위협 언어·교리', 'T_plus', 'delta', 'T']`, B 인덱스 = 대상 순서, 하한 3종 int64·`type4_days` bool, `days`·사건표 date 모두 `datetime64[us]`(pandas 3.0), `calc_days()` 끝 = 2026-10-29(오늘).

## L8 커밋
각 커밋 전 금지 경로 검사:
```
커밋 1 docs (3 files, +254 −2) → OK
커밋 2 .gitattributes (+3) → OK
커밋 3 core.py (+94) → OK
커밋 4 core.py (+52 −1) → OK
```
```
$ git log --oneline develop..HEAD
f348c35 feat: 계산 코어 2b 전용·사건 하한(⑩)
4ec4ddb feat: 계산 코어 2a 상승·완화 지수(②~⑧)
233e31c chore: 긴장도 CSV 줄바꿈 LF 고정(.gitattributes)
485b789 docs: F2-1 작업 프롬프트·설계 문서 반영
$ git status --porcelain
?? .obsidian/
```

## L9 동기화 · 푸시 · PR
```
$ git fetch origin
$ git merge origin/develop
Already up to date.
$ <py> -m pytest -q
..............                                                           [100%]
$ <py> -m pytest -q -o addopts=
14 passed in 4.17s
$ git push -u origin feature/tension-core
 * [new branch]      feature/tension-core -> feature/tension-core
branch 'feature/tension-core' set up to track 'origin/feature/tension-core'.
$ gh pr create --draft --base develop --label feat --title "[FEAT] 긴장도 계산 코어(F2)" --body-file "$B/pr_F2.md"
Warning: 1 uncommitted change
https://github.com/kjy700317-maker/Team-Project/pull/19
```
(`1 uncommitted change` = `?? .obsidian/`)
