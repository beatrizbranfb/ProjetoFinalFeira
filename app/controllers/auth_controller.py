from app.models.user import User
from bottle import request, redirect, route, template, auth_basic


def check_auth(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        request.session['user'] = user.id
        request.session['role'] = user.role
        return True
    return False


@route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        user = User.find_by_username(username)
        if user and user.password == password:
            request.session['user'] = user.id
            request.session['role'] = user.role
            redirect('/')
        else:
            return template('auth/login', error='Invalid username or password')
    return template('auth/login', error=None)

@route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        email = request.forms.get('email')

        if User.find_by_username(username):
            return template('auth/register', error="Nome de usuário já existe.")
        if not username or not password or not email:
            return template('auth/register', error="Todos os campos são obrigatórios.")
        
        User.create(username=username, password=password, email=email)
        redirect('/login')
    return template('auth/register', error=None)

@route('/logout')
def logout():
    request.session.clear()
    redirect('/login')

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
            redirect('/') # Ou uma página de acesso negado
        return func(*args, **kwargs)
    return wrapper
