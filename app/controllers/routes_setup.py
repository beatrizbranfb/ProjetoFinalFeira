from bottle import route, static_file
import os

from app.controllers import auth_controller
from app.controllers import product_controller
from app.controllers import cart_controller

def setup_routes(app, base_dir):

    @app.route('/static/<filepath:path>')
    def serve_static(filepath):
        return static_file(filepath, root=os.path.join(base_dir, 'static'))

    app.route('/login', callback=auth_controller.login)
    app.route('/login', method='POST', callback=auth_controller.login)
    app.route('/register', callback=auth_controller.register)
    app.route('/register', method='POST', callback=auth_controller.register)
    app.route('/logout', callback=auth_controller.logout)

    app.route('/', callback=product_controller.list_products)
    app.route('/products', callback=product_controller.list_products)
    app.route('/products/<product_id:int>', callback=product_controller.product_details)
    app.route('/products/add', callback=product_controller.add_product)
    app.route('/products/add', method='POST', callback=product_controller.add_product)
    app.route('/products/edit/<product_id:int>', callback=product_controller.edit_product)
    app.route('/products/edit/<product_id:int>', method='POST', callback=product_controller.edit_product)
    app.route('/products/delete/<product_id:int>', method='POST', callback=product_controller.delete_product)

    app.route('/cart', callback=cart_controller.view_cart)
    app.route('/cart/add/<product_id:int>', method='POST', callback=cart_controller.add_to_cart)
    app.route('/cart/remove/<product_id:int>', method='POST', callback=cart_controller.remove_from_cart)
    app.route('/cart/update/<product_id:int>', method='POST', callback=cart_controller.update_cart_item)
    app.route('/cart/checkout', method='POST', callback=cart_controller.checkout)

    @app.error(404)
    def error404(error):
        from controllers.application import app_renderer
        return app_renderer.render_page('error_404', message="A página não existe.")