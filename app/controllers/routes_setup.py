from bottle import route, static_file, Bottle
import os

from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.cart_controller import CartController

class RouteRenderer:
    def __init__(self):
        self.app = Bottle()

    def setup_routes(self, base_dir):

        @self.app.route('/static/<filepath:path>')
        def serve_static(filepath):
            return static_file(filepath, root=os.path.join(base_dir, 'static'))

        self.app.route('/login', callback=UserController.login)
        self.app.route('/login', method='POST', callback=UserController.login)
        self.app.route('/register', callback=UserController.register)
        self.app.route('/register', method='POST', callback=UserController.register)
        self.app.route('/logout', callback=UserController.logout)

        self.app.route('/', callback=ProductController.list_products)
        self.app.route('/products', callback=ProductController.list_products)
        self.app.route('/products/<product_id:int>', callback=ProductController.product_details)
        self.app.route('/products/add', callback=ProductController.add_product)
        self.app.route('/products/add', method='POST', callback=ProductController.add_product)
        self.app.route('/products/edit/<product_id:int>', callback=ProductController.edit_product)
        self.app.route('/products/edit/<product_id:int>', method='POST', callback=ProductController.edit_product)
        self.app.route('/products/delete/<product_id:int>', method='POST', callback=ProductController.delete_product)

        self.app.route('/cart', callback=CartController.view_cart)
        self.app.route('/cart/add/<product_id:int>', method='POST', callback=CartController.add_to_cart)
        self.app.route('/cart/remove/<product_id:int>', method='POST', callback=CartController.remove_from_cart)
        self.app.route('/cart/update/<product_id:int>', method='POST', callback=CartController.update_cart_item)
        self.app.route('/cart/checkout', method='POST', callback=CartController.checkout)
