import time
from exchanges.coinbase import get_price_coinbase
from exchanges.kraken import get_price_kraken
from config import ARBITRAGE_THRESHOLD

def scan_arbitrage(symbol='ETH/USD', amount=0):  # amount=0 = dry run
    cb_price = get_price_coinbase(symbol)
    kr_price = get_price_kraken(symbol)

    low_ex, low_price = ('coinbase', cb_price) if cb_price < kr_price else ('kraken', kr_price)
    high_ex, high_price = ('coinbase', cb_price) if cb_price > kr_price else ('kraken', kr_price)

    spread = (high_price - low_price) / low_price

    print(f"{symbol}: Kraken={kr_price:.2f}, Coinbase={cb_price:.2f}, Spread={spread*100:.2f}%")

    if spread >= ARBITRAGE_THRESHOLD:
        print(f"[ARBITRAGE OPPORTUNITY] Buy {low_ex} @ {low_price:.2f} → Sell {high_ex} @ {high_price:.2f} | Spread: {spread*100:.2f}%")
        if amount > 0:
            print("[EXECUTION] Simulated market buy/sell with amount:", amount)
    else:
        print("No arb opportunity.\n")

if __name__ == "__main__":
    while True:
        scan_arbitrage('ETH/USD')
        time.sleep(10)
