from bottle import route, static_file
import os

from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.cart_controller import CartController

class RouteRenderer:

    def setup_routes(app, base_dir):

        @app.route('/static/<filepath:path>')
        def serve_static(filepath):
            return static_file(filepath, root=os.path.join(base_dir, 'static'))

        @app.route('/login', callback=UserController.login)
        @app.route('/login', method='POST', callback=UserController.login)
        @app.route('/register', callback=UserController.register)
        @app.route('/register', method='POST', callback=UserController.register)
        @app.route('/logout', callback=UserController.logout)

        @app.route('/', callback=ProductController.list_products)
        @app.route('/products', callback=ProductController.list_products)
        @app.route('/products/<product_id:int>', callback=ProductController.product_details)
        @app.route('/products/add', callback=ProductController.add_product)
        @app.route('/products/add', method='POST', callback=ProductController.add_product)
        @app.route('/products/edit/<product_id:int>', callback=ProductController.edit_product)
        @app.route('/products/edit/<product_id:int>', method='POST', callback=ProductController.edit_product)
        @app.route('/products/delete/<product_id:int>', method='POST', callback=ProductController.delete_product)

        @app.route('/cart', callback=CartController.view_cart)
        @app.route('/cart/add/<product_id:int>', method='POST', callback=CartController.add_to_cart)
        @app.route('/cart/remove/<product_id:int>', method='POST', callback=CartController.remove_from_cart)
        @app.route('/cart/update/<product_id:int>', method='POST', callback=CartController.update_cart_item)
        @app.route('/cart/checkout', method='POST', callback=CartController.checkout)

        @app.error(404)
        def error404(error):
            from controllers.application import app_renderer
            return app_renderer.render_page('error_404', message="A página não existe.")