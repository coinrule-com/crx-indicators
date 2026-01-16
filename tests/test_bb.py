import pytest
from coinrule_x_indicators.indicators.bb import BollingerBands
from tests.utils import load_candles
import pandas as pd
import numpy as np

def test_bb_initialization():
    indicator = BollingerBands(period=20, std_dev=2.0)
    assert indicator.period == 20
    assert indicator.std_dev == 2.0

def test_bb_calculation():
    candles = load_candles("candles.json")
    indicator = BollingerBands(period=20, std_dev=2.0)
    result = indicator.calculate(candles)
    
    # Check structure
    assert "upper" in result
    assert "middle" in result
    assert "lower" in result
    assert "percent_b" in result
    
    # Manual Verification
    closes = pd.Series([c.close for c in candles])
    middle = closes.rolling(window=20).mean()
    # Use ddof=0 to match implementation
    std = closes.rolling(window=20).std(ddof=0)
    
    expected_middle = middle.iloc[-1]
    expected_upper = expected_middle + (2.0 * std.iloc[-1])
    expected_lower = expected_middle - (2.0 * std.iloc[-1])
    
    assert round(result['middle'], 4) == round(expected_middle, 4)
    assert round(result['upper'], 4) == round(expected_upper, 4)
    assert round(result['lower'], 4) == round(expected_lower, 4)
    
    # Check relationships
    assert result['upper'] > result['middle'] > result['lower']
    expected_bandwidth = (result['upper'] - result['lower']) / result['middle']
    assert round(result['bandwidth'], 4) == round(expected_bandwidth, 4)

def test_bb_precise_value():
    """
    Test precise values matching user expectations.
    Values based on Population Standard Deviation (ddof=0).
    Expected:
        Upper: 24.471
        Middle: 24.025
        Lower: 23.578
        Close: 24.277
        %B: 0.783 (approx)
        Bandwidth: (24.471 - 23.578) / 24.025 = 0.037
    """
    candles = load_candles("candles.json")
    indicator = BollingerBands(period=20, std_dev=2.0)
    result = indicator.calculate(candles)
    
    assert round(result['upper'], 3) == 24.471
    assert round(result['middle'], 3) == 24.025
    assert round(result['lower'], 3) == 23.578
    # Calculated %B using full precision floats results in approx 0.782
    assert round(result['percent_b'], 3) == 0.782
    assert round(result['bandwidth'], 3) == 0.037

def test_bb_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = BollingerBands(period=20)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert round(incremental_result["middle"], 6) == round(batch_result["middle"], 6)
    assert round(incremental_result["upper"], 6) == round(batch_result["upper"], 6)
    assert round(incremental_result["lower"], 6) == round(batch_result["lower"], 6)
    assert round(incremental_result["bandwidth"], 6) == round(batch_result["bandwidth"], 6)