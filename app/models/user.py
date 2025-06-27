class User:
    def __init__(self, user_id, username, password, email):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email

    def is_admin(self):
        return False


class AdminUser(User):
    def __init__(self, user_id, username, password, email, permissions):
        super().__init__(user_id, username, password, email)
        self.permissions= permissions 
        if not permissions:
            permissions=["user"]

    def is_admin(self):
        return True