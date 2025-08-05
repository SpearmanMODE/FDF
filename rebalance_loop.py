# rebalance_loop.py

import time
import traceback
from allocator.meta_allocator import MetaAllocator
from datetime import datetime

PODS = ["trendpod", "breakoutpod", "momentumpod", "meanrevertpod"]

def main():
    while True:
        try:
            print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rebalancing FDF strategy pods...")
            ma = MetaAllocator(PODS)
            weights = ma.optimize()
            print("[Rebalance] ✅ New Weights:", weights)
        except Exception as e:
            print("[Rebalance] ❌ Error during rebalance:")
            traceback.print_exc()

        # Sleep for 1 hour
        time.sleep(3600)

if __name__ == "__main__":
    main()
