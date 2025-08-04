# dashboards/equity_dashboard.py

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objs as go
import numpy as np

LOG_DIR = "pod_logs"
PODS = ["trendpod", "scalperpod", "breakoutpod", "arbpod"]
INITIAL_CAPITAL = 10000.0

st.set_page_config(page_title="Flynn Delta Fund Dashboard", layout="wide")
st.title("📊 Flynn Delta Fund: Real-Time Equity Dashboard")

@st.cache_data(ttl=5)
def load_logs():
    all_data = []

    for pod in PODS:
        log_file = os.path.join(LOG_DIR, f"{pod}.log")
        if not os.path.exists(log_file):
            continue
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    entry['pod'] = pod
                    all_data.append(entry)
                except Exception:
                    continue

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)

    # Clean timestamp
    df = df[df['timestamp'].notnull()]
    df = df[df['timestamp'].apply(lambda x: isinstance(x, str) and len(x) > 5 and ':' in x)]
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df[df['timestamp'].notnull()]
    df.sort_values('timestamp', inplace=True)

    return df

def calculate_sharpe(pnl_series):
    if len(pnl_series) < 2:
        return np.nan
    returns = pnl_series.dropna()
    if returns.std() == 0:
        return np.nan
    return (returns.mean() / returns.std()) * np.sqrt(252)

def calculate_drawdown(equity):
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1.0
    return drawdown.min()

# Load logs
df = load_logs()

if df.empty:
    st.warning("No trading data found.")
else:
    df['pnl'] = pd.to_numeric(df['pnl'], errors='coerce')
    df['equity'] = INITIAL_CAPITAL + df['pnl'].fillna(0).cumsum()

    latest = df.iloc[-1]
    st.metric("💰 Total PnL", f"${df['pnl'].sum():.2f}")
    st.metric("📈 Current Equity", f"${latest['equity']:.2f}")

    # Daily PnL
    df['date'] = df['timestamp'].dt.date
    daily_pnl = df[df['pnl'].notna()].groupby('date')['pnl'].sum()
    st.subheader("📆 Daily PnL")
    st.bar_chart(daily_pnl)

    # Equity vs Goal
    goal_line = [INITIAL_CAPITAL + 500 * (i / len(df)) for i in range(len(df))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['equity'], mode='lines+markers', name='Equity'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=goal_line, mode='lines', name='PnL Goal', line=dict(dash='dash')))
    fig.update_layout(title="Cumulative Equity vs $500/Day Goal", xaxis_title="Time", yaxis_title="Equity ($)", template="plotly_white", height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Recent Trades
    st.subheader("🔁 Recent Trades by Pod")
    recent_trades = df[['timestamp', 'pod', 'action', 'price', 'pnl', 'equity']].sort_values('timestamp', ascending=False).head(15)
    st.dataframe(recent_trades, use_container_width=True)

    # Per-Pod Analytics
    st.subheader("📊 Pod Performance Metrics")
    for pod in PODS:
        pod_df = df[df['pod'] == pod]
        if pod_df.empty:
            continue
        total_pnl = pod_df['pnl'].sum()
        sharpe = calculate_sharpe(pod_df['pnl'])
        drawdown = calculate_drawdown(pod_df['equity'])

        col1, col2, col3 = st.columns(3)
        col1.metric(f"[{pod}] Total PnL", f"${total_pnl:.2f}")
        col2.metric(f"[{pod}] Sharpe Ratio", f"{sharpe:.2f}" if pd.notna(sharpe) else "N/A")
        col3.metric(f"[{pod}] Max Drawdown", f"{drawdown:.2%}" if pd.notna(drawdown) else "N/A")

    st.caption("🧠 Updated every 5 seconds | Aggregates across all pods")





