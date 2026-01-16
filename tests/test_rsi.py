import pytest
from coinrule_x_indicators.indicators.rsi import RSI
from tests.utils import load_candles

def test_rsi_initialization():
    rsi = RSI(period=14)
    assert rsi.period == 14

def test_rsi_insufficient_data():
    # Load the mock data (currently only 1 candle)
    candles = load_candles("candles.json")
    
    # Force insufficient data by taking only the first 5 candles
    small_candles = candles[:5]
    
    rsi = RSI(period=14)
    result = rsi.calculate(small_candles)
    
    # Expect 0.0 because len(small_candles) (5) < period (14)
    assert result == 0.0

def test_rsi_calculation_with_real_data():
    # Use the full dataset
    candles = load_candles("candles.json")
    
    if len(candles) < 15:
        pytest.skip("Not enough data to test calculation")
        
    rsi = RSI(period=14)
    result = rsi.calculate(candles)
    
    # RSI must be between 0 and 100
    assert 0 <= result <= 100
    assert isinstance(result, float)

def test_rsi_precise_value():
    """Test that RSI matches the expected value of 55.20 for the provided dataset."""
    candles = load_candles("candles.json")
    
    rsi = RSI(period=14)
    result = rsi.calculate(candles)
    
    # Check if result matches 55.20 with 2 decimal places precision
    assert round(result, 2) == 55.20

def test_rsi_incremental():
    """Test that incremental calculation matches batch calculation."""
    candles = load_candles("candles.json")
    indicator = RSI(period=14)
    
    batch_result = indicator.calculate(candles)
    
    indicator.reset()
    for candle in candles[:-1]:
        indicator.update(candle)
    
    incremental_result = indicator.update(candles[-1])
    
    assert round(incremental_result, 4) == round(batch_result, 4)