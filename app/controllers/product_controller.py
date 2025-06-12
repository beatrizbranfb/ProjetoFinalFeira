from app.controllers.auth_controller import login_required, get_user_role, employee_required
from app.models.product import Product
from bottle import request, redirect, route
from app.controllers.application import app_renderer


@route('/')
@route('/products')
@login_required
def list_products():
    products = Product.get_all()
    user_role = get_user_role()
    return app_renderer.render_page('produtos/listar.tpl', products=products, user_role=user_role)

@route('/products/<product_id:int>')
@login_required
def product_details(product_id):
    product = Product.find_by_id(product_id)
    if not product:
        return app_renderer.render_page('error_404', message="Produto não encontrado.")
    return app_renderer.render_page('produtos/detalhes.tpl', product=product)

@route('/products/add', method=['GET', 'POST'])
@employee_required
def add_product():
    if request.method == 'POST':
        name = request.forms.get('name')
        description = request.forms.get('description')
        price = float(request.forms.get('price'))
        stock = int(request.forms.get('stock'))

        if not name or not price or not stock:
            return app_renderer.render_page('produtos/adicionareditar', product=None, error="Todos os campos são obrigatórios.")

        product = Product(name=name, description=description, price=price, stock=stock)
        product.create()
        redirect('/products')
    return app_renderer.render_page('produtos/adicionareditar', product=None, error=None)

@route('/products/edit/<product_id:int>', method=['GET', 'POST'])
@employee_required
def edit_product(product_id):
    product = Product.find_by_id(product_id)
    if not product:
        return app_renderer.render_page('error_404', message="Produto não encontrado.")

    if request.method == 'POST':
        product.name = request.forms.get('name')
        product.description = request.forms.get('description')
        product.price = float(request.forms.get('price'))
        product.stock = int(request.forms.get('stock'))
        product.save()
        redirect('/products')
    return app_renderer.render_page('produtos/adicionareditar', product=product, error=None)

@route('/products/delete/<product_id:int>', method=['POST'])
@employee_required
def delete_product(product_id):
    product = Product.find_by_id(product_id)
    if product:
        product.delete()
    redirect('/products')
