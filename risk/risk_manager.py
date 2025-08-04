# risk/risk_manager.py

import json
import os
from datetime import datetime

class RiskManager:
    def __init__(self, max_daily_loss=500, max_trade_loss=100, max_position_size=3000):
        self.max_daily_loss = max_daily_loss
        self.max_trade_loss = max_trade_loss
        self.max_position_size = max_position_size

    def check_trade_risk(self, trade):
        pnl = trade.get("pnl")
        price = trade.get("price")
        symbol = trade.get("symbol")

        if pnl is not None and abs(pnl) > self.max_trade_loss:
            print(f"[RiskManager] 🚨 TRADE LOSS LIMIT EXCEEDED on {symbol}: ${pnl}")
            return False

        if price > self.max_position_size:
            print(f"[RiskManager] 🚨 POSITION SIZE TOO LARGE on {symbol}: ${price}")
            return False

        return True

    def check_daily_loss(self, pod_name):
        log_path = os.path.join("pod_logs", f"{pod_name.lower()}.log")
        if not os.path.exists(log_path):
            return True

        with open(log_path, "r") as f:
            trades = [json.loads(line) for line in f.readlines() if line.strip()]

        today = datetime.utcnow().date().isoformat()
        daily_trades = [t for t in trades if t['timestamp'].startswith(today) and t.get('pnl') is not None]

        total_pnl = sum(t['pnl'] for t in daily_trades if t['pnl'] is not None)
        if total_pnl < -self.max_daily_loss:
            print(f"[RiskManager] ❌ DAILY LOSS LIMIT EXCEEDED for {pod_name}: ${total_pnl:.2f}")
            return False

        return True

