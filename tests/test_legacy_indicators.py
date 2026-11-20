from coinrule_x_indicators import BtcDominance, StochasticRSI, SuperTrend, TWAP, VIX, VWAP
from coinrule_x_indicators.core import CandleData

_HOUR = 3_600_000
_EPOCH = 259_200_000


def _candle(index, open_, high, low, close, volume=1.0, start=None):
    stamp = (start if start is not None else _EPOCH + 10 * _HOUR) + index * 60_000
    return CandleData(stamp, open_, high, low, close, volume)


def test_stochastic_rsi_stays_between_zero_and_one_hundred():
    candles = [_candle(i, 100 + i, 101 + i, 99 + i, 100.5 + i) for i in range(40)]
    result = StochasticRSI(period=14).calculate(candles)
    assert 0.0 <= result["k"] <= 100.0
    assert 0.0 <= result["d"] <= 100.0


def test_stochastic_rsi_update_matches_calculate():
    candles = [_candle(i, 100 + (i % 7), 108, 95, 100 + ((i * 3) % 11)) for i in range(50)]
    indicator = StochasticRSI(period=5)
    for candle in candles:
        latest = indicator.update(candle)
    assert latest == indicator.calculate(candles)


def test_stochastic_rsi_without_enough_candles_is_zero():
    candles = [_candle(i, 100, 101, 99, 100) for i in range(5)]
    assert StochasticRSI(period=14).calculate(candles) == {"k": 0.0, "d": 0.0}


def test_supertrend_update_matches_calculate():
    candles = [
        _candle(i, 100, 110 + (i % 3), 90 - (i % 2), 100 + (i % 5))
        for i in range(30)
    ]
    indicator = SuperTrend(period=5, multiplier=3)
    for candle in candles:
        latest = indicator.update(candle)
    assert latest == indicator.calculate(candles)
    assert latest > 0


def test_supertrend_without_enough_candles_is_zero():
    candles = [_candle(i, 100, 110, 90, 100) for i in range(4)]
    assert SuperTrend(period=10).calculate(candles) == 0.0


def test_twap_averages_ohlc4_inside_the_anchor():
    anchor = 180_000
    start = _EPOCH + 5 * anchor
    inside = [
        _candle(0, 10, 14, 6, 10, start=start),
        _candle(1, 20, 24, 16, 20, start=start),
        _candle(2, 30, 34, 26, 30, start=start),
    ]
    before = CandleData(start - 60_000, 1000, 1000, 1000, 1000, 1)
    result = TWAP(anchor_ms=anchor).calculate([before, *inside])
    expected = sum((c.open + c.high + c.low + c.close) / 4 for c in inside) / 3
    assert result == expected


def test_vwap_weights_typical_price_by_volume():
    anchor = 180_000
    start = _EPOCH + 5 * anchor
    candles = [
        _candle(0, 10, 12, 8, 10, volume=1, start=start),
        _candle(1, 20, 24, 18, 21, volume=3, start=start),
        _candle(2, 30, 36, 24, 30, volume=0, start=start),
    ]
    first = (12 + 8 + 10) / 3
    second = (24 + 18 + 21) / 3
    assert VWAP(anchor_ms=anchor).calculate(candles) == (first * 1 + second * 3) / 4


def test_vwap_with_no_volume_is_zero():
    anchor = 180_000
    start = _EPOCH + 5 * anchor
    candles = [
        _candle(0, 10, 12, 8, 10, volume=0, start=start),
        _candle(1, 20, 24, 18, 21, volume=0, start=start),
        _candle(2, 30, 36, 24, 30, volume=0, start=start),
    ]
    assert VWAP(anchor_ms=anchor).calculate(candles) == 0.0


def test_an_anchor_longer_than_the_candles_is_zero():
    candles = [_candle(i, 10, 12, 8, 10) for i in range(3)]
    assert TWAP(anchor_ms=86_400_000).calculate(candles) == 0.0


def test_vix_and_btc_dominance_hold_a_supplied_close():
    vix = VIX()
    dominance = BtcDominance()
    assert vix.value is None
    assert dominance.value is None
    vix.set_value(18)
    dominance.set_value("54.2")
    assert vix.value == 18.0
    assert dominance.value == 54.2
    vix.reset()
    assert vix.value is None
