# tests/test_breakoutpod.py

import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from strategies.breakout import BreakoutPod

pod = BreakoutPod()
for _ in range(20):
    pod.run_once()
