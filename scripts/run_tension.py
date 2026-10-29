"""긴장도 계산 최소판(F2-2) — data/tension/events_기본.csv·_확장.csv → data/tension/_check/일별_기본.csv·일별_확장.csv.

경로는 고정. 출력은 깃 제외 폴더 _check(.gitignore data/tension/_*) — 검산용(사용자 10-29).
입력·시나리오·출력 폴더 인자, 커밋할 결과 위치, 요약·연도별 CSV는 F4에서 정한다.

사용: python scripts/run_tension.py [--end YYYY-MM-DD]   (기본 config.END_DATE — None이면 실행일)
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from utils.tension import core  # noqa: E402
from utils.tension import io as tio  # noqa: E402

SCENARIOS = (("기본", config.BUNDLES_BASE), ("확장", config.BUNDLES_EXT))
OUT_DIR = ROOT / config.TENSION_DATA_DIR / "_check"  # F2-2 검산용 — 깃 제외. 커밋할 결과 위치는 F4


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="사건표 기본·확장 → 일별 결과 CSV(검산용 최소판)")
    p.add_argument("--end", default=config.END_DATE, help="계산 끝날 YYYY-MM-DD (기본: 실행일)")
    args = p.parse_args(argv)

    type4 = tio.type4_event_ids(tio.load_type4_table(ROOT / config.TYPE4_TABLE_PATH))
    days = core.calc_days(config.CALC_START_DATE, args.end)
    print(f"계산 기간 {days[0]:%Y-%m-%d} ~ {days[-1]:%Y-%m-%d} · {len(days)}일 · 모델 {config.TENSION_MODEL_VERSION}")

    for name, bundles in SCENARIOS:
        events, excluded = tio.load_events(ROOT / config.TENSION_DATA_DIR / f"events_{name}.csv")
        daily, info = core.daily_table(events, days, bundles, type4)
        out = OUT_DIR / f"일별_{name}.csv"
        tio.write_csv(daily.round(3), out, index=True)
        print(f"[{name}] 사건 {len(events)}행 · load 제외 {len(excluded)}")
        print(f"  T구간 {'/'.join(f'{v:g}' for v in info['cuts'])} · 반올림 전 {'/'.join(f'{v:.2f}' for v in info['quantiles_raw'])}")
        print(f"  마지막 날 화면 단계: {daily['화면_단계문구'].iloc[-1]}")
        print(f"  쓴 파일: {out}")
        if info["half_warning"]:
            print("  경고: T 구간 분위가 정확히 x.5 — 짝수 반올림 결과를 사람이 확인(산출식 1A.5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
