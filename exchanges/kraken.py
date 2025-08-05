import requests
import time

def get_price_history_kraken(symbol='ETHUSD', lookback=20):
    """
    Fetch last N closing prices from Kraken using OHLC endpoint.
    Returns a list of closing prices.
    """
    symbol_map = {
        'ETHUSD': 'XETHZUSD',
        'BTCUSD': 'XBTUSD',
    }

    kraken_symbol = symbol_map.get(symbol, symbol)
    interval = 1  # 1-minute candles

    try:
        url = f"https://api.kraken.com/0/public/OHLC?pair={kraken_symbol}&interval={interval}"
        response = requests.get(url)
        data = response.json()

        if not data.get("result"):
            return []

        result_key = list(data["result"].keys())[0]
        candles = data["result"][result_key][-lookback:]

        closes = [float(c[4]) for c in candles]  # closing prices
        return closes

    except Exception as e:
        print(f"[Kraken] Failed to fetch price history: {e}")
        return []


