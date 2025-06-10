from bottle import route, request, template, redirect
from models.order import Order, OrderItem
from models.product import Product
from controllers.auth_controller import login_required, get_user_role

@route('/cart')
@login_required
def view_cart():
    user_id = request.session.get('user_id')
    cart = Order.get_user_pending_order(user_id)
    if not cart:
        cart = Order.create(user_id)
    return template('cart/view_cart', cart=cart)

@route('/cart/add/<product_id:int>', method=['POST'])
@login_required
def add_to_cart(product_id):
    user_id = request.session.get('user_id')
    quantity = int(request.forms.get('quantity', 1))

    cart = Order.get_user_pending_order(user_id)
    if not cart:
        cart = Order.create(user_id)

    try:
        cart.add_item(product_id, quantity)
        redirect('/cart')
    except ValueError as e:
        return template('products/product_details', product=Product.find_by_id(product_id), error=str(e))


@route('/cart/remove/<product_id:int>', method=['POST'])
@login_required
def remove_from_cart(product_id):
    user_id = request.session.get('user_id')
    cart = Order.get_user_pending_order(user_id)
    if cart:
        cart.remove_item(product_id)
    redirect('/cart')

@route('/cart/update/<product_id:int>', method=['POST'])
@login_required
def update_cart_item(product_id):
    user_id = request.session.get('user_id')
    new_quantity = int(request.forms.get('quantity', 0))

    cart = Order.get_user_pending_order(user_id)
    if cart:
        try:
            cart.update_item_quantity(product_id, new_quantity)
            redirect('/cart')
        except ValueError as e:
            return template('cart/view_cart', cart=cart, error=str(e))
    return redirect('/cart')

@route('/cart/checkout', method=['POST'])
@login_required
def checkout():
    user_id = request.session.get('user_id')
    cart = Order.get_user_pending_order(user_id)

    if not cart or not cart.items:
        return template('cart/view_cart', cart=cart, error="Seu carrinho está vazio.")

    try:
        cart.complete_order()
        return template('cart/checkout_success', order=cart)
    except ValueError as e:
        return template('cart/view_cart', cart=cart, error=str(e))
