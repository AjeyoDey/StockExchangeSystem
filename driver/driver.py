import time
import uuid

from entity.EnumClasses import StockAction
from entity.Order import Order
from entity.impl.OrderBookImpl import OrderBook
from entity.impl.UserDirectoryImpl import UserDirectory
from service.OrderMatcherService import OrderMatcherService
from service.OrderService import OrderService
from service.UserManagementService import UserManagementService


def main():
    # For testability, all the concrete classes can be changes with test classes
    order_book = OrderBook()
    user_directory = UserDirectory()
    order_service = OrderService(order_book=order_book)
    user_management_service = UserManagementService(
        user_directory=user_directory,
        order_book=order_book
    )

    user1 = user_management_service.add_user(name="AjeyoDey", email="ajeyo.dey@gmail.com", phone="7086686134")
    user2 = user_management_service.add_user(name="AjeyoDey2", email="ajeyo.dey2@gmail.com", phone="7086686135")
    user3 = user_management_service.add_user(name="AjeyoDey3", email="ajeyo.dey3@gmail.com", phone="7086686136")

    order1 = Order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=50, quantity=100, user=user1
    )
    order2 = Order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=100, quantity=50, user=user3
    )
    order3 = Order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=40, quantity=10, user=user1
    )
    order4 = Order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=50, quantity=10, user=user2
    )
    order5 = Order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=100, quantity=20, user=user2
    )
    order6 = Order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=50, quantity=10, user=user2
    )

    google_order1 = Order(
        symbol="GOOGL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=50, quantity=100, user=user1
    )
    google_order2 = Order(
        symbol="GOOGL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=100, quantity=50, user=user3
    )
    google_order3 = Order(
        symbol="GOOGL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=40, quantity=10, user=user1
    )
    google_order4 = Order(
        symbol="GOOGL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=50, quantity=50, user=user2
    )
    google_order5 = Order(
        symbol="GOOGL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=110, quantity=60, user=user2
    )
    google_order6 = Order(
        symbol="GOOGL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=60, quantity=10, user=user2
    )

    order_service.add_order(order1)
    order_service.add_order(order2)
    order_service.add_order(order3)
    order_service.add_order(order4)
    order_service.add_order(order5)
    order_service.add_order(order6)

    order_service.add_order(google_order1)
    order_service.add_order(google_order2)
    order_service.add_order(google_order3)
    order_service.add_order(google_order4)
    order_service.add_order(google_order5)
    order_service.add_order(google_order6)

    # Start matching for symbol - APPL
    order_matching_service = OrderMatcherService(order_book=order_book)
    order_matching_service.start_matching_for_symbols(['APPL', 'GOOGL'])
    # order_matching_service.start_matching('GOOGL')

    # Stop the matcher service
    time.sleep(20) # Let the matcher run for some time and then
    # order_matching_service.stop_matching()



    users_orders = order_book.get_orders_for_user("APPL", user1)

    order_book.print_status(symbol="GOOGL")
    order_book.print_status(symbol="APPL")


if __name__ == "__main__":
    main()