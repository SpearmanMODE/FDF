# meta_rebalancer.py

import schedule
import time
from allocator.meta_allocator import MetaAllocator

PODS = ["trendpod", "breakoutpod", "momentumpod"]  # Customize as needed

def rebalance_job():
    print("[MetaAllocator] Rebalancing...")
    ma = MetaAllocator(PODS)
    new_allocs = ma.optimize()
    print("[MetaAllocator] New Allocations:", new_allocs)

# Schedule to run hourly
schedule.every().hour.do(rebalance_job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(10)
