# allocator/performance_tracker.py

import json
import os
import pandas as pd
import numpy as np

LOG_DIR = "pod_logs"
WINDOW = 7  # trailing days

def load_daily_pnl(pod):
    path = os.path.join(LOG_DIR, f"{pod}.log")
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        if "PnL:" in line and "SELL" in line:
            try:
                parts = line.split("|")
                pnl = float(parts[-1].split(":")[-1].strip())
                timestamp = parts[0].split()[0]  # crude date
                entries.append({"date": timestamp, "pnl": pnl})
            except Exception:
                continue

    df = pd.DataFrame(entries)
    if df.empty:
        return []

    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna().sort_values("date").drop_duplicates("date", keep="last")
    df.set_index("date", inplace=True)
    return df["pnl"].tail(WINDOW)
