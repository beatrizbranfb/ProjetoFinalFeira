from app.models.product import Product
from app.controllers.db import database


class Order:

    def __init__(self, order_id, user_id, order_date, total_amount, status='pending'):
        self.id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.status = status
        self.items = [] # OrderItems

        @staticmethod
        def get_db():
            return database.get_db()

        @classmethod
        def create(cls, user_id):
            with cls.get_db() as db:
                cursor = db.execute("INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)",
                                    (user_id, 0.0, 'pending'))
                db.commit()
                return cls(cursor.lastrowid, user_id, status= 'pending')

        @classmethod
        def find_by_id(cls, order_id):
            with cls.get_db() as db:
                cursor = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
                order_data = cursor.fetchone()
                if order_data:
                    order = cls(
                        order_data['id'],
                        order_data['user_id'],
                        order_data['order_date'],
                        order_data['total'],
                        order_data['status']
                    )
                    order.load_items()
                    return order
                return None

        @classmethod
        def get_user_pending_order(cls, user_id):
            with cls.get_db() as db:
                cursor = db.execute("SELECT * FROM orders WHERE user_id = ? AND status = 'pending'", (user_id,))
                order_data = cursor.fetchone()
                if order_data:
                    order = cls(
                        order_data['id'],
                        order_data['user_id'],
                        order_data['order_date'],
                        order_data['total_amount'],
                        order_data['status'])
                    order.load_items()
                    return order
                return None

        def save(self):
            with self.get_db() as db:
                db.execute("UPDATE orders SET total_amount=?, status=? WHERE id=?",
                        (self.total_amount, self.status, self.id))
                db.commit()

        def add_item(self, product_id, quantity):
            product = Product.find_by_id(product_id)
            if not product:
                raise ValueError("Product not found")
            if product.stock < quantity:
                raise ValueError(f"Insufficient stock of product {product.name}")
            with self.get_db() as db:
                cursor = db.execute("SELECT * FROM order_items WHERE order_id = ? AND product_id = ?",
                                (self.id, product_id))
                existing_item = cursor.fetchone()
                if existing_item:
                    new_quantity = existing_item['quantity'] + quantity
                    if product.stock < new_quantity:
                        raise ValueError(f"Insufficient stock of '{product.name}'. Available quantity: {product.stock}")
                    db.execute("UPDATE order_items SET quantity = ?, price = ? WHERE id = ?",
                            (new_quantity, product.price, existing_item['id']))
                else:
                    db.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                            (self.id, product_id, quantity, product.price))
                db.commit()
                self.update_total_amount()
                self.load_items()

        def remove_item(self, product_id):
            with self.get_db() as db:
                db.execute("DELETE FROM order_items WHERE order_id = ? AND product_id = ?",
                        (self.id, product_id))
                db.commit()
                self.update_total_amount()
                self.load_items()

        def update_item_quantity(self, product_id, new_quantity):
            if new_quantity <= 0:
                self.remove_item(product_id)
                return
            product = Product.find_by_id(product_id)
            if not product:
                raise ValueError("Product not found")
            if product.stock < new_quantity:
                raise ValueError(f"Insufficient stock of product {product.name}")
            with self.get_db() as db:
                db.execute("UPDATE order_items SET quantity = ? WHERE order_id = ? AND product_id = ?",
                       (new_quantity, self.id, product_id))
                db.commit()
                self.update_total_amount()
                self.load_items()

        def update_total_amount(self):
            with self.get_db() as db:
                cursor = db.execute("SELECT SUM(quantity * price) FROM order_items WHERE order_id = ?", (self.id,))
                self.total_amount = cursor.fetchone()[0] or 0.0
                self.save()

        def load_items(self):
            with self.get_db() as db:
                cursor = db.execute("SELECT oi.id, oi.product_id, oi.quantity, oi.price, p.name as product_name "
                                    "FROM order_items oi JOIN products p ON oi.product_id = p.id "
                                    "WHERE oi.order_id = ?", (self.id,))
                self.items = [OrderItem(
                    i['id'], i['order_id'],
                    i['product_id'], i['quantity'],
                    i['price'], i['product_name']
                    ) for i in cursor.fetchall()]

        def complete_order(self):
            if not self.items:
                raise ValueError("Cannot complete order with no items")
            with self.get_db() as db:
                for item in self.items:
                    product = Product.find_by_id(item.product_id)
                    if not product or product.stock < item.quantity:
                        raise ValueError(f"Insufficient stock for product {item.product_name}")
                    product.stock -= item.quantity
                    product.save()
                self.status = 'completed'
                self.save()
                db.commit()

class OrderItem:
    def __init__(self, item_id, order_id, product_id, quantity, price, product_name=None):
        self.id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.product_name = product_name
