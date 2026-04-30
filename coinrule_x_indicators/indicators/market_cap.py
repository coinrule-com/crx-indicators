from coinrule_x_indicators.core import MetricIndicator


class MarketCap(MetricIndicator):
    """
    Market Cap indicator.
    Holds the externally-provided market capitalization (USD) for an asset.
    Useful for filtering trading universes (e.g. excluding low-cap assets).
    """

    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        """
        Set the market cap value.

        Args:
            value: The market capitalization in USD.
        """
        self._value = float(value)
