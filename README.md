# Backtesting Engine (Foundations)

This project implements a simple, educational backtesting engine for daily OHLCV data.
It is designed as a reusable foundation for later projects (such as a paper-trading bot).

## Features

- Load and clean daily OHLCV data using `yfinance`
- Compute simple indicators (e.g. Simple Moving Average)
- Define strategies (e.g. moving average crossover)
- Generate signals and positions with no look-ahead
- Simulate P&L and equity curve over time
- Compute core performance metrics (total return, annualized return/vol, Sharpe)
- Produce a concise, human-readable performance summary

## Requirements

- Python 3.9+ (recommended)
- Packages listed in `requirements.txt`:
  - `numpy`
  - `pandas`
  - `yfinance`
  - `matplotlib` (optional, for plotting)

## Installation

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

After installing dependencies, you can run a basic backtest from the command line:

```bash
python run_backtest.py
```

By default, the script will:

- Download daily OHLCV data for a sample ticker (e.g. `SPY`)
- Run a simple moving average crossover strategy over a sample date range
- Print a textual summary of configuration and core performance metrics

You can modify the ticker, date range, and strategy parameters inside
`01__backtesting/run_backtest.py` or extend the engine by adding new strategies
under the `backtesting` package.

## Project Layout

- `01__backtesting/` — Project 1: Backtesting engine
  - `backtesting/`
    - `data.py`: Data download and cleaning utilities
    - `indicators.py`: Indicator computations (e.g. SMA)
    - `strategy.py`: Strategy definitions and signal/position generation
    - `backtester.py`: Backtest loop and P&L/equity curve logic
    - `metrics.py`: Risk/return metrics
    - `report.py`: Human-readable reporting utilities
  - `run_backtest.py`: Script entry point for the backtest
- `run_backtest.py`: Launcher (run from repo root; delegates to 01__backtesting)
- `requirements.txt`: Python dependencies

## Assumptions & Limitations

- End-of-day (daily) data only
- Long-only, fully invested or flat positions in the initial strategy
- Transaction costs and slippage are ignored by default (can be extended later)
- Backtests are run offline in a local development environment

See `00__PROJECT_REQUIREMENTS.md` for the detailed functional and non-functional
requirements that this project is designed to satisfy.

