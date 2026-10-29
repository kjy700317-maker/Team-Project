"""긴장도 계산 최소판(F2-2) — data/tension/events_기본.csv·_확장.csv → data/tension/_check/일별_기본.csv·일별_확장.csv.

경로는 고정. 출력은 깃 제외 폴더 _check(.gitignore data/tension/_*) — 검산용(사용자 10-29).
입력·시나리오·출력 폴더 인자, 커밋할 결과 위치, 요약·연도별 CSV는 F4에서 정한다.

사용: python scripts/run_tension.py [--end YYYY-MM-DD]   (기본 config.END_DATE — None이면 실행일)
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

SCENARIOS = (("기본", config.BUNDLES_BASE), ("확장", config.BUNDLES_EXT))
OUT_DIR = ROOT / config.TENSION_DATA_DIR / "_check"  # F2-2 검산용 — 깃 제외. 커밋할 결과 위치는 F4


def _end_date(text):
    """--end 값 검사 — YYYY-MM-DD 형식의 실제 날짜만(F2 검토 9)."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise argparse.ArgumentTypeError(f"YYYY-MM-DD 형식이 아님: {text}")
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"없는 날짜: {text}") from None
    return text


def _run(end) -> None:
    table = tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH)
    type4 = tio.type4_event_ids(table)
    if not type4:
        raise ValueError("판정표에 4거 유형(Y) 사건이 없음")
    days = core.calc_days(config.CALC_START_DATE, end)
    print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")
    results = []
    for name, bundles in SCENARIOS:
        path = ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"사건표 없음: {path} - scripts/build_events.py로 먼저 만든다")
        events, excluded = tio.load_events(path)
        problems = tio.check_type4_against_events(table, events)
        if len(problems):
            listed = "; ".join(f"{r.사건ID} {r.문제}" for r in problems.head(10).itertuples())
            raise ValueError(f"[{name}] 판정표와 사건표가 맞지 않음 {len(problems)}건: {listed}")
        daily, info = core.daily_table(events, days, bundles, type4)
        results.append((name, events, excluded, daily, info))
    for name, events, excluded, daily, info in results:   # 두 시나리오가 모두 계산된 뒤에만 쓴다
        out = OUT_DIR / f"일별_{name}.csv"
        tio.write_csv(daily.round(3), out, index=True)
        print(f"[{name}] 사건 {len(events)}행 · load 제외 {len(excluded)}")
        print(f"  T구간 {'/'.join(f'{v:g}' for v in info['cuts'])} · 반올림 전 {'/'.join(f'{v:.2f}' for v in info['quantiles_raw'])}")
        print(f"  마지막 날 화면 단계: {daily['화면_단계문구'].iloc[-1]}")
        print(f"  쓴 파일: {out}")
        if info["half_warning"]:
            print("  경고: T 구간 분위가 정확히 x.5 - 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):   # cp949 콘솔에 없는 글자가 있어도 멈추지 않게(F2 검토 6)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)")
    p.add_argument("--end", default=config.END_DATE, type=_end_date, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
    args = p.parse_args(argv)
    try:
        _run(args.end)
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"멈춤: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
