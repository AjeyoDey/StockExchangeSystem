from datetime import datetime


class Order:
    def __init__(self, order_id, price, quantity, user=None):
        self.order_id = order_id
        self.price = price
        self.quantity = quantity
        self.user = user
        self.timestamp = datetime.now()

    def __lt__(self, other):
        return (self.price, self.timestamp) < (other.price, other.timestamp)