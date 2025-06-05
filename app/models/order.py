from app.models.product import Product


class Order:
    def __init__(self, order_id, user_id, order_date, total, status='pending'):
        self.id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total = total
        self.status = status
        self.items = [] # OrderItems


class OrderItem:
    def __init__(self, item_id, order_id, product_id, quantity, price, product_name=None):
        self.id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.product_name = product_name
