from abc import abstractmethod, ABC

from entity.Order import Order
from entity.User import User


class OrderInterface(ABC):
    @abstractmethod
    def get_orders_for_user(self, symbol, user: User):
        raise Exception("OrderInterface's method - get_orders_for_user - not implemented.")

    @abstractmethod
    def add_order(self, order: Order):
        raise Exception("OrderInterface's method - add_order - not implemented.")

    @abstractmethod
    def modify_order(self, symbol, order_id, new_price, new_quantity):
        raise Exception("OrderInterface's method - modify_order - not implemented.")

    @abstractmethod
    def cancel_order(self, symbol, order_id):
        raise Exception("OrderInterface's method - cancel_order - not implemented.")