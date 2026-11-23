"""Volume-weighted average price over one legacy anchor window.

Each candle contributes its typical price ``(high + low + close) / 3``,
weighted by volume. The window is the anchor that contains the latest candle.
"""

from collections import deque
from typing import Deque, List

from coinrule_x_indicators.core import CandleData, CandleIndicator
from coinrule_x_indicators.indicators.anchors import candles_in_anchor


class VWAP(CandleIndicator):
    """Volume-weighted typical price inside ``anchor_ms``."""

    def __init__(self, anchor_ms: int = 3_600_000):
        if anchor_ms <= 0:
            raise ValueError("VWAP anchor must be a positive number of milliseconds")
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
        volume = 0.0
        weighted = 0.0
        for candle in window:
            typical = (candle.high + candle.low + candle.close) / 3.0
            weighted += typical * candle.volume
            volume += candle.volume
        if volume == 0.0:
            return 0.0
        return weighted / volume

    def update(self, candle: CandleData) -> float:
        self._history.append(candle)
        self._value = self.calculate(list(self._history))
        if self._value != 0.0:
            self._initialized = True
        return float(self._value)
