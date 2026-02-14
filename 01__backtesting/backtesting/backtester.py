from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class BacktestConfig:
    """Configuration for the backtest simulation."""

    initial_capital: float = 100_000.0
    # For this foundation project we use a simple position sizing rule:
    # - full notional exposure (100% of equity) when in a non-zero position
    # - flat when signal == 0
    # This is documented to make it easy to extend later.


def apply_positions_from_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert `signal` into a `position` series suitable for P&L computation.

    We interpret:
    - `signal` at time t as the trading decision made at the *close* of t
    - `position` at time t as the exposure applied over the period (t, t+1]

    To avoid look-ahead bias, we:
    - shift the signal forward by one period to obtain the position.
    """
    if "signal" not in df.columns:
        raise KeyError("DataFrame must contain a 'signal' column.")

    df["position"] = df["signal"].shift(1).fillna(0)
    return df


def compute_returns(
    df: pd.DataFrame,
    config: BacktestConfig,
    price_col: str = "Close",
) -> pd.DataFrame:
    """
    Compute period returns and equity curve from prices and positions.

    Assumptions
    -----------
    - Simple returns based on percentage price change
    - Full notional exposure when position != 0 (long-only in this project)
    - No transaction costs or slippage
    """
    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not found in DataFrame.")
    if "position" not in df.columns:
        raise KeyError("DataFrame must contain a 'position' column.")

    # Periodic simple returns of the underlying
    df["asset_return"] = df[price_col].pct_change().fillna(0.0)

    # Strategy return is position * underlying return
    df["strategy_return"] = df["position"] * df["asset_return"]

    # Equity curve
    equity = (1.0 + df["strategy_return"]).cumprod() * config.initial_capital
    df["equity_curve"] = equity

    return df

