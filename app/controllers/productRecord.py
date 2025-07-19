from app.models.product import Product
import json


class ProductRecord():

    def __init__(self):
        self.__all_products = []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/products.json", "r") as fjson:
                product_data = json.load(fjson)
                self.__all_products = []
                for p_data in product_data:
                    product = Product(**p_data)
                    if not hasattr(product, 'image'):
                        product.image = '/static/images/default_product.png'
                    self.__all_products.append(product)
        except FileNotFoundError:
            print('Não existem produtos registrados!')

    def __write(self):
        try:
            with open("app/controllers/db/products.json", "w") as fjson:
                product_data = [vars(product) for product in self.__all_products]
                json.dump(product_data, fjson)
                print('Arquivo gravado com sucesso (Produto)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Produto)!')

    def add_product(self, name, price, stock, description):
        new_product = Product(id=len(self.__all_products) + 1, name=name, price=price, stock=stock, description=description)
        if not hasattr(new_product, 'image'):
            new_product.image = '/static/images/default_product.png'
        self.__all_products.append(new_product)
        self.__write()
        return new_product

    def get_all_products(self):
        return self.__all_products
    
    def get_product_by_id(self, product_id):
        for product in self.__all_products:
            if product.id == product_id:
                return product
        return None
    
    def delete_product(self, product_id):
        product_to_delete = self.get_product_by_id(product_id)
        if product_to_delete:
            self.__all_products.remove(product_to_delete)
            self.__write()
            return True
        return False

    def update_product(self, product_id, name=None, price=None, stock=None, description=None):
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock
        if description is not None:
            product.description = description
        
        self.__write()
        return product