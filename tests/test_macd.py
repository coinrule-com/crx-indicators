import pytest
import pandas as pd
import numpy as np

from coinrule_x_indicators import MACD
from coinrule_x_indicators.core import CandleData
from tests.utils import load_candles


def _make_candles(closes: list) -> list:
    ts = 1_700_000_000_000
    out = []
    for i, c in enumerate(closes):
        out.append(
            CandleData(
                timestamp=ts + i * 60_000,
                open=c,
                high=c,
                low=c,
                close=c,
                volume=1.0,
            )
        )
    return out


def test_macd_init_defaults():
    m = MACD()
    assert m.fast == 12 and m.slow == 26 and m.signal_period == 9


def test_macd_invalid_periods():
    with pytest.raises(ValueError, match="positive"):
        MACD(fast=0, slow=26, signal=9)
    with pytest.raises(ValueError, match="fast period must be less"):
        MACD(fast=26, slow=26, signal=9)


def test_macd_insufficient_data():
    candles = _make_candles([100.0 + i * 0.1 for i in range(10)])
    m = MACD(fast=12, slow=26, signal=9)
    r = m.calculate(candles)
    assert r == {"macd": 0.0, "signal": 0.0, "histogram": 0.0}


def test_macd_histogram_relation():
    np.random.seed(42)
    closes = (100 + np.cumsum(np.random.randn(80))).tolist()
    candles = _make_candles(closes)
    m = MACD(12, 26, 9)
    r = m.calculate(candles)
    assert pytest.approx(r["histogram"], rel=1e-9) == r["macd"] - r["signal"]


def test_macd_matches_pandas_pipeline():
    closes = [100.0 + float(i) * 0.05 for i in range(60)]
    candles = _make_candles(closes)
    s = pd.Series(closes)
    fast, slow, sig = 12, 26, 9
    fe = s.ewm(span=fast, adjust=False, min_periods=fast).mean()
    se = s.ewm(span=slow, adjust=False, min_periods=slow).mean()
    line = fe - se
    sig_line = line.ewm(span=sig, adjust=False, min_periods=sig).mean()
    hist = line - sig_line

    m = MACD(fast, slow, sig)
    r = m.calculate(candles)
    assert pytest.approx(r["macd"], rel=1e-9) == float(line.iloc[-1])
    assert pytest.approx(r["signal"], rel=1e-9) == float(sig_line.iloc[-1])
    assert pytest.approx(r["histogram"], rel=1e-9) == float(hist.iloc[-1])


def test_macd_incremental_matches_batch():
    candles = load_candles("candles.json")
    m = MACD(12, 26, 9)
    batch = m.calculate(candles)

    m.reset()
    for c in candles[:-1]:
        m.update(c)
    inc = m.update(candles[-1])

    assert pytest.approx(inc["macd"], rel=1e-5) == pytest.approx(batch["macd"], rel=1e-5)
    assert pytest.approx(inc["signal"], rel=1e-5) == pytest.approx(batch["signal"], rel=1e-5)
    assert pytest.approx(inc["histogram"], rel=1e-5) == pytest.approx(batch["histogram"], rel=1e-5)


def test_macd_import_from_package():
    from coinrule_x_indicators import MACD as M2

    assert M2 is MACD
