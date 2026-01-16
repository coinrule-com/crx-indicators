import pytest
from coinrule_x_indicators.indicators.price import Price
from tests.utils import load_candles

def test_price_indicator():
    candles = load_candles("candles.json")
    
    indicator = Price()
    
    # Calculate returns the close of the last candle passed
    assert indicator.calculate(candles) == candles[-1].close
    
    # Update sets the current price
    indicator.update(candles[-1])
    assert indicator.value == candles[-1].close
    assert indicator._initialized is True
