import pytest
from coinrule_x_indicators.indicators.ema import EMA
from tests.utils import load_candles
import pandas as pd

def test_ema_initialization():
    indicator = EMA(period=20)
    assert indicator.period == 20

def test_ema_calculation():
    candles = load_candles("candles.json")
    indicator = EMA(period=10)
    result = indicator.calculate(candles)
    
    # Manual verification
    closes = pd.Series([c.close for c in candles])
    expected = closes.ewm(span=10, adjust=False).mean().iloc[-1]
    
    assert round(result, 4) == round(expected, 4)
    assert result > 0

def test_ema_precise_value():
    """Test that EMA matches the expected value of 24.005 for the provided dataset."""
    candles = load_candles("candles.json")
    
    ema = EMA(period=9)
    result = ema.calculate(candles)
    
    # Check if result matches 24.005 with 3 decimal places precision
    assert round(result, 3) == 24.005

def test_ema_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = EMA(period=10)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    # EMA might have slight floating point differences due to different calculation order, 
    # but they should be very close.
    assert round(incremental_result, 6) == round(batch_result, 6)