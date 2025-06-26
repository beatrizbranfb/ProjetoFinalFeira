from app.controllers.user_controller import UserController, login_required, admin_required
from app.controllers.productRecord import ProductRecord
from bottle import request, redirect, route
from app.controllers.application import app_renderer

class ProductController:

    def __init__(self):
        self.__products = ProductRecord()
        self.__user_controller = UserController()
        self.pages = {
            'list_products': self.list_products,
            'product_details': self.product_details,
            'add_product': self.add_product,
            'edit_product': self.edit_product,
            'delete_product': self.delete_product
        }

    @route('/')
    @route('/products')
    @login_required
    def list_products(self):
        products = self.__products.get_all_products()
        user_role = self.__user_controller.get_user_role()
        return app_renderer.render_page('produtos/listar.tpl', products=products, user_role=user_role)

    @route('/products/<product_id:int>')
    @login_required
    def product_details(self, product_id):
        product = self.__products.get_product_by_id(product_id)
        if not product:
            return app_renderer.render_page('error_404', message="Produto não encontrado.")
        return app_renderer.render_page('produtos/detalhes.tpl', product=product)

    @route('/products/add', method=['GET', 'POST'])
    @admin_required
    def add_product(self):
        if request.method == 'POST':
            name = request.forms.get('name')
            description = request.forms.get('description')
            price = float(request.forms.get('price'))
            stock = int(request.forms.get('stock'))

            if not name or not price or not stock:
                return app_renderer.render_page('produtos/adicionar_editar', product=None, error="Todos os campos são obrigatórios.")

            self.__products.add_product(name=name, description=description, price=price, stock=stock)
            redirect('/products')
        return app_renderer.render_page('produtos/adicionar_editar', product=None, error=None)

    @route('/products/edit/<product_id:int>', method=['GET', 'POST'])
    @admin_required
    def edit_product(self, product_id):
        product = self.__products.get_product_by_id(product_id)
        if not product:
            return app_renderer.render_page('error_404', message="Produto não encontrado.")

        if request.method == 'POST':
            product.name = request.forms.get('name')
            product.description = request.forms.get('description')
            product.price = float(request.forms.get('price'))
            product.stock = int(request.forms.get('stock'))
            product = self.__products.update_product(
                product_id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock
            )
            redirect('/products')
        return app_renderer.render_page('produtos/adicionar_editar', product=product, error=None)

    @route('/products/delete/<product_id:int>', method=['POST'])
    @admin_required
    def delete_product(self, product_id):
        product = self.__products.get_product_by_id(product_id)
        if product:
            product.delete()
        redirect('/products')
