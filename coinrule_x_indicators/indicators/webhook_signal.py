import json
from typing import Dict, Union
from coinrule_x_indicators.core import CustomSignalIndicator


class WebhookSignal(CustomSignalIndicator):
    """
    Webhook Signal indicator.
    Receives and validates external signals from Webhook API.
    Signal format: {"ticker":"BTC","signal":"open_long/open_short/close_long/close_short"}
    """

    VALID_SIGNALS = {"open_long", "open_short", "close_long", "close_short"}

    def __init__(self):
        super().__init__()

    def process_signal(self, signal_json: str) -> bool:
        """
        Process and validate an external Webhook signal.

        Args:
            signal_json: JSON string in format {"ticker":"BTC","signal":"open_long"}

        Returns:
            True if signal was valid and stored, False otherwise.
        """
        try:
            # Parse JSON
            signal_data = json.loads(signal_json)

            # Validate structure
            if not isinstance(signal_data, dict):
                return False

            # Validate required fields
            if "ticker" not in signal_data or "signal" not in signal_data:
                return False

            # Validate types
            if not isinstance(signal_data["ticker"], str):
                return False
            if not isinstance(signal_data["signal"], str):
                return False

            # Validate signal value
            if signal_data["signal"] not in self.VALID_SIGNALS:
                return False

            # Store valid signal
            self._signal = {
                "ticker": signal_data["ticker"],
                "signal": signal_data["signal"]
            }
            return True

        except (json.JSONDecodeError, KeyError, TypeError):
            return False

    def clear(self):
        """
        Clear the stored signal.
        Called by the runner after all strategies are evaluated.
        """
        self._signal = None
