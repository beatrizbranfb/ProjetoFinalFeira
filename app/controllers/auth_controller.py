from app.models.user import User
from bottle import request, redirect, route, auth_basic
from app.controllers.application import app_renderer


def check_auth(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        request.session['user'] = user.id
        request.session['role'] = user.role
        return True
    return False

def is_logged_in():
    return 'user_id' in request.session

def get_user_role():
    return request.session.get('role')

# Decorador para rotas que precisem de login
def login_required(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            redirect('/login')
        return func(*args, **kwargs)
    return wrapper

# Decorador para rotas que precisem de um usuário funcionário
def employee_required(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            redirect('/login')
        if get_user_role() != 'employee':
            redirect('/')
        return func(*args, **kwargs)
    return wrapper

@route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')

        user = User.find_by_username(username)
        if user:
            if user.password == password:
                request.session['user'] = user.id
                request.session['role'] = user.role
                redirect('/')
            else:
                return app_renderer.render_page('pagina de login.tpl', error='Usuário ou senha inválidos.')
        else:
            return app_renderer.render_page('pagina de login.tpl', error="Usuário ou senha inválidos.")
    return app_renderer.render_page('pagina de login.tpl', error=None)

@route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        email = request.forms.get('email')

        if User.find_by_username(username):
            return app_renderer.render_page('pagina de registro.tpl', error="Nome de usuário já existe.")
        if not username or not password or not email:
            return app_renderer.render_page('pagina de registro.tpl', error="Todos os campos são obrigatórios.")
        
        User.create(username=username, password=password, email=email)
        redirect('/login')
    return app_renderer.render_page('pagina de registro.tpl', error=None)

@route('/logout')
def logout():
    request.session.clear()
    redirect('/login')
