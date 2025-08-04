import pandas as pd

class StrategyPod:
    def __init__(self, name, capital, strategy_logic):
        self.name = name
        self.capital = capital
        self.strategy = strategy_logic
        self.pnl_history = []
        self.trade_history = []
        self.delta = 0
        self.stats = {}

    def run(self, market_data):
        trades, pnl = self.strategy.execute(market_data, self.capital)
        self.pnl_history.append(pnl)
        self.trade_history.extend(trades)
        self.delta = pnl / self.capital
        self.update_stats()
        return trades

    def update_stats(self, window=30):
        pnl_series = pd.Series(self.pnl_history[-window:])
        returns = pnl_series / self.capital

        self.stats = {
            'avg_return': returns.mean(),
            'volatility': returns.std(),
            'sharpe': returns.mean() / (returns.std() + 1e-6),
            'max_drawdown': (pnl_series.cummax() - pnl_series).max(),
            'win_rate': sum(p > 0 for p in pnl_series) / len(pnl_series) if len(pnl_series) > 0 else 0,
        }

    def get_features(self):
        return {
            'name': self.name,
            'capital': self.capital,
            'delta': self.delta,
            **self.stats
        }

