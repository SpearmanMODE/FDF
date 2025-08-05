import os

LIVE_MODE = os.getenv("FDF_LIVE_MODE", "False") == "True"
IBKR_CONFIG = {
    "host": "127.0.0.1",
    "port": 7497,
    "client_id": 1
}
# config.py

# Capital per pod
CAPITAL_ALLOCATION = {
    "ScalperPod": 2500,
    "TrendPod": 2500,
    "BreakoutPod": 2000,
    "ArbPod": 3000,
}

# Spread threshold for arbitrage (0.6%)
ARBITRAGE_THRESHOLD = 0.006

# Exchange API Keys
EXCHANGES = {
    "coinbase": {
        "apiKey": "YOUR_COINBASE_API_KEY",
        "secret": "YOUR_COINBASE_SECRET",
        "password": "YOUR_COINBASE_API_PASSPHRASE"
    },
    "kraken": {
        "apiKey": "YOUR_KRAKEN_API_KEY",
        "secret": "YOUR_KRAKEN_SECRET"
    }
}
