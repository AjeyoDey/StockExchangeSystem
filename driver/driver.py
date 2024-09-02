import time
import uuid

from entity.EnumClasses import StockAction
from entity.OrderBook import OrderBook
from entity.UserDirectory import UserDirectory
from service.OrderMatcherService import OrderMatcherService
from service.UserManagementService import UserManagementService


def main():
    order_book = OrderBook()
    user_directory = UserDirectory()
    user_management_service = UserManagementService(
        user_directory=user_directory,
        order_book=order_book
    )
    user1 = user_management_service.add_user(name="AjeyoDey", email="ajeyo.dey@gmail.com", phone="7086686134")

    order1 = order_book.add_order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=50, quantity=100, user=user1
    )
    order2 = order_book.add_order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=100, quantity=50, user=user1
    )
    order3 = order_book.add_order(
        symbol="APPL", order_type=StockAction.SELL,
        order_id=uuid.uuid4(), price=40, quantity=10, user=user1
    )
    order4 = order_book.add_order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=50, quantity=10, user=user1
    )
    order5 = order_book.add_order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=100, quantity=20, user=user1
    )
    order6 = order_book.add_order(
        symbol="APPL", order_type=StockAction.BUY,
        order_id=uuid.uuid4(), price=50, quantity=10, user=user1
    )

    orderMatchingService = OrderMatcherService(order_book=order_book)
    orderMatchingService.start_matching('APPL')

    # Stop the matcher service
    time.sleep(100)
    orderMatchingService.stop_matching()

    order_book.print_status(symbol="APPL")
    users_orders = order_book.get_orders_for_user("APPL", user1)

    print(f"users-orders - {users_orders}")


if __name__ == "__main__":
    main()