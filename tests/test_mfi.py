import pytest

from coinrule_x_indicators.core import CandleIndicator
from coinrule_x_indicators.indicators.candle import Candle
from coinrule_x_indicators.indicators.mfi import MFI
from tests.utils import load_candles


def test_mfi_initialization():
    mfi = MFI(period=14)
    assert mfi.period == 14


def test_mfi_insufficient_data():
    candles = load_candles("candles.json")
    mfi = MFI(period=14)
    assert mfi.calculate(candles[:5]) == 0.0


def test_mfi_calculation_with_real_data():
    candles = load_candles("candles.json")
    if len(candles) < 16:
        pytest.skip("Not enough data to test calculation")

    mfi = MFI(period=14)
    result = mfi.calculate(candles)
    assert 0 <= result <= 100
    assert isinstance(result, float)


def test_mfi_incremental():
    candles = load_candles("candles.json")
    indicator = MFI(period=14)

    batch_result = indicator.calculate(candles)

    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)

    incremental_result = indicator.update(candles[-1])
    assert round(incremental_result, 4) == round(batch_result, 4)


def test_candle_from_field_classmethods():
    close = Candle._from_field("close")
    assert isinstance(close, Candle)
    assert close.field == "close"

    via_base = CandleIndicator._from_field("high")
    assert isinstance(via_base, Candle)
    assert via_base.field == "high"
