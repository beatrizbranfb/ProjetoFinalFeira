class User:
    def __init__(self, id, username, password, email, role = 'user'):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def is_admin(self):
        return False


class AdminUser(User):
    def __init__(self, id, username, password, email, permissions=None):
        super().__init__(id, username, password, email, role = 'admin')
        self.permissions = permissions if permissions is not None else []

    def is_admin(self):
        return True
    
    def __str__(self): 
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', is_admin={self.is_admin()})"