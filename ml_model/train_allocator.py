import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# --- Load Historical Pod Features ---
# Assume you have a CSV with features + next_period_delta as target
df = pd.read_csv("data/allocator/pod_features.csv")

# Features used for training
FEATURES = [
    'avg_return', 'volatility', 'sharpe',
    'max_drawdown', 'win_rate', 'capital'
]

TARGET = 'next_period_delta'  # or 'next_period_sharpe'

X = df[FEATURES]
y = df[TARGET]

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# --- Train XGBoost Regressor ---
model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# --- Evaluation ---
preds = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, preds):.3f}")
print(f"MSE: {mean_squared_error(y_test, preds):.5f}")

# --- Save Model ---
model.save_model("ml_models/models/xgb_allocator.json")
joblib.dump(model, "ml_models/models/xgb_allocator.pkl")
