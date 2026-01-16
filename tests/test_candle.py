import pytest
from coinrule_x_indicators.indicators.candle import Candle
from tests.utils import load_candles

def test_candle_indicator():
    candles = load_candles("candles.json")
    
    # Test close field
    ind_close = Candle(field="close")
    assert ind_close.calculate(candles) == candles[-1].close
    
    # Test volume field
    ind_vol = Candle(field="volume")
    assert ind_vol.calculate(candles) == candles[-1].volume
    
    # Test update
    val = ind_close.update(candles[-1])
    assert val == candles[-1].close
    assert ind_close._initialized is True
