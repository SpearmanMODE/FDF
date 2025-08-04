# tests/test_scalperpod.py

import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from strategies.scalper import ScalperPod

pod = ScalperPod()
for _ in range(10):  # simulate 10 ticks
    pod.run_once()
