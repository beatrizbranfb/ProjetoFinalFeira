from app.controllers.db import database


class User:
    def __init__(self, user_id, username, password, email, role='default'):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    @staticmethod
    def get_db():
        return database.get_db()

    @classmethod
    def find_by_username(cls, username):
        with cls.get_db() as db:
            cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(
                    user_data['id'],
                    user_data['username'],
                    user_data['password'],
                    user_data['email'],
                    user_data['role']
                    )
            return None

    @classmethod
    def create(cls, username, password, email, role='customer'):
        with cls.get_db() as db:
            cursor = db.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                                (username, password, email, role))
            db.commit()
            return cursor.lastrowid

    def save(self):
        with self.get_db() as db:
            db.execute("UPDATE users SET username=?, password=?, email=?, role=? WHERE id=?",
                       (self.username, self.password, self.email, self.role, self.id))
            db.commit()

    def delete(self):
        with self.get_db() as db:
            db.execute("DELETE FROM users WHERE id=?", (self.id,))
            db.commit()