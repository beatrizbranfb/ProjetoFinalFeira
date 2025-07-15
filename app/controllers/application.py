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
    
    def products(self):
        return template('app/views/cliente_produto.html')


app_renderer = Application()
