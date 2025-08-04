import sys
import os

# Force path to project root so `exchanges` can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from exchanges.ibkr import connect_ibkr, get_price_ibkr

ib = connect_ibkr()
if ib:
    price = get_price_ibkr(ib)
  # or 'BTCUSD', 'EURUSD', etc.
    print(f"IBKR ETHUSD Price: {price}")
    ib.disconnect()
