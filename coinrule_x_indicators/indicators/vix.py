from coinrule_x_indicators.core import MetricIndicator


class VIX(MetricIndicator):
    """Latest VIX close supplied by a market-wide feed.

    VIX is not calculated from the strategy symbol. The runner sets the
    freshest close for the rule's interval.
    """

    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        self._value = float(value)
