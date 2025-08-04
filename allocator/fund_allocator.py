# allocator/fund_allocator.py

from config import CAPITAL_ALLOCATION
import logging

logger = logging.getLogger(__name__)

class FundAllocator:
    def __init__(self):
        self.allocations = CAPITAL_ALLOCATION.copy()
        self.performance = {pod: {'pnl': 0.0} for pod in CAPITAL_ALLOCATION}

    def update_performance(self, pod_name, pnl):
        if pod_name not in self.performance:
            self.performance[pod_name] = {'pnl': 0.0}
        self.performance[pod_name]['pnl'] += pnl

    def rebalance(self, new_allocations=None):
        if new_allocations:
            total_cap = sum(CAPITAL_ALLOCATION.values())
            self.allocations = {
                pod: round(new_allocations.get(pod, 0.0) * total_cap, 2)
                for pod in CAPITAL_ALLOCATION
            }
            logger.info(f"[Rebalance] New Allocations: {self.allocations}")
            return self.allocations

        total_perf = sum([max(0, v['pnl']) for v in self.performance.values()])
        if total_perf == 0:
            return self.allocations

        new_allocations = {}
        for pod, base_cap in CAPITAL_ALLOCATION.items():
            weight = max(0, self.performance[pod]['pnl']) / total_perf
            new_allocations[pod] = round(weight * sum(CAPITAL_ALLOCATION.values()), 2)

        self.allocations = new_allocations
        logger.info(f"[Rebalance] Auto Allocations: {self.allocations}")
        return new_allocations

    def get_allocation(self, pod_name):
        return self.allocations.get(pod_name, 0.0)

    def get_position_size(self, pod_name, price, leverage=1.0):
        capital = self.get_allocation(pod_name)
        return round((capital * leverage) / price, 6)

# Optional singleton
allocator = FundAllocator()


