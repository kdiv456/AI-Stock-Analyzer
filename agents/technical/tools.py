"""Market-data tools for the Technical Analysis Agent."""

import json
import math

import yfinance as yf


def _get_price_history(ticker: str, period: str):
    """Fetch daily price history used internally by indicator calculations."""
    prices = yf.Ticker(ticker).history(period=period, interval="1d", auto_adjust=False)
    if prices.empty:
        raise ValueError("No historical price data is available.")
    return prices



def get_current_price(ticker: str) -> str:
    """Fetch the latest available daily closing price for a stock.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
    """
    try:
        prices = yf.Ticker(ticker).history(period="5d", auto_adjust=False)
        if prices.empty:
            raise ValueError("No recent price data is available.")

        latest = prices.iloc[-1]
        result = {
            "ticker": ticker.upper(),
            "date": latest.name.strftime("%Y-%m-%d"),
            "close": round(float(latest["Close"]), 2),
            "currency": yf.Ticker(ticker).fast_info.get("currency"),
            "source": "Yahoo Finance",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to fetch the current price for {ticker}: {error}"}
        )


def get_historical_prices(ticker: str, period: str = "1y") -> str:
    """Fetch daily closing-price and volume history for technical calculations.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        period: yfinance lookback period, for example ``6mo``, ``1y``, or ``2y``.
    """
    try:
        prices = yf.Ticker(ticker).history(period=period, interval="1d", auto_adjust=False)
        if prices.empty:
            raise ValueError("No historical price data is available.")

        history = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            }
            for date, row in prices.iterrows()
        ]

        result = {
            "ticker": ticker.upper(),
            "period": period,
            "interval": "1d",
            "source": "Yahoo Finance",
            "prices": history,
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {
                "error": (
                    f"Unable to fetch historical prices for {ticker} "
                    f"for period {period}: {error}"
                )
            }
        )


def calculate_sma(ticker: str, window: int = 20, period: str = "1y") -> str:
    """Calculate the latest simple moving average (SMA) from daily closing prices.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        window: Number of trading days included in the average.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if window < 1:
            raise ValueError("window must be at least 1.")

        prices = _get_price_history(ticker, period)
        if len(prices) < window:
            raise ValueError(f"At least {window} trading days of data are required.")

        sma = prices["Close"].rolling(window=window).mean().iloc[-1]
        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "SMA",
            "window_days": window,
            "value": round(float(sma), 2),
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate SMA for {ticker}: {error}"}
        )


def calculate_ema(ticker: str, window: int = 20, period: str = "1y") -> str:
    """Calculate the latest exponential moving average (EMA) from daily closing prices.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        window: Number of trading days used to calculate the EMA.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if window < 1:
            raise ValueError("window must be at least 1.")

        prices = _get_price_history(ticker, period)
        if len(prices) < window:
            raise ValueError(f"At least {window} trading days of data are required.")

        ema = prices["Close"].ewm(span=window, adjust=False).mean().iloc[-1]
        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "EMA",
            "window_days": window,
            "value": round(float(ema), 2),
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate EMA for {ticker}: {error}"}
        )


def calculate_rsi(ticker: str, window: int = 14, period: str = "1y") -> str:
    """Calculate the latest Relative Strength Index (RSI) from daily closing prices.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        window: Number of trading days used for the RSI calculation.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if window < 1:
            raise ValueError("window must be at least 1.")

        prices = _get_price_history(ticker, period)
        if len(prices) <= window:
            raise ValueError(f"More than {window} trading days of data are required.")

        changes = prices["Close"].diff()
        gains = changes.clip(lower=0)
        losses = -changes.clip(upper=0)
        average_gain = gains.rolling(window=window).mean().iloc[-1]
        average_loss = losses.rolling(window=window).mean().iloc[-1]

        if average_loss == 0:
            rsi = 100.0 if average_gain > 0 else 50.0
        else:
            relative_strength = average_gain / average_loss
            rsi = 100 - (100 / (1 + relative_strength))

        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "RSI",
            "window_days": window,
            "value": round(float(rsi), 2),
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate RSI for {ticker}: {error}"}
        )


def calculate_macd(
    ticker: str,
    fast_window: int = 12,
    slow_window: int = 26,
    signal_window: int = 9,
    period: str = "1y",
) -> str:
    """Calculate the latest MACD line, signal line, and histogram.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        fast_window: Fast EMA length, usually 12 trading days.
        slow_window: Slow EMA length, usually 26 trading days.
        signal_window: MACD signal EMA length, usually 9 trading days.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if min(fast_window, slow_window, signal_window) < 1:
            raise ValueError("All MACD windows must be at least 1.")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be smaller than slow_window.")

        prices = _get_price_history(ticker, period)
        if len(prices) < slow_window:
            raise ValueError(f"At least {slow_window} trading days of data are required.")

        fast_ema = prices["Close"].ewm(span=fast_window, adjust=False).mean()
        slow_ema = prices["Close"].ewm(span=slow_window, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        histogram = macd_line - signal_line

        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "MACD",
            "fast_window_days": fast_window,
            "slow_window_days": slow_window,
            "signal_window_days": signal_window,
            "macd_line": round(float(macd_line.iloc[-1]), 2),
            "signal_line": round(float(signal_line.iloc[-1]), 2),
            "histogram": round(float(histogram.iloc[-1]), 2),
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate MACD for {ticker}: {error}"}
        )


def calculate_bollinger_bands(
    ticker: str,
    window: int = 20,
    standard_deviations: float = 2.0,
    period: str = "1y",
) -> str:
    """Calculate the latest Bollinger Band levels from daily closing prices.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        window: Number of trading days in the moving average.
        standard_deviations: Number of standard deviations for each outer band.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if window < 2:
            raise ValueError("window must be at least 2.")
        if standard_deviations <= 0:
            raise ValueError("standard_deviations must be greater than 0.")

        prices = _get_price_history(ticker, period)
        if len(prices) < window:
            raise ValueError(f"At least {window} trading days of data are required.")

        middle_band = prices["Close"].rolling(window=window).mean().iloc[-1]
        standard_deviation = prices["Close"].rolling(window=window).std().iloc[-1]
        upper_band = middle_band + (standard_deviations * standard_deviation)
        lower_band = middle_band - (standard_deviations * standard_deviation)

        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "Bollinger Bands",
            "window_days": window,
            "standard_deviations": standard_deviations,
            "current_close": round(float(prices["Close"].iloc[-1]), 2),
            "middle_band": round(float(middle_band), 2),
            "upper_band": round(float(upper_band), 2),
            "lower_band": round(float(lower_band), 2),
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate Bollinger Bands for {ticker}: {error}"}
        )


def calculate_volatility(ticker: str, window: int = 20, period: str = "1y") -> str:
    """Calculate annualized historical volatility from daily closing-price returns.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        window: Number of daily returns used in the calculation.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if window < 2:
            raise ValueError("window must be at least 2.")

        prices = _get_price_history(ticker, period)
        if len(prices) <= window:
            raise ValueError(f"More than {window} trading days of data are required.")

        daily_returns = prices["Close"].pct_change().dropna().tail(window)
        annualized_volatility = daily_returns.std() * math.sqrt(252) * 100
        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "Annualized Historical Volatility",
            "window_days": window,
            "value_percent": round(float(annualized_volatility), 2),
            "trading_days_per_year": 252,
            "source": "Yahoo Finance daily closing prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {"error": f"Unable to calculate volatility for {ticker}: {error}"}
        )


def detect_support_resistance(
    ticker: str, lookback_days: int = 60, period: str = "1y"
) -> str:
    """Find trailing support and resistance from the lowest low and highest high.

    Args:
        ticker: Stock ticker symbol, for example ``AAPL`` or ``RELIANCE.NS``.
        lookback_days: Number of recent trading days used to identify the range.
        period: yfinance lookback period used to obtain price data.
    """
    try:
        if lookback_days < 1:
            raise ValueError("lookback_days must be at least 1.")

        prices = _get_price_history(ticker, period)
        if len(prices) < lookback_days:
            raise ValueError(
                f"At least {lookback_days} trading days of data are required."
            )

        recent_prices = prices.tail(lookback_days)
        result = {
            "ticker": ticker.upper(),
            "date": prices.index[-1].strftime("%Y-%m-%d"),
            "indicator": "Support and Resistance",
            "lookback_days": lookback_days,
            "current_close": round(float(prices["Close"].iloc[-1]), 2),
            "support": round(float(recent_prices["Low"].min()), 2),
            "resistance": round(float(recent_prices["High"].max()), 2),
            "method": "Lowest daily low and highest daily high over the lookback period.",
            "source": "Yahoo Finance daily OHLC prices",
        }
        return json.dumps(result, indent=2)
    except Exception as error:
        return json.dumps(
            {
                "error": (
                    f"Unable to detect support and resistance for {ticker}: {error}"
                )
            }
        )
