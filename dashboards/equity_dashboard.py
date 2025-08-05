import streamlit as st
import json
import os
import datetime
LIVE_MODE = os.getenv("FDF_LIVE_MODE", "False") == "True"

st.set_page_config(page_title="FDF Dashboard", layout="wide")

st.title("📊 Flynn Delta Fund — Live Dashboard")

# === Live Mode Status ===
mode_color = "green" if not LIVE_MODE else "red"
st.markdown(f"### ⚙️ Execution Mode: :{mode_color}[{'LIVE' if LIVE_MODE else 'DRY RUN'}]")

# === Volatility Regime ===
def get_current_regime():
    path = "allocator/last_regime.json"
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        return data.get("regime", "unknown").upper()
    return "UNKNOWN"

st.markdown(f"### 🌐 Volatility Regime: `{get_current_regime()}`")

# === Current Pod Allocations ===
def load_weights():
    path = "allocator/weights.json"
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

weights = load_weights()
if weights:
    st.markdown("### 🧠 Pod Weights")
    st.bar_chart(weights)
else:
    st.info("No weights.json file found yet.")

# === Daily PnL Summary ===
st.markdown("### 📅 Daily PnL Summary")

if weights:
    st.markdown("### 📅 Daily PnL Summary")
    cols = st.columns(len(weights))
    for i, (pod, weight) in enumerate(weights.items()):
        perf_path = f"metrics/{pod}_performance.json"
        if os.path.exists(perf_path):
            with open(perf_path) as f:
                data = json.load(f)
            pnl = sum(data.get("returns", []))
            cols[i].metric(label=pod.upper(), value=f"${pnl:,.2f}", delta=f"{weight*100:.1f}% alloc")
else:
    st.info("No pod weights available yet — waiting on MetaAllocator.")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")






