from bottle import template, request


class Application:

    def render_page(self, template_name, **kwargs):
        kwargs['user_id'] = request.session.get('user_id')
        kwargs['is_admin'] = request.session.get('role') == 'admin'
        return template(template_name, **kwargs)

    def __init__(self):
        self.pages = {
        }

    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()

    def helper(self):
        return template('app/views/index.html')
    
    # def login(self):
    #     return template('app/views/login.html')

    # def register(self):
    #     return template('app/views/criar_conta.html')

    # def cart(self):
    #     return template('app/views/cliente_carrinho.html')
    
    def products(self):
        return template('app/views/cliente_produto.html')
    
    # def profile(self):
    #     return template('app/views/cliente_perfil.html')
    
    # def orders(self):
    #     return template('app/views/cliente_pedidos.html')
    
    # def administrador(self):
    #     return template('app/views/administrador_dashboard.html')
    
    

    



app_renderer = Application()
