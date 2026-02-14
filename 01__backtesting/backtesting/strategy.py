from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class MovingAverageCrossoverConfig:
    """Configuration for a simple moving average crossover strategy."""

    short_window: int = 20
    long_window: int = 50
    price_col: str = "Close"
    long_only: bool = True  # if False, allow long/short positions


def moving_average_crossover_signals(
    df: pd.DataFrame,
    config: MovingAverageCrossoverConfig,
) -> pd.DataFrame:
    """
    Generate signals for a moving average crossover strategy.

    The strategy:
    - Goes long when short MA crosses above long MA
    - Exits (or goes short) when short MA crosses below long MA

    To avoid look-ahead bias when computing P&L, we treat the
    signal at time t as the decision made at the *close* of t,
    which is implemented as a position that is applied from t+1.
    The backtest module will handle the appropriate shift.

    Returns
    -------
    pd.DataFrame
        DataFrame with added columns:
        - "signal": raw trading signal (+1, 0, -1)
    """
    price_col = config.price_col
    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not found in DataFrame.")

    if config.short_window <= 0 or config.long_window <= 0:
        raise ValueError("Window lengths must be positive integers.")

    if config.short_window >= config.long_window:
        raise ValueError("short_window must be less than long_window.")

    short_ma = (
        df[price_col]
        .rolling(window=config.short_window, min_periods=config.short_window)
        .mean()
    )
    long_ma = (
        df[price_col]
        .rolling(window=config.long_window, min_periods=config.long_window)
        .mean()
    )

    df["short_ma"] = short_ma
    df["long_ma"] = long_ma

    # Raw signal: +1 when short MA > long MA, -1 when short MA < long MA
    raw_signal = np.where(short_ma > long_ma, 1, 0 if config.long_only else -1)

    # Where either MA is NaN (insufficient history), stay flat
    raw_signal = np.where(short_ma.isna() | long_ma.isna(), 0, raw_signal)

    df["signal"] = raw_signal

    return df

