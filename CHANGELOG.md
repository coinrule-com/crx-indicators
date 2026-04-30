# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-04-30

### Added

- **Market Cap**: Metric indicator holding the externally-provided market capitalization (USD) for an asset. Useful for filtering trading universes (e.g. excluding low-cap assets).

## [1.0.0] - 2026-01-06

### Added

- **Initial Release** of Coinrule X Indicators library.
- **RSI**: Relative Strength Index with Wilder's Smoothing.
- **RSI SMA**: Simple Moving Average of RSI.
- **SMA**: Simple Moving Average.
- **EMA**: Exponential Moving Average.
- **ADX**: ADX indicator with Wilder's Smoothing.
- **ATR**: ATR indicator with Wilder's Smoothing.
- **Volume SMA**: Simple Moving Average of Volume.
- **Bollinger Bands**: Full implementation with Upper, Middle, Lower bands, bandwidth and %B.
- **Donchian Channels**: Added Donchian Channels indicator to provide the upper and lower bounds of the highest and lowest prices over a specified period.
- **Price**: Price indicator to provide the latest price of the current (open) candle.
- **Candle**: Candle indicator to provide the raw candle fields (open, high, low, close, volume).
- **Registry**: Immutable indicator registry system (`registry.yaml`).
- **Tests**: Comprehensive test suite with standard market data.
- **Registry Validation**: Added `coinrule_x-validate-indicators` CLI tool to validate `registry.yaml` files.
- **GitHub Actions**: Added GitHub Actions for release and publish to PyPI.
- **Unrealized Profit**: Metric indicator enabling retrieval of the unrealized profit for the current ticker’s open position
- **Liquidation Price**: Metric indicator enabling retrieval of the liquidation price for the current ticker’s open position
- **Webhook Signal**: Indicator to handle signals received from external sources, such as TradingView
