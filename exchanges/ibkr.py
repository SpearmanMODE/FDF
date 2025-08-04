from ib_insync import IB, Contract
from config import IBKR_CONFIG

def connect_ibkr():
    ib = IB()
    try:
        ib.connect(IBKR_CONFIG['host'], IBKR_CONFIG['port'], clientId=IBKR_CONFIG['client_id'])
        print("[IBKR] Connected.")
        return ib
    except Exception as e:
        print("[IBKR] Connection failed:", e)
        return None

def get_price_ibkr(ib):
    contract = Contract(
        symbol='ETH',
        secType='CRYPTO',
        exchange='PAXOS',
        currency='USD'
    )

    ib.qualifyContracts(contract)
    ticker = ib.reqMktData(contract, genericTickList='', snapshot=False, regulatorySnapshot=True)

    ib.sleep(2)

    price = ticker.marketPrice()
    if price != price:  # NaN check
        price = 2850.00  # Mock fallback price
        print("[WARNING] Live data unavailable. Using fallback price.")

    print(f"[DEBUG] Market data: {ticker}")
    return price



