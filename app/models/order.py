class Order:

    def __init__(self, id, user_id, order_date, total_amount, status='pending', items=None):
        self.id = id 
        self.user_id = user_id 
        self.order_date = order_date
        self.total_amount = total_amount
        self.status = status
        self.items = items if items is not None else [] 


class OrderItem:
    def __init__(self, order_id, product_id, quantity, product_name=None):
        self.order_id = order_id
        self.product_id = product_id 
        self.quantity = quantity
        self.product_name = product_name