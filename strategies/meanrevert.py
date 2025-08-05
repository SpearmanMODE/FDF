import os
import json
import random
import numpy as np
from collections import deque
from datetime import datetime

from utils.telegram import send_telegram_alert
from allocator.fund_allocator import allocator
from utils.metrics import update_performance_file
from risk.risk_manager import RiskManager
from utils.order_executor import execute_order
from config import LIVE_MODE

class MeanRevertPod:
    def __init__(self, ib, symbol='ETH', window=20, threshold=1.5):
        self.ib = ib
        self.symbol = symbol
        self.logs = []
        self.prices = deque(maxlen=window)
        self.position = None
        self.name = "MeanRevertPod"
        self.risk = RiskManager()
        self.threshold = threshold
        self.entry_price = None

    def fetch_price(self):
        from exchanges.kraken import get_price_kraken
        from exchanges.coinbase import get_price_coinbase

        price = get_price_kraken(symbol='ETHUSD')
        if price is None:
            price = get_price_coinbase(symbol='ETH-USD')
        return price if price else 2850.0 + random.uniform(-5, 5)

    def compute_zscore(self):
        arr = np.array(self.prices)
        mean = np.mean(arr)
        std = np.std(arr)
        latest = arr[-1]
        return (latest - mean) / std if std > 0 else 0.0

    def log_trade(self, action, price):
        pnl = None
        size = allocator.get_position_size(self.name, price)

        if action == 'BUY':
            if size * price > self.risk.max_position_size:
                print(f"[{self.name}] BUY blocked: size too large.")
                return

            execute_order(self.ib, self.symbol, "BUY", size, price=price, live=LIVE_MODE)
            self.entry_price = price
            self.position = 'long'

        elif action == 'SELL' and self.entry_price:
            pnl = round(price - self.entry_price, 2)
            trade_meta = {"symbol": self.symbol, "price": price, "pnl": pnl}

            if not self.risk.check_trade_risk(trade_meta):
                print(f"[{self.name}] Trade blocked by RiskManager (loss).")
                return
            if not self.risk.check_daily_loss(self.name):
                print(f"[{self.name}] Daily loss exceeded.")
                return

            execute_order(self.ib, self.symbol, "SELL", size, price=price, live=LIVE_MODE)

            self.position = 'flat'
            allocator.update_performance(self.name, pnl)
            update_performance_file(self.name.lower(), pnl)
            self.entry_price = None

        log = {
            'timestamp': datetime.utcnow().isoformat(),
            'symbol': self.symbol,
            'action': action,
            'price': round(price, 2),
            'position': self.position,
            'pnl': pnl,
            'size': size
        }

        msg = f"[{self.name}] {action} @ {price:.2f} | Size: {size}"
        if pnl is not None:
            msg += f" | PnL: {pnl:.2f}"
        print(msg)
        send_telegram_alert(msg)

        self.logs.append(log)
        with open(f"pod_logs/meanrevertpod.log", "a") as f:
            f.write(json.dumps(log) + "\n")

    def run_once(self):
        price = self.fetch_price()
        if price is None:
            print(f"[{self.name}] No price available.")
            return

        self.prices.append(price)
        if len(self.prices) < self.prices.maxlen:
            print(f"[{self.name}] Collecting prices: {len(self.prices)}/{self.prices.maxlen}")
            return

        z = self.compute_zscore()
        print(f"[{self.name}] Z-score: {z:.2f} | Price: {price:.2f}")

        if self.position != 'long' and z <= -self.threshold:
            self.log_trade('BUY', price)
        elif self.position == 'long' and z >= 0:
            self.log_trade('SELL', price)
