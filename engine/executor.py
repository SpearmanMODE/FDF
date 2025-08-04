from exchanges.ibkr import connect_ibkr, place_order_ibkr

def execute_order(exchange_name, symbol, side, amount=0):
    if exchange_name == "ibkr":
        ib = connect_ibkr()
        if amount == 0:
            print(f"[SIM] IBKR: {side.upper()} {symbol} (amount=0)")
            return
        return place_order_ibkr(ib, symbol=symbol, side=side, size=amount)

    # Existing logic for ccxt exchanges...
