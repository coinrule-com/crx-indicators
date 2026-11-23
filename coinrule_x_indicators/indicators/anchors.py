"""Anchor windows used by the legacy TWAP and VWAP names.

Candles in this library are oldest first. The latest candle is the last one.
Week, month, and year windows follow UTC boundaries. A three-day window uses
the legacy reference instant. Every other anchor is a fixed-length bucket
from the legacy epoch offset.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Sequence, Tuple

from coinrule_x_indicators.core import CandleData

_WEEK_MS = 604_800_000
_MONTH_MS = 2_592_000_000
_YEAR_MS = 31_536_000_000
_THREE_DAY_MS = 259_200_000
_DAY_MS = 86_400_000
_BUCKET_EPOCH_MS = 259_200_000
_THREE_DAY_EPOCH_MS = 1_733_875_200_000


def candles_in_anchor(candles: Sequence[CandleData], anchor_ms: int) -> List[CandleData]:
    """Candles that belong to the anchor containing the latest candle."""
    if len(candles) < 2 or anchor_ms <= 0:
        return []
    period = candles[-1].timestamp - candles[-2].timestamp
    if period <= 0 or period > anchor_ms or period * len(candles) < anchor_ms:
        return []
    start, end = _bounds(candles[-1].timestamp, anchor_ms)
    return [candle for candle in candles if start <= candle.timestamp < end]


def _bounds(latest_ms: int, anchor_ms: int) -> Tuple[int, int]:
    if anchor_ms == _WEEK_MS:
        start = _start_of_week(latest_ms)
        return start, start + _WEEK_MS
    if anchor_ms == _MONTH_MS:
        start = _start_of_month(latest_ms)
        return start, _start_of_next_month(start)
    if anchor_ms == _YEAR_MS:
        moment = datetime.fromtimestamp(latest_ms / 1000, tz=timezone.utc)
        start = int(datetime(moment.year, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
        end = int(datetime(moment.year + 1, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
        return start, end
    if anchor_ms == _THREE_DAY_MS:
        start = _THREE_DAY_EPOCH_MS + ((latest_ms - _THREE_DAY_EPOCH_MS) // anchor_ms) * anchor_ms
        return start, start + anchor_ms
    start = _BUCKET_EPOCH_MS + ((latest_ms - _BUCKET_EPOCH_MS) // anchor_ms) * anchor_ms
    return start, start + anchor_ms


def _start_of_week(timestamp_ms: int) -> int:
    moment = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    monday_offset = (moment.weekday()) * _DAY_MS
    midnight = (timestamp_ms // _DAY_MS) * _DAY_MS
    return midnight - monday_offset


def _start_of_month(timestamp_ms: int) -> int:
    moment = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    return int(datetime(moment.year, moment.month, 1, tzinfo=timezone.utc).timestamp() * 1000)


def _start_of_next_month(timestamp_ms: int) -> int:
    moment = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    year = moment.year + (1 if moment.month == 12 else 0)
    month = 1 if moment.month == 12 else moment.month + 1
    return int(datetime(year, month, 1, tzinfo=timezone.utc).timestamp() * 1000)
