import threading
import uuid

from entity.User import User


class UserDirectory:
    def __init__(self):
        self.directory = []
        self.lock = threading.Lock()

    def add_user(self, user: User):
        with self.lock:
            self.directory.append(user)

    def remove_user_by_id(self, user_id: uuid.UUID):
        with self.lock:
            self.directory = [user for user in self.directory if user.id != user_id]

    def find_user_by_id(self, user_id: uuid.UUID):
        with self.lock:
            for user in self.directory:
                if user.id == user_id:
                    return user
            return None
