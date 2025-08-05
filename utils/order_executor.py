from ib_insync import MarketOrder, LimitOrder, Contract, Stock
import logging

logger = logging.getLogger(__name__)

def build_contract(symbol="ETH", exchange="PAXOS", currency="USD"):
    return Contract(
        conId=0,
        symbol=symbol,
        secType="CRYPTO",
        exchange=exchange,
        currency=currency
    )

def execute_order(ib, symbol, action, quantity, exchange="PAXOS", currency="USD", price=None, live=True):
    contract = build_contract(symbol, exchange, currency)

    if not live or quantity == 0:
        logger.info(f"[SIMULATION] {action} {symbol} @ {price} | qty: {quantity} (NOT EXECUTED)")
        return {"status": "simulated", "symbol": symbol, "qty": quantity, "price": price}

    order = MarketOrder(action, quantity) if price is None else LimitOrder(action, quantity, price)
    trade = ib.placeOrder(contract, order)
    ib.sleep(1)  # allow order to process

    status = trade.orderStatus.status
    fill_price = trade.orderStatus.avgFillPrice

    logger.info(f"[EXECUTED] {action} {symbol} | Qty: {quantity} | Fill: {fill_price} | Status: {status}")

    return {
        "status": status,
        "fill_price": fill_price,
        "symbol": symbol,
        "qty": quantity
    }
