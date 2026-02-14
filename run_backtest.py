"""
Launcher for the backtesting project (01__backtesting).

Run from repo root: python run_backtest.py
"""

import runpy
import sys
from pathlib import Path

# Ensure 01__backtesting is on the path so "backtesting" package resolves
_ROOT = Path(__file__).resolve().parent
_PROJECT_DIR = _ROOT / "01__backtesting"
if str(_PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROJECT_DIR))

# Run the project script (avoids name collision with this launcher)
runpy.run_path(str(_PROJECT_DIR / "run_backtest.py"), run_name="__main__")
