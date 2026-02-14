from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


def total_return(returns: pd.Series) -> float:
    """Total multiplicative return over the period."""
    return float((1.0 + returns).prod() - 1.0)


def annualized_return(returns: pd.Series, periods_per_year: int = 252) -> float:
    """
    Annualized return assuming simple compounding.

    Parameters
    ----------
    returns : pd.Series
        Period returns (e.g., daily).
    periods_per_year : int
        Number of periods per year (252 for trading days).
    """
    cumulative = 1.0 + total_return(returns)
    n_periods = returns.shape[0]
    if n_periods == 0:
        return 0.0
    years = n_periods / periods_per_year
    if years <= 0:
        return 0.0
    return float(cumulative ** (1.0 / years) - 1.0)


def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    """Annualized volatility of returns."""
    vol = float(returns.std(ddof=1))
    return float(vol * np.sqrt(periods_per_year))


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Compute the (excess) Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Period returns (e.g., daily) of the strategy.
    risk_free_rate : float
        Annualized risk-free rate (e.g., 0.02 for 2% per year).
    periods_per_year : int
        Number of periods per year.
    """
    if returns.empty:
        return 0.0

    # Convert annual risk-free to per-period
    rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess_returns = returns - rf_per_period

    mean_excess = float(excess_returns.mean())
    vol_excess = float(excess_returns.std(ddof=1))
    if vol_excess == 0:
        return 0.0

    return float(mean_excess / vol_excess * np.sqrt(periods_per_year))


def max_drawdown(equity_curve: pd.Series) -> float:
    """
    Maximum drawdown of an equity curve, expressed as a negative fraction.

    Returns
    -------
    float
        Minimum (most negative) drawdown value over the series.
    """
    if equity_curve.empty:
        return 0.0

    running_max = equity_curve.cummax()
    drawdowns = equity_curve / running_max - 1.0
    return float(drawdowns.min())


def summarize_performance(
    strategy_returns: pd.Series,
    equity_curve: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> dict[str, Optional[float]]:
    """
    Compute core performance metrics and return as a dictionary.
    """
    metrics: dict[str, Optional[float]] = {}
    metrics["total_return"] = total_return(strategy_returns)
    metrics["annualized_return"] = annualized_return(
        strategy_returns, periods_per_year=periods_per_year
    )
    metrics["annualized_volatility"] = annualized_volatility(
        strategy_returns, periods_per_year=periods_per_year
    )
    metrics["sharpe_ratio"] = sharpe_ratio(
        strategy_returns,
        risk_free_rate=risk_free_rate,
        periods_per_year=periods_per_year,
    )
    metrics["max_drawdown"] = max_drawdown(equity_curve)
    return metrics

