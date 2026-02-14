from __future__ import annotations

from typing import Literal

import pandas as pd


def add_sma(
    df: pd.DataFrame,
    window: int,
    price_col: str = "Close",
    column_name: str | None = None,
    min_periods: int | Literal["window"] = "window",
) -> pd.DataFrame:
    """
    Add a Simple Moving Average (SMA) column to the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with at least a `price_col` column.
    window : int
        Lookback window length for the SMA.
    price_col : str, default "Close"
        Column to compute the SMA on.
    column_name : str | None, default None
        Name for the resulting SMA column. If None, uses f"SMA_{window}".
    min_periods : int | \"window\"
        Minimum number of observations required to have a value; if \"window\",
        uses the same value as `window`.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with a new SMA column added.
    """
    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not found in DataFrame.")

    if window <= 0:
        raise ValueError("SMA window must be a positive integer.")

    if min_periods == "window":
        min_periods_int = window
    else:
        min_periods_int = int(min_periods)

    col_name = column_name or f"SMA_{window}"

    df[col_name] = (
        df[price_col]
        .rolling(window=window, min_periods=min_periods_int)
        .mean()
    )

    return df

