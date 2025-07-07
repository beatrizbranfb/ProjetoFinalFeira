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
            'delete_product': self.delete_product,
            'view_stock': self.view_stock
        }
    
    @route('/stock')
    @admin_required
    def view_stock(self):
        products = self.__products.get_all_products()
        return app_renderer.render_page('administrador_estoque.html', products=products)

    @route('/products')
    @login_required
    def list_products(self):
        products = self.__products.get_all_products()
        user_role = self.__user_controller.get_user_role()
        return app_renderer.render_page('cliente_produto.html', products=products, user_role=user_role)

    @route('/products/<product_id:int>')
    @login_required
    def product_details(self, product_id):
        product = self.__products.get_product_by_id(product_id)
        if not product:
            return app_renderer.render_page('error_404', message="Produto não encontrado.")
        return app_renderer.render_page('produtos/detalhes.tpl', product=product)

    @route('/products/add', method='POST')
    @admin_required
    def add_product(self):
        name = request.forms.get('name')
        price = request.forms.get('price')
        stock = request.forms.get('stock')
        category = request.forms.get('category')

        if not name or not price or not stock or not category:
            return app_renderer.render_page('error_400', message="Todos os campos são obrigatórios.")

        try:
            price = float(price)
            stock = float(stock)
        except ValueError:
            return app_renderer.render_page('error_400', message="Preço e quantidade devem ser números.")
        
        description = category

        self.__products.add_product(name=name, price=price, stock=stock, description=description)
        return redirect('/stock')
        
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
            return redirect('/stock')
        return app_renderer.render_page('produtos/adicionar_editar', product=product, error=None)

    @route('/products/delete/<product_id:int>', method=['POST'])
    @admin_required
    def delete_product(self, product_id):
        self.__products.delete_product(product_id)
        return redirect('/stock')
