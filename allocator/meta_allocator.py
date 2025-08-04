# allocator/meta_allocator.py

import numpy as np
import pandas as pd
from allocator.fund_allocator import allocator

class MetaAllocator:
    def __init__(self, pods, risk_free_rate=0.01):
        self.pods = pods
        self.risk_free_rate = risk_free_rate

    def optimize(self):
        performances = []
        for pod in self.pods:
            pnl = allocator.performance.get(pod, {}).get('pnl', 0.0)
            performances.append([pnl])

        pnl_df = pd.DataFrame(performances, index=self.pods).T.fillna(0)

        returns = pnl_df.pct_change(axis=1).dropna(axis=1, how='all')
        if returns.empty:
            return {pod: 1 / len(self.pods) for pod in self.pods}

        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        weights = np.ones(len(self.pods)) / len(self.pods)
        best_sharpe = -np.inf
        best_weights = weights

        for _ in range(500):
            w = np.random.dirichlet(np.ones(len(self.pods)), size=1)[0]
            port_return = np.dot(w, mean_returns)
            port_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
            sharpe = (port_return - self.risk_free_rate) / port_vol if port_vol > 0 else 0
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_weights = w

        allocation = dict(zip(self.pods, best_weights))
        allocator.rebalance(allocation)
        return allocation

