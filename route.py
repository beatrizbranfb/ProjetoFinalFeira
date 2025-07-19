
from bottle import TEMPLATE_PATH, request, response, static_file
import os
import uuid
import sys

from app.controllers.application import app_renderer
from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.cart_controller import CartController

import eventlet
import eventlet.wsgi


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

APP_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(APP_ROOT_DIR, 'views'))

ctl = app_renderer
user_ctl = UserController()
product_ctl = ProductController(app = app_renderer)
cart_ctl = CartController(app = app_renderer)

sessions = {}

@app_renderer.app.hook('before_request')
def setup_session():
    session_id = request.get_cookie("session_id")
    if session_id and session_id in sessions:
        request.session = sessions[session_id]
    else:
        session_id = str(uuid.uuid4())
        request.session = {}
        sessions[session_id] = request.session
        response.set_cookie("session_id", session_id, path='/', httponly=True)

@app_renderer.app.hook('after_request')
def teardown_session():
    session_id = request.get_cookie("session_id")
    if session_id:
        sessions[session_id] = request.session

#---------------------------------------------------------------------------------------
#Rotas
@app_renderer.app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app_renderer.app.route('/')
def helper(info=None):
    return ctl.render('helper')

#--------------------------------------------------------------------------------------

app_renderer.app.route('/', callback=ctl.helper) 
app_renderer.app.route('/login', method=['GET', 'POST'], callback=user_ctl.login)
app_renderer.app.route('/register', method=['GET', 'POST'], callback=user_ctl.register)
app_renderer.app.route('/logout', callback=user_ctl.logout)

app_renderer.app.route('/products', callback=product_ctl.list_products)
app_renderer.app.route('/products/<product_id:int>', callback=product_ctl.product_details)
app_renderer.app.route('/products/add_stock/<product_id:int>', method='POST', callback=product_ctl.add_stock)
app_renderer.app.route('/products/remove_stock/<product_id:int>', method='POST', callback=product_ctl.remove_stock)
app_renderer.app.route('/products/add', method=['GET', 'POST'], callback=product_ctl.add_product)
app_renderer.app.route('/products/add/<product_id:int>', method='POST', callback=product_ctl.add_product)
app_renderer.app.route('/products/edit/<product_id:int>', method=['GET', 'POST'], callback=product_ctl.edit_product)
app_renderer.app.route('/products/delete/<product_id:int>', method='POST', callback=product_ctl.delete_product)

app_renderer.app.route('/cart', callback=cart_ctl.view_cart)
app_renderer.app.route('/cart/add/<product_id:int>', method='POST', callback=cart_ctl.add_to_cart)
app_renderer.app.route('/cart/remove/<product_id:int>', method='POST', callback=cart_ctl.remove_from_cart)
app_renderer.app.route('/cart/update/<product_id:int>', method='POST', callback=cart_ctl.update_cart_item)
app_renderer.app.route('/cart/checkout', method='POST', callback=cart_ctl.checkout)

app_renderer.app.route('/profile', callback=user_ctl.profile)
app_renderer.app.route('/orders', callback=cart_ctl.view_orders)

app_renderer.app.route('/admin', callback=user_ctl.admin_dashboard)
app_renderer.app.route('/admin_clientes', callback=user_ctl.admin_clientes)
app_renderer.app.route('/acesso_neg', callback=user_ctl.acesso_neg)

app_renderer.app.route('/stock', callback=product_ctl.view_stock)
app_renderer.app.route('/stock/add', method='POST', callback=product_ctl.add_product)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8080)), app_renderer.wsgi_app)
