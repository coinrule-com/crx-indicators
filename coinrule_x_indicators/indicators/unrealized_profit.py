from coinrule_x_indicators.core import MetricIndicator


class UnrealizedProfit(MetricIndicator):
    """
    Unrealized Profit indicator.
    Holds the externally-provided unrealized profit value for a position.
    """

    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        """
        Set the unrealized profit value.

        Args:
            value: The unrealized profit amount.
        """
        self._value = float(value)
