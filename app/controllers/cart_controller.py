from bottle import route, request, redirect
from app.controllers.cartRecord import CartRecord, CartItemRecord
from app.controllers.productRecord import ProductRecord
from app.controllers.user_controller import login_required, get_user_role
from app.controllers.application import app_renderer


@route('/cart')
@login_required
def view_cart():
    user_id = request.session.get('user_id')
    cart = CartRecord.get_user_orders(user_id)
    if not cart:
        cart = CartRecord.add_order(user_id)
    return app_renderer.render_page('carrinho listagem', cart=cart)

@route('/cart/add/<product_id:int>', method=['POST'])
@login_required
def add_to_cart(product_id):
    user_id = request.session.get('user_id')
    quantity = int(request.forms.get('quantity', 1))

    cart = CartRecord.get_user_orders(user_id)
    if not cart:
        cart = CartRecord.add_order(user_id)

    try:
        cart.add_item(product_id, quantity)
        redirect('/cart')
    except ValueError as e:
        return app_renderer.render_page('produtos/detalhes.tpl', product=ProductRecord.get_product_by_id(product_id), error=str(e))


@route('/cart/remove/<product_id:int>', method=['POST'])
@login_required
def remove_from_cart(product_id):
    user_id = request.session.get('user_id')
    cart = CartRecord.get_user_orders(user_id)
    if cart:
        cart.remove_item(product_id)
    redirect('/cart')

@route('/cart/update/<product_id:int>', method=['POST'])
@login_required
def update_cart_item(product_id):
    user_id = request.session.get('user_id')
    try:
        new_quantity = int(request.forms.get('quantity', 0))
        if new_quantity < 0:
            raise ValueError("Quantidade não pode ser negativa.")
    except (ValueError, TypeError):
        cart = CartRecord.get_user_orders(user_id)
        return app_renderer.render_page('carrinho listagem.tpl', cart=cart, error="Quantidade inválida.")

    cart = CartRecord.get_user_orders(user_id)
    if cart:
        try:
            cart.update_item_quantity(product_id, new_quantity)
            redirect('/cart')
        except ValueError as e:
            return app_renderer.render_page('carrinho listagem.tpl', cart=cart, error=str(e))
    return redirect('/cart')

@route('/cart/checkout', method=['POST'])
@login_required
def checkout():
    user_id = request.session.get('user_id')
    cart = CartRecord.get_user_orders(user_id)

    if not cart or not cart.items:
        return app_renderer.render_page('carrinho listagem', cart=cart, error="Seu carrinho está vazio.")

    try:
        cart.complete_order()
        return app_renderer.render_page('carrinho completo', order=cart)
    except ValueError as e:
        return app_renderer.render_page('carrinho listagem', cart=cart, error=str(e))
