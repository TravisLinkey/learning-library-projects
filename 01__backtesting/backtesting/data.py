from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd
import yfinance as yf


@dataclass
class DataConfig:
    """Configuration for historical data download."""

    ticker: str
    start: str  # e.g. "2015-01-01"
    end: str  # e.g. "2025-01-01"
    interval: str = "1d"  # daily by default
    tz: Optional[str] = None  # timezone for index; None = leave as-is


def download_ohlcv(config: DataConfig) -> pd.DataFrame:
    """
    Download daily OHLCV data using yfinance.

    Returns
    -------
    pd.DataFrame
        DataFrame with DatetimeIndex and OHLCV columns.
    """
    df = yf.download(
        config.ticker,
        start=config.start,
        end=config.end,
        interval=config.interval,
        auto_adjust=False,
        progress=False,
    )

    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError(f"No data returned for {config.ticker} with supplied parameters.")

    # Standardize index and basic columns
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    if config.tz is not None:
        # Localize or convert to target timezone
        if df.index.tz is None:
            df.index = df.index.tz_localize(config.tz)
        else:
            df.index = df.index.tz_convert(config.tz)

    df = df.rename(
        columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Adj Close": "Adj Close",
            "Volume": "Volume",
        }
    )

    return df


def clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply basic cleaning to an OHLCV DataFrame.

    - Ensure DatetimeIndex
    - Sort ascending by date
    - Drop duplicated timestamps
    - Handle missing values (forward-fill then back-fill)
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    df = df.sort_index()

    # Drop any duplicated timestamps, keeping the first occurrence
    df = df[~df.index.duplicated(keep="first")]

    # Handle missing values with a simple documented approach:
    # 1) forward-fill
    # 2) back-fill remaining (e.g., at the very beginning)
    df = df.ffill().bfill()

    return df

