from app.controllers.userRecord import UserRecord, AdminUser
from bottle import request, redirect, route, template
from app.controllers.application import app_renderer

class UserController:

    def __init__(self):
        self.__users = UserRecord()
        self.pages = {
            'login': self.login,
            'register': self.register,
            'logout': self.logout
        }

    def check_auth(self,username, password):
        user = self.__users.getUserByUsername(username)
        if user and user.password == password:
            request.session['user'] = user.id
            request.session['role'] = user.role
            return True
        return False

    def is_logged_in(self):
        return 'user_id' in request.session

    def get_user_role(self):
        if request.session.get('user'):
            return 'admin' if isinstance(request.session['user'], AdminUser) else 'user'
        return None

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            email = request.forms.get('email')
            password = request.forms.get('password')

            user = self.__users.getUserByEmail(email)
            if user:
                if user.password == password:
                    request.session['user'] = user.id
                    redirect('/products')
                else:
                    return app_renderer.render_page('login', error='Usuário ou senha inválidos.')
            else:
                return app_renderer.render_page('login', error="Usuário ou senha inválidos.")
        return app_renderer.render_page('login', error=None)

    @route('/register', methods=['GET', 'POST'])
    def register(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            confirm_password = request.forms.get('confirm_password')
            email = request.forms.get('email')

            if password != confirm_password:
                return app_renderer.render_page('/register', error="As senhas não correspondem.")
            if self.__users.getUserByUsername(username):
                return app_renderer.render_page('/register', error="Nome de usuário já existe.")
            if not username or not password or not email:
                return app_renderer.render_page('/register', error="Todos os campos são obrigatórios.")

            self.__users.book(username=username, password=password, email=email)
            redirect('/login')
        return app_renderer.render_page('/register', error=None)

    @route('/logout')
    def logout(self):
        request.session.clear()
        redirect('/login')

ctl = UserController()

# Decorador para rotas que precisem de login
def login_required(func):
    def wrapper(*args, **kwargs):
        if not ctl.is_logged_in():
            redirect('/login')
        return func(*args, **kwargs)
    return wrapper

# Decorador para rotas que precisem de um usuário administrador
def admin_required(func):
    def wrapper(*args, **kwargs):
        if ctl.get_user_role() == 'admin':
            return func(*args, **kwargs)
        else:
            print("Acesso negado: usuário não é um administrador.")
            redirect('/login')
            return None
    return wrapper