from coinrule_x_indicators.core import MetricIndicator


class BtcDominance(MetricIndicator):
    """Latest BTC dominance close supplied by a market-wide feed.

    Dominance is not calculated from the strategy symbol. The runner sets the
    freshest close for the rule's interval.
    """

    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        self._value = float(value)
