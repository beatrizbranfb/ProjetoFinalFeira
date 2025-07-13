from bottle import Bottle, run, TEMPLATE_PATH, request, response, static_file, route, template, redirect
import os
import uuid
import sys
from app.controllers.application import Application
from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from app.controllers.cart_controller import CartController


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

APP_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(APP_ROOT_DIR, 'views'))

app = Bottle()
ctl = Application()
user_ctl = UserController()
product_ctl = ProductController()
cart_ctl = CartController()

sessions = {}

@app.hook('before_request')
def setup_session():
    session_id = request.get_cookie("session_id")
    if session_id and session_id in sessions:
        request.session = sessions[session_id]
    else:
        session_id = str(uuid.uuid4())
        request.session = {}
        sessions[session_id] = request.session
        response.set_cookie("session_id", session_id, path='/', httponly=True)

@app.hook('after_request')
def teardown_session():
    session_id = request.get_cookie("session_id")
    if session_id:
        sessions[session_id] = request.session

#---------------------------------------------------------------------------------------
#Rotas
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')
        
@app.route('/')
def helper(info=None):
    return ctl.render('helper')

#--------------------------------------------------------------------------------------

app.route('/', callback=ctl.helper) 
app.route('/login', method=['GET', 'POST'], callback=user_ctl.login)
app.route('/register', method=['GET', 'POST'], callback=user_ctl.register)
app.route('/logout', callback=user_ctl.logout)

app.route('/products/<product_id:int>', callback=product_ctl.product_details)
app.route('/products/add_stock/<product_id:int>', method='POST', callback=product_ctl.add_stock)
app.route('/products/remove_stock/<product_id:int>', method='POST', callback=product_ctl.remove_stock)
app.route('/products/add', method=['GET', 'POST'], callback=product_ctl.add_product)
app.route('/products/edit/<product_id:int>', method=['GET', 'POST'], callback=product_ctl.edit_product)
app.route('/products/delete/<product_id:int>', method='POST', callback=product_ctl.delete_product)
app.route('/products', callback=product_ctl.list_products)

app.route('/cart', callback=cart_ctl.view_cart)
app.route('/cart/add/<product_id:int>', method='POST', callback=cart_ctl.add_to_cart)
app.route('/cart/remove/<product_id:int>', method='POST', callback=cart_ctl.remove_from_cart)
app.route('/cart/update/<product_id:int>', method='POST', callback=cart_ctl.update_cart_item)
app.route('/cart/checkout', method='POST', callback=cart_ctl.checkout)

app.route('/profile', callback=ctl.profile)
app.route('/orders', callback=ctl.orders)

app.route('/administrador', callback=user_ctl.admin_dashboard)
app.route('/admin_clientes', callback=user_ctl.admin_clientes)

app.route('/stock', callback=product_ctl.view_stock)
app.route('/stock/add', method='POST', callback=product_ctl.add_product)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)