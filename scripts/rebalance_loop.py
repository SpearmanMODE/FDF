# scripts/rebalance_loop.py

import schedule
import time
import logging
from allocator.meta_allocator import MetaAllocator

logging.basicConfig(
    filename="rebalance.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

def job():
    try:
        logging.info("Starting rebalance...")
        ma = MetaAllocator()
        result = ma.optimize()
        logging.info(f"Rebalance complete: {result}")
    except Exception as e:
        logging.error(f"Error during rebalance: {e}")

schedule.every().hour.at(":00").do(job)

if __name__ == "__main__":
    logging.info("Rebalance scheduler started")
    job()  # run once on launch
    while True:
        schedule.run_pending()
        time.sleep(10)
