from datetime import datetime

from entity.EnumClasses import OrderType, StockAction


class Order:
    def __init__(self, order_id, price, quantity, order_type: StockAction, symbol: str, user=None):
        self.order_id = order_id
        self.order_type = order_type
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.user = user
        self.timestamp = datetime.now()

    def __lt__(self, other):
        return (self.price, self.timestamp) < (other.price, other.timestamp)