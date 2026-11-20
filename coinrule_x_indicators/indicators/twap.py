"""Time-weighted average price over one legacy anchor window.

Each candle contributes ``(open + high + low + close) / 4``. The result is
the average of the candles in the anchor that contains the latest candle.
"""

from collections import deque
from typing import Deque, List

from coinrule_x_indicators.core import CandleData, CandleIndicator
from coinrule_x_indicators.indicators.anchors import candles_in_anchor


class TWAP(CandleIndicator):
    """Average OHLC/4 inside ``anchor_ms``."""

    def __init__(self, anchor_ms: int = 3_600_000):
        if anchor_ms <= 0:
            raise ValueError("TWAP anchor must be a positive number of milliseconds")
        self.anchor_ms = anchor_ms
        self._history: Deque[CandleData] = deque(maxlen=2000)
        super().__init__(anchor_ms=anchor_ms)

    def reset(self) -> None:
        super().reset()
        self._history.clear()

    def calculate(self, candles: List[CandleData]) -> float:
        window = candles_in_anchor(candles, self.anchor_ms)
        if not window:
            return 0.0
        total = 0.0
        for candle in window:
            total += (candle.open + candle.high + candle.low + candle.close) / 4.0
        return total / len(window)

    def update(self, candle: CandleData) -> float:
        self._history.append(candle)
        self._value = self.calculate(list(self._history))
        if self._value != 0.0:
            self._initialized = True
        return float(self._value)
