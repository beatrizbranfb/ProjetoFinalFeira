from app.controllers.db import database


class Product:
    def __init__(self, product_id, name, description, price, stock):
        self.id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    @staticmethod
    def get_db():
        return database.get_db()
    
    @classmethod
    def get_all(cls):
        with cls.get_db() as db:
            cursor = db.execute("SELECT * FROM products")
            return [cls(
                p['id'],
                p['name'],
                p['description'],
                p['price'],
                p['stock']
                ) 
            for p in cursor.fetchall()]
    
    @classmethod
    def find_by_id(cls, product_id):
        with cls.get_db() as db:
            cursor = db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product_data = cursor.fetchone()
            if product_data:
                return cls(
                    product_data['id'],
                    product_data['name'],
                    product_data['description'],
                    product_data['price'],
                    product_data['stock']
                )
            return None
        
    @classmethod
    def create(self):
        with self.get_db() as db:
            cursor = db.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
                                (self.name, self.description, self.price, self.stock))
            db.commit()
            self.id = cursor.lastrowid
    
    def save(self):
        with self.get_db() as db:
            db.execute("UPDATE products SET name=?, description=?, price=?, stock=? WHERE id=?",
                       (self.name, self.description, self.price, self.stock, self.id))
            db.commit()

    def delete(self):
        with self.get_db() as db:
            db.execute("DELETE FROM products WHERE id=?", (self.id,))
            db.commit()