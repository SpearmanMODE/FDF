# strategies/scalper.py

import os
import json
import random
from datetime import datetime
from collections import deque
from utils.telegram import send_telegram_alert
from allocator.fund_allocator import allocator
from utils.metrics import update_performance_file
from risk.risk_manager import RiskManager
risk = RiskManager()

class ScalperPod:
    def __init__(self, symbol='ETH'):
        self.symbol = symbol
        self.logs = []
        self.prices = deque(maxlen=5)
        self.position = None
        self.name = "ScalperPod"

    def fetch_price(self):
        from exchanges.kraken import get_price_kraken
        price = get_price_kraken(symbol='ETHUSD')
        return price if price else 2850.0 + random.uniform(-5, 5)

    def log_trade(self, action, price):
        from allocator.fund_allocator import allocator
        from utils.metrics import update_performance_file
        from risk.risk_manager import RiskManager

        risk = RiskManager()
        pnl = None

        if action == 'BUY':
            size = allocator.get_position_size(self.name, price)

            if size * price > risk.max_position_size:
                print(f"[{self.name}] BUY blocked: position size too large (${size * price:.2f})")
                return

            self.entry_price = price
            self.position = 'long'

        elif action == 'SELL' and hasattr(self, 'entry_price'):
            pnl = round(price - self.entry_price, 2)

            trade_meta = {
                "symbol": self.symbol,
                "price": price,
                "pnl": pnl
        }

        if not risk.check_trade_risk(trade_meta):
            print(f"[{self.name}] Trade blocked by RiskManager (trade loss).")
            return

        if not risk.check_daily_loss(self.name):
            print(f"[{self.name}] Daily loss exceeded. No trades allowed.")
            return

        self.position = 'flat'
        allocator.update_performance(self.name, pnl)
        update_performance_file(self.name.lower(), pnl)
        del self.entry_price

        size = allocator.get_position_size(self.name, price)
        log = {
            'timestamp': datetime.utcnow().isoformat(),
            'symbol': self.symbol,
            'action': action,
            'price': round(price, 2),
            'position': self.position,
            'pnl': pnl,
            'size': size
        }

        msg = f"[{self.name.upper()}] {action} @ {price:.2f} | Size: {size}"
        if pnl is not None:
            msg += f" | PnL: {pnl:.2f}"
        print(msg)
        send_telegram_alert(msg)

        self.logs.append(log)
        log_path = os.path.join("pod_logs", "scalperpod.log")
        with open(log_path, "a") as f:
            f.write(json.dumps(log) + "\n")

    def run_once(self):
        price = self.fetch_price()
        if price is None:
            return

        self.prices.append(price)
        if len(self.prices) < 3:
            return

        change = (self.prices[-1] - self.prices[-2]) / self.prices[-2]

        if self.position != 'long' and change > 0.002:  # 0.2% up
            self.log_trade('BUY', price)
        elif self.position == 'long' and change < -0.002:  # 0.2% down
            self.log_trade('SELL', price)


