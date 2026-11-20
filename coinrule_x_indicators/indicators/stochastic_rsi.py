"""Stochastic RSI, matching the legacy collector.

The RSI length is also the stochastic lookback. ``%K`` is a 3-period average
of that stochastic, and ``%D`` is a 3-period average of ``%K``.
"""

from collections import deque
from typing import Deque, Dict, List

import pandas as pd

from coinrule_x_indicators.core import CandleData, CandleIndicator
from coinrule_x_indicators.indicators.rsi import RSI

_SMOOTH = 3
_ZEROS = {"k": 0.0, "d": 0.0}


class StochasticRSI(CandleIndicator):
    """Stochastic RSI lines ``k`` and ``d``."""

    def __init__(self, period: int = 14):
        if period <= 0:
            raise ValueError("Stochastic RSI period must be a positive integer")
        self.period = period
        self._history: Deque[CandleData] = deque(maxlen=max(300, period * 8))
        super().__init__(period=period)

    def reset(self) -> None:
        super().reset()
        self._history.clear()

    def calculate(self, candles: List[CandleData]) -> Dict[str, float]:
        rsi = RSI(period=self.period).calculate_series(candles)
        values = [float(item) for item in rsi.tolist() if not pd.isna(item)]
        needed = self.period + _SMOOTH + _SMOOTH - 2
        if len(values) < needed:
            return dict(_ZEROS)
        stochastic = []
        for index in range(self.period - 1, len(values)):
            window = values[index - self.period + 1:index + 1]
            low = min(window)
            high = max(window)
            current = window[-1]
            if high == low:
                stochastic.append(0.0)
            else:
                stochastic.append((current - low) / (high - low) * 100.0)
        k_values = [
            sum(stochastic[index - _SMOOTH + 1:index + 1]) / _SMOOTH
            for index in range(_SMOOTH - 1, len(stochastic))
        ]
        if len(k_values) < _SMOOTH:
            return dict(_ZEROS)
        d_value = sum(k_values[-_SMOOTH:]) / _SMOOTH
        return {"k": float(k_values[-1]), "d": float(d_value)}

    def update(self, candle: CandleData) -> Dict[str, float]:
        self._history.append(candle)
        self._value = self.calculate(list(self._history))
        if self._value["k"] != 0.0 or self._value["d"] != 0.0:
            self._initialized = True
        return self._value
