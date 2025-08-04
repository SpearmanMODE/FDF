# exchanges/kraken.py

import requests

def get_price_kraken(symbol='ETHUSD'):
    """
    Fetches the latest price for the given symbol from Kraken.
    symbol: str like 'ETHUSD', 'BTCUSD', 'SOLUSD'
    """
    try:
        url = f'https://api.kraken.com/0/public/Ticker?pair={symbol}'
        response = requests.get(url)
        data = response.json()
        result = next(iter(data['result'].values()))
        price = float(result['c'][0])  # 'c' is [last trade price, lot volume]
        return price
    except Exception as e:
        print(f"[KRAKEN] Failed to fetch price for {symbol}: {e}")
        return None

