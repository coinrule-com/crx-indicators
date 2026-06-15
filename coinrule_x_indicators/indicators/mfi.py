from collections import deque
from typing import Deque, List, Optional

import pandas as pd

from coinrule_x_indicators.core import CandleData, CandleIndicator


class MFI(CandleIndicator):
    """
    Money Flow Index (MFI) — volume-weighted RSI on typical price.

    Arguments:
        period (int): Lookback period. Default: 14.
    """

    def __init__(self, period: int = 14):
        self.period = period
        self._prev_tp: Optional[float] = None
        self._pos_flows: Deque[float] = deque(maxlen=period)
        self._neg_flows: Deque[float] = deque(maxlen=period)
        super().__init__(period=period)

    def reset(self):
        super().reset()
        self._prev_tp = None
        self._pos_flows.clear()
        self._neg_flows.clear()

    @staticmethod
    def _typical_price(candle: CandleData) -> float:
        return (candle.high + candle.low + candle.close) / 3.0

    def calculate_series(self, candles: List[CandleData]) -> pd.Series:
        if len(candles) < self.period + 1:
            return pd.Series([0.0] * len(candles))

        df = self.candles_to_df(candles)
        tp = (df["high"] + df["low"] + df["close"]) / 3.0
        rmf = tp * df["volume"]
        delta = tp.diff()
        pos_mf = rmf.where(delta > 0, 0.0).fillna(0.0)
        neg_mf = rmf.where(delta < 0, 0.0).fillna(0.0)
        pos_sum = pos_mf.rolling(window=self.period, min_periods=self.period).sum()
        neg_sum = neg_mf.rolling(window=self.period, min_periods=self.period).sum()
        mfr = pos_sum / neg_sum.replace(0, float("nan"))
        mfi = 100.0 - (100.0 / (1.0 + mfr))
        return mfi.fillna(0.0)

    def calculate(self, candles: List[CandleData]) -> float:
        series = self.calculate_series(candles)
        if len(series) == 0:
            return 0.0
        val = series.iloc[-1]
        return 0.0 if pd.isna(val) else float(val)

    def _mfi_from_flows(self) -> float:
        if len(self._pos_flows) < self.period:
            return 0.0
        pos_sum = sum(self._pos_flows)
        neg_sum = sum(self._neg_flows)
        if neg_sum == 0:
            return 100.0 if pos_sum > 0 else 0.0
        mfr = pos_sum / neg_sum
        return 100.0 - (100.0 / (1.0 + mfr))

    def update(self, candle: CandleData) -> float:
        tp = self._typical_price(candle)
        rmf = tp * candle.volume

        if self._prev_tp is None:
            self._prev_tp = tp
            self._value = 0.0
            return 0.0

        if tp > self._prev_tp:
            self._pos_flows.append(rmf)
            self._neg_flows.append(0.0)
        elif tp < self._prev_tp:
            self._pos_flows.append(0.0)
            self._neg_flows.append(rmf)
        else:
            self._pos_flows.append(0.0)
            self._neg_flows.append(0.0)

        self._prev_tp = tp
        self._value = self._mfi_from_flows()
        if len(self._pos_flows) >= self.period:
            self._initialized = True
        return float(self._value)
