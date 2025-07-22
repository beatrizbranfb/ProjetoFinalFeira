from bottle import route, request, redirect, post
from app.controllers.cartRecord import CartRecord, CartItemRecord
from app.controllers.productRecord import ProductRecord
from app.controllers.user_controller import login_required
from app.controllers.application import app_renderer


class CartController:
    def __init__(self, app):
        self.__cart_item_record = CartItemRecord()
        self.__cart_record = CartRecord(cart_item_record=self.__cart_item_record, app_renderer=app)
        self.pages = {
            'view_cart': self.view_cart,
            'view_orders': self.view_orders,
            'add_to_cart': self.add_to_cart,
            'remove_from_cart': self.remove_from_cart,
            'update_cart_item': self.update_cart_item,
            'checkout': self.checkout,
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
    
    @route('/orders')
    @login_required
    def view_orders(self):
        user_id = request.session.get('user_id')
        user_orders = self.__cart_record.get_user_orders(user_id)



        for order in user_orders:
            order.total_amount = sum(item['total_price'] for item in order.items)

        return app_renderer.render_page("cliente_pedidos.html", orders=user_orders)

    @route('/cart/add/<product_id:int>', method=['POST'])
    @login_required
    def add_to_cart(self, product_id):
        user_id = request.session.get('user_id')
        quantity = int(request.forms.get('quantity', 1))

        print(f"\n--- DEBUG: Chamada para add_to_cart ---")
        print(f"  User ID: {user_id}, Product ID: {product_id}, Quantity: {quantity}")

        cart = self.__cart_record.get_active_cart_by_user_id(user_id)
        if not cart:
            print("  Nenhum carrinho ativo encontrado. Criando um novo.")
            cart = self.__cart_record.add_order(user_id)
        print(f"  Carrinho ativo usado para adicionar item: ID {cart.id}, Status: {cart.status}")

        try:
            if quantity <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            self.__cart_item_record.add_item(cart.id, product_id, quantity)
            print(f"  Item adicionado com sucesso ao carrinho ID {cart.id}.")
            return redirect('/cart')
        except ValueError as e:
            print(f"  ERRO ao adicionar item ao carrinho: {e}")
            return redirect('/cart')

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
            self.__cart_record.add_order(user_id)
            return redirect('/orders')
        except ValueError as e:
            return app_renderer.render_page('cliente_carrinho.html', cart=cart_data, error=str(e))

    @post('/admin/confirmar_pedido/<order_id:int>', method = 'POST')
    def confirmar_pedido_admin(self, order_id):
        self.__cart_record.update_order_status(order_id, 'completed')
        return redirect('/admin_clientes')

