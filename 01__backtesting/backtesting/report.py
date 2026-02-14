from __future__ import annotations

from typing import Mapping, Any


def format_percentage(x: float, decimals: int = 2) -> str:
    return f"{x * 100:.{decimals}f}%"  # e.g., 0.1234 -> "12.34%"


def build_text_report(
    config: Mapping[str, Any],
    metrics: Mapping[str, float],
) -> str:
    """
    Build a simple human-readable textual report.

    Parameters
    ----------
    config : Mapping[str, Any]
        High-level configuration of the backtest (ticker, dates, parameters).
    metrics : Mapping[str, float]
        Core performance metrics from the backtest.
    """
    lines: list[str] = []
    lines.append("=== Backtest Summary ===")
    lines.append("")
    lines.append("Configuration:")
    lines.append(f"  Ticker:       {config.get('ticker')}")
    lines.append(f"  Date range:   {config.get('start_date')} -> {config.get('end_date')}")
    lines.append(f"  Strategy:     {config.get('strategy_name')}")
    lines.append(
        f"  Parameters:   {config.get('strategy_params', {})}"
    )
    lines.append("")
    lines.append("Performance:")

    total_ret = metrics.get("total_return")
    ann_ret = metrics.get("annualized_return")
    ann_vol = metrics.get("annualized_volatility")
    sharpe = metrics.get("sharpe_ratio")
    mdd = metrics.get("max_drawdown")

    if total_ret is not None:
        lines.append(f"  Total return:          {format_percentage(total_ret)}")
    if ann_ret is not None:
        lines.append(f"  Annualized return:     {format_percentage(ann_ret)}")
    if ann_vol is not None:
        lines.append(f"  Annualized volatility: {format_percentage(ann_vol)}")
    if sharpe is not None:
        lines.append(f"  Sharpe ratio:          {sharpe:.2f}")
    if mdd is not None:
        lines.append(f"  Max drawdown:          {format_percentage(mdd)}")

    return "\n".join(lines)

