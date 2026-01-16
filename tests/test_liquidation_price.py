import pytest
from coinrule_x_indicators.indicators.liquidation_price import LiquidationPrice


def test_liquidation_price_initialization():
    """Test that indicator initializes correctly."""
    indicator = LiquidationPrice()
    assert indicator.value is None


def test_liquidation_price_set_value():
    """Test setting a liquidation price value."""
    indicator = LiquidationPrice()

    indicator.set_value(45000.50)
    assert indicator.value == 45000.50

    indicator.set_value(50000.0)
    assert indicator.value == 50000.0


def test_liquidation_price_float_conversion():
    """Test that values are converted to float."""
    indicator = LiquidationPrice()

    indicator.set_value(42000)
    assert isinstance(indicator.value, float)
    assert indicator.value == 42000.0


def test_liquidation_price_reset():
    """Test that reset clears the value."""
    indicator = LiquidationPrice()

    indicator.set_value(48000.0)
    assert indicator.value == 48000.0

    indicator.reset()
    assert indicator.value is None


def test_liquidation_price_negative_values():
    """Test that indicator accepts negative values (short positions)."""
    indicator = LiquidationPrice()

    indicator.set_value(-1000.0)
    assert indicator.value == -1000.0


def test_liquidation_price_equality():
    """Test that two indicators with same config are equal."""
    ind1 = LiquidationPrice()
    ind2 = LiquidationPrice()

    assert ind1 == ind2
    assert hash(ind1) == hash(ind2)
