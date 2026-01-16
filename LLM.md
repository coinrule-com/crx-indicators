# Coinrule X Indicators - LLM Indicator Usage Guide

This document provides comprehensive information about available indicators in the Coinrule X indicator library for use in AI-generated trading strategies.

## Overview

This guide explains how to use prebuilt indicators within the Coinrule X framework when generating trading strategies. It also describes the recommended practices and patterns to follow if you need to create a custom indicator.

## Architecture

### Indicator Base Classes

All indicators inherit from one of these abstract base classes:

#### 1. CandleIndicator

Calculates values from historical OHLCV candle data.

```python
from coinrule_x_indicators.core import CandleIndicator, CandleData

class MyCustomIndicator(CandleIndicator):
    def __init__(self, period: int = 14):
        self.period = period
        super().__init__(period=period)

    def calculate(self, candles: List[CandleData]) -> Union[float, Dict[str, float]]:
        """Stateless batch calculation on historical candles."""
        # Return float for single-value indicators
        # Return Dict[str, float] for multi-value indicators (e.g., {"upper": 100, "lower": 50})
        pass

    def update(self, candle: CandleData) -> Union[float, Dict[str, float]]:
        """Stateful incremental update with new candle."""
        pass
```

**CandleData Structure:**

```python
@dataclass
class CandleData:
    timestamp: int    # Unix timestamp in milliseconds
    open: float
    high: float
    low: float
    close: float
    volume: float
```

#### 2. MetricIndicator

Holds externally-provided numeric values (e.g., position metrics).

```python
from coinrule_x_indicators.core import MetricIndicator

class MyMetricIndicator(MetricIndicator):
    def __init__(self):
        super().__init__()

    def set_value(self, value: float):
        """Set the indicator value."""
        self._value = float(value)
```

#### 3. CustomSignalIndicator

Receives and validates external signals (e.g., webhooks from TradingView).

```python
from coinrule_x_indicators.core import CustomSignalIndicator

class MySignalIndicator(CustomSignalIndicator):
    def __init__(self):
        super().__init__()

    def process_signal(self, signal_json: str) -> bool:
        """Parse and validate external signal. Return True if valid."""
        # Parse JSON, validate, store in self._signal
        pass

    def clear(self):
        """Clear stored signal after use."""
        self._signal = None
```

---

## Available Indicators

### Trend Indicators

#### SMA (Simple Moving Average)

**Import:** `from coinrule_x_indicators import SMA`

Calculates the arithmetic mean of prices over a specified period.

**Parameters:**

- `period` (int, default=20): Lookback period

**Returns:** `float` - The simple moving average value

**Usage:**

```python
sma_20 = SMA(period=20)
sma_50 = SMA(period=50)

# Strategy example: Golden cross
if sma_20.value > sma_50.value:
    # Short-term trend above long-term trend
```

---

#### EMA (Exponential Moving Average)

**Import:** `from coinrule_x_indicators import EMA`

Calculates exponentially weighted moving average, giving more weight to recent prices.

**Parameters:**

- `period` (int, default=20): Lookback period

**Returns:** `float` - The exponential moving average value

**Usage:**

```python
ema_12 = EMA(period=12)
ema_26 = EMA(period=26)

# Strategy example: EMA crossover
if ema_12.value > ema_26.value:
    # Fast EMA above slow EMA (bullish)
```

---

### Momentum Indicators

#### RSI (Relative Strength Index)

**Import:** `from coinrule_x_indicators import RSI`

Measures momentum by comparing the magnitude of recent gains to recent losses.

**Parameters:**

- `period` (int, default=14): Lookback period

**Returns:** `float` - RSI value between 0 and 100

**Interpretation:**

- RSI > 70: Overbought conditions
- RSI < 30: Oversold conditions
- RSI = 50: Neutral momentum

**Usage:**

```python
rsi = RSI(period=14)

# Strategy example: Oversold bounce
if rsi.value < 30:
    # Potential oversold reversal opportunity
```

---

#### RSISMA (RSI with SMA)

**Import:** `from coinrule_x_indicators import RSISMA`

Combines RSI with a simple moving average of RSI for smoothed momentum signals.

**Parameters:**

- `rsi_period` (int, default=14): RSI calculation period
- `sma_period` (int, default=14): SMA smoothing period on RSI

**Returns:** `Dict[str, float]`

- `rsi`: Current RSI value
- `rsi_sma`: SMA of RSI values

**Usage:**

```python
rsi_sma = RSISMA(rsi_period=14, sma_period=9)

# Strategy example: RSI crossing its moving average
if rsi_sma.value["rsi"] > rsi_sma.value["rsi_sma"]:
    # Momentum accelerating upward
```

---

#### ADX (Average Directional Index)

**Import:** `from coinrule_x_indicators import ADX`

Measures trend strength regardless of direction.

**Parameters:**

- `period` (int, default=14): Lookback period

**Returns:** `Dict[str, float]`

- `adx`: Trend strength (0-100, higher = stronger trend)
- `plus_di`: Positive directional indicator
- `minus_di`: Negative directional indicator

**Interpretation:**

- ADX < 20: Weak trend or ranging market
- ADX > 25: Strong trend developing
- ADX > 50: Very strong trend

**Usage:**

```python
adx = ADX(period=14)

# Strategy example: Trend strength filter
if adx.value["adx"] > 25 and adx.value["plus_di"] > adx.value["minus_di"]:
    # Strong uptrend confirmed
```

---

### Volatility Indicators

#### BollingerBands

**Import:** `from coinrule_x_indicators import BollingerBands`

Volatility bands around a moving average, useful for identifying compression and expansion.

**Parameters:**

- `period` (int, default=20): Moving average period
- `std_dev` (float, default=2.0): Standard deviation multiplier

**Returns:** `Dict[str, float]`

- `upper`: Upper band (mean + std_dev \* std)
- `middle`: Middle band (SMA)
- `lower`: Lower band (mean - std_dev \* std)
- `percent_b`: Price position within bands (0 = lower, 1 = upper)
- `bandwidth`: Band width relative to middle (volatility measure)

**Usage:**

```python
bb = BollingerBands(period=20, std_dev=2.0)

# Strategy example: Squeeze breakout
if bb.value["bandwidth"] < 0.1:  # Bands compressed
    # Low volatility, potential breakout coming

# Strategy example: Band penetration
if bb.value["percent_b"] > 1.0:
    # Price above upper band (extended move)
```

---

#### ATR (Average True Range)

**Import:** `from coinrule_x_indicators import ATR`

Measures market volatility by calculating the average range between high and low prices.

**Parameters:**

- `period` (int, default=14): Lookback period

**Returns:** `float` - Average true range value

**Usage:**

```python
atr = ATR(period=14)

# Strategy example: Volatility expansion
atr_current = atr.value
# Compare to historical ATR to detect volatility changes
# ATR is often used for stop-loss placement
```

---

### Channel/Breakout Indicators

#### DonchianChannels

**Import:** `from coinrule_x_indicators import DonchianChannels`

Tracks highest high and lowest low over a period, useful for breakout strategies.

**Parameters:**

- `period` (int, default=20): Lookback period

**Returns:** `Dict[str, float]`

- `upper`: Highest high over period
- `middle`: Midpoint of channel
- `lower`: Lowest low over period

**Usage:**

```python
donchian = DonchianChannels(period=20)
price = Price()

# Strategy example: Channel breakout
if price.value > donchian.value["upper"]:
    # Price broke above recent high (bullish breakout)

if price.value < donchian.value["lower"]:
    # Price broke below recent low (bearish breakout)
```

---

### Price/Volume Indicators

#### Price

**Import:** `from coinrule_x_indicators import Price`

Returns the current/live price of the asset.

**Parameters:** None

**Returns:** `float` - Latest price (close of most recent candle)

**Usage:**

```python
price = Price()
sma_200 = SMA(period=200)

# Strategy example: Price relative to moving average
if price.value > sma_200.value:
    # Price trading above 200-period moving average
```

---

#### Candle

**Import:** `from coinrule_x_indicators import Candle`

Provides access to raw candle OHLCV fields.

**Parameters:**

- `field` (str, default="close"): Field to return ('open', 'high', 'low', 'close', 'volume')

**Returns:** `float` - Specified candle field value

**Usage:**

```python
close = Candle(field="close")
high = Candle(field="high")
low = Candle(field="low")
volume = Candle(field="volume")

# Strategy example: High/Low comparison
if close.value > high.value * 0.95:
    # Close near high of candle (bullish)
```

---

#### VolumeSMA

**Import:** `from coinrule_x_indicators import VolumeSMA`

Simple moving average of volume, useful for detecting volume surges.

**Parameters:**

- `period` (int, default=20): Lookback period

**Returns:** `float` - Average volume over period

**Usage:**

```python
volume = Candle(field="volume")
volume_sma = VolumeSMA(period=20)

# Strategy example: Volume surge
if volume.value > volume_sma.value * 2.0:
    # Volume is 2x average (high conviction move)
```

---

### Metric Indicators (Position Metrics)

#### LiquidationPrice

**Import:** `from coinrule_x_indicators import LiquidationPrice`

Holds the liquidation price for a leveraged position (externally provided).

**Parameters:** None

**Returns:** `float` - Liquidation price value

**Usage:**

```python
liq_price = LiquidationPrice()
price = Price()

# Strategy example: Risk management
# Note: Value is set externally via liq_price.set_value(price)
# In strategies, you typically read it for risk checks
```

---

#### UnrealizedProfit

**Import:** `from coinrule_x_indicators import UnrealizedProfit`

Holds the unrealized profit/loss for an open position (externally provided).

**Parameters:** None

**Returns:** `float` - Unrealized P&L value (positive = profit, negative = loss)

**Usage:**

```python
unrealized_pnl = UnrealizedProfit()

# Strategy example: Trailing take-profit
# Note: Value is set externally via unrealized_pnl.set_value(pnl)
# In strategies, you can use this for conditional exits
```

---

### Signal Indicators (External Signals)

#### WebhookSignal

**Import:** `from coinrule_x_indicators import WebhookSignal`

Receives and validates external trading signals via webhook (e.g., from TradingView).

**Parameters:** None

**Signal Format (JSON):**

```json
{
  "ticker": "BTC",
  "signal": "open_long" | "open_short" | "close_long" | "close_short"
}
```

**Returns:** `Dict[str, str]` via `.signal` property

- `ticker`: Asset ticker
- `signal`: One of the four valid signals

**Usage:**

```python
webhook = WebhookSignal()

# Note: Signal is processed externally via webhook.process_signal(json_string)
# In strategies, you read the validated signal

if webhook.signal and webhook.signal["signal"] == "open_long":
    # External signal triggered long entry
```

---

## Creating Custom Indicators

If the required indicator is **not available** in the library, you can create it by extending `CandleIndicator`:

```python
from coinrule_x_indicators.core import CandleIndicator, CandleData
from typing import List
import pandas as pd

class VWAP(CandleIndicator):
    """Volume Weighted Average Price."""

    def __init__(self, period: int = 20):
        self.period = period
        super().__init__(period=period)

    def calculate(self, candles: List[CandleData]) -> float:
        if len(candles) < self.period:
            return 0.0

        df = self.candles_to_df(candles[-self.period:])
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        vwap = (typical_price * df['volume']).sum() / df['volume'].sum()

        return float(vwap)

    def update(self, candle: CandleData) -> float:
        # Implement stateful update logic
        # (For simplicity, recalculate or maintain sliding window)
        pass
```

**Note:** Custom indicators **must not** introduce any new dependencies. Only use the libraries already used in the Coinrule X Indicators framework (e.g., `pandas`, `numpy`, standard Python libraries).

**Custom Indicator Requirements:**

1. Inherit from `CandleIndicator`
2. Implement `calculate()` for batch computation
3. Implement `update()` for incremental updates
4. Use `self.candles_to_df(candles)` helper to convert to pandas DataFrame
5. Return `float` for single values or `Dict[str, float]` for multiple values
6. Handle insufficient data gracefully (return 0.0 or appropriate default)

---

## Questions?

If you need an indicator that doesn't exist:

1. Check if you can combine existing indicators to achieve the same goal
2. If not, create a custom `CandleIndicator` following the template above
3. Ensure your custom indicator follows the same patterns as built-in indicators
