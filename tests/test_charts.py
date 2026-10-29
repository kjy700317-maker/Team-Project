"""charts.py 테스트(F4) — Streamlit 없이 Figure를 만들고 HTML로 저장되는지(사건표 없이 돈다)."""
import subprocess
import sys
from pathlib import Path

import plotly.graph_objects as go

from utils.tension import charts, io as tio

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
CUTS = (115, 256, 315, 378)


def _daily(name="기본"):
    return tio.read_csv_kr(FIX / f"v014_일별_{name}.csv", index_col=0, parse_dates=True)


def test_trend_figure_parts():
    fig = charts.trend_figure(_daily(), CUTS, compare=_daily("확장"))
    assert isinstance(fig, go.Figure)
    names = [t.name for t in fig.data]
    assert names == ["A2 자료 없음(2024-11-05 이후)", "T 원값(단계 판정)", "표시선 = 7일 평균",
                     "확장(C5 포함) 7일 평균", "최종 단계"]
    rects = [s for s in fig.layout.shapes if s.type == "rect"]
    assert len(rects) == 5                                         # T 구간 띠 5개
    texts = [a.text for a in fig.layout.annotations]
    assert [f"{k}거 {c}" for k, c in zip(range(2, 6), CUTS)] == [t for t in texts if "거 " in t]
    assert "천안함" in texts and "2026-09 DMZ 지뢰" in texts           # 위기 10건 세로선 이름
    assert list(fig.data[-1].z[0]) == _daily()["단계_최종"].tolist()   # 아래 띠 = 단계_최종


def test_trend_figure_without_a2_period():
    d = _daily().loc[:"2024-06-30"]
    fig = charts.trend_figure(d, CUTS)
    assert [t.name for t in fig.data] == ["T 원값(단계 판정)", "표시선 = 7일 평균", "최종 단계"]


def test_save_html(tmp_path):
    out = charts.save_html(charts.trend_figure(_daily(), CUTS), tmp_path / "a" / "추이.html")
    assert out.exists() and out.stat().st_size > 10_000
    assert "plotly" in out.read_text(encoding="utf-8").lower()


def test_charts_does_not_import_streamlit():
    code = "import sys; import utils.tension.charts; assert 'streamlit' not in sys.modules"
    p = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode("utf-8", "replace")
