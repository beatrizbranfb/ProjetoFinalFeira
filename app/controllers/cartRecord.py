from app.models.order import Order, OrderItem
import json
from datetime import datetime


class CartRecord():

    def __init__(self):
        self.__all_orders = []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/orders.json", "r") as fjson:
                order_data = json.load(fjson)
                self.__all_orders = [Order(**order) for order in order_data]
        except FileNotFoundError:
            print('Não existem carrinhos registrados!')

    def __write(self):
        try:
            with open("app/controllers/db/orders.json", "w") as fjson:
                order_data = [vars(order) for order in self.__all_orders]
                json.dump(order_data, fjson)
                print('Arquivo gravado (carrinho)!')
        except FileNotFoundError:
            print('Não conseguiu gravar (carrinho)!')

    def add_order(self, user_id):
        new_order = Order(len(self.__all_orders) + 1, user_id, datetime.now(), 0.0)
        self.__all_orders.append(new_order)
        self.__write()
        return new_order
    
    def add_items(self):
        OrderItemRecord = CartItemRecord()
        for order in self.__all_orders:
            for item in order.items:
                OrderItemRecord(order.id, item.product_id, item.quantity)

    
    def get_tot_amount(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            order.total_amount = sum(item.quantity * item.product.price for item in order.items)
            return order.total_amount
        return 0.0

    def get_all_orders(self):
        return self.__all_orders
    
    def get_user_orders(self, user_id):
        user_orders = [order for order in self.__all_orders if order.user_id == user_id]
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

class CartItemRecord():

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
        new_item = OrderItem(order_id, product_id, quantity)
        self.__all_items.append(new_item)
        self.__write()
        return new_item
    
    def del_item(self, item_id):
        item = next((item for item in self.__all_items if item.id == item_id), None)
        if item:
            self.__all_items.remove(item)
            self.__write()
            return item
        return None

    def get_all_items(self):
        return self.__all_items
