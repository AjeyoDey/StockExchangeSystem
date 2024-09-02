import uuid


class User:
    def __init__(self, name: str, email: str, phone: str):
        self.id = uuid.uuid4()
        self.name = name
        self.phone = phone
        self.email = email

