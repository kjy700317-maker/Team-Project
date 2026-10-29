# F2-3 실행 로그

python = `C:/Users/money/anaconda3/envs/python311/python.exe`(아래 `<py>`), 모든 python 명령 앞에 `PYTHONIOENCODING=utf-8`. `$B` = `$HOME/bongsu_F2-3_20261029`.

## L1 시작 점검
기대와 모두 같음(status 4줄 · 브랜치 · ahead/behind 없음 · `604f4f2 docs: F2 검토 보고서` · PR OPEN·draft · 14 passed).
```
$ git status --porcelain
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
 M "docs/tension/\354\202\260\354\266\234\354\213\235_\354\240\225\353\246\254.md"
?? .obsidian/
?? docs/dev/tasks/F2-3_fix.md
$ git branch --show-current
feature/tension-core
$ git fetch origin
$ git status -sb | head -1
## feature/tension-core...origin/feature/tension-core
$ git log --oneline -1
604f4f2 docs: F2 검토 보고서
$ gh pr view 19 --json state,isDraft
{"isDraft":true,"state":"OPEN"}
$ python --version
Python 3.11.17
$ numpy pandas
2.4.6 3.0.6
$ pytest
..............                                                           [100%]
14 passed in 2.32s
```

## L1-2·L1-3 커밋 1 · develop 맞추기
`15  0` — develop에만 있는 커밋 0 → merge 건너뜀(pytest는 L1과 같은 상태라 다시 돌리지 않음).
```
$ git add (3 docs)
warning: in the working copy of 'docs/dev/진행기록.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/tasks/F2-3_fix.md', LF will be replaced by CRLF the next time Git touches it
$ forbidden check
OK
 docs/dev/tasks/F2-3_fix.md                         | 535 +++++++++++++++++++++
 ...247\204\355\226\211\352\270\260\353\241\235.md" |  12 +-
 ...66\234\354\213\235_\354\240\225\353\246\254.md" |   5 +-
 3 files changed, 550 insertions(+), 2 deletions(-)
$ git commit
[feature/tension-core 6177205] docs: F2-3 작업 프롬프트·설계 문서 반영
 3 files changed, 550 insertions(+), 2 deletions(-)
 create mode 100644 docs/dev/tasks/F2-3_fix.md
$ git rev-list --left-right --count HEAD...origin/develop
15	0
```

## L2 패치 적용
부록 B·C는 프롬프트 파일에서 코드 블록을 파이썬으로 잘라 그대로 저장(`$B/extract.py` — 줄 수 verify 136 · diff 254, 프롬프트 줄 141~276 · 281~534와 같음). `--check` 첫 시도 통과(`--ignore-whitespace` 안 씀).
```
$ git apply --check "$B/F2-3.diff"
check OK
applied
$ git diff --stat
 scripts/run_tension.py | 53 ++++++++++++++++++++++-----
 utils/tension/core.py  | 99 +++++++++++++++++++++++++++++++++++++++-----------
 2 files changed, 121 insertions(+), 31 deletions(-)
```

## L3 확인 명령(3-1~3-4)
```
$ 3-1 public functions
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
$ 3-2 grep 1
$ 3-2 grep 2
$ 3-3 pytest
..............                                                           [100%]
14 passed in 2.26s
$ 3-4 --help
usage: run_tension.py [-h] [--end END]

사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)

options:
  -h, --help  show this help message and exit
  --end END   계산 끝날 YYYY-MM-DD (기본: 실행일)
```

## L4-1 v0.1.4 대조 검산(F2-2 부록 B — `$HOME/bongsu_F2-2_20261029/verify_core_2cd.py` 있음, 그것을 씀)
```
$ 4-1 verify_core_2cd.py
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
rc=0
```

## L4-2 이번 변경 검산(`$B/verify_F2-3.py`)
```
$ 4-2 verify_F2-3.py
python 3.11.17 · numpy 2.4.6 · pandas 3.0.6

[1] 자료 이상 → 멈춤
  END 2019-12-30 → ValueError: 계산 기간 2010-01-01~2019-12-30이 기준기간 2010-01-01~2019-12-31을 다 담지 않음 - 끝날짜는 2019-12-31 이후로 ✓
  END 2019-12-31 → 계산됨(3652일) ✓
  시작 2010-01-02 → ValueError: 계산 기간 2010-01-02~2026-10-27이 기준기간 2010-01-01~2019-12-31을 다 담지 않음 - 끝날짜는 2019-12-31 이후로 ✓
  tension_components도 END 2019-12-30 → ValueError: 계산 기간 2010-01-01~2019-12-30이 기준기간 2010-01-01~2019-12-31을 다 담지 않음 - 끝날짜는 2019-12-31 이후로 ✓
  완화 행 없음 → ValueError: 기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): ['완화'] ✓
  핵·미사일 기준기간 0건 → ValueError: 기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): ['핵·미사일'] ✓
  사건 0행 → ValueError: 기준기간 평소값 B가 0 이하이거나 없음(기준기간 사건 0건): ['핵·미사일', '군사 과시', '위협 언어·교리', '완화'] ✓
  2018년부터만 사건(θ₁ = 0) → ValueError: T 구간 첫 문턱(2거 시작)이 0 - 0 이하(기준기간 T가 대부분 0, 자료 부족) ✓
  사망 사건 A7-0100 없음(판정표 Y 검사와 따로) → ValueError: 사망·침몰 사건(KILL_EVENTS): 사건표에 없는 사건ID ['A7-0100'] ✓
  판정표 Y 사건 A3-0028 없음 → ValueError: 4거 유형 사건(판정표 Y): 사건표에 없는 사건ID ['A3-0028'] ✓
  type4_ids가 문자열 → TypeError: 4거 유형 사건(판정표 Y): 문자열 하나가 아니라 사건ID 모음(set·tuple·list)으로 넘긴다 ✓
  kill_ids가 문자열 → TypeError: 사망·침몰 사건(KILL_EVENTS): 문자열 하나가 아니라 사건ID 모음(set·tuple·list)으로 넘긴다 ✓
  type4_ids 빈 집합은 core에서 허용(4거 유형일 0일) — 멈춤은 run_tension ✓

[2] daily_table params
  PARAM_KEYS 20개 = 이 검산의 키와 같음 ✓
  params None · {} · config 값 그대로 → 기본 결과와 같음 ✓
  info['params']에 넘긴 값 ✓
  모르는 키 → ValueError: params에 모르는 키 ['halflife'] — 쓸 수 있는 키: ['base_period', 'half_life', 'relief_c', 'relief_cap', 'quantiles', 'si ✓
  base_period=(2011, 2019) → 바뀐 열 ['T_원값'] (기대 ['T_원값'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  half_life=7 → 바뀐 열 ['T_원값'] (기대 ['T_원값'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  relief_c=0.2 → 바뀐 열 ['T_원값'] (기대 ['T_원값'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  relief_cap=0.3 → 바뀐 열 ['T_원값'] (기대 ['T_원값'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  quantiles=(0.6, 0.9, 0.95, 0.98) → 바뀐 열 ['단계_T'] (기대 ['단계_T'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  sigma=5 → 바뀐 열 ['하한_물리', '하한_E5'] (기대 ['하한_물리', '하한_E5'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  window=10 → 바뀐 열 ['하한_물리', '하한_E5'] (기대 ['하한_물리', '하한_E5'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  phys_thresholds={'3거': 2, '4거': 7, '풍선3거': 6} → 바뀐 열 ['하한_물리'] (기대 ['하한_물리'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  type4_stage=3 → 바뀐 열 ['하한_물리'] (기대 ['하한_물리'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  kill_ids=('A7-0098',) → 바뀐 열 ['하한_물리'] (기대 ['하한_물리'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  kill_stage=4 → 바뀐 열 ['하한_물리'] (기대 ['하한_물리'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  e5_thresholds={'3거': 5, '4거': 10} → 바뀐 열 ['하한_E5'] (기대 ['하한_E5'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  icbm_s=8.0 → 바뀐 열 ['하한_사건'] (기대 ['하한_사건'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  event_stage=2 → 바뀐 열 ['하한_사건'] (기대 ['하한_사건'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  step_days=3 → 바뀐 열 ['단계_최종'] (기대 ['단계_최종'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  ma_days=3 → 바뀐 열 ['T_표시7일'] (기대 ['T_표시7일'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  provisional_days=3 → 바뀐 열 ['잠정'] (기대 ['잠정'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  trend_days=7 → 바뀐 열 ['변화14_표시'] (기대 ['변화14_표시'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  trend_pct_min=100 → 바뀐 열 ['변화율14_표시'] (기대 ['변화율14_표시'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  a2_end='2024-12-31' → 바뀐 열 ['A2자료'] (기대 ['A2자료'] 중 하나 이상) · 열 이름·순서 그대로 ✓
  params relief_c=0.2의 T = tension_components(relief_c=0.2)의 T ✓
  params sigma·window = floor_physical(sigma=5, window=10) ✓

[3] run_tension.py 입력 검사
  --end 2019-12-30 → rc 1 (기대 1) · 멈춤: 계산 기간 2010-01-01~2019-12-30이 기준기간 2010-01-01~2019-12-31을 다 담지 않음 - 끝날짜는 2019-12-31 이후로 ✓
  --end 2026-13-01 → rc 2 (기대 2) · run_tension.py: error: argument --end: 없는 날짜: 2026-13-01 ✓
  --end abc → rc 2 (기대 2) · run_tension.py: error: argument --end: YYYY-MM-DD 형식이 아님: abc ✓
  --end 20261027 → rc 2 (기대 2) · run_tension.py: error: argument --end: YYYY-MM-DD 형식이 아님: 20261027 ✓
  --end 2026-10-27 13:00 → rc 2 (기대 2) · run_tension.py: error: argument --end: YYYY-MM-DD 형식이 아님: 2026-10-27 13:00 ✓
  cp949 출력에서 멈춤 메시지 → rc 1 · UnicodeEncodeError 없음 ✓
  멈춘 실행은 _check 파일을 쓰지 않음(수정 시각 그대로) ✓
멈춤: 사건표 없음: C:\Users\money\dev\Team-Project\data\_없는폴더_F2-3\events_기본.csv - scripts/build_events.py로 먼저 만든다
계산 기간 2010-01-01 ~ 2026-10-27 · 6144일 · 모델 v0.1.4
  사건표 없음 → main() 반환 1 (기대 1, 메시지 '사건표 없음'은 위 stderr) ✓
  정상 --end 2026-10-27 → rc 0 ✓

전체: 통과
rc=0
```

## L6 커밋 3·4
```
$ git add utils/tension/core.py
 utils/tension/core.py | 99 +++++++++++++++++++++++++++++++++++++++------------
 1 file changed, 77 insertions(+), 22 deletions(-)
$ forbidden check
OK
[feature/tension-core 8eb9002] fix: 계산 코어 자료 이상 멈춤·daily_table params
 1 file changed, 77 insertions(+), 22 deletions(-)
$ git add scripts/run_tension.py
 scripts/run_tension.py | 53 +++++++++++++++++++++++++++++++++++++++++---------
 1 file changed, 44 insertions(+), 9 deletions(-)
$ forbidden check
OK
[feature/tension-core 91fa47d] fix: run_tension 입력 검사·메시지
 1 file changed, 44 insertions(+), 9 deletions(-)
$ git log --oneline origin/develop..HEAD
91fa47d fix: run_tension 입력 검사·메시지
8eb9002 fix: 계산 코어 자료 이상 멈춤·daily_table params
6177205 docs: F2-3 작업 프롬프트·설계 문서 반영
604f4f2 docs: F2 검토 보고서
8aad2a6 docs: CLAUDE.md 마지막 답 한국어 요약 규칙
927dd0b docs: F2 검토 작업 프롬프트·설계 문서 반영
7076eaa docs: F2-2 보고서
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
$ git status --porcelain
?? .obsidian/
```

## L7 푸시 · PR
fetch 뒤 develop 쪽 0 → merge 안 함. PR 본문: `$B/pr_F2_old.md`(이전) → `$B/pr_F2.md`(요약 첫 줄 교체 · 변경 사항에 fix 커밋 2개 · 테스트에 F2-3 두 줄). 첫 편집에서 멈춤 경우 수를 12로 잘못 적어 11(ValueError 9·TypeError 2)로 고쳐 다시 편집. 보고서 커밋 뒤 `git push`는 이 로그 커밋 다음이라 여기 없음(채팅 답에 결과).
```
$ git fetch origin
$ git rev-list --left-right --count HEAD...origin/develop
17	0
$ pytest
14 passed in 2.19s
$ git push
To https://github.com/kjy700317-maker/Team-Project.git
   604f4f2..91fa47d  feature/tension-core -> feature/tension-core
$ gh pr view 19 --json body
saved 44 lines
$ gh pr edit 19 --body-file pr_F2.md
https://github.com/kjy700317-maker/Team-Project/pull/19
$ gh pr view 19 --json state,isDraft
{"isDraft":true,"state":"OPEN"}
$ gh pr edit 19 --body-file pr_F2.md (경우 수 정정)
https://github.com/kjy700317-maker/Team-Project/pull/19
{"isDraft":true,"state":"OPEN"}
```

