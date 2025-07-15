from app.models.order import Order, OrderItem
import json
from datetime import datetime
from app.controllers.productRecord import ProductRecord

class CartRecord:

    def __init__(self):
        self.__all_orders = []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/orders.json", "r") as fjson:
                orders_data = json.load(fjson)
                self.__all_orders = []
                for order_dict in orders_data:
                    if isinstance(order_dict.get('order_date'), str):
                        order_dict['order_date'] = datetime.fromisoformat(order_dict['order_date'])
                    self.__all_orders.append(Order(**order_dict))
        except (FileNotFoundError, json.JSONDecodeError):
            print('Arquivo de carrinhos não encontrado ou corrompido. Começando com uma lista vazia.')
            self.__all_orders = []

    def __write(self):
        try:
            with open("app/controllers/db/orders.json", "w") as fjson:
                orders_list = [o.__dict__.copy() for o in self.__all_orders]
                for order_dict in orders_list:
                    order_dict['order_date'] = order_dict['order_date'].isoformat()
                json.dump(orders_list, fjson, indent=4)
                print('Arquivo gravado (carrinho)!')
        except FileNotFoundError:
            print('Não conseguiu gravar (carrinho)!')

    def add_order(self, user_id):
        new_order = Order(len(self.__all_orders) + 1, user_id, datetime.now(), 0.0, status='pending')
        self.__all_orders.append(new_order)
        self.__write()
        return new_order
    
    def get_tot_amount(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            product_record = ProductRecord()
            total_sum = 0.0
            for item_obj in order.items:
                product = product_record.get_product_by_id(item_obj.product_id)
                if product:
                    total_sum += item_obj.quantity * product.price
            order.total_amount = total_sum
            return total_sum
        return 0.0

    def get_all_orders(self):
        return self.__all_orders

    def get_active_cart_by_user_id(self, user_id):
        for order in reversed(self.__all_orders): 
            if order.user_id == user_id and order.status == 'pending':
                return order
        return None

    def get_user_orders(self, user_id):
        user_orders = []
        product_record = ProductRecord()

        for order in self.__all_orders:
            if order.user_id == user_id:

                augmented_items = []
                for item_obj in order.items:
                    product = product_record.get_product_by_id(item_obj.product_id)
                    if product:
                        augmented_items.append({
                            "product_id": item_obj.product_id,
                            "name": product.name,
                            "price": product.price,
                            "quantity": item_obj.quantity
                        })
                order.total_amount = self.get_tot_amount(order.id)
                order.items = augmented_items
                user_orders.append(order)
        return user_orders
    
    def get_order_by_id(self, order_id):
        for order in self.__all_orders:
            if order.id == order_id:
                return order
        return None
    
    def update_order_status(self, order_id, status):
        order = self.get_order_by_id(order_id)
        if order:
            order.status = 'completed' if status == 'completed' else 'pending'
            self.__write()
            return order
        return None
    
    def delete_order(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            self.__all_orders.remove(order)
            self.__write()
            return order
        return None

    def get_user_cart(self, user_id):
        cart = self.get_active_cart_by_user_id(user_id)
        if not cart:
            return None

        cart_item_record = CartItemRecord()  
        product_record = ProductRecord()

        items = []
        subtotal = 0.0

        for item in cart_item_record.get_all_items():
            if item.order_id == cart.id:
                product = product_record.get_product_by_id(item.product_id)
                if product:
                    total_price = product.price * item.quantity
                    subtotal += total_price
                    items.append({
                        "product_id": item.product_id,
                        "name": product.name,
                        "price": product.price,
                        "image": getattr(product, "image", ""),
                        "quantity": item.quantity,
                        "total_price": total_price
                    })

        cart.items = items

        return {
            "id": cart.id,
            "user_id": user_id,
            "items": items,
            "subtotal": subtotal,
            "delivery_fee": 5.0,
            "total": subtotal + 5.0
        }



class CartItemRecord:

    def __init__(self):
        self.__all_items = []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/cart_items.json", "r") as fjson:
                item_data = json.load(fjson)
                self.__all_items = [OrderItem(**item) for item in item_data]
        except FileNotFoundError:
            print('Não existem itens de carrinho registrados!')

    def __write(self):
        try:
            with open("app/controllers/db/cart_items.json", "w") as fjson:
                item_data = [vars(item) for item in self.__all_items]
                json.dump(item_data, fjson)
                print('Arquivo gravado com sucesso (Item do Carrinho)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Item do Carrinho)!')

    def add_item(self, order_id, product_id, quantity):
        existing_item = self.get_cart_item(order_id, product_id)
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = OrderItem(order_id, product_id, quantity)
            self.__all_items.append(new_item)
        self.__write()

    
    def del_item(self, order_id, product_id):
        item = self.get_cart_item(order_id, product_id)
        if item:
            self.__all_items.remove(item)
            self.__write()
            return item
        return None
    
    def update_item_quantity(self, order_id, product_id, new_quantity):
        item = self.get_cart_item(order_id, product_id)
        if item:
            if new_quantity <= 0:
                self.del_item(order_id, product_id)
            else:
                item.quantity = new_quantity
                self.__write()
            return item
        elif new_quantity > 0:
            return self.add_item(order_id, product_id, new_quantity)
        return None

    def get_all_items(self):
        return self.__all_items
    
    def get_cart_item(self, order_id, product_id):
        for item in self.__all_items:
            if item.order_id == order_id and item.product_id == product_id:
                return item
        return None
