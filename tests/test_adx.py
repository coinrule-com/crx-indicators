import pytest
import pandas as pd
import numpy as np
from coinrule_x_indicators.indicators.adx import ADX
from tests.utils import load_candles

def test_adx_initialization():
    indicator = ADX(period=14)
    assert indicator.period == 14

def test_adx_calculation():
    candles = load_candles("candles.json")
    period = 14
    indicator = ADX(period=period)
    result = indicator.calculate(candles)
    
    # Check structure
    assert "adx" in result
    assert "plus_di" in result
    assert "minus_di" in result
    
    # Manual Verification (simplified check of logic flow)
    df = pd.DataFrame([c.to_dict() for c in candles])
    high = df['high']
    low = df['low']
    close_prev = df['close'].shift(1)
    high_prev = high.shift(1)
    low_prev = low.shift(1)
    
    tr = pd.concat([
        high - low,
        (high - close_prev).abs(),
        (low - close_prev).abs()
    ], axis=1).max(axis=1)
    
    up_move = high - high_prev
    down_move = low_prev - low
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    
    # Use com=period-1 for Wilder's
    tr_s = pd.Series(tr).ewm(com=period-1, min_periods=period, adjust=False).mean()
    pdm_s = pd.Series(plus_dm).ewm(com=period-1, min_periods=period, adjust=False).mean()
    mdm_s = pd.Series(minus_dm).ewm(com=period-1, min_periods=period, adjust=False).mean()
    
    pdi = 100 * (pdm_s / tr_s)
    mdi = 100 * (mdm_s / tr_s)
    
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    expected_adx = dx.ewm(com=period-1, min_periods=period, adjust=False).mean().iloc[-1]
    
    assert round(result['adx'], 4) == round(expected_adx, 4)
    assert 0 <= result['adx'] <= 100
    assert 0 <= result['plus_di'] <= 100
    assert 0 <= result['minus_di'] <= 100

def test_adx_precise_value():
    """Test that ADX matches exactly for the provided dataset."""
    candles = load_candles("candles.json")
    adx = ADX(period=14)
    result = adx.calculate(candles)
    # 19.2000...
    assert round(result['adx'], 2) == 19.20
    assert round(result['plus_di'], 2) == 21.35
    assert round(result['minus_di'], 2) == 20.30

def test_adx_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = ADX(period=14)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert round(incremental_result["adx"], 4) == round(batch_result["adx"], 4)