from app.controllers.auth_controller import login_required, get_user_role, employee_required
from app.models.product import Product
from bottle import request, redirect, route, template


@route('/')
@route('/products')
@login_required
def list_products():
    products = Product.get_all()
    user_role = get_user_role()
    return template('products/list_products', products=products, user_role=user_role)

@route('/products/<product_id:int>')
@login_required
def product_details(product_id):