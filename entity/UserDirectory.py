import uuid
from abc import ABC, abstractmethod

from entity.User import User


class UserDirectory(ABC):
    @abstractmethod
    def add_user(self, user: User):
        raise Exception("UserDirectoryInterface's method - add_user - not implemented.")

    @abstractmethod
    def remove_user_by_id(self, user_id: uuid.UUID):
        raise Exception("UserDirectoryInterface's method - remove_user_by_id - not implemented.")

    @abstractmethod
    def find_user_by_id(self, user_id: uuid.UUID):
        raise Exception("UserDirectoryInterface's method - find_user_by_id - not implemented.")