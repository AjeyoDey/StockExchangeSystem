import uuid

from entity.impl.OrderBookImpl import OrderBook
from entity.User import User
from entity.impl.UserDirectoryImpl import UserDirectory


class UserManagementService:
    def __init__(self, user_directory: UserDirectory, order_book: OrderBook):
        self.user_directory = user_directory
        self.order_book = order_book

    def add_user(self, name: str, email: str, phone: str):
        user = User(name, email, phone)
        self.user_directory.add_user(user)
        return user  # Return the user

    def delete_user(self, user_id: uuid.UUID):
        user = self.user_directory.find_user_by_id(user_id)
        if user:
            self.user_directory.remove_user_by_id(user_id)
            return True
        return False  # Return False if user was not found

    def get_user(self, user_id: uuid.UUID):
        return self.user_directory.find_user_by_id(user_id)

    def fetch_active_trades(self, user: User):
        # Fetch active trades of the User
        pass
