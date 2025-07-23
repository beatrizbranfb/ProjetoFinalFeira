from app.controllers.user_controller import login_required, admin_required
from app.controllers.productRecord import ProductRecord
from bottle import request, redirect, route
from app.controllers.application import app_renderer

class ProductController:

    def __init__(self, app):
        self.__products = ProductRecord(app_renderer=app)
        self.pages = {
            'list_products': self.list_products,
            'product_details': self.product_details,
            'add_product': self.add_product,
            'edit_product': self.edit_product,
            'delete_product': self.delete_product,
            'view_stock': self.view_stock,
            'add_stock': self.add_stock,
            'remove_stock': self.remove_stock,
        }
    
    @route('/stock')
    @admin_required
    def view_stock(self):
        all_products = self.__products.get_all_products()
        products = all_products

        selected_category = request.query.get('category')
        search_query = request.query.get('search')
        sort_by = request.query.get('sort')

        if selected_category:
            products = [p for p in products if p.description == selected_category]
        
        if search_query:
            search_lower = search_query.lower()
            products = [p for p in products if search_lower in p.name.lower()]
        if sort_by:
            reverse = sort_by.endswith('_desc')
            key_attr = sort_by.split('_')[0]
            
            if key_attr in ['name', 'stock']:
                products.sort(key=lambda p: getattr(p, key_attr), reverse=reverse)

        return app_renderer.render_page(
            'administrador_estoque.html',
            products=products,
            selected_category=selected_category,
            search_query=search_query
        )

    @route('/products')
    @login_required
    def list_products(self):
        from bottle import request

        produtos = ProductRecord().get_all_products()
        search_query = request.query.get('q', '').lower().strip()
        sort_option = request.query.get('sort', '')

        if search_query:
            produtos = [p for p in produtos if search_query in p.name.lower()]

        if sort_option == 'name-asc':
            produtos.sort(key=lambda p: p.name.lower())
        elif sort_option == 'name-desc':
            produtos.sort(key=lambda p: p.name.lower(), reverse=True)
        elif sort_option == 'price-asc':
            produtos.sort(key=lambda p: p.price)
        elif sort_option == 'price-desc':
            produtos.sort(key=lambda p: p.price, reverse=True)

        return app_renderer.render_page('cliente_produto.html', products=produtos, request=request)

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
        image = request.forms.get('image')

        if not name or not price or not stock or not category:
            return app_renderer.render_page('error_400', message="Todos os campos são obrigatórios.")

        try:
            price = float(price)
            stock = float(stock)
        except ValueError:
            return app_renderer.render_page('error_400', message="Preço e quantidade devem ser números.")
        
        description = category

        try:
            self.__products.add_product(name=name, price=price, stock=stock, description=description)
        except Exception as e:
            return app_renderer.render_page('error_500', message=f"Erro ao adicionar produto: {str(e)}")
        return redirect('/stock')

    @route('/products/edit/<product_id:int>', method=['GET', 'POST'])
    def edit_product(self, product_id):
        product = self.__products.get_product_by_id(product_id)
        if not product:
            return app_renderer.render_page('error_404', message="Produto não encontrado.")

        if request.method == 'POST':
            product.name = request.forms.get('name')
            product.description = request.forms.get('category') 
            try:
                product.price = float(request.forms.get('price'))
                product.stock = int(request.forms.get('stock'))
            except ValueError:
                return app_renderer.render_page('error_400', message="Preço e quantidade devem ser números.")
            
            product = self.__products.update_product(
            product_id=product.id,
            description=product.description,
            price=product.price,
            stock=product.stock
            )
            return redirect('/stock')
        return redirect('/stock')

    @route('/products/delete/<product_id:int>', method=['POST'])
    @admin_required
    def delete_product(self, product_id):
        self.__products.delete_product(product_id)
        return redirect('/stock')
    
    @route('/products/add_stock/<product_id:int>', method='POST')
    @admin_required
    def add_stock(self, product_id):
        quantity = int(request.forms.get('quantity') or 0)
        product = self.__products.get_product_by_id(product_id)
        if product:
            new_stock = product.stock + quantity
            self.__products.update_product(product_id=product.id, name=product.name, description=product.description, price=product.price, stock=new_stock)
        return redirect('/stock')


    @route('/products/remove_stock/<product_id:int>', method='POST')
    def remove_stock(self, product_id):
        quantity = int(request.forms.get('quantity') or 0)
        product = self.__products.get_product_by_id(product_id)
        if product:
            new_stock = max(product.stock - quantity, 0)
            self.__products.update_product(product_id=product.id, name=product.name, description=product.description, price=product.price, stock=new_stock)
        return redirect('/stock')
    
    
