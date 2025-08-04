import numpy as np
import json
import os

def calculate_metrics(pnl_history, window=20):
    if len(pnl_history) < 2:
        return {"sharpe": 0, "drawdown": 0, "win_rate": 0}

    recent = pnl_history[-window:]
    returns = np.array(recent)

    mean = np.mean(returns)
    std = np.std(returns)
    sharpe = (mean / std) * np.sqrt(252) if std > 0 else 0

    equity_curve = np.cumsum(returns)
    high_water = np.maximum.accumulate(equity_curve)
    drawdown = np.min((equity_curve - high_water) / high_water) if high_water.any() else 0

    wins = np.sum(returns > 0)
    win_rate = wins / len(returns)

    return {
        "sharpe": round(sharpe, 3),
        "drawdown": round(drawdown, 3),
        "win_rate": round(win_rate, 3),
    }

def update_performance_file(pod_name, pnl):
    filename = f"pod_logs/{pod_name}_performance.json"
    data = {"name": pod_name, "pnl_history": []}

    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)

    data["pnl_history"].append(pnl)
    metrics = calculate_metrics(data["pnl_history"])

    data.update(metrics)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
