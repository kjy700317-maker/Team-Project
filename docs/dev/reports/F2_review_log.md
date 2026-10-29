# F2 검토 실행 로그

모든 python = `PYTHONIOENCODING=utf-8 C:/Users/money/anaconda3/envs/python311/python.exe`(아래 `<py>`), 리포 루트에서 실행. `$B` = `$HOME/bongsu_F2review_20261029`(리포 밖). 스크립트·출력은 `$B`의 파일을 그대로 붙였다.

## L1 시작 점검 (1절)

```
$ git status --porcelain
 M "docs/dev/\354\247\204\355\226\211\352\270\260\353\241\235.md"
?? .obsidian/
?? docs/dev/tasks/F2_review.md
$ git branch --show-current
feature/tension-core
$ git fetch origin
$ git status -sb | head -1
## feature/tension-core...origin/feature/tension-core
$ git log --oneline -1
7076eaa docs: F2-2 보고서
$ gh pr view 19 --json state,isDraft,headRefName
{"headRefName":"feature/tension-core","isDraft":true,"state":"OPEN"}
$ git rev-list --left-right --count HEAD...origin/develop
11	0
$ PYTHONIOENCODING=utf-8 <py> --version
Python 3.11.17
$ PYTHONIOENCODING=utf-8 <py> -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
2.4.6 3.0.6
$ PYTHONIOENCODING=utf-8 <py> -m pytest
..............                                                           [100%]
14 passed in 1.99s
```

## L2 커밋 1·2 (1-2 · 1-3)

```
$ git add docs/dev/tasks/F2_review.md docs/dev/진행기록.md
warning: in the working copy of 'docs/dev/진행기록.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/dev/tasks/F2_review.md', LF will be replaced by CRLF the next time Git touches it
$ git diff --cached --name-only | grep -E '^(data/raw/|진행 현황 및 계획 정리/)|\.env$|\.json$|events_|일별_' && echo "금지경로 있음 — 멈춤" || echo "OK"
OK
$ git diff --cached --stat
 docs/dev/tasks/F2_review.md | 119 ++++++++++++++++++++++++++++++++++++++++++++
 docs/dev/진행기록.md        |  16 ++++--
 2 files changed, 130 insertions(+), 5 deletions(-)
$ git commit -m "docs: F2 검토 작업 프롬프트·설계 문서 반영"
927dd0b docs: F2 검토 작업 프롬프트·설계 문서 반영

$ PYTHONIOENCODING=utf-8 <py> "$B/add_korean_summary.py"     # 부록 A 글자 그대로
CLAUDE.md: 7절에 한국어 요약 규칙 1줄 넣음
$ git diff --stat CLAUDE.md
 CLAUDE.md | 1 +
 1 file changed, 1 insertion(+)
$ git diff CLAUDE.md | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) '
+**세션 마지막 채팅 답은 항상 한국어로**(10-29 사용자): 결과(완료·일부·멈춤) · 검산 숫자 · 커밋·PR · 막힌 것 · 프롬프트와 다르게 한 것을 짧게 요약한다.
$ git add CLAUDE.md && (금지 경로 검사)
OK
$ git commit -m "docs: CLAUDE.md 마지막 답 한국어 요약 규칙"
8aad2a6 docs: CLAUDE.md 마지막 답 한국어 요약 규칙
```

## L3 실제 사건표 구성 (R2·R5 보조) — `$B/probe_data.py`

```python
"""R2·R5 보조 — 실제 사건표(기본)의 묶음·요소 구성, 완화 S 값, 풍선 이름, 사망·침몰·4거 ID 존재 확인. 읽기만."""
from common import *  # noqa: F401,F403

ev = real("기본")
print("dtypes:", dict(ev.dtypes.astype(str)))
print("행", len(ev), "· 날짜", ev["date"].min().date(), "~", ev["date"].max().date())
print("\n[묶음 × 요소]")
print(pd.crosstab(ev["묶음"], ev["요소"]))
rel = ev[ev["묶음"] == "완화"]
print("\n[완화 S 값 빈도] (φ 0.2가 곱해졌으면 1 미만 값이 보여야 함)")
print(rel["S"].round(4).value_counts().sort_index().to_dict())
print("완화 기간", rel["date"].min().date(), "~", rel["date"].max().date(), "· 2010-06-30까지", int((rel["date"] <= "2010-06-30").sum()), "건")
ph = ev[ev["묶음"] == "물리 충돌"]
bal = ph["사건명"].astype(str).str.contains("balloon", case=False)
print("\n[물리 충돌 중 Balloon 포함] 요소별", ph[bal]["요소"].value_counts().to_dict(),
      "· 대소문자 정확히 'Balloon'", int(ph["사건명"].astype(str).str.contains("Balloon").sum()), "· 대소문자 무시", int(bal.sum()))
print("\n[KILL_EVENTS 존재]", {k: ev.loc[ev['사건ID'] == k, 'date'].dt.strftime('%Y-%m-%d').tolist() for k in config.KILL_EVENTS})
t4 = sorted(TYPE4)
print("[4거 유형 ID] 판정표 Y", len(t4), "· 사건표에 있음", int(ev["사건ID"].isin(t4).sum()),
      "· 그중 묶음", ev.loc[ev["사건ID"].isin(t4), "묶음"].value_counts().to_dict())
print("[A2 S ≥ 7.5]", int(((ev["요소"] == "A2") & (ev["S"] >= 7.5)).sum()), "· A2 S 7.49~7.51", ev.loc[(ev["요소"] == "A2") & ev["S"].between(7.49, 7.51), "S"].unique().tolist())
print("[S 범위]", ev["S"].min(), "~", ev["S"].max())
```

```
dtypes: {'사건ID': 'str', 'date': 'datetime64[us]', '요소': 'str', '묶음': 'str', 'S': 'float64', '사건명': 'str'}
행 720 · 날짜 2010-01-27 ~ 2026-09-30

[묶음 × 요소]
요소        A1   A2  A3  A4   A5  A6  A7  B1  B4  C1  C2  C3  E5  F2
묶음                                                                
군사 과시      0    0   0  30  113  17   0   0   0   0   0   0   0   0
물리 충돌      0    0  37   0    0   0  31   0   0   0   0   0   0   0
북러 밀착      0    0   0   0    0   0   0   0   0   0   0   0  24   0
북러(표시만)    0    0   0   0    0   0   0   0   0   0   0   0  52   0
완화         0    0   0   0    0   0   0   0   0   0   0   0   0  81
위협 언어·교리   0    0   0   0    0   0   0   0  40  55  34  37   0   0
핵·미사일      4  137   0   0    0   0   0  28   0   0   0   0   0   0

[완화 S 값 빈도] (φ 0.2가 곱해졌으면 1 미만 값이 보여야 함)
{0.15: 5, 0.3: 17, 0.4: 2, 0.45: 22, 0.5: 1, 0.6: 3, 0.75: 1, 2.25: 10, 3.0: 4, 3.75: 1, 4.5: 9, 5.25: 3, 6.0: 2, 7.5: 1}
완화 기간 2010-02-01 ~ 2019-01-31 · 2010-06-30까지 3 건

[물리 충돌 중 Balloon 포함] 요소별 {'A3': 31} · 대소문자 정확히 'Balloon' 31 · 대소문자 무시 31

[KILL_EVENTS 존재] {'A7-0098': ['2010-03-26'], 'A7-0100': ['2010-11-23']}
[4거 유형 ID] 판정표 Y 16 · 사건표에 있음 16 · 그중 묶음 {'물리 충돌': 16}
[A2 S ≥ 7.5] 14 · A2 S 7.49~7.51 [7.5]
[S 범위] 0.0 ~ 12.5
```

## L4 R4 경계 10가지 — `$B/common.py` · `$B/r4_edges.py`

```python
"""F2 검토 실험 공통 — 리포 루트를 sys.path에 넣고 core·io·config를 가져온다. 리포 루트에서 실행."""
import sys
import warnings
from pathlib import Path

ROOT = Path.cwd()
assert (ROOT / "utils" / "tension" / "core.py").exists(), "리포 루트에서 실행"
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import config  # noqa: E402
from utils.tension import core, io as tio  # noqa: E402

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

BASE = config.BUNDLES_BASE
TYPE4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))


def real(name="기본"):
    ev, _ = tio.load_events(ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv")
    return ev


def mk(rows):
    """합성 사건표: rows = [(사건ID, 'YYYY-MM-DD', 요소, 묶음, S, 사건명)]. io.load_events가 돌려주는 꼴과 같은 dtype."""
    df = pd.DataFrame(rows, columns=list(tio.EVENT_COLUMNS))
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["S"] = df["S"].astype("float64")
    return df


def bg_rows(prefix="BG", bundles=BASE + ("완화",), dates=("2012-03-01", "2015-06-01", "2018-09-01", "2021-01-01")):
    """기준기간 안팎에 묶음마다 사건 몇 건 — B_g > 0을 만들기 위한 바탕."""
    out = []
    for bi, b in enumerate(bundles):
        for di, d in enumerate(dates):
            out.append((f"{prefix}-{bi}{di}", d, "X", b, 5.0, "bg"))
    return out


def run(events, end="2026-10-27", bundles=BASE, type4=TYPE4, start=config.CALC_START_DATE):
    """daily_table을 돌리고 (daily, info, 잡힌 경고 목록) 반환. 예외는 그대로 올린다."""
    days = core.calc_days(start, end)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        daily, info = core.daily_table(events, days, bundles, type4)
    return daily, info, [f"{x.category.__name__}: {x.message}" for x in w]


def brief(daily, info, warns=()):
    T = daily["T_원값"]
    print(f"  B = {dict((k, round(float(v), 4)) for k, v in info['B'].items())}")
    print(f"  cuts = {list(info['cuts'])} · 반올림 전 = {[round(float(v), 4) for v in info['quantiles_raw']]} · half_warning = {info['half_warning']}")
    print(f"  T: NaN {int(T.isna().sum())} · inf {int(np.isinf(T).sum())} · min {T.min():.4g} · max {T.max():.4g}")
    print(f"  단계_T 분포 {daily['단계_T'].value_counts().sort_index().to_dict()} · 단계_최종 분포 {daily['단계_최종'].value_counts().sort_index().to_dict()}")
    print(f"  상위% NaN {int(daily['그날까지_상위%'].isna().sum())} · 완화할인 NaN {int(daily['완화할인'].isna().sum())} · 변화율 NaN {int(daily['변화율14_표시'].isna().sum())}")
    print(f"  경고 {len(warns)}건{': ' + ' | '.join(sorted(set(warns)))[:400] if warns else ''}")
```

```python
"""R4 경계 조건 10가지 — 합성 사건표(또는 실제 사건표)로 daily_table을 실제로 돌린다. 판정: 예외 / 조용히 틀림 / 맞음."""
import traceback

from common import *  # noqa: F401,F403


def case(title, fn):
    print(f"\n=== {title}")
    try:
        fn()
    except Exception as e:  # 예외도 결과다
        print(f"  예외: {type(e).__name__}: {e}")
        print("  " + traceback.format_exc().strip().splitlines()[-3])


# ① 사건 0행
def c1():
    ev = mk([])
    print("  dtypes", dict(ev.dtypes.astype(str)))
    d, info, w = run(ev)
    brief(d, info, w)


# ② 기준기간에 한 묶음 사건 0건 (B_g = 0) — 군사 과시는 2021년에만, 완화는 정상
def c2a():
    rows = [r for r in bg_rows() if not (r[3] == "군사 과시" and r[1] < "2020")]
    d, info, w = run(mk(rows))
    brief(d, info, w)
    print("  2021-01-01 Tg_군사 과시 =", d.loc["2021-01-01", "Tg_군사 과시"], "· T =", d.loc["2021-01-01", "T_원값"],
          "· 단계_T =", d.loc["2021-01-01", "단계_T"])


# ②' 완화 묶음만 기준기간 0건 (B^완 = 0) — 상승 묶음은 정상
def c2b():
    rows = [r for r in bg_rows() if r[3] != "완화"]
    d, info, w = run(mk(rows))
    brief(d, info, w)
    print("  delta NaN", int(info["components"]["delta"].isna().sum()), "/", len(d))


# ②'' 실제 사건표에서 완화 행을 모두 뺀 경우(F2 자료가 없는 사건표)
def c2c():
    ev = real("기본")
    d0, i0, _ = run(ev)
    d, info, w = run(ev[ev["묶음"] != "완화"].reset_index(drop=True))
    brief(d, info, w)
    print("  (참고: 완화 포함 원래 cuts", list(i0["cuts"]), ")")


# ③ 계산 기간 밖 날짜만
def c3():
    rows = [("O1", "2009-12-31", "A2", "핵·미사일", 7.5, "x"), ("O2", "2030-01-01", "A1", "핵·미사일", 10.0, "x"),
            ("O3", "2009-06-01", "F2", "완화", 3.0, "x")]
    d, info, w = run(mk(rows))
    brief(d, info, w)


# ④ 같은 날 여러 사건(같은 묶음 3건 + 다른 묶음 1건)
def c4():
    rows = bg_rows() + [("S1", "2016-01-06", "A1", "핵·미사일", 10.0, "a"), ("S2", "2016-01-06", "A2", "핵·미사일", 4.8, "b"),
                        ("S3", "2016-01-06", "B1", "핵·미사일", 5.0, "c"), ("S4", "2016-01-06", "C1", "위협 언어·교리", 6.25, "d")]
    d, info, w = run(mk(rows))
    R = info["components"]
    lam = 2 ** (-1 / 14)
    exp_R = R.loc["2016-01-05", "R_핵·미사일"] * lam + 19.8
    print("  R_핵·미사일 2016-01-06 =", R.loc["2016-01-06", "R_핵·미사일"], "· 기대 λ·R(전날)+19.8 =", exp_R,
          "· 차", abs(R.loc["2016-01-06", "R_핵·미사일"] - exp_R))
    print("  하한_사건 2016-01-05/06/07 =", d.loc["2016-01-05":"2016-01-07", "하한_사건"].tolist())


# ⑤ END가 기준기간 끝보다 이름 — 실제 사건표, end 2015-12-31 / 2010-06-30
def c5():
    ev = real("기본")
    full, fi, _ = run(ev)
    for end in ("2015-12-31", "2010-06-30"):
        d, info, w = run(ev, end=end)
        print(f"  [end {end}] {len(d)}일")
        brief(d, info, w)
        same = d.index
        diffT = (d["T_원값"] - full.loc[same, "T_원값"]).abs().max()
        diffL = int((d["단계_최종"] != full.loc[same, "단계_최종"]).sum())
        print(f"  같은 날짜에서 전체 실행과 비교: T 최대 차 {diffT:.4g} · 단계_최종 다른 날 {diffL}/{len(same)}")
    print("  (전체 B", {k: round(float(v), 4) for k, v in fi["B"].items()}, "cuts", list(fi["cuts"]), ")")


# ⑥ calc_days(end=None)
def c6():
    days = core.calc_days()
    print("  calc_days() =", days[0].date(), "~", days[-1].date(), len(days), "일 · dtype", days.dtype,
          "· 오늘", pd.Timestamp.today().normalize().date())
    d, info, w = run(real("기본"), end=None)
    print("  마지막 날", d.index[-1].date(), "· 잠정 True", int(d["잠정"].sum()), "· 마지막 문구", d["화면_단계문구"].iloc[-1])


# ⑦ 시작일(2010-01-01)에 사건 1건씩(상승 3묶음·완화) — 그 뒤 사건 없음 / 분위 0
def c7():
    rows = [(f"D{i}", "2010-01-01", "X", b, 5.0, "x") for i, b in enumerate(BASE + ("완화",))]
    d, info, w = run(mk(rows))
    brief(d, info, w)
    print("  첫날 T", d["T_원값"].iloc[0], "· 2019-12-31 T", d.loc["2019-12-31", "T_원값"])
    # ⑦' 기준기간 대부분 T = 0 (사건이 2016년부터) → 70분위 0 → θ1 = 0
    rows2 = [(f"E{i}{j}", dt, "X", b, 5.0, "x") for i, b in enumerate(BASE + ("완화",))
             for j, dt in enumerate(("2016-03-01", "2018-03-01", "2019-06-01"))]
    d2, info2, w2 = run(mk(rows2))
    print("  [⑦' 사건 2016년부터]")
    brief(d2, info2, w2)
    print("  2012-01-01(T = 0인 날) 단계_T =", d2.loc["2012-01-01", "단계_T"], "· T =", d2.loc["2012-01-01", "T_원값"])


# ⑧ ⑭ 동점 — 실제 사건표 2010년 초(T̄ = 0)
def c8():
    d, info, w = run(real("기본"))
    head = d.loc[:"2010-02-03", ["T_원값", "T_표시7일", "그날까지_상위%"]]
    print(head.iloc[[0, 1, 2, 24, 25, 26, 27, 28, 33]].to_string())
    # 정의대로 직접 계산(O(n²))과 비교
    tb = d["T_표시7일"].to_numpy()
    ref = np.array([100 - 100 * np.sum(tb[: i + 1] <= tb[i]) / (i + 1) for i in range(len(tb))])
    print("  상위% 정의 직접 계산과 최대 차:", np.abs(ref - d["그날까지_상위%"].to_numpy()).max())
    # T̄ 정의(있는 날만 평균) 직접 계산과 rolling 차
    T = d["T_원값"].to_numpy()
    tb_ref = np.array([T[max(0, i - 6): i + 1].mean() for i in range(len(T))])
    diff = np.abs(tb_ref - tb)
    print(f"  T̄ rolling vs 직접 평균 최대 차 {diff.max():.3g} · 0이어야 하는 날(직접=0) rolling≠0 {int(((tb_ref == 0) & (tb != 0)).sum())}")
    ref2 = np.array([100 - 100 * np.sum(tb_ref[: i + 1] <= tb_ref[i]) / (i + 1) for i in range(len(tb_ref))])
    print("  직접 T̄로 낸 상위%와 코드 상위% 다른 날:", int((np.round(ref2, 3) != np.round(d['그날까지_상위%'].to_numpy(), 3)).sum()))


# ⑨ step_down 첫날이 높은 단계
def c9():
    J = pd.Series([5] + [1] * 30, index=pd.date_range("2010-01-01", periods=31))
    L = core.step_down(J)
    print("  J = [5, 1×30] → L =", L.tolist())
    J2 = pd.Series([3, 5, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1], index=pd.date_range("2010-01-01", periods=17))
    print("  J2 =", J2.tolist(), "→ L =", core.step_down(J2).tolist(), "(중간에 J=4가 와도 u는 이어짐 — ⑫ 식 그대로)")
    print("  첫날 L = J:", core.step_down(pd.Series([4, 4, 2], index=pd.date_range("2010-01-01", periods=3))).tolist())
    try:
        core.step_down(pd.Series([], dtype="int64"))
    except Exception as e:
        print("  빈 J:", type(e).__name__, e)


# ⑩ type4_ids가 비었을 때
def c10():
    ev = real("기본")
    full, _, _ = run(ev)
    d, info, w = run(ev, type4=frozenset())
    print("  물리_4거유형일 True", int(d["물리_4거유형일"].sum()), "(전체 실행", int(full["물리_4거유형일"].sum()), ")",
          "· 하한_물리 4 이상 날", int((d["하한_물리"] >= 4).sum()), "(전체", int((full["하한_물리"] >= 4).sum()), ")",
          "· 경고", len(w))
    d2, _, _ = run(ev, type4=set())
    print("  set() 도 같음:", d2.equals(d))
    d3, _, _ = run(ev, type4="A7-0120")  # 문자열 하나를 넘기는 실수
    print("  문자열 'A7-0120'을 넘기면 4거유형일 True", int(d3["물리_4거유형일"].sum()), "(목록 ['A7-0120']이면",
          int(run(ev, type4=["A7-0120"])[0]["물리_4거유형일"].sum()), ")")


for t, f in [("① 사건 0행", c1), ("② 기준기간 상승 묶음 0건(B_g=0)", c2a), ("②' 기준기간 완화 0건(B완=0)", c2b),
             ("②'' 실제 사건표 − 완화 행", c2c), ("③ 계산 기간 밖 날짜만", c3), ("④ 같은 날 여러 사건", c4),
             ("⑤ END < 2019-12-31", c5), ("⑥ calc_days(end=None)", c6), ("⑦ 시작일 사건 1건 · 분위 0", c7),
             ("⑧ ⑭ 동점(2010 초 T̄=0)", c8), ("⑨ step_down 첫날 높은 단계", c9), ("⑩ type4_ids 빔", c10)]:
    case(t, f)
```

출력 (`<py> "$B/r4_edges.py"`):

```

=== ① 사건 0행
  dtypes {'사건ID': 'object', 'date': 'datetime64[s]', '요소': 'object', '묶음': 'object', 'S': 'float64', '사건명': 'object'}
  B = {'핵·미사일': 0.0, '군사 과시': 0.0, '위협 언어·교리': 0.0, '완화': 0.0}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 6144 · inf 0 · min nan · max nan
  단계_T 분포 {1: 6144} · 단계_최종 분포 {1: 6144}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6144
  경고 0건

=== ② 기준기간 상승 묶음 0건(B_g=0)
  B = {'핵·미사일': 0.085, '군사 과시': 0.0, '위협 언어·교리': 0.085, '완화': 0.085}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 4018 · inf 2126 · min inf · max inf
  단계_T 분포 {1: 6144} · 단계_최종 분포 {1: 6144}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6144
  경고 0건
  2021-01-01 Tg_군사 과시 = inf · T = inf · 단계_T = 1

=== ②' 기준기간 완화 0건(B완=0)
  B = {'핵·미사일': 0.085, '군사 과시': 0.085, '위협 언어·교리': 0.085, '완화': 0.0}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 6144 · inf 0 · min nan · max nan
  단계_T 분포 {1: 6144} · 단계_최종 분포 {1: 6144}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6144
  경고 0건
  delta NaN 6144 / 6144

=== ②'' 실제 사건표 − 완화 행
  B = {'핵·미사일': 2.5538, '군사 과시': 2.5507, '위협 언어·교리': 2.3177, '완화': 0.0}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 6144 · inf 0 · min nan · max nan
  단계_T 분포 {1: 6144} · 단계_최종 분포 {1: 4891, 2: 317, 3: 644, 4: 278, 5: 14}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6144
  경고 0건
  (참고: 완화 포함 원래 cuts [np.float64(115.0), np.float64(256.0), np.float64(315.0), np.float64(378.0)] )

=== ③ 계산 기간 밖 날짜만
  B = {'핵·미사일': 0.0, '군사 과시': 0.0, '위협 언어·교리': 0.0, '완화': 0.0}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 6144 · inf 0 · min nan · max nan
  단계_T 분포 {1: 6144} · 단계_최종 분포 {1: 6144}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6144
  경고 0건

=== ④ 같은 날 여러 사건
  R_핵·미사일 2016-01-06 = 19.80009772389906 · 기대 λ·R(전날)+19.8 = 19.80009772389906 · 차 0.0
  하한_사건 2016-01-05/06/07 = [1, 3, 1]

=== ⑤ END < 2019-12-31
  [end 2015-12-31] 2191일
  B = {'핵·미사일': 1.0622, '군사 과시': 1.9216, '위협 언어·교리': 2.0939, '완화': 0.3991}
  cuts = [np.float64(110.0), np.float64(234.0), np.float64(309.0), np.float64(415.0)] · 반올림 전 = [109.9182, 234.1909, 308.7136, 415.4424] · half_warning = False
  T: NaN 0 · inf 0 · min 0 · max 789.7
  단계_T 분포 {1: 1534, 2: 437, 3: 110, 4: 66, 5: 44} · 단계_최종 분포 {1: 1183, 2: 475, 3: 247, 4: 210, 5: 76}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 1063
  경고 0건
  같은 날짜에서 전체 실행과 비교: T 최대 차 240.3 · 단계_최종 다른 날 466/2191
  [end 2010-06-30] 181일
  B = {'핵·미사일': 0.0, '군사 과시': 0.9714, '위협 언어·교리': 1.7161, '완화': 0.1142}
  cuts = [np.float64(nan), np.float64(nan), np.float64(nan), np.float64(nan)] · 반올림 전 = [nan, nan, nan, nan] · half_warning = False
  T: NaN 181 · inf 0 · min nan · max nan
  단계_T 분포 {1: 181} · 단계_최종 분포 {1: 117, 2: 14, 3: 15, 4: 28, 5: 7}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 181
  경고 0건
  같은 날짜에서 전체 실행과 비교: T 최대 차 nan · 단계_최종 다른 날 33/181
  (전체 B {'핵·미사일': 2.5538, '군사 과시': 2.5507, '위협 언어·교리': 2.3177, '완화': 0.7573} cuts [np.float64(115.0), np.float64(256.0), np.float64(315.0), np.float64(378.0)] )

=== ⑥ calc_days(end=None)
  calc_days() = 2010-01-01 ~ 2026-10-29 6146 일 · dtype datetime64[us] · 오늘 2026-10-29
  마지막 날 2026-10-29 · 잠정 True 6 · 마지막 문구 1거

=== ⑦ 시작일 사건 1건 · 분위 0
  B = {'핵·미사일': 0.0283, '군사 과시': 0.0283, '위협 언어·교리': 0.0283, '완화': 0.0283}
  cuts = [np.float64(0.0), np.float64(0.0), np.float64(2.0), np.float64(249.0)] · 반올림 전 = [0.0, 0.0002, 2.0918, 249.351] · half_warning = False
  T: NaN 0 · inf 0 · min 1.442e-128 · max 8820
  단계_T 분포 {3: 5960, 4: 110, 5: 74} · 단계_최종 분포 {3: 5954, 4: 110, 5: 80}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 6023
  경고 0건
  첫날 T 8820.465060260865 · 2019-12-31 T 5.523305166726049e-75
  [⑦' 사건 2016년부터]
  B = {'핵·미사일': 0.085, '군사 과시': 0.085, '위협 언어·교리': 0.085, '완화': 0.085}
  cuts = [np.float64(0.0), np.float64(14.0), np.float64(207.0), np.float64(896.0)] · 반올림 전 = [0.0, 14.4256, 207.2977, 896.0298] · half_warning = False
  T: NaN 0 · inf 0 · min 0 · max 2940
  단계_T 분포 {2: 5778, 3: 183, 4: 108, 5: 75} · 단계_최종 분포 {2: 5760, 3: 183, 4: 108, 5: 93}
  상위% NaN 0 · 완화할인 NaN 0 · 변화율 NaN 5847
  경고 0건
  2012-01-01(T = 0인 날) 단계_T = 2 · T = 0.0

=== ⑧ ⑭ 동점(2010 초 T̄=0)
            T_원값  T_표시7일  그날까지_상위%
날짜                                
2010-01-01   0.0     0.0       0.0
2010-01-02   0.0     0.0       0.0
2010-01-03   0.0     0.0       0.0
2010-01-25   0.0     0.0       0.0
2010-01-26   0.0     0.0       0.0
2010-01-27   0.0     0.0       0.0
2010-01-28   0.0     0.0       0.0
2010-01-29   0.0     0.0       0.0
2010-02-03   0.0     0.0       0.0
  상위% 정의 직접 계산과 최대 차: 1.4210854715202004e-14
  T̄ rolling vs 직접 평균 최대 차 2.27e-13 · 0이어야 하는 날(직접=0) rolling≠0 0
  직접 T̄로 낸 상위%와 코드 상위% 다른 날: 0

=== ⑨ step_down 첫날 높은 단계
  J = [5, 1×30] → L = [5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
  J2 = [3, 5, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1] → L = [3, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3] (중간에 J=4가 와도 u는 이어짐 — ⑫ 식 그대로)
  첫날 L = J: [4, 4, 4]
  빈 J: IndexError single positional indexer is out-of-bounds

=== ⑩ type4_ids 빔
  물리_4거유형일 True 0 (전체 실행 16 ) · 하한_물리 4 이상 날 99 (전체 106 ) · 경고 0
  set() 도 같음: True
  문자열 'A7-0120'을 넘기면 4거유형일 True 0 (목록 ['A7-0120']이면 1 )
```

## L5 R5 자료형 · R6 순수성 · R2 수치 · R3 config 묶임 — `$B/r5_r6_r2.py`

```python
"""R5 자료형 · R6 순수성/결정성 · R2 문서↔코드 수치 확인 · R3 config 기본값 묶임 — 실제 사건표(기본·확장)."""
import copy
import importlib

from common import *  # noqa: F401,F403

ev = real("기본")
ev_x = real("확장")

# ---- R6 입력 불변 · 결정성 ----
snap, snap_x = ev.copy(deep=True), ev_x.copy(deep=True)
t4_snap = copy.copy(TYPE4)
d1, i1, w1 = run(ev)
d1b, i1b, _ = run(ev)
dx, ix, wx = run(ev_x, bundles=config.BUNDLES_EXT)
print("[R6] events 그대로:", ev.equals(snap), "· 확장 그대로:", ev_x.equals(snap_x), "· type4 그대로:", TYPE4 == t4_snap)
print("[R6] 같은 입력 두 번 → daily.equals:", d1.equals(d1b), "· info B equals:", i1["B"].equals(i1b["B"]))

# ---- R5 자료형 ----
print("\n[R5] 인덱스 dtype", d1.index.dtype, "· 이름", d1.index.name)
print("[R5] 열 dtype:", {c: str(t) for c, t in d1.dtypes.items()})
print("[R5] 기본 실행 중 잡힌 경고:", w1, "· 확장:", wx)
print("[R5] NaN 열:", {c: int(d1[c].isna().sum()) for c in d1.columns if d1[c].isna().any()})
print("[R5] cuts 타입", type(i1["cuts"]), i1["cuts"].dtype, "· half_warning", i1["half_warning"])

# ---- R2 ⑦ δ vs 일별 '완화할인' ----
for name, d, info in (("기본", d1, i1), ("확장", dx, ix)):
    comp = info["components"]
    delta = comp["delta"]
    disp = d["완화할인"]
    diff_raw = (delta - disp).abs()
    diff3 = int((delta.round(3) != disp.round(3)).sum())
    tp0 = comp["T_plus"] == 0
    print(f"\n[R2 ⑦ {name}] |δ − 완화할인| 최대 {diff_raw.max():.3g} · round(3) 다른 날 {diff3} · T⁺ = 0인 날 {int(tp0.sum())}"
          f" (그중 δ > 0 {int((tp0 & (delta > 0)).sum())}, δ round(3) > 0 {int((tp0 & (delta.round(3) > 0)).sum())})")
    print(f"  δ 상한 κ에 붙은 날 {int((delta >= config.RELIEF_CAP).sum())} · 완화할인 round(3) = 0.5 날 {int((disp.round(3) == 0.5).sum())}")
    post = delta.loc["2020-01-01":]
    print(f"  2020-01-01 이후 δ: 최대 {post.max():.3g} · 0 아님 {int((post > 0).sum())}일 · round(3) 0 아님 {int((post.round(3) > 0).sum())}일")

# ---- R2 ⑮ G가 시나리오에 따라 바뀌는가 ----
gb, gx = d1["원점수_게이지"], dx["원점수_게이지"]
mask = core.base_mask(d1.index)
print(f"\n[R2 ⑮] 게이지 기준기간 평균: 기본 {gb[mask].mean():.3f} · 확장 {gx[mask].mean():.3f} (1A.3 사: 7.42)")
print("  위기 눈금 기본:", core.crisis_window_max(gb).round(1).to_dict())
print("  위기 눈금 확장:", core.crisis_window_max(gx).round(1).to_dict())
print(f"  확장 게이지 = 기본 3묶음 R + 제재·압박 R? 확장 사건표의 기본 3묶음 R 합과의 최대 차 "
      f"{(gx - sum(ix['components'][f'R_{b}'] for b in BASE)).abs().max():.3f}")

# ---- R2 T 반올림(일별 CSV 3자리)과 단계 문턱 ----
for name, d, info in (("기본", d1, i1), ("확장", dx, ix)):
    T = d["T_원값"]
    LT = d["단계_T"]
    LT_r = core.stage_from_index(T.round(3), info["cuts"])
    print(f"\n[R2 ⑨ {name}] round(3)한 T로 다시 판정하면 단계_T 다른 날 {int((LT != LT_r).sum())}")
    near = pd.concat([(T - c).abs() for c in info["cuts"]], axis=1).min(axis=1)
    print(f"  T가 문턱에서 0.0005 안인 날 {int((near < 5e-4).sum())} · 0.01 안 {int((near < 1e-2).sum())}")

# ---- R2 ⑥ T⁺: sum/len vs mean(axis=1) ----
Tg = i1["components"][[f"Tg_{b}" for b in BASE]]
print(f"\n[R2 ⑥] |T⁺(sum/len) − Tg.mean(axis=1)| 최대 {(i1['components']['T_plus'] - Tg.mean(axis=1)).abs().max():.3g}")

# ---- R3 config 기본값은 import 때 묶인다 ----
old = config.RELIEF_C
config.RELIEF_C = 1.0
d_patch, _, _ = run(ev)
print(f"\n[R3] config.RELIEF_C = 1.0으로 바꾼 뒤 daily_table → 결과가 바뀌었나: {not d_patch.equals(d1)}")
direct = core.tension_components(ev, d1.index, BASE, relief_c=1.0)[0]["delta"]
print(f"  같은 값을 인자로 넘기면 δ 최대 {direct.max():.3f} (기본 {i1['components']['delta'].max():.3f})")
importlib.reload(core)
d_reload, _, _ = run(ev)
print(f"  core를 reload하면 바뀌나: {not d_reload.equals(d1)}")
config.RELIEF_C = old
importlib.reload(core)
```

```
[R6] events 그대로: True · 확장 그대로: True · type4 그대로: True
[R6] 같은 입력 두 번 → daily.equals: True · info B equals: True

[R5] 인덱스 dtype datetime64[us] · 이름 날짜
[R5] 열 dtype: {'T_원값': 'float64', 'T_표시7일': 'float64', '잠정': 'bool', 'Tg_핵·미사일': 'float64', 'Tg_군사 과시': 'float64', 'Tg_위협 언어·교리': 'float64', '완화할인': 'float64', '원점수_게이지': 'float64', '단계_T': 'int64', '하한_물리': 'int64', '물리_4거유형일': 'bool', '하한_E5': 'int64', '하한_사건': 'int64', '단계_판정': 'int64', '단계_최종': 'int64', '그날까지_상위%': 'float64', 'A2자료': 'str', '화면_단계문구': 'str', '변화14_표시': 'float64', '변화율14_표시': 'float64'}
[R5] 기본 실행 중 잡힌 경고: [] · 확장: []
[R5] NaN 열: {'변화14_표시': 14, '변화율14_표시': 2337}
[R5] cuts 타입 <class 'numpy.ndarray'> float64 · half_warning False

[R2 ⑦ 기본] |δ − 완화할인| 최대 0.077 · round(3) 다른 날 35 · T⁺ = 0인 날 66 (그중 δ > 0 35, δ round(3) > 0 35)
  δ 상한 κ에 붙은 날 272 · 완화할인 round(3) = 0.5 날 273
  2020-01-01 이후 δ: 최대 4.77e-09 · 0 아님 2492일 · round(3) 0 아님 0일

[R2 ⑦ 확장] |δ − 완화할인| 최대 0.077 · round(3) 다른 날 35 · T⁺ = 0인 날 66 (그중 δ > 0 35, δ round(3) > 0 35)
  δ 상한 κ에 붙은 날 272 · 완화할인 round(3) = 0.5 날 273
  2020-01-01 이후 δ: 최대 4.77e-09 · 0 아님 2492일 · round(3) 0 아님 0일

[R2 ⑮] 게이지 기준기간 평균: 기본 7.422 · 확장 10.679 (1A.3 사: 7.42)
  위기 눈금 기본: {'천안함': 1.9, '연평도': 11.1, '3차 핵': 13.7, '목함지뢰': 4.1, '4차 핵': 18.2, '6차 핵': 33.8, '판문점 정상회담': 5.7, '2022-11 집중발사': 55.7, '2024-06 북러조약': 33.3, '2026-09 DMZ 지뢰': 25.0}
  위기 눈금 확장: {'천안함': 1.9, '연평도': 16.1, '3차 핵': 17.9, '목함지뢰': 8.7, '4차 핵': 19.6, '6차 핵': 45.9, '판문점 정상회담': 7.5, '2022-11 집중발사': 59.2, '2024-06 북러조약': 44.6, '2026-09 DMZ 지뢰': 27.2}
  확장 게이지 = 기본 3묶음 R + 제재·압박 R? 확장 사건표의 기본 3묶음 R 합과의 최대 차 29.654

[R2 ⑨ 기본] round(3)한 T로 다시 판정하면 단계_T 다른 날 0
  T가 문턱에서 0.0005 안인 날 0 · 0.01 안 0

[R2 ⑨ 확장] round(3)한 T로 다시 판정하면 단계_T 다른 날 0
  T가 문턱에서 0.0005 안인 날 0 · 0.01 안 0

[R2 ⑥] |T⁺(sum/len) − Tg.mean(axis=1)| 최대 0

[R3] config.RELIEF_C = 1.0으로 바꾼 뒤 daily_table → 결과가 바뀌었나: False
  같은 값을 인자로 넘기면 δ 최대 0.500 (기본 0.500)
  core를 reload하면 바뀌나: True
```

추가 확인(⑭ 처음 상위% 0인 날 · ⑩ 충격 응답):

```
[⑭] 2010-01-01부터 상위% = 0 연속 73 일 · 그중 T̄ = 0 66 일 · 첫 양수 2010-03-15
[⑩] 충격 응답 k=0,10,20,29,30: [np.float64(1.0), np.float64(0.6065), np.float64(0.1353), np.float64(0.0149), np.float64(0.0)] · exp(-k²/200): [1.0, 0.6065, 0.1353, 0.0149]
```

## L6 R5 경고를 오류로 · R7 재실행 · R2 완화할인 35일

(`-W error::FutureWarning`·`-W error::RuntimeWarning`로 pytest·r5_r6_r2·run_tension·r4_edges 실행 — 예외/경고 줄 없음. pytest 첫 실행은 `tail -2`가 요약 줄을 잘라 아래 끝에 다시 돌린 결과를 붙임)

```
### R7-b 재실행(리포 밖 cwd, rc 바로 잡음) --end 2026-13-01
rc=1
pandas._libs.tslibs.parsing.DateParseError: month must be in 1..12: 2026-13-01

### R7-h2 PYTHONIOENCODING 없이 run_tension(출력 $B) — 일반 print
rc=0
  ������ �� ȭ�� �ܰ�: 2��
  �� ����: C:\Users\money\bongsu_F2review_20261029\out_check\�Ϻ�_Ȯ��.csv

### R7-h3 cp949에서 half_warning 문구
rc=1
UnicodeEncodeError: 'cp949' codec can't encode character '\u2014' in position 23: illegal multibyte sequence

### R5 -W error::FutureWarning pytest
..............                                                           [100%]

### R5 -W error::FutureWarning -W error::RuntimeWarning -W error::DeprecationWarning r5_r6_r2.py (앞 3줄)
[R6] events 그대로: True · 확장 그대로: True · type4 그대로: True
[R6] 같은 입력 두 번 → daily.equals: True · info B equals: True

rc=0

### R5 -W error::FutureWarning -W error::RuntimeWarning run_tension(--end 2026-10-27, 출력 $B)
rc=0
0

### R5 -W error::FutureWarning -W error::RuntimeWarning r4_edges.py — 예외/경고 줄만
=== ① 사건 0행
=== ② 기준기간 상승 묶음 0건(B_g=0)
=== ②' 기준기간 완화 0건(B완=0)
=== ②'' 실제 사건표 − 완화 행
=== ③ 계산 기간 밖 날짜만
=== ④ 같은 날 여러 사건
=== ⑤ END < 2019-12-31
=== ⑥ calc_days(end=None)
=== ⑦ 시작일 사건 1건 · 분위 0
=== ⑧ ⑭ 동점(2010 초 T̄=0)
=== ⑨ step_down 첫날 높은 단계
=== ⑩ type4_ids 빔

### R2 완화할인 ≠ δ 인 35일
2010-02-01 ~ 2010-03-07 · 35 일 · 연속 구간 수 1
            T_plus   delta  완화할인  단계_최종
2010-02-01     0.0  0.0528   0.0      4
2010-02-02     0.0  0.0503   0.0      4
2010-02-03     0.0  0.0478   0.0      4
            T_plus   delta  완화할인  단계_최종
2010-03-06     0.0  0.0537   0.0      1
2010-03-07     0.0  0.0511   0.0      1
14 passed in 1.74s
```

## L7 R7 run_tension.py — `$B/r7_run.py`(OUT_DIR·ROOT를 `$B`로 바꿔 main 호출)

```python
"""R7 run_tension.py — 출력 폴더·ROOT를 $B로 돌려 실행(리포 _check를 덮어쓰지 않음). 인자: case 이름."""
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
import run_tension as rt  # noqa: E402

B = Path(sys.argv[1])
case = sys.argv[2]
rt.OUT_DIR = B / "out_check"
if case == "noevents":  # 판정표만 있고 사건표 없는 ROOT
    fake = B / "fake_root"
    (fake / "data" / "tension").mkdir(parents=True, exist_ok=True)
    (fake / "data" / "tension" / "물리사건_유형판정표.csv").write_bytes((ROOT / "data/tension/물리사건_유형판정표.csv").read_bytes())
    rt.ROOT = fake
    sys.exit(rt.main(["--end", "2026-10-27"]))
if case == "normal":
    rc = rt.main(["--end", "2026-10-27"])
    out = rt.OUT_DIR / "일별_기본.csv"
    raw = out.read_bytes()
    print("rc", rc, "· BOM", raw[:3] == b"\xef\xbb\xbf", "· CRLF", b"\r\n" in raw, "· 첫 2줄:")
    print("\n".join(raw.decode("utf-8-sig").splitlines()[:2]))
    print("마지막 줄:", raw.decode("utf-8-sig").splitlines()[-1])
    lab = raw.decode("utf-8-sig").splitlines()[-1].split(",")[-3]
    print("화면_단계문구 코드포인트:", [hex(ord(ch)) for ch in lab if not ch.isalnum()])
    sys.exit(rc)
if case == "end2015":
    sys.exit(rt.main(["--end", "2015-12-31"]))
```

```
### R7-a 정상(--end 2026-10-27, 출력 $B/out_check)
계산 기간 2010-01-01 ~ 2026-10-27 · 6144일 · 모델 v0.1.4
[기본] 사건 720행 · load 제외 0
  T구간 115/256/315/378 · 반올림 전 115.27/256.48/314.82/377.91
  마지막 날 화면 단계: 2거 · 하강 중(판정 1거)
  쓴 파일: C:\Users\money\bongsu_F2review_20261029\out_check\일별_기본.csv
[확장] 사건 941행 · load 제외 0
  T구간 110/237/314/374 · 반올림 전 109.88/237.44/313.69/374.19
  마지막 날 화면 단계: 1거
  쓴 파일: C:\Users\money\bongsu_F2review_20261029\out_check\일별_확장.csv
rc 0 · BOM True · CRLF False · 첫 2줄:
날짜,T_원값,T_표시7일,잠정,Tg_핵·미사일,Tg_군사 과시,Tg_위협 언어·교리,완화할인,원점수_게이지,단계_T,하한_물리,물리_4거유형일,하한_E5,하한_사건,단계_판정,단계_최종,그날까지_상위%,A2자료,화면_단계문구,변화14_표시,변화율14_표시
2010-01-01,0.0,0.0,False,0.0,0.0,0.0,0.0,0.0,1,1,False,1,1,1,1,0.0,,1거,,
마지막 줄: 2026-10-27,92.432,107.759,True,52.205,5.366,219.725,0.0,6.563,1,1,False,1,1,1,2,40.169,A2 자료 없음(2024-11-05까지),2거 · 하강 중(판정 1거),-107.759,-50.0
화면_단계문구 코드포인트: ['0x20', '0xb7', '0x20', '0x20', '0x28', '0x20', '0x29']
rc=0

### R7-b 리포 밖 cwd에서 실제 스크립트 --end 2026-13-01
  File "pandas/_libs/tslibs/parsing.pyx", line 321, in pandas._libs.tslibs.parsing.parse_datetime_string
  File "pandas/_libs/tslibs/parsing.pyx", line 674, in pandas._libs.tslibs.parsing.dateutil_parse
pandas._libs.tslibs.parsing.DateParseError: month must be in 1..12: 2026-13-01
rc=0

### R7-c --end abc
  File "pandas/_libs/tslibs/parsing.pyx", line 652, in pandas._libs.tslibs.parsing.dateutil_parse
pandas._libs.tslibs.parsing.DateParseError: Unknown datetime string format, unable to parse: abc
rc=1

### R7-d --end 2009-12-31 (시작일보다 이름)
             ~~~~~~~~~~~~~^^^^^
IndexError: index 0 is out of bounds for axis 0 with size 0
rc=1

### R7-e 사건표 없음
             ^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\money\\bongsu_F2review_20261029\\fake_root\\data\\tension\\events_기본.csv'
rc=1

### R7-f --end 2015-12-31 (경고 없이 기준기간이 줄어듦)
계산 기간 2010-01-01 ~ 2015-12-31 · 2191일 · 모델 v0.1.4
[기본] 사건 720행 · load 제외 0
  T구간 110/234/309/415 · 반올림 전 109.92/234.19/308.71/415.44
  마지막 날 화면 단계: 2거
  쓴 파일: C:\Users\money\bongsu_F2review_20261029\out_check\일별_기본.csv
[확장] 사건 941행 · load 제외 0
  T구간 117/220/276/369 · 반올림 전 117.41/219.85/276.01/369.21
  마지막 날 화면 단계: 2거
  쓴 파일: C:\Users\money\bongsu_F2review_20261029\out_check\일별_확장.csv
rc=0

### R7-g --end 20261027 / "2026-10-27 13:00" (형식 느슨)
2026-10-27 00:00:00 2026-10-27 00:00:00

### R7-h PYTHONIOENCODING 없이 파이프(cp949 콘솔) — --end abc 전 단계 print만 확인
UnicodeEncodeError: 'cp949' codec can't encode character '\u2014' in position 17: illegal multibyte sequence
cp949
```

주: 위 R7-b의 `rc=0`은 서브셸 파이프의 `PIPESTATUS`를 잘못 읽은 것 — L6 첫 절에서 다시 돌려 `rc=1` 확인. R7-h는 `print` 한 줄만 cp949로 돌린 것이고, 실제 run_tension 경로는 L6 R7-h2(cp949로 나온 깨진 글자 — 로그에는 U+FFFD로 보임, rc 0)·R7-h3(x.5 경고 문구 UnicodeEncodeError, rc 1).

## L8 커밋 3 · 푸시

이 로그가 커밋 3에 들어가므로 커밋 3 해시와 `git push`·`gh pr view` 출력은 세션 마지막 채팅 답에 적는다. 커밋 전 금지 경로 검사:

```
$ git diff --cached --name-only | grep -E ... && echo "금지경로 있음 — 멈춤" || echo "OK"
OK
$ git diff --cached --name-only
docs/dev/reports/F2_review.md
docs/dev/reports/F2_review_log.md
```
