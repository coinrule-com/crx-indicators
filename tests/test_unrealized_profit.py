import pytest
from coinrule_x_indicators.indicators.unrealized_profit import UnrealizedProfit


def test_unrealized_profit_initialization():
    """Test that indicator initializes correctly."""
    indicator = UnrealizedProfit()
    assert indicator.value is None


def test_unrealized_profit_set_value():
    """Test setting unrealized profit values."""
    indicator = UnrealizedProfit()

    # Positive profit
    indicator.set_value(150.75)
    assert indicator.value == 150.75

    # Negative profit (loss)
    indicator.set_value(-75.25)
    assert indicator.value == -75.25


def test_unrealized_profit_float_conversion():
    """Test that values are converted to float."""
    indicator = UnrealizedProfit()

    indicator.set_value(100)
    assert isinstance(indicator.value, float)
    assert indicator.value == 100.0


def test_unrealized_profit_reset():
    """Test that reset clears the value."""
    indicator = UnrealizedProfit()

    indicator.set_value(250.50)
    assert indicator.value == 250.50

    indicator.reset()
    assert indicator.value is None


def test_unrealized_profit_zero_value():
    """Test that indicator can hold zero value (breakeven)."""
    indicator = UnrealizedProfit()

    indicator.set_value(0.0)
    assert indicator.value == 0.0


def test_unrealized_profit_large_values():
    """Test that indicator handles large profit/loss values."""
    indicator = UnrealizedProfit()

    # Large profit
    indicator.set_value(999999.99)
    assert indicator.value == 999999.99

    # Large loss
    indicator.set_value(-999999.99)
    assert indicator.value == -999999.99


def test_unrealized_profit_equality():
    """Test that two indicators with same config are equal."""
    ind1 = UnrealizedProfit()
    ind2 = UnrealizedProfit()

    assert ind1 == ind2
    assert hash(ind1) == hash(ind2)
