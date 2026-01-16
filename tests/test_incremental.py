import pytest
from coinrule_x_indicators.indicators.sma import SMA
from tests.utils import load_candles

def test_seed_method():
    candles = load_candles("candles.json")
    indicator = SMA(period=10)
    
    # Seed with all candles
    indicator.seed(candles)
    seed_result = indicator.value
    
    batch_result = indicator.calculate(candles)
    
    assert round(seed_result, 6) == round(batch_result, 6)
