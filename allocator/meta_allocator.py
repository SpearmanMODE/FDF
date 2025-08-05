import os
import json
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from allocator.fund_allocator import allocator
from exchanges.kraken import get_price_history_kraken
from utils.telegram import send_telegram_message

load_dotenv(dotenv_path="./.env")


class MetaAllocator:
    def __init__(self, pods=None, risk_free_rate=0.01, max_weight_per_pod=0.4):
        self.pods = pods or ["trendpod", "breakoutpod", "scalperpod", "arbpod", "meanrevertpod"]
        self.risk_free_rate = risk_free_rate
        self.max_weight = max_weight_per_pod
        self.regime = self.detect_volatility_regime()

    def detect_volatility_regime(self):
        prices = get_price_history_kraken('ETHUSD', lookback=20)
        if not prices or len(prices) < 20:
            return "unknown"
        stddev = np.std(prices)
        if stddev < 15:
            return "low"
        elif stddev > 50:
            return "high"
        return "medium"

    def regime_bias(self, pod):
        if self.regime == "high":
            return 1.3 if "trend" in pod or "breakout" in pod else 0.7
        elif self.regime == "low":
            return 1.3 if "scalper" in pod or "meanrevert" in pod else 0.7
        return 1.0

    def optimize(self):
        performances = []
        for pod in self.pods:
            pnl = allocator.performance.get(pod, {}).get('pnl', 0.0)
            performances.append([pnl])

        pnl_df = pd.DataFrame(performances, index=self.pods).T.fillna(0)
        returns = pnl_df.pct_change(axis=1).dropna(axis=1, how='all')

        # Fallback to equal weights if insufficient data
        if returns.empty:
            normalized = {pod: round(1 / len(self.pods), 4) for pod in self.pods}
        else:
            mean_returns = returns.mean()
            cov_matrix = returns.cov()

            best_weights = np.ones(len(self.pods)) / len(self.pods)
            best_sharpe = -np.inf

            for _ in range(300):
                raw_weights = np.random.dirichlet(np.ones(len(self.pods)))
                biased_weights = [
                    w * self.regime_bias(pod)
                    for w, pod in zip(raw_weights, self.pods)
                ]
                w = np.array(biased_weights)
                w /= w.sum()

                port_return = np.dot(w, mean_returns)
                port_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
                sharpe = (port_return - self.risk_free_rate) / port_vol if port_vol > 0 else 0

                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_weights = w

            capped_weights = {pod: min(round(w, 4), self.max_weight) for pod, w in zip(self.pods, best_weights)}
            total = sum(capped_weights.values())
            normalized = {pod: round(w / total, 4) for pod, w in capped_weights.items()}

        # Final rebalance
        allocator.rebalance(normalized)

        # Save weights
        with open("allocator/weights.json", "w") as f:
            json.dump(normalized, f, indent=2)

        with open("allocator/last_regime.json", "w") as f:
            json.dump({"regime": self.regime}, f)

        # Telegram alert
        try:
            print("[MetaAllocator] Attempting to send Telegram message...")
            message = (
                "📊 *MetaAllocator Rebalance*\n"
                f"🌐 Volatility Regime: `{self.regime.upper()}`\n"
                "📉 Weights:\n```json\n"
                f"{json.dumps(normalized, indent=2)}\n```"
            )
            send_telegram_message(message)
        except Exception as e:
            print(f"[MetaAllocator] Telegram error: {e}")

        return normalized

