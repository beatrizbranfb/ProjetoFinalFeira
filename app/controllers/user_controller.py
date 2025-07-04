from app.controllers.userRecord import UserRecord
from bottle import request, redirect, route
from app.controllers.application import app_renderer

# Decorador para rotas que precisem de login
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

# Decorador para rotas que precisem de um usuário administrador
def admin_required(func):
    def wrapper(*args, **kwargs):
        if request.session.get('role') == 'admin':
            return func(*args, **kwargs)
        else:
            print("Acesso negado: usuário não é um administrador.")
            return redirect('/login')
    return wrapper

class UserController:

    def __init__(self):
        self.__users = UserRecord()
        self.pages = {
            'login': self.login,
            'register': self.register,
            'logout': self.logout
        }

    def is_logged_in(self):
        return 'user_id' in request.session

    def get_user_role(self):
        return request.session.get('role')

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            email = request.forms.get('email')
            password = request.forms.get('password')

            user = self.__users.getUserByEmail(email)
            if user:
                if user.password == password:
                    request.session['user_id'] = user.id
                    request.session['role'] = user.role
                    if user.role == 'admin':
                        return redirect('/administrador')
                    else:
                        return redirect('/products')
                else:
                    return app_renderer.render_page('login.html', error='Usuário ou senha inválidos.')
            else:
                return app_renderer.render_page('login.html', error="Usuário ou senha inválidos.")
        return app_renderer.render_page('login.html', error=None)

    @route('/register', methods=['GET', 'POST'])
    def register(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            confirm_password = request.forms.get('confirm_password')
            email = request.forms.get('email')

            if password != confirm_password:
                return app_renderer.render_page('criar_conta.html', error="As senhas não correspondem.")
            if self.__users.getUserByUsername(username):
                return app_renderer.render_page('criar_conta.html', error="Nome de usuário já existe.")
            if not username or not password or not email:
                return app_renderer.render_page('criar_conta.html', error="Todos os campos são obrigatórios.")

            self.__users.book(username=username, password=password, email=email)
            return redirect('/login')
        return app_renderer.render_page('criar_conta.html', error=None)

    @route('/logout')
    def logout(self):
        request.session.clear()
        return redirect('/login')

    @route('/administrador')
    @admin_required
    def admin_dashboard(self):
        return app_renderer.render_page('administrador_dashboard.html')

ctl = UserController()