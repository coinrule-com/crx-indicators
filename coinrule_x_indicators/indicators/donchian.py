from typing import List, Dict, Union
import pandas as pd
from collections import deque
from coinrule_x_indicators.core import CandleIndicator, CandleData

class DonchianChannels(CandleIndicator):
    """
    Donchian Channels.
    
    Arguments:
        period (int): Lookback period. Default: 20.
    """
    
    def __init__(self, period: int = 20):
        self.period = period
        self._high_history = deque(maxlen=period)
        self._low_history = deque(maxlen=period)
        super().__init__(period=period)

    def reset(self):
        super().reset()
        self._high_history = deque(maxlen=self.period)
        self._low_history = deque(maxlen=self.period)

    def calculate(self, candles: List[CandleData]) -> Dict[str, float]:
        if not candles:
             return {"upper": 0.0, "middle": 0.0, "lower": 0.0}
             
        df = self.candles_to_df(candles)
        
        # Calculate Rolling High and Low
        upper = df['high'].rolling(window=self.period, min_periods=self.period).max()
        lower = df['low'].rolling(window=self.period, min_periods=self.period).min()
        middle = (upper + lower) / 2
        
        last_upper = upper.iloc[-1]
        last_lower = lower.iloc[-1]
        last_middle = middle.iloc[-1]
        
        if pd.isna(last_upper):
            # Not enough data
            # Fallback to current available max/min if we want partial results, 
            # or 0.0 standard behavior
            return {"upper": 0.0, "middle": 0.0, "lower": 0.0}

        return {
            "upper": float(last_upper),
            "middle": float(last_middle),
            "lower": float(last_lower)
        }

    def update(self, candle: CandleData) -> Dict[str, float]:
        self._high_history.append(candle.high)
        self._low_history.append(candle.low)
        
        if len(self._high_history) < self.period:
            # Not enough data yet
            # We can return partial max/min or 0.
            # Consistent with other indicators, return 0 until warmed up
            self._value = {"upper": 0.0, "middle": 0.0, "lower": 0.0}
            return self._value

        self._initialized = True
        
        # O(N) calculation for sliding window max/min
        # Since period is small (typ 20-50), this is acceptable.
        upper = max(self._high_history)
        lower = min(self._low_history)
        middle = (upper + lower) / 2
            
        self._value = {
            "upper": float(upper),
            "middle": float(middle),
            "lower": float(lower)
        }
        
        return self._value
