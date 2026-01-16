from coinrule_x_indicators.core import MetricIndicator


class LiquidationPrice(MetricIndicator):
    """
    Liquidation Price indicator.
    Holds the externally-provided liquidation price value for a position.
    """

    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        """
        Set the liquidation price value.

        Args:
            value: The liquidation price.
        """
        self._value = float(value)
