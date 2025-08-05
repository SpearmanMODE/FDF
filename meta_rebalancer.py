# meta_rebalancer.py

import schedule
import time
import os
from dotenv import load_dotenv

# ✅ Always load .env from script directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

from allocator.meta_allocator import MetaAllocator

# Define pods to include in the allocator
PODS = ["trendpod", "breakoutpod", "momentumpod", "meanrevertpod"]

def rebalance_job():
    print("[MetaAllocator] Rebalancing...")
    ma = MetaAllocator(PODS)
    new_allocs = ma.optimize()
    print("[MetaAllocator] New Allocations:", new_allocs)

# Run immediately once on startup
rebalance_job()

# Schedule hourly execution
schedule.every().hour.do(rebalance_job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(10)



