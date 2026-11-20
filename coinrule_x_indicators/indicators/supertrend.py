"""Supertrend band used by the legacy names.

The ATR length is the legacy period. The multiplier defaults to 3 and the
band is chosen from the close, which is the collector's configuration.
"""

from collections import deque
from typing import Deque, List, Optional

import pandas as pd

from coinrule_x_indicators.core import CandleData, CandleIndicator
from coinrule_x_indicators.indicators.atr import ATR


class SuperTrend(CandleIndicator):
    """Latest Supertrend value for one ATR length and multiplier."""

    def __init__(self, period: int = 10, multiplier: float = 3.0):
        if period <= 0:
            raise ValueError("Supertrend period must be a positive integer")
        if multiplier <= 0:
            raise ValueError("Supertrend multiplier must be positive")
        self.period = period
        self.multiplier = float(multiplier)
        self._history: Deque[CandleData] = deque(maxlen=max(300, period * 8))
        super().__init__(period=period, multiplier=self.multiplier)

    def reset(self) -> None:
        super().reset()
        self._history.clear()

    def calculate(self, candles: List[CandleData]) -> float:
        if len(candles) <= self.period:
            return 0.0
        atr = ATR(period=self.period).calculate_series(candles)
        previous_upper: Optional[float] = None
        previous_lower: Optional[float] = None
        previous_supertrend: Optional[float] = None
        previous_close: Optional[float] = None
        value = 0.0
        for index in range(self.period, len(candles)):
            raw_atr = atr.iloc[index]
            if pd.isna(raw_atr):
                continue
            candle = candles[index]
            width = float(raw_atr) * self.multiplier
            basic_upper = (candle.high + candle.low) / 2.0 + width
            basic_lower = (candle.high + candle.low) / 2.0 - width
            if previous_upper is None or previous_close is None or previous_lower is None:
                upper = basic_upper
                lower = basic_lower
                rising = candle.close > upper
            else:
                upper = (
                    basic_upper
                    if basic_upper < previous_upper or previous_close > previous_upper
                    else previous_upper
                )
                lower = (
                    basic_lower
                    if basic_lower > previous_lower or previous_close < previous_lower
                    else previous_lower
                )
                if previous_supertrend == previous_upper:
                    rising = candle.close > upper
                else:
                    rising = candle.close > lower
            value = lower if rising else upper
            previous_upper = upper
            previous_lower = lower
            previous_supertrend = value
            previous_close = candle.close
        return float(value)

    def update(self, candle: CandleData) -> float:
        self._history.append(candle)
        self._value = self.calculate(list(self._history))
        if self._value != 0.0:
            self._initialized = True
        return float(self._value)
