from models import User


class UserInfo:
    user: User

    def __init__(self, user: User):
        self.user = user

    def is_customer(self) -> bool:
        return self.user.role.name == "customer"

    def is_seller(self) -> bool:
        return self.user.role.name == "seller"

    def is_admin(self) -> bool:
        return self.user.role.name == "admin"
