"""F0 뼈대 확인 — 계산 테스트는 F3에서."""
import importlib

import config


def test_import_package():
    mod = importlib.import_module("utils.tension")
    assert mod.__doc__


def test_config_values_match_adr():
    assert config.HALF_LIFE_DAYS == 14
    assert config.BASE_PERIOD == (2010, 2019)
    assert config.STAGE_QUANTILES == (0.70, 0.90, 0.95, 0.98)
    assert (config.RELIEF_C, config.RELIEF_CAP) == (0.1, 0.5)
    assert config.PHYS_FLOOR == {"3거": 3, "4거": 7, "풍선3거": 6}
    assert config.E5_FLOOR == {"3거": 4, "4거": 10}
    assert config.KILL_EVENTS == ("A7-0098", "A7-0100")
    assert config.EVENT_FLOOR_ICBM_S == 7.5
    assert config.STEP_DOWN_DAYS == 7 and config.DISPLAY_MA_DAYS == 7
    assert len(config.CRISIS_LIST) == 10


def test_half_life_definition():
    lam = 2 ** (-1 / config.HALF_LIFE_DAYS)
    assert abs(lam ** config.HALF_LIFE_DAYS - 0.5) < 1e-12
