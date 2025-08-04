import streamlit as st
import pandas as pd
import plotly.express as px
import os
import joblib

# Load trained AI model
MODEL_PATH = "ml_models/models/xgb_allocator.pkl"
model = joblib.load(MODEL_PATH)

# Load pod performance features
FEATURES_CSV = "data/allocator/live_pod_features.csv"  # auto-updated by engine
df = pd.read_csv(FEATURES_CSV)

# Define feature columns used in training
FEATURES = ['avg_return', 'volatility', 'sharpe', 'max_drawdown', 'win_rate', 'capital']

# Predict allocation weights
X = df[FEATURES]
alloc_preds = model.predict(X)
alloc_weights = alloc_preds / alloc_preds.sum()
df["AI_Allocation_%"] = (alloc_weights * 100).round(2)

# --- Streamlit Layout ---
st.set_page_config(page_title="Delta Fund Dashboard", layout="wide")
st.title("📈 Flynn & Associates Delta Fund - Quant Strategy Dashboard")

# --- KPI Summary ---
col1, col2, col3 = st.columns(3)
col1.metric("🧠 AI-Model", "XGBoost")
col2.metric("📊 Pods Active", len(df))
col3.metric("📦 Total Capital", f"${df['capital'].sum():,.2f}")

# --- Capital Allocations Chart ---
fig_alloc = px.pie(
    df,
    values="AI_Allocation_%", 
    names="name",
    title="🧠 AI-Based Capital Allocation by Strategy Pod",
    hole=0.4
)
st.plotly_chart(fig_alloc, use_container_width=True)

# --- PnL Over Time (Optional) ---
if os.path.exists("data/allocator/pod_navs.csv"):
    nav_df = pd.read_csv("data/allocator/pod_navs.csv", parse_dates=["timestamp"])
    fig_line = px.line(
        nav_df,
        x="timestamp",
        y="nav",
        color="name",
        title="📈 Strategy NAVs Over Time"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- Strategy Table ---
st.markdown("### 🧾 Strategy Pod Performance")
st.dataframe(df.round(4), use_container_width=True)

st.caption("🔁 Updates as live pods log features and NAVs to `/data/allocator`.")
