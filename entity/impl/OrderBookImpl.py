import heapq
import threading
from datetime import datetime

from entity.EnumClasses import StockAction, OrderType
from entity.Order import Order
from entity.OrderBook import OrderInterface
from entity.User import User


class OrderBook(OrderInterface):
    def __init__(self):
        self.order_books = {}  # Dictionary to store order books for each stock
        self.broker_profit = 0
        self.lock = threading.Lock()

    def _get_order_book(self, symbol):
        if symbol not in self.order_books:
            self.order_books[symbol] = {
                OrderType.BUY_ORDERS: [], # To be maintained as a MaxHeap
                OrderType.SELL_ORDERS: [], # To be maintained as a MinHeap
                OrderType.MATCHED_ORDERS: []
            }
        return self.order_books[symbol]

    def get_orders_for_user(self, symbol, user):
        with self.lock:
            order_book = self._get_order_book(symbol)

            # Fetch buy orders for user
            buy_orders = [
                (price, timestamp, order)
                for price, timestamp, order in order_book[OrderType.BUY_ORDERS]
                if order.user == user
            ]

            # Fetch sell orders for user
            sell_orders = [
                (price, timestamp, order)
                for price, timestamp, order in order_book[OrderType.SELL_ORDERS]
                if order.user == user
            ]

            # Fetch matched orders for user
            matched_orders = [
                trade
                for trade in order_book[OrderType.MATCHED_ORDERS]
                if trade['buyer_user_id'] == user.id or trade['seller_user_id'] == user.id
            ]

            return {
                'buy_orders': buy_orders,
                'sell_orders': sell_orders,
                'matched_orders': matched_orders
            }

    def add_order(self, order: Order):
        timestamp = datetime.now()  # Use current timestamp for ordering
        symbol, order_type, order_id, price, quantity = order.symbol, order.order_type, order.order_id, order.price, order.quantity
        order_book = self._get_order_book(symbol)

        if order_type == StockAction.BUY:
            heapq.heappush(order_book[OrderType.BUY_ORDERS], (-price, timestamp, order))  # Use negative price for max-heap
        elif order_type == StockAction.SELL:
            heapq.heappush(order_book[OrderType.SELL_ORDERS], (price, timestamp, order))
        else:
            raise ValueError("Invalid order type")

        # TODO - Match orders separately in a different thread
        # self.match_orders(symbol)

    def modify_order(self, symbol, order_id, new_price, new_quantity):
        with self.lock:
            order_book = self._get_order_book(symbol)
            order_type = None
            order_to_modify = None

            # Find the order to modify
            for heap_type in [OrderType.BUY_ORDERS, OrderType.SELL_ORDERS]:
                orderBookHeap = order_book[heap_type]
                for i, (price, timestamp, order) in enumerate(orderBookHeap):
                    if order.order_id == order_id:
                        order_to_modify = order
                        order_type = heap_type
                        orderBookHeap[i] = orderBookHeap[-1]  # Replace with the last element
                        orderBookHeap.pop()  # Remove the last element
                        heapq.heapify(orderBookHeap)  # Restore heap property
                        break
                if order_to_modify:
                    break

            if not order_to_modify:
                raise Exception("Order not found")

                # Modify the order
            order_to_modify.price = new_price
            order_to_modify.quantity = new_quantity
            timestamp = datetime.now()  # Update timestamp for modification

            # Re-insert the modified order
            if order_type == OrderType.BUY_ORDERS:
                heapq.heappush(order_book[OrderType.BUY_ORDERS], (-new_price, timestamp, order_to_modify))
            elif order_type == OrderType.SELL_ORDERS:
                heapq.heappush(order_book[OrderType.SELL_ORDERS], (new_price, timestamp, order_to_modify))

    def cancel_order(self, symbol, order_id):
        # Can only cancel a order if the Matching Order is not working
        # since it takes a lock to do the matching on OrderBook.
        with self.lock:
            order_book = self._get_order_book(symbol)

            # Remove order from buy orders
            order_book[OrderType.BUY_ORDERS] = [
                entry for entry in order_book[OrderType.BUY_ORDERS] if entry[2].order_id != order_id
            ]
            heapq.heapify(order_book[OrderType.BUY_ORDERS])

            # Remove order from sell orders
            order_book[OrderType.SELL_ORDERS] = [
                entry for entry in order_book[OrderType.SELL_ORDERS] if entry[2].order_id != order_id
            ]
            heapq.heapify(order_book[OrderType.SELL_ORDERS])

    def match_order(self, symbol):
        with self.lock:
            if self.order_books[symbol][OrderType.BUY_ORDERS] and self.order_books[symbol][OrderType.SELL_ORDERS]:
                order_book = self._get_order_book(symbol)
                buy_order: Order = order_book[OrderType.BUY_ORDERS][0][2]  # Peek at the highest buy order
                sell_order: Order = order_book[OrderType.SELL_ORDERS][0][2]  # Peek at the lowest sell order

                if buy_order.price >= sell_order.price:
                    trade_quantity = min(buy_order.quantity, sell_order.quantity)
                    trade_price = buy_order.price
                    self.broker_profit += trade_quantity * (buy_order.price - sell_order.price)

                    matched_order = {
                        'buy_order_id': buy_order.order_id,
                        'sell_order_id': sell_order.order_id,
                        'quantity': trade_quantity,
                        'price': trade_price,
                        'buyer_user_id': buy_order.user.id,
                        'seller_user_id': sell_order.user.id,
                        'timestamp': datetime.now()
                    }
                    self._append_matched_orders(symbol=symbol, matched_orders=[matched_order])

                    # Update quantities in OrderBook=
                    # Atomic Transactions (Both to be executed together in a pair)
                    self._updateOrdersForSymbol(symbol, OrderType.BUY_ORDERS, trade_quantity)
                    self._updateOrdersForSymbol(symbol, OrderType.SELL_ORDERS, trade_quantity)

    # Private function internal to OrderBook
    def _append_matched_orders(self, symbol, matched_orders):
        for matched_order in matched_orders:
            self.order_books[symbol][OrderType.MATCHED_ORDERS].append(matched_order)

    # Private function internal to OrderBook
    def _updateOrdersForSymbol(self, symbol: str, orderType: OrderType, quantity: int):
        # Does not acquired it's own lock, only to be called from functions which have already locked OrderBook
        # Update quantities in OrderBook=
        if orderType == OrderType.BUY_ORDERS:
            order_book = self._get_order_book(symbol)
            buy_order_tuple = heapq.heappop(order_book[OrderType.BUY_ORDERS])  # Peek at the highest buy order
            buy_order = buy_order_tuple[2]
            buy_order.quantity -= quantity
            if buy_order.quantity > 0:
                heapq.heappush(order_book[OrderType.BUY_ORDERS], (buy_order_tuple[0], buy_order_tuple[1], buy_order))

        if orderType == OrderType.SELL_ORDERS:
            order_book = self._get_order_book(symbol)
            sell_order_tuple = heapq.heappop(order_book[OrderType.SELL_ORDERS])  # Peek at the highest buy order
            sell_order = sell_order_tuple[2]
            sell_order.quantity -= quantity
            if sell_order.quantity > 0:
                heapq.heappush(order_book[OrderType.SELL_ORDERS], (sell_order_tuple[0], sell_order_tuple[1], sell_order)
                               )
        # Remove fully matched orders

    def print_status(self, symbol):
        order_book = self._get_order_book(symbol)
        print(f"\n{symbol} Buy Orders:")
        for _, _, order in order_book[OrderType.BUY_ORDERS]:
            print(f"Order ID: {order.order_id}, Price: {-order.price}, Quantity: {order.quantity}")

        print(f"\n{symbol} Sell Orders:")
        for _, _, order in order_book[OrderType.SELL_ORDERS]:
            print(f"Order ID: {order.order_id}, Price: {order.price}, Quantity: {order.quantity}")

        print(f"\n{symbol} Matched Trades:")
        for trade in order_book[OrderType.MATCHED_ORDERS]:
            print(
                f"Buy Order ID: {trade['buy_order_id']}, Sell Order ID: {trade['sell_order_id']}, Quantity: {trade['quantity']}, Price: {trade['price']}")
