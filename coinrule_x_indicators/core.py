from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
import pandas as pd

@dataclass
class CandleData:
    """Represents a standardized OHLCV candle."""
    timestamp: int  # Unix timestamp in milliseconds
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }


class Indicator(ABC):
    """
    Base class for all Coinrule X indicators.
    Provides common interface for type hints and shared functionality.
    """

    def __init__(self, **kwargs):
        """Initialize indicator with configuration arguments."""
        self.config = kwargs
        self._id = f"{self.__class__.__name__}_{kwargs}"

    def __eq__(self, other):
        if not isinstance(other, Indicator):
            return False
        return self.__class__ == other.__class__ and self.config == other.config

    def __hash__(self):
        config_tuple = tuple(sorted(self.config.items()))
        return hash((self.__class__.__name__, config_tuple))

    @abstractmethod
    def reset(self):
        """Reset the indicator state."""
        pass

    @property
    @abstractmethod
    def value(self) -> Union[float, Dict[str, float], Dict[str, str], None]:
        """Return the current indicator value."""
        pass


class CandleIndicator(Indicator):
    """Abstract base class for candle-based indicators that calculate from OHLCV data."""

    def __init__(self, **kwargs):
        """Initialize indicator with configuration arguments."""
        super().__init__(**kwargs)
        self.reset()

    def reset(self):
        """Reset the indicator state."""
        self._value: Union[float, Dict[str, float], None] = None
        self._initialized = False

    @property
    def value(self) -> Union[float, Dict[str, float], None]:
        """Return the latest calculated value."""
        return self._value

    def candles_to_df(self, candles: List[CandleData]) -> pd.DataFrame:
        """Helper to convert list of CandleData to DataFrame."""
        return pd.DataFrame([c.to_dict() for c in candles])

    @abstractmethod
    def calculate(self, candles: List[CandleData]) -> Union[float, Dict[str, float]]:
        """
        Calculate the latest indicator value based on historical candles (stateless).
        
        Args:
            candles: List of historical candles, ending with the most recent closed candle.
            
        Returns:
            The calculated indicator value as a float, or a dictionary for multi-value indicators.
        """
        pass

    @abstractmethod
    def update(self, candle: CandleData) -> Union[float, Dict[str, float]]:
        """
        Update indicator with a new candle and return the latest value (stateful).
        
        Args:
            candle: The latest closed candle.
            
        Returns:
            The newly calculated indicator value.
        """
        pass

    def seed(self, candles: List[CandleData]):
        """
        Warm up the indicator state with historical data.

        Args:
            candles: Historical candles for initialization.
        """
        self.reset()
        for candle in candles:
            self.update(candle)


class MetricIndicator(Indicator):
    """
    Abstract base class for metric indicators that hold pure numeric values.
    These indicators don't calculate from candles but are externally provided.
    """

    def __init__(self, **kwargs):
        """Initialize metric indicator with configuration arguments."""
        super().__init__(**kwargs)
        self.reset()

    def reset(self):
        """Reset the indicator state."""
        self._value: Union[float, None] = None

    @property
    def value(self) -> Union[float, None]:
        """Return the current value."""
        return self._value

    @abstractmethod
    def set_value(self, value: float):
        """
        Set the indicator value.

        Args:
            value: The numeric value to set.
        """
        pass


class CustomSignalIndicator(Indicator):
    """
    Abstract base class for custom signal indicators that receive external signals.
    These indicators parse and validate external signals (e.g., from TradingView).
    """

    def __init__(self, **kwargs):
        """Initialize custom signal indicator with configuration arguments."""
        super().__init__(**kwargs)
        self.reset()

    def reset(self):
        """Reset the indicator state."""
        self._signal: Union[Dict[str, str], None] = None

    @property
    def value(self) -> Union[Dict[str, str], None]:
        """Return the current signal (alias for signal property)."""
        return self._signal

    @property
    def signal(self) -> Union[Dict[str, str], None]:
        """Return the current signal."""
        return self._signal

    @abstractmethod
    def process_signal(self, signal_json: str) -> bool:
        """
        Process and validate an external signal.

        Args:
            signal_json: JSON string containing the signal data.

        Returns:
            True if signal was valid and stored, False otherwise.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear the stored signal.
        Called by the runner after all strategies are evaluated.
        """
        pass
