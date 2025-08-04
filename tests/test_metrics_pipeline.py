import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from allocator.fund_allocator import allocator
from utils.metrics import update_performance_file

# Simulate a SELL with a +12.75 PnL
pod_name = "scalperpod"
pnl = 12.75

allocator.update_performance(pod_name.capitalize(), pnl)  # "ScalperPod"
update_performance_file(pod_name, pnl)

print(f"✅ Simulated SELL for {pod_name} with PnL = {pnl}")

