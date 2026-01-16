import pytest
import pandas as pd
from coinrule_x_indicators.indicators.atr import ATR
from tests.utils import load_candles

def test_atr_initialization():
    indicator = ATR(period=14)
    assert indicator.period == 14

def test_atr_calculation():
    candles = load_candles("candles.json")
    period = 14
    indicator = ATR(period=period)
    result = indicator.calculate(candles)
    
    # Manual Verification
    df = pd.DataFrame([c.to_dict() for c in candles])
    high = df['high']
    low = df['low']
    close_prev = df['close'].shift(1)
    
    tr1 = high - low
    tr2 = (high - close_prev).abs()
    tr3 = (low - close_prev).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Wilder's Smoothing
    expected = tr.ewm(com=period-1, adjust=False).mean().iloc[-1]
    
    assert round(result, 4) == round(expected, 4)
    assert result > 0

def test_atr_precise_value():
    """Test that ATR matches exactly for the provided dataset."""
    candles = load_candles("candles.json")
    atr = ATR(period=14)
    result = atr.calculate(candles)
    # 0.287728...
    assert round(result, 5) == 0.28773

def test_atr_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = ATR(period=14)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert round(incremental_result, 6) == round(batch_result, 6)