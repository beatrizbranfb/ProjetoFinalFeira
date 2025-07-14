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
            return redirect('/acesso_neg')
    return wrapper

class UserController:

    def __init__(self):
        self.__users = UserRecord()
        self.pages = {
            'login': self.login,
            'register': self.register,
            'logout': self.logout,
            'profile': self.profile,
            'admin_dashboard': self.admin_dashboard,
            'admin_clientes': self.admin_clientes,
            'admin_stock': self.admin_stock,
            'acesso_neg': self.acesso_neg
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
                    self.__users.checkUser(user.username, user.password)
                    if request.session['role'] == 'admin':
                        request.session['permissions'] = user.permissions
                        return redirect('/admin')
                    elif request.session['role'] == 'user':
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
    
    @route('/profile')
    @login_required
    def profile(self):
        return app_renderer.render_page('cliente_perfil.html')

    @route('/admin')
    @admin_required
    def admin_dashboard(self):
        return app_renderer.render_page('administrador_dashboard.html')
    
    @route('/admin_clientes')
    @admin_required
    def admin_clientes(self):
        return app_renderer.render_page('administrador_clientes.html')

    @route('/admin_stock')
    @admin_required
    def admin_stock(self):
        return app_renderer.render_page('administrador_estoque.html')

    @route('/acesso_neg')
    def acesso_neg(self):
        return app_renderer.render_page('acesso_neg.html')

ctl = UserController()