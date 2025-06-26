

class Order:

    def __init__(self, order_id, user_id, order_date, total_amount, status='pending'):
        self.id = order_id # Unique identifier for the order
        self.user_id = user_id # Instance of User
        self.order_date = order_date
        self.total_amount = total_amount
        self.status = status
        self.items = [] # OrderItems


class OrderItem:
    def __init__(self, order_id, product_id, quantity, product_name=None):
        self.order_id = order_id # Instance of Order
        self.product_id = product_id # Instance of Product
        self.quantity = quantity
        self.product_name = product_name