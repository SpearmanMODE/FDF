import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exchanges.kraken import get_price_history_kraken

prices = get_price_history_kraken('ETHUSD', lookback=20)

if not prices:
    print("[❌] No prices returned from Kraken.")
elif len(prices) < 20:
    print(f"[⚠️] Only got {len(prices)} prices:", prices)
else:
    print(f"[✅] Got {len(prices)} prices from Kraken.")
    print("Last 5 closes:", prices[-5:])
