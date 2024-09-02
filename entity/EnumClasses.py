import enum


class StockAction(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(enum.Enum):
    BUY_ORDERS = "buy_orders"
    SELL_ORDERS = "sell_orders"
    MATCHED_ORDERS = "matched_trades"