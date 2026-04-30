from coinrule_x_indicators.indicators.market_cap import MarketCap


def test_market_cap_initialization():
    indicator = MarketCap()
    assert indicator.value is None


def test_market_cap_set_value():
    indicator = MarketCap()
    indicator.set_value(1_250_000_000.0)
    assert indicator.value == 1_250_000_000.0


def test_market_cap_float_conversion():
    indicator = MarketCap()
    indicator.set_value(500_000_000)
    assert isinstance(indicator.value, float)
    assert indicator.value == 500_000_000.0


def test_market_cap_reset():
    indicator = MarketCap()
    indicator.set_value(750_000_000.0)
    assert indicator.value == 750_000_000.0
    indicator.reset()
    assert indicator.value is None


def test_market_cap_zero_value():
    indicator = MarketCap()
    indicator.set_value(0.0)
    assert indicator.value == 0.0


def test_market_cap_large_values():
    indicator = MarketCap()
    indicator.set_value(2_500_000_000_000.0)
    assert indicator.value == 2_500_000_000_000.0


def test_market_cap_equality():
    ind1 = MarketCap()
    ind2 = MarketCap()
    assert ind1 == ind2
    assert hash(ind1) == hash(ind2)
