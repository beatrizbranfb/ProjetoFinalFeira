from bottle import template, request

class Application:
    def __init__(self):
        pass

    def render_page(self, template_name, **kwargs):
        kwargs['user_id'] = request.session.get('user_id')
        kwargs['user_role'] = request.session.get('role')
        return template(template_name, **kwargs)

app_renderer = Application()
