import pytest
import json
from coinrule_x_indicators.indicators.webhook_signal import WebhookSignal


def test_webhook_signal_initialization():
    """Test that indicator initializes correctly."""
    indicator = WebhookSignal()
    assert indicator.signal is None


def test_webhook_signal_valid_open_long():
    """Test processing a valid open_long signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":"open_long"}'
    result = indicator.process_signal(signal_json)

    assert result is True
    assert indicator.signal == {"ticker": "BTC", "signal": "open_long"}


def test_webhook_signal_valid_open_short():
    """Test processing a valid open_short signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"ETH","signal":"open_short"}'
    result = indicator.process_signal(signal_json)

    assert result is True
    assert indicator.signal == {"ticker": "ETH", "signal": "open_short"}


def test_webhook_signal_valid_close_long():
    """Test processing a valid close_long signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"SOL","signal":"close_long"}'
    result = indicator.process_signal(signal_json)

    assert result is True
    assert indicator.signal == {"ticker": "SOL", "signal": "close_long"}


def test_webhook_signal_valid_close_short():
    """Test processing a valid close_short signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"MATIC","signal":"close_short"}'
    result = indicator.process_signal(signal_json)

    assert result is True
    assert indicator.signal == {"ticker": "MATIC", "signal": "close_short"}


def test_webhook_signal_invalid_signal_type():
    """Test that invalid signal types are rejected."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":"invalid_signal"}'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_missing_ticker():
    """Test that signals without ticker are rejected."""
    indicator = WebhookSignal()

    signal_json = '{"signal":"open_long"}'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_missing_signal():
    """Test that signals without signal field are rejected."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC"}'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_invalid_json():
    """Test that invalid JSON is rejected."""
    indicator = WebhookSignal()

    signal_json = 'not a valid json'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_non_dict_json():
    """Test that non-dict JSON is rejected."""
    indicator = WebhookSignal()

    signal_json = '["array", "not", "dict"]'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_wrong_ticker_type():
    """Test that non-string ticker is rejected."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":123,"signal":"open_long"}'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_wrong_signal_type():
    """Test that non-string signal is rejected."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":123}'
    result = indicator.process_signal(signal_json)

    assert result is False
    assert indicator.signal is None


def test_webhook_signal_clear():
    """Test that clear method resets the signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":"open_long"}'
    indicator.process_signal(signal_json)

    assert indicator.signal is not None

    indicator.clear()
    assert indicator.signal is None


def test_webhook_signal_overwrite():
    """Test that new signals overwrite previous ones."""
    indicator = WebhookSignal()

    signal1 = '{"ticker":"BTC","signal":"open_long"}'
    indicator.process_signal(signal1)
    assert indicator.signal == {"ticker": "BTC", "signal": "open_long"}

    signal2 = '{"ticker":"ETH","signal":"close_short"}'
    indicator.process_signal(signal2)
    assert indicator.signal == {"ticker": "ETH", "signal": "close_short"}


def test_webhook_signal_reset():
    """Test that reset clears the signal."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":"open_long"}'
    indicator.process_signal(signal_json)

    assert indicator.signal is not None

    indicator.reset()
    assert indicator.signal is None


def test_webhook_signal_equality():
    """Test that two indicators with same config are equal."""
    ind1 = WebhookSignal()
    ind2 = WebhookSignal()

    assert ind1 == ind2
    assert hash(ind1) == hash(ind2)


def test_webhook_signal_extra_fields():
    """Test that extra fields in JSON don't cause issues."""
    indicator = WebhookSignal()

    signal_json = '{"ticker":"BTC","signal":"open_long","extra":"field","another":123}'
    result = indicator.process_signal(signal_json)

    assert result is True
    # Only ticker and signal should be stored
    assert indicator.signal == {"ticker": "BTC", "signal": "open_long"}
