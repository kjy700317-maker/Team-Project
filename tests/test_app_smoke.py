"""화면 AppTest(F5, U10) — 화면 브랜치를 합친 뒤 홈과 페이지 5개가 예외 없이 뜨는지(5페이지 = 가정 바꿔 보기, F10). 화면 코드는 고치지 않는다(담당 파일 원칙)."""
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ["홈.py", "pages/1_긴장도_지수.py", "pages/2_사건_기록.py", "pages/3_월별_연별.py", "pages/4_보고서.py", "pages/5_시뮬레이션.py"]


@pytest.mark.parametrize("path", SCREENS)
def test_screen_runs_without_exception(path):
    at = AppTest.from_file(str(ROOT / path), default_timeout=120).run()
    assert not at.exception, [e.value for e in at.exception]
