# tests/test_trendpod.py

import sys
import os

# Ensure the project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from exchanges.ibkr import connect_ibkr
from strategies.trend import TrendPod

ib = connect_ibkr()

if ib:
    pod = TrendPod(ib)
    for _ in range(10):  # simulate 10 ticks
        pod.run_once()

    ib.disconnect()

