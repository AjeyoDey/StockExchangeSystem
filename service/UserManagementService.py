import uuid

from entity.OrderBook import OrderBook
from entity.User import User
from entity.UserDirectory import UserDirectory


class UserManagementService:
    def __init__(self, user_directory: UserDirectory, order_book: OrderBook):
        self.user_directory = user_directory
        self.order_book = order_book

    def add_user(self, name: str, email: str, phone: str):
        user = User(name, email, phone)
        self.user_directory.add_user(user)
        return user.id  # Return the user's ID for reference

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
