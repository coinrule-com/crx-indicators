import pytest
from coinrule_x_indicators.indicators.rsi_sma import RSISMA
from tests.utils import load_candles
import pandas as pd
import numpy as np

def test_rsi_sma_initialization():
    indicator = RSISMA(rsi_period=14, sma_period=9)
    assert indicator.rsi_period == 14
    assert indicator.sma_period == 9

def test_rsi_sma_insufficient_data():
    candles = load_candles("candles.json")
    # Take fewer candles than sum of periods generally needed
    small_candles = candles[:20] 
    
    indicator = RSISMA(rsi_period=14, sma_period=14)
    result = indicator.calculate(small_candles)
    
    # Likely 0 because RSI needs 14, then SMA needs 14 periods of RSI. 
    # RSI starts producing values at index 14 (or so). 
    # So we need approx 28 candles to get a valid SMA.
    assert result == 0.0

def test_rsi_sma_calculation():
    """Test using pandas manual calculation to verify"""
    candles = load_candles("candles.json")
    
    rsi_p = 14
    sma_p = 14
    
    indicator = RSISMA(rsi_period=rsi_p, sma_period=sma_p)
    result = indicator.calculate(candles)
    
    # Manual Calc
    df = pd.DataFrame([c.to_dict() for c in candles])
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.ewm(com=rsi_p-1, min_periods=rsi_p, adjust=False).mean()
    avg_loss = loss.ewm(com=rsi_p-1, min_periods=rsi_p, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    
    sma_series = rsi_series.rolling(window=sma_p, min_periods=sma_p).mean()
    expected = sma_series.iloc[-1]
    
    print(f"Result: {result}, Expected: {expected}")
    assert round(result, 4) == round(expected, 4)
    # Just to have a concrete value assertion for regression
    assert 40 < result < 70

def test_rsi_sma_precise_value():
    """Test that RSI matches the expected value of 44.78 for the provided dataset."""
    candles = load_candles("candles.json")
    
    rsi_p = 14
    sma_p = 14
    
    indicator = RSISMA(rsi_period=rsi_p, sma_period=sma_p)
    result = indicator.calculate(candles)
    
    # Check if result matches 44.78 with 2 decimal places precision
    assert round(result, 2) == 44.78

def test_rsi_sma_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    
    rsi_p = 14
    sma_p = 14
    
    indicator = RSISMA(rsi_period=rsi_p, sma_period=sma_p)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert round(incremental_result, 2) == round(batch_result, 2)