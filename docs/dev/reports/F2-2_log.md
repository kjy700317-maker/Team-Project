# F2-2 실행 로그

python = `C:/Users/money/anaconda3/envs/python311/python.exe`(아래 `<py>`), 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. `$B` = `$HOME/bongsu_F2-2_20261029`.

## L1 시작 점검
```
$ git status --porcelain
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2-2_core.md
$ git branch --show-current
feature/tension-core
$ git status -sb | head -1
## feature/tension-core...origin/feature/tension-core
$ git log --oneline -1
f9b87e7 docs: F2-1 보고서
$ gh pr view 19 --json state,isDraft,headRefName
{"headRefName":"feature/tension-core","isDraft":true,"state":"OPEN"}
$ <py> --version
Python 3.11.17
$ <py> -c "import numpy, pandas; ..."
2.4.6 3.0.6
```

## L1-1 판정표 사본 다시 체크아웃
`rm`은 Claude Code 자동 모드 권한 검사에서 거부됨("Irreversible Local Destruction"). 파일이 추적 중이고 변경 없음(`git diff --stat` 빈 출력)을 확인한 뒤 `rm` 대신 `$B`로 옮겨(백업) `git restore` — 결과는 같다.
```
$ git diff --stat -- data/tension/물리사건_유형판정표.csv
(출력 없음)
$ git ls-files --eol data/tension/물리사건_유형판정표.csv   (이전)
i/lf    w/crlf  attr/text eol=lf      	"data/tension/…물리사건_유형판정표.csv"
$ mv data/tension/물리사건_유형판정표.csv "$B/판정표_백업.csv"   (rm 대신 — 백업으로 옮김)
$ git restore data/tension/물리사건_유형판정표.csv
$ git ls-files --eol data/tension/물리사건_유형판정표.csv
i/lf    w/lf    attr/text eol=lf      	"data/tension/\353\254\274\353\246\254\354\202\254\352\261\264_\354\234\240\355\230\225\355\214\220\354\240\225\355\221\234.csv"
$ git status --porcelain
 M "docs/dev/\354\213\235_\355\225\250\354\210\230_\353\214\200\354\235\221\355\221\234.md"
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2-2_core.md
```

## L1-2 커밋 1 — 구현 메인 문서
```
$ git add docs/dev/tasks/F2-2_core.md docs/dev/진행기록.md docs/dev/식_함수_대응표.md
warning: in the working copy of 'docs/dev/식_함수_대응표.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/진행기록.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/tasks/F2-2_core.md', LF will be replaced by CRLF the next time Git touches it
$ git diff --cached --stat
 docs/dev/tasks/F2-2_core.md                        | 389 +++++++++++++++++++++
 ...10\230_\353\214\200\354\235\221\355\221\234.md" |   3 +-
 ...247\204\355\226\211\352\270\260\353\241\235.md" |  52 ++-
 3 files changed, 438 insertions(+), 6 deletions(-)
$ (금지 경로 검사)
OK
$ git commit -m "docs: F2-2 작업 프롬프트·설계 문서 반영"
c183fa6 docs: F2-2 작업 프롬프트·설계 문서 반영
$ git fetch origin
$ git rev-list --left-right --count HEAD...origin/develop
6	0
```

## L1-3 develop 맞추기
```
(오른쪽 0 → merge 건너뜀)
$ <py> -m pytest
..............                                                           [100%]
14 passed in 1.94s
```

## L1-4 커밋 2 — CLAUDE.md 테스트 명령
`$B/fix_claude_md.py` = 부록 C 글자 그대로.
```
$ <py> "$B/fix_claude_md.py"
CLAUDE.md: 테스트 명령 1곳 바꿈
$ git diff --stat CLAUDE.md
 CLAUDE.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git diff CLAUDE.md | grep -E '^[-+][^-+]'
(위 grep 출력 없음 — 바뀐 줄이 '- 테스트:'로 시작해 diff 줄이 '--'·'+-'가 되어 정규식에 안 걸림. 대신:)
$ git diff CLAUDE.md | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '
-- 테스트: `<작업 프롬프트가 지정한 python.exe> -m pytest -q`
+- 테스트: `<작업 프롬프트가 지정한 python.exe> -m pytest`
$ (금지 경로 검사)
OK
381d0e3 docs: CLAUDE.md 테스트 명령 -q 중복 제거
```

## L2c 2c 중간 확인(커밋 4 전)
방법: `$B/check_2c.py` — 사건표 → `tension_components` → `stage_cuts`·`stage_from_index` → `judge(LT, floor_physical, floor_e5, floor_event)` → `step_down`, `단계_T`·`단계_판정`·`단계_최종`을 v0.1.4 일별 CSV와 비교.
```
$ <py> "$B/check_2c.py"
기본 cuts 115/256/315/378 raw 115.27/256.48/314.82/377.91 half False
  단계_T: dtype int64 · 다른 날 0
  단계_판정: dtype int64 · 다른 날 0
  단계_최종: dtype int64 · 다른 날 0
확장 cuts 110/237/314/374 raw 109.88/237.44/313.69/374.19 half False
  단계_T: dtype int64 · 다른 날 0
  단계_판정: dtype int64 · 다른 날 0
  단계_최종: dtype int64 · 다른 날 0
```
```
warning: in the working copy of 'utils/tension/core.py', LF will be replaced by CRLF the next time Git touches it
$ git diff --cached --stat
 utils/tension/core.py | 42 ++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 42 insertions(+)
$ (금지 경로 검사)
OK
f1fd789 feat: 계산 코어 2c 구간·판정·하강(⑨⑪⑫)
```

## L5 확인 명령(5-1~5-6) — 2d·run_tension.py 작성 뒤, 커밋 5 전
5-2 두 grep은 출력 없음(grep 종료 코드 1).
```
$ 5-1
a2_note | (보조) A2자료 — a2_end보다 뒤인 날 "A2 자료 없음(a2_end까지)", 그 밖 빈 문자열.
base_mask | (보조) 𝒯₀ 기준기간 — 연도가 base_period 안인 날 True.
baseline_means | ④ 평소값 — 기준기간 R의 평균(열마다).
calc_days | (보조) 𝒯 계산 기간 — start~end 하루 간격, end가 None이면 오늘.
crisis_window_max | ⑮ 위기 눈금 — 위기일 t_c부터 t_c + 14일까지 x의 최댓값(x = 원점수_게이지면 게이지 눈금, 단계_최종이면 위기 단계).
cumulative_top_pct | ⑭ 그날까지 상위% — 100 − 100 · #{s ≤ t : T̄_s ≤ T̄_t} / #{s ≤ t}.
cuts_half_warning | ⑨ 반올림 경계 — 반올림 전 분위 중 하나라도 정확히 x.5면 True(짝수 반올림 주의, 1A.5).
daily_columns | (보조) 일별 CSV 열 순서 — 인덱스(날짜) 빼고 기본 20열·확장 21열.
daily_sums | ② 묶음별 일 합 — 묶음 g의 그날 사건 점수 합, 사건 없는 날 0.
daily_table | ②~⑰ 일별 결과 — 사건표에서 일별 CSV의 모든 열(반올림 전)과 계산 정보를 한 번에.
decay_cumulative | ③ 감쇠 누적 — R_t = λ·R_t−1 + d_t, λ = 2^(−1/반감기), 시작값 0.
display_ma | ⑬ 표시선 T̄ — 7일 후행 이동평균(처음 6일은 있는 날만 평균).
floor_e5 | ⑩ E5 하한 F^E5 — 북러 밀착 ρ≥4→3, ≥10→4.
floor_event | ⑩ 사건 하한 F^사 — 핵실험(A1) 또는 ICBM(A2, S ≥ 7.5) 당일 3거.
floor_physical | ⑩ 물리 하한 F^물 — 풍선 뺀 A3·A7 ρ≥3→3·≥7→4, 풍선 ρ≥6→3, 4거 유형일 ≥4, 사망·침몰일 5.
half_gauss_window | ⑩ 하한 원점수 — ρ_t = Σ_{k<창} exp(−k²/(2σ²)) · d_t−k (반가우스 σ10·30일).
judge | ⑪ 판정 J — 단계_T와 하한들 중 가장 높은 단계.
provisional | (보조) 잠정 — 마지막 날 − n일보다 뒤인 날(최근 6일) True.
raw_gauge | ⑮ 원점수 게이지 R^합 — 상승 묶음 R_g의 합(확장이면 제재·압박 포함).
relative_index | ⑤ 평소 대비 — T_g = 100 · R_g / B_g.
relief_discount | ⑦ 완화 할인 — δ = min(c · R완 / B완, κ).
relief_display | (보조) 완화할인 열 — 1 − T / mean(T_g), mean = 0인 날 0 (δ와 다름 — 대응표 2절).
rising_index | ⑥ 상승 지수 — 상승 묶음 T_g의 평균(동일 가중).
stage_cuts | ⑨ T 구간 — 기준기간 T의 70·90·95·98분위를 반올림한 정수 문턱 θ와 반올림 전 분위.
stage_from_index | ⑨ T 구간 단계 L^T — 1 + #{j : T ≥ θ_j} (1~5거).
stage_label | ⑰ 단계 카드 문구 — L > J면 "L거 · 하강 중(판정 J거)", 그 밖 "L거".
step_down | ⑫ 최종 단계 L — 판정이 같거나 높으면 즉시 따라가고, 낮은 날이 n일 쌓이면 한 단계 내림(첫날 L = J).
tension_components | ②~⑧ 묶음 — 사건표에서 R·B·T_g·T⁺·δ·T를 한 번에.
tension_index | ⑧ 긴장도 — T = T⁺ · (1 − δ).
trend | ⑯ 추세 — Δ = T̄_t − T̄_t−14, 변화율 = 100 · Δ / T̄_t−14 (T̄_t−14 ≥ 50일 때만, 그 밖 NaN).
type4_days | ⑩ 물리 4거 유형 사건일 — 판정표 Y 사건의 사건표 날짜면 True.
31
$ 5-2 (a)
(exit 1)
$ 5-2 (b)
(exit 1)
$ 5-3
6:import bisect
8:import numpy as np
9:import pandas as pd
11:import config
$ 5-4 <py> -m pytest
..............                                                           [100%]
14 passed in 2.16s
$ 5-5 <py> scripts/run_tension.py --help
usage: run_tension.py [-h] [--end END]

사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)

options:
  -h, --help  show this help message and exit
  --end END   계산 끝날 YYYY-MM-DD (기본: 실행일)
$ 5-6 git check-ignore -v ...
.gitignore:262:data/tension/_*	"data/tension/_check/\354\235\274\353\263\204_\352\270\260\353\263\270.csv"
.gitignore:262:data/tension/_*	"data/tension/_check/\354\235\274\353\263\204_\355\231\225\354\236\245.csv"
```

## L6 v0.1.4 대조 검산(부록 B)
`$B/verify_core_2cd.py` = 부록 B 글자 그대로. 커밋 5 전(작업트리에 2d + run_tension.py)에 한 번, 커밋 6 뒤(작업트리 깨끗)에 한 번 돌림 — 두 출력은 머리 줄 빼고 같다(`diff` 결과 SAME). 아래는 커밋 6 뒤 최종 출력.
```
$ git status --porcelain
?? .obsidian/
$ <py> "$B/verify_core_2cd.py"  (커밋 뒤 최종)
python 3.11.17 · numpy 2.4.6 · pandas 3.0.6
계산 기간 2010-01-01 ~ 2026-10-27 6144 일

[기본] 사건 720행 · load 제외 0
  열 20개 — 이름·순서가 기준과 같음 ✓
  날짜 인덱스 같음 · 이름 '날짜' ✓
  정수 열 int64 · 참거짓 열 bool ✓
  T_원값: 다른 칸 0 · 최대차 0.000500 ✓
  T_표시7일: 다른 칸 0 · 최대차 0.000500 ✓
  잠정: 다른 칸 0 ✓
  Tg_핵·미사일: 다른 칸 0 · 최대차 0.000500 ✓
  Tg_군사 과시: 다른 칸 0 · 최대차 0.000500 ✓
  Tg_위협 언어·교리: 다른 칸 0 · 최대차 0.000500 ✓
  완화할인: 다른 칸 0 · 최대차 0.000500 ✓
  원점수_게이지: 다른 칸 0 · 최대차 0.000500 ✓
  단계_T: 다른 칸 0 ✓
  하한_물리: 다른 칸 0 ✓
  물리_4거유형일: 다른 칸 0 ✓
  하한_E5: 다른 칸 0 ✓
  하한_사건: 다른 칸 0 ✓
  단계_판정: 다른 칸 0 ✓
  단계_최종: 다른 칸 0 ✓
  그날까지_상위%: 다른 칸 0 · 최대차 0.000500 ✓
  A2자료: 다른 칸 0 ✓
  화면_단계문구: 다른 칸 0 ✓
  변화14_표시: 다른 칸 0 · 최대차 0.000500 ✓
  변화율14_표시: 다른 칸 0 · 최대차 0.000500 ✓
  [0절] 단계_최종 다른 날 0 · T_원값 최대차 0.000500 < 0.001 ✓
  T구간 115/256/315/378 (기준 115/256/315/378) ✓
  T구간 반올림 전 115.27/256.48/314.82/377.91 (기준 115.27/256.48/314.82/377.91) ✓
  경계_x.5_주의 False (기준 False) ✓
  1거% 48.4 (기준 48.4) ✓
  2거% 22.2 (기준 22.2) ✓
  3거% 11.9 (기준 11.9) ✓
  4거% 9.5 (기준 9.5) ✓
  5거% 8.0 (기준 8.0) ✓
  바뀜/년 19.6 (기준 19.6) ✓
  위기 천안함: 단계 5 (기준 5) · 게이지 1.9 (기준 1.9) ✓
  위기 연평도: 단계 5 (기준 5) · 게이지 11.1 (기준 11.1) ✓
  위기 3차 핵: 단계 3 (기준 3) · 게이지 13.7 (기준 13.7) ✓
  위기 목함지뢰: 단계 4 (기준 4) · 게이지 4.1 (기준 4.1) ✓
  위기 4차 핵: 단계 3 (기준 3) · 게이지 18.2 (기준 18.2) ✓
  위기 6차 핵: 단계 5 (기준 5) · 게이지 33.8 (기준 33.8) ✓
  위기 판문점 정상회담: 단계 1 (기준 1) · 게이지 5.7 (기준 5.7) ✓
  위기 2022-11 집중발사: 단계 5 (기준 5) · 게이지 55.7 (기준 55.7) ✓
  위기 2024-06 북러조약: 단계 5 (기준 5) · 게이지 33.3 (기준 33.3) ✓
  위기 2026-09 DMZ 지뢰: 단계 4 (기준 4) · 게이지 25.0 (기준 25.0) ✓
  2018 평균단계 1.02 (기준 1.02) ✓
  2018 3거이상일 0 (기준 0) ✓
  2021 평균단계 1.06 (기준 1.06) ✓
  2023 4거이상% 60.0 (기준 60.0) ✓
  2023 5거% 41.0 (기준 41.0) ✓
  현재(10-27) 2 (기준 2) ✓
  E5가 판정을 올린 날 147 (기준 147) ✓
  원점수 기준기간 평균 7.42 (기준 7.42) ✓
  T원값 최대 749 (기준 749) ✓
  표시선 최대 701 (기준 701) ✓
  현재 표시(잠정) 107.8 (기준 107.8) ✓
  현재 그날까지 상위% 40.2 (기준 40.2) ✓
  현재 원점수 6.6 (기준 6.6) ✓
  현재 14일 변화 -107.8 (기준 -107.8) ✓
  현재 화면 단계 '2거 · 하강 중(판정 1거)' (기준 '2거 · 하강 중(판정 1거)') ✓
  END 2026-11-10로 늘려도 2026-10-27까지 값 같음(잠정 뺌): True · 잠정이 바뀐 날 6 (기대 6) ✓

[확장] 사건 941행 · load 제외 0
  열 21개 — 이름·순서가 기준과 같음 ✓
  날짜 인덱스 같음 · 이름 '날짜' ✓
  정수 열 int64 · 참거짓 열 bool ✓
  T_원값: 다른 칸 0 · 최대차 0.000500 ✓
  T_표시7일: 다른 칸 0 · 최대차 0.000500 ✓
  잠정: 다른 칸 0 ✓
  Tg_핵·미사일: 다른 칸 0 · 최대차 0.000500 ✓
  Tg_군사 과시: 다른 칸 0 · 최대차 0.000500 ✓
  Tg_위협 언어·교리: 다른 칸 0 · 최대차 0.000500 ✓
  Tg_제재·압박: 다른 칸 0 · 최대차 0.000500 ✓
  완화할인: 다른 칸 0 · 최대차 0.000500 ✓
  원점수_게이지: 다른 칸 0 · 최대차 0.000500 ✓
  단계_T: 다른 칸 0 ✓
  하한_물리: 다른 칸 0 ✓
  물리_4거유형일: 다른 칸 0 ✓
  하한_E5: 다른 칸 0 ✓
  하한_사건: 다른 칸 0 ✓
  단계_판정: 다른 칸 0 ✓
  단계_최종: 다른 칸 0 ✓
  그날까지_상위%: 다른 칸 0 · 최대차 0.000500 ✓
  A2자료: 다른 칸 0 ✓
  화면_단계문구: 다른 칸 0 ✓
  변화14_표시: 다른 칸 0 · 최대차 0.000500 ✓
  변화율14_표시: 다른 칸 0 · 최대차 0.000500 ✓
  [0절] 단계_최종 다른 날 0 · T_원값 최대차 0.000500 < 0.001 ✓
  T구간 110/237/314/374 (기준 110/237/314/374) ✓
  T구간 반올림 전 109.88/237.44/313.69/374.19 (기준 109.88/237.44/313.69/374.19) ✓
  경계_x.5_주의 False (기준 False) ✓
  1거% 47.4 (기준 47.4) ✓
  2거% 22.9 (기준 22.9) ✓
  3거% 14.0 (기준 14.0) ✓
  4거% 8.2 (기준 8.2) ✓
  5거% 7.4 (기준 7.4) ✓
  바뀜/년 19.0 (기준 19.0) ✓
  위기 천안함: 단계 5 (기준 5) · 게이지 1.9 (기준 1.9) ✓
  위기 연평도: 단계 5 (기준 5) · 게이지 16.1 (기준 16.1) ✓
  위기 3차 핵: 단계 3 (기준 3) · 게이지 17.9 (기준 17.9) ✓
  위기 목함지뢰: 단계 4 (기준 4) · 게이지 8.7 (기준 8.7) ✓
  위기 4차 핵: 단계 3 (기준 3) · 게이지 19.6 (기준 19.6) ✓
  위기 6차 핵: 단계 5 (기준 5) · 게이지 45.9 (기준 45.9) ✓
  위기 판문점 정상회담: 단계 1 (기준 1) · 게이지 7.5 (기준 7.5) ✓
  위기 2022-11 집중발사: 단계 5 (기준 5) · 게이지 59.2 (기준 59.2) ✓
  위기 2024-06 북러조약: 단계 5 (기준 5) · 게이지 44.6 (기준 44.6) ✓
  위기 2026-09 DMZ 지뢰: 단계 4 (기준 4) · 게이지 27.2 (기준 27.2) ✓
  2018 평균단계 1.07 (기준 1.07) ✓
  2018 3거이상일 6 (기준 6) ✓
  2021 평균단계 1.03 (기준 1.03) ✓
  2023 4거이상% 57.0 (기준 57.0) ✓
  2023 5거% 38.0 (기준 38.0) ✓
  현재(10-27) 1 (기준 1) ✓
  E5가 판정을 올린 날 143 (기준 143) ✓
  원점수 기준기간 평균 10.68 (기준 10.68) ✓
  T원값 최대 624 (기준 624) ✓
  표시선 최대 574 (기준 574) ✓
  현재 표시(잠정) 86.0 (기준 86.0) ✓
  현재 그날까지 상위% 47.6 (기준 47.6) ✓
  현재 원점수 7.1 (기준 7.1) ✓
  현재 14일 변화 -86.0 (기준 -86.0) ✓
  현재 화면 단계 '1거' (기준 '1거') ✓
  END 2026-11-10로 늘려도 2026-10-27까지 값 같음(잠정 뺌): True · 잠정이 바뀐 날 6 (기대 6) ✓

[run_tension.py --end 2026-10-27]
계산 기간 2010-01-01 ~ 2026-10-27 · 6144일 · 모델 v0.1.4
[기본] 사건 720행 · load 제외 0
  T구간 115/256/315/378 · 반올림 전 115.27/256.48/314.82/377.91
  마지막 날 화면 단계: 2거 · 하강 중(판정 1거)
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\_check\일별_기본.csv
[확장] 사건 941행 · load 제외 0
  T구간 110/237/314/374 · 반올림 전 109.88/237.44/313.69/374.19
  마지막 날 화면 단계: 1거
  쓴 파일: C:\Users\money\dev\Team-Project\data\tension\_check\일별_확장.csv
  종료 코드 0 ✓
  일별_기본.csv: BOM True · CRLF False · 줄 수 6145 (기대 True · False · 6145) ✓
    열·날짜가 기준 파일과 같음 ✓
    값: 허용 밖 다른 칸 0  · 글자까지 다른 칸 0(참고) ✓
  (참고) 기준 파일과 바이트까지 같음: True
  일별_확장.csv: BOM True · CRLF False · 줄 수 6145 (기대 True · False · 6145) ✓
    열·날짜가 기준 파일과 같음 ✓
    값: 허용 밖 다른 칸 0  · 글자까지 다른 칸 0(참고) ✓
  (참고) 기준 파일과 바이트까지 같음: True

전체: 통과
exit 0
```

## L8 커밋 5·6
커밋 5 시점 확인 = L5 + L6(커밋 전 실행) · 커밋 6 시점 확인 = L6 최종(커밋 뒤 재실행).
```
(커밋 5 시점 확인: core.py 2d + 작업트리의 run_tension.py로 부록 B 전체 통과 — L6_first, 5-1~5-6)
warning: in the working copy of 'utils/tension/core.py', LF will be replaced by CRLF the next time Git touches it
$ git diff --cached --stat
 utils/tension/core.py | 102 ++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 102 insertions(+)
$ (금지 경로 검사)
OK
9a16a00 feat: 계산 코어 2d 표시·문구·일별 조립(⑬~⑰)
warning: in the working copy of 'scripts/run_tension.py', LF will be replaced by CRLF the next time Git touches it
$ git diff --cached --stat
 scripts/run_tension.py | 47 +++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 47 insertions(+)
$ (금지 경로 검사)
OK
84b39b6 feat: 긴장도 계산 최소판 run_tension.py
```

## L9 동기화 · 푸시 · PR #19 본문
`$B/pr_F2_old.md`로 이전 본문을 받고 요약 첫 줄·변경 사항(8절 1·3~6)·테스트(6절 숫자)를 더한 `$B/pr_F2.md`로 갱신.
```
$ git fetch origin
$ git rev-list --left-right --count HEAD...origin/develop
10	0
$ git merge origin/develop
Already up to date.
$ <py> -m pytest
..............                                                           [100%]
14 passed in 2.10s
$ git push
To https://github.com/kjy700317-maker/Team-Project.git
   f9b87e7..84b39b6  feature/tension-core -> feature/tension-core
$ git log --oneline origin/develop..HEAD
84b39b6 feat: 긴장도 계산 최소판 run_tension.py
9a16a00 feat: 계산 코어 2d 표시·문구·일별 조립(⑬~⑰)
f1fd789 feat: 계산 코어 2c 구간·판정·하강(⑨⑪⑫)
381d0e3 docs: CLAUDE.md 테스트 명령 -q 중복 제거
c183fa6 docs: F2-2 작업 프롬프트·설계 문서 반영
f9b87e7 docs: F2-1 보고서
f348c35 feat: 계산 코어 2b 전용·사건 하한(⑩)
4ec4ddb feat: 계산 코어 2a 상승·완화 지수(②~⑧)
233e31c chore: 긴장도 CSV 줄바꿈 LF 고정(.gitattributes)
485b789 docs: F2-1 작업 프롬프트·설계 문서 반영
$ gh pr edit 19 --body-file "$B/pr_F2.md"
https://github.com/kjy700317-maker/Team-Project/pull/19
$ gh pr view 19 --json state,isDraft
{"isDraft":true,"state":"OPEN"}
```
