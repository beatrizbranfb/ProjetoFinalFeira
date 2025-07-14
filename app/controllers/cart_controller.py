from bottle import route, request, redirect
from app.controllers.cartRecord import CartRecord, CartItemRecord
from app.controllers.productRecord import ProductRecord
from app.controllers.user_controller import login_required
from app.controllers.application import app_renderer


class CartController:
    def __init__(self):
        self.__cart_record = CartRecord()
        self.__cart_item_record = CartItemRecord()
        self.pages = {
            'view_cart': self.view_cart,
            'add_to_cart': self.add_to_cart,
            'remove_from_cart': self.remove_from_cart,
            'update_cart_item': self.update_cart_item,
            'checkout': self.checkout
        }

    @route('/cart')
    @login_required
    def view_cart(self):
        user_id = request.session.get('user_id')
        cart = self.__cart_record.get_user_cart(user_id)
        if not cart:
            self.__cart_record.add_order(user_id)
            cart = self.__cart_record.get_user_cart(user_id)


        return app_renderer.render_page('cliente_carrinho.html', cart=cart)

    @route('/cart/add/<product_id:int>', method=['POST'])
    @login_required
    def add_to_cart(self, product_id):
        user_id = request.session.get('user_id')
        quantity = int(request.forms.get('quantity', 1))

        cart = self.__cart_record.get_active_cart_by_user_id(user_id)
        if not cart:
            cart = self.__cart_record.add_order(user_id)

        try:
            if quantity <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            self.__cart_item_record.add_item(cart.id, product_id, quantity)
            return redirect('/cart')
        except ValueError as e:
            return app_renderer.render_page('cliente_carrinho.html', product=ProductRecord.get_product_by_id(product_id), error=str(e))


    @route('/cart/remove/<product_id:int>', method=['POST'])
    @login_required
    def remove_from_cart(self, product_id):
        user_id = request.session.get('user_id')
        cart = self.__cart_record.get_active_cart_by_user_id(user_id)
        if cart:
            self.__cart_item_record.del_item(cart.id, product_id)
        return redirect('/cart')


    @route('/cart/update/<product_id:int>', method=['POST'])
    @login_required
    def update_cart_item(self, product_id):
        user_id = request.session.get('user_id')
        cart = self.__cart_record.get_active_cart_by_user_id(user_id)
        if not cart:
            return redirect('/cart')

        try:
            new_quantity = int(request.forms.get('quantity', 0))
        except (ValueError, TypeError):
            return app_renderer.render_page('cliente_carrinho.html', cart=self.__cart_record.get_user_cart(user_id), error="Quantidade inválida.")

        try:
            self.__cart_item_record.update_item_quantity(cart.id, product_id, new_quantity)
            return redirect('/cart')
        except ValueError as e:
            return app_renderer.render_page('cliente_carrinho.html', cart=self.__cart_record.get_user_cart(user_id), error=str(e))


    @route('/cart/checkout', method=['POST'])
    @login_required
    def checkout(self):
        user_id = request.session.get('user_id')
        cart = self.__cart_record.get_active_cart_by_user_id(user_id)

        cart_data = self.__cart_record.get_user_cart(user_id)

        if not cart_data or not cart_data["items"]:
            return app_renderer.render_page('cliente_carrinho.html', cart=cart_data, error="Seu carrinho está vazio.")

        try:
            self.__cart_record.update_order_status(cart.id, status='completed')
            return app_renderer.render_page('cliente_carrinho.html', order=cart_data)
        except ValueError as e:
            return app_renderer.render_page('cliente_carrinho.html', cart=cart_data, error=str(e))

