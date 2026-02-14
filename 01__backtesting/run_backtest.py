from __future__ import annotations

"""
Simple entry point to run an example backtest using the core engine.

You can modify the ticker, date range, and strategy parameters below.
"""

from datetime import date

from backtesting.backtester import BacktestConfig, apply_positions_from_signals, compute_returns
from backtesting.data import DataConfig, clean_ohlcv, download_ohlcv
from backtesting.metrics import summarize_performance
from backtesting.report import build_text_report
from backtesting.strategy import MovingAverageCrossoverConfig, moving_average_crossover_signals


def main() -> None:
    # --- Configuration (edit here) ---
    ticker = "SPY"
    start_date = "2015-01-01"
    end_date = date.today().strftime("%Y-%m-%d")

    data_cfg = DataConfig(
        ticker=ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        tz=None,  # leave as-is
    )

    strat_cfg = MovingAverageCrossoverConfig(
        short_window=50,
        long_window=200,
        price_col="Close",
        long_only=True,
    )

    bt_cfg = BacktestConfig(initial_capital=100_000.0)

    # --- Pipeline ---

    # 1) Load and clean data
    raw = download_ohlcv(data_cfg)
    data = clean_ohlcv(raw)

    # 2) Strategy signals
    data = moving_average_crossover_signals(data, strat_cfg)

    # 3) Convert signals to positions and compute P&L / equity curve
    data = apply_positions_from_signals(data)
    data = compute_returns(data, bt_cfg, price_col=strat_cfg.price_col)

    # 4) Metrics
    metrics = summarize_performance(
        strategy_returns=data["strategy_return"],
        equity_curve=data["equity_curve"],
        risk_free_rate=0.0,  # assumption documented here
        periods_per_year=252,
    )

    # 5) Reporting
    config_summary = {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "strategy_name": "Moving Average Crossover",
        "strategy_params": {
            "short_window": strat_cfg.short_window,
            "long_window": strat_cfg.long_window,
            "long_only": strat_cfg.long_only,
        },
    }

    report_text = build_text_report(config_summary, metrics)
    print(report_text)


if __name__ == "__main__":
    main()

