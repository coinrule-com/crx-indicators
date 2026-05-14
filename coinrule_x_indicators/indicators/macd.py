from collections import deque
from typing import Deque, Dict, List

import pandas as pd

from coinrule_x_indicators.core import CandleData, CandleIndicator


def _macd_zeros() -> Dict[str, float]:
    return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}


class MACD(CandleIndicator):
    """
    Moving Average Convergence Divergence (MACD).

    Uses EMA(span=fast|slow|signal, adjust=False) on close prices, matching
    typical TradingView / pandas conventions.

    Arguments:
        fast: Fast EMA period (default 12).
        slow: Slow EMA period (default 26).
        signal: Signal line EMA period (default 9).

    ``value`` / ``calculate`` / ``update`` return a dict:
        macd — MACD line (fast EMA − slow EMA of close)
        signal — EMA of the MACD line
        histogram — MACD line − signal
    """

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        if fast <= 0 or slow <= 0 or signal <= 0:
            raise ValueError("MACD periods must be positive integers")
        if fast >= slow:
            raise ValueError("MACD fast period must be less than slow period")
        self.fast = fast
        self.slow = slow
        self.signal_period = signal
        # Enough history for incremental path to match batch pandas at the tail
        maxlen = max(300, slow + signal + slow + 20)
        self._history: Deque[CandleData] = deque(maxlen=maxlen)
        super().__init__(fast=fast, slow=slow, signal=signal)

    def reset(self) -> None:
        super().reset()
        self._history.clear()

    def calculate(self, candles: List[CandleData]) -> Dict[str, float]:
        if len(candles) < self.slow:
            return _macd_zeros()

        df = self.candles_to_df(candles)
        close = df["close"]
        fast_ema = close.ewm(span=self.fast, adjust=False, min_periods=self.fast).mean()
        slow_ema = close.ewm(span=self.slow, adjust=False, min_periods=self.slow).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(
            span=self.signal_period, adjust=False, min_periods=self.signal_period
        ).mean()
        histogram = macd_line - signal_line

        m = macd_line.iloc[-1]
        s = signal_line.iloc[-1]
        h = histogram.iloc[-1]
        if pd.isna(m) or pd.isna(s) or pd.isna(h):
            return _macd_zeros()

        return {"macd": float(m), "signal": float(s), "histogram": float(h)}

    def update(self, candle: CandleData) -> Dict[str, float]:
        self._history.append(candle)
        self._value = self.calculate(list(self._history))
        if len(self._history) >= self.slow + self.signal_period - 1:
            self._initialized = True
        return self._value
