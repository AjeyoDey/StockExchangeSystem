import heapq
import threading
import time
from collections import defaultdict
from datetime import datetime

from entity.EnumClasses import OrderType
from entity.OrderBook import OrderBook


class OrderMatcherService:
    def __init__(self, order_book: OrderBook):
        self.order_book = order_book
        self.matching_threads = defaultdict(threading.Thread)
        self.stop_event = threading.Event()

    def start_matching(self, symbol):
        """Start a new thread to continuously match orders for the given symbol."""
        def match_loop():
            while not self.stop_event.is_set():
                self.order_book.match_order(symbol)
                time.sleep(1)  # Wait 1 second before trying to match again
                self.order_book.print_status('APPL')

        # Create and start a new thread for matching orders for the specified symbol
        if symbol not in self.matching_threads:
            thread = threading.Thread(target=match_loop, daemon=True)
            self.matching_threads[symbol] = thread
            thread.start()

    def stop_matching(self):
        """Stop all matching threads."""
        self.stop_event.set()
        for symbol, thread in self.matching_threads.items():
            thread.join()  # Wait for all threads to finish
