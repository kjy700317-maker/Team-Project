"""긴장도 계산(F4) — 사건표 → 결과 CSV(일별·요약·월별·연도별) + 추이 그림(선택).

기본: data/tension/events_기본.csv·_확장.csv → data/tension/일별_기본.csv·일별_확장.csv·요약.csv·월별.csv·연도별.csv
(결과 CSV는 커밋 — D1). 끝날 기본값은 config.END_DATE(None = 실행일, U3). 회귀 검산은 --end 2026-10-27.

사용: python scripts/run_tension.py [--end YYYY-MM-DD] [--events-dir DIR] [--out DIR] [--scenario 기본 확장] [--figure DIR]
  --figure DIR : 추이_<시나리오>.html을 DIR에 저장(확인용 — 커밋하지 않는 data/tension/_check 권장)
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from utils.tension import core  # noqa: E402
from utils.tension import io as tio  # noqa: E402
from utils.tension import summary as sm  # noqa: E402

# 시나리오 이름 → (요약 열 이름, 묶음) — 요약 열 이름은 v0.1.4 요약과 같게
SCENARIOS = {"기본": ("기본", config.BUNDLES_BASE), "확장": ("확장(C5 포함)", config.BUNDLES_EXT)}
DATA_DIR = ROOT / config.TENSION_DATA_DIR


def _end_date(text):
    """--end 값 검사 — YYYY-MM-DD 형식의 실제 날짜만(F2 검토 9)."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise argparse.ArgumentTypeError(f"YYYY-MM-DD 형식이 아님: {text}")
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"없는 날짜: {text}") from None
    return text


def _run(end, events_dir, out_dir, names, figure_dir) -> None:
    table = tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH)
    type4 = tio.type4_event_ids(table)
    if not type4:
        raise ValueError("판정표에 4거 유형(Y) 사건이 없음")
    days = core.calc_days(config.CALC_START_DATE, end)
    print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")
    results = []
    for name in names:
        label, bundles = SCENARIOS[name]
        path = events_dir / f"events_{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"사건표 없음: {path} - scripts/build_events.py로 먼저 만든다")
        events, excluded = tio.load_events(path)
        problems = tio.check_type4_against_events(table, events)
        if len(problems):
            listed = "; ".join(f"{r.사건ID} {r.문제}" for r in problems.head(10).itertuples())
            raise ValueError(f"[{name}] 판정표와 사건표가 맞지 않음 {len(problems)}건: {listed}")
        daily, info = core.daily_table(events, days, bundles, type4)
        vals = sm.summary_values(daily, info, days, bundles, input_name=path.name, n_type4=len(type4))
        results.append((name, label, events, excluded, daily, info, vals))
    # 모든 시나리오가 계산된 뒤에만 쓴다(중간에 멈추면 아무 파일도 바꾸지 않음)
    for name, label, events, excluded, daily, info, vals in results:
        out = out_dir / f"일별_{name}.csv"
        tio.write_csv(daily.round(3), out, index=True)
        print(f"[{name}] 사건 {len(events)}행 · load 제외 {len(excluded)} · T구간 {vals['T구간(2·3·4·5거 시작)']}"
              f" · 마지막 날 {daily['화면_단계문구'].iloc[-1]}")
        print(f"  쓴 파일: {out}")
        if info["half_warning"]:
            print("  경고: T 구간 분위가 정확히 x.5 - 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")
    tio.write_csv(sm.summary_table({label: vals for _, label, *_, vals in results}), out_dir / "요약.csv", index=True)
    dailies = {name: daily for name, _, _, _, daily, _, _ in results}
    tio.write_csv(sm.period_tables(dailies, "월"), out_dir / "월별.csv")
    tio.write_csv(sm.period_tables(dailies, "연"), out_dir / "연도별.csv")
    print(f"  쓴 파일: {out_dir / '요약.csv'} · 월별.csv · 연도별.csv")
    if figure_dir is not None:
        from utils.tension import charts   # 그림을 원할 때만 plotly를 읽는다
        for name, label, _, _, daily, info, _ in results:
            compare = dailies.get("확장") if name == "기본" else None
            fig = charts.trend_figure(daily, info["cuts"], compare=compare,
                                      title=f"봉수 긴장도 {config.TENSION_MODEL_VERSION} · {label} · {days[-1]:%Y-%m-%d}")
            print(f"  그림: {charts.save_html(fig, figure_dir / f'추이_{name}.html')}")


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):   # cp949 콘솔에 없는 글자가 있어도 멈추지 않게(F2 검토 6)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="사건표 → 일별·요약·월별·연도별 결과 CSV")
    p.add_argument("--end", default=config.END_DATE, type=_end_date, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
    p.add_argument("--events-dir", type=Path, default=DATA_DIR, help="사건표 폴더(events_<시나리오>.csv)")
    p.add_argument("--out", type=Path, default=DATA_DIR, help="결과 폴더")
    p.add_argument("--scenario", nargs="+", choices=list(SCENARIOS), default=list(SCENARIOS), help="계산할 시나리오")
    p.add_argument("--figure", type=Path, default=None, help="추이 그림 HTML 폴더(없으면 그리지 않음)")
    args = p.parse_args(argv)
    names = [n for n in SCENARIOS if n in args.scenario]   # 순서는 기본 → 확장
    try:
        _run(args.end, args.events_dir, args.out, names, args.figure)
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"멈춤: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
