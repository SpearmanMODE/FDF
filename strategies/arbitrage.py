import os
import json
from datetime import datetime
from utils.telegram import send_telegram_alert
from allocator.fund_allocator import allocator
from utils.metrics import update_performance_file
from risk.risk_manager import RiskManager
from exchanges.kraken import get_price_kraken
from exchanges.coinbase import get_price_coinbase

class ArbPod:
    def __init__(self, symbol="ETHUSD", threshold=0.005):
        self.symbol = symbol
        self.name = "ArbPod"
        self.threshold = threshold  # 0.5% arbitrage threshold
        self.position = None
        self.logs = []
        self.risk = RiskManager()

    def fetch_prices(self):
        price_kraken = get_price_kraken(symbol="ETHUSD")
        price_coinbase = get_price_coinbase(symbol="ETH-USD")
        return price_kraken, price_coinbase

    def run_once(self):
        price_k, price_c = self.fetch_prices()
        if not price_k or not price_c:
            print(f"[{self.name}] Failed to fetch prices.")
            return

        spread = abs(price_k - price_c) / ((price_k + price_c) / 2)

        if spread >= self.threshold:
            direction = "BUY KRAKEN / SELL COINBASE" if price_k < price_c else "BUY COINBASE / SELL KRAKEN"
            pnl = round(abs(price_c - price_k), 2)

            # Simulate position sizing
            size = allocator.get_position_size(self.name, price_k)

            if not self.risk.check_trade_risk({"pnl": pnl, "price": price_k, "symbol": self.symbol}):
                print(f"[{self.name}] Trade blocked by RiskManager.")
                return

            if not self.risk.check_daily_loss(self.name):
                print(f"[{self.name}] Daily loss limit hit.")
                return

            allocator.update_performance(self.name, pnl)
            update_performance_file(self.name.lower(), pnl)

            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "symbol": self.symbol,
                "action": direction,
                "price_kraken": price_k,
                "price_coinbase": price_c,
                "spread": round(spread, 4),
                "pnl": pnl,
                "size": size
            }

            msg = f"[{self.name}] {direction} | Spread: {spread:.4%} | PnL: {pnl:.2f}"
            print(msg)
            send_telegram_alert(msg)

            self.logs.append(log)
            log_path = os.path.join("pod_logs", "arbpod.log")
            with open(log_path, "a") as f:
                f.write(json.dumps(log) + "\n")
        else:
            print(f"[{self.name}] Spread {spread:.4%} too small. No action.")


