from entity.Order import Order
from entity.impl.OrderBookImpl import OrderBook
from entity.User import User

class OrderService:
    def __init__(self, order_book: OrderBook):
        self.orderBook = order_book

    def add_order(self, order: Order):
        self.orderBook.add_order(order)

    def get_orders_for_user(self, symbol, user: User):
        self.orderBook.get_orders_for_user(symbol, user)

    def modify_order(self, symbol, order_id, new_price, new_quantity):
        self.orderBook.modify_order(symbol, order_id, new_price, new_quantity)

    def cancel_order(self, symbol, order_id):
        self.orderBook.cancel_order(symbol, order_id)
