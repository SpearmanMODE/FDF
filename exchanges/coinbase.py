import requests

def get_price_coinbase(symbol='ETH-USD'):
    """
    Fetch the current price for a symbol (e.g., 'ETH-USD', 'BTC-USD') from Coinbase.
    """
    try:
        url = f'https://api.coinbase.com/v2/prices/{symbol}/spot'
        response = requests.get(url)
        data = response.json()
        price = float(data['data']['amount'])
        return price
    except Exception as e:
        print(f"[COINBASE] Failed to fetch price for {symbol}: {e}")
        return None# exchanges/coinbase.py


