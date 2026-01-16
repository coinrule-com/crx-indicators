import pytest
from coinrule_x_indicators.indicators.donchian import DonchianChannels
from tests.utils import load_candles
import pandas as pd
import numpy as np

def test_donchian_initialization():
    indicator = DonchianChannels(period=20)
    assert indicator.period == 20

def test_donchian_calculation():
    candles = load_candles("candles.json")
    indicator = DonchianChannels(period=20)
    result = indicator.calculate(candles)
    
    # Check structure
    assert "upper" in result
    assert "middle" in result
    assert "lower" in result
    
    # Verify values manually
    df = pd.DataFrame([vars(c) for c in candles])
    highs = df['high']
    lows = df['low']
    
    # Expected max/min over last 20 periods
    expected_upper = highs.rolling(window=20).max().iloc[-1]
    expected_lower = lows.rolling(window=20).min().iloc[-1]
    expected_middle = (expected_upper + expected_lower) / 2
    
    assert result['upper'] == expected_upper
    assert result['lower'] == expected_lower
    assert result['middle'] == expected_middle

def test_donchian_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = DonchianChannels(period=20)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert incremental_result["upper"] == batch_result["upper"]
    assert incremental_result["lower"] == batch_result["lower"]
    assert incremental_result["middle"] == batch_result["middle"]

def test_donchian_window_shifting():
    """Test that the window correctly shifts and drops old values."""
    # Create simple linear candles to predict max/min easily
    # Highs: 1, 2, 3, 4, 5
    # Window 3: Max should be 3, then 4, then 5.
    
    class MockCandle:
        def __init__(self, high, low, close=0):
            self.high = high
            self.low = low
            self.close = close
            
    candles = [
        MockCandle(10, 1),
        MockCandle(11, 2),
        MockCandle(12, 3), # Window [10, 11, 12] -> Max 12, Min 1
        MockCandle(13, 4), # Window [11, 12, 13] -> Max 13, Min 2
        MockCandle(9, 5)   # Window [12, 13, 9] -> Max 13, Min 3
    ]
    
    indicator = DonchianChannels(period=3)
    
    # Update first 3
    for c in candles[:3]:
        indicator.update(c)
    
    res = indicator._value
    assert res['upper'] == 12
    assert res['lower'] == 1
    
    # Update 4th
    res = indicator.update(candles[3])
    assert res['upper'] == 13
    assert res['lower'] == 2
    
    # Update 5th (Lower high)
    res = indicator.update(candles[4])
    assert res['upper'] == 13
    assert res['lower'] == 3
