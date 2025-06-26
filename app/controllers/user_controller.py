from app.controllers.userRecord import UserRecord, AdminUser
from bottle import request, redirect, route
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
            username = request.forms.get('username')
            password = request.forms.get('password')

            user = self.__users.getUserByUsername(username)
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
    def register(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            email = request.forms.get('email')

            if self.__users.getUserByUsername(username):
                return app_renderer.render_page('pagina de registro.tpl', error="Nome de usuário já existe.")
            if not username or not password or not email:
                return app_renderer.render_page('pagina de registro.tpl', error="Todos os campos são obrigatórios.")

            self.__users.book(username=username, password=password, email=email)
            redirect('/login')
        return app_renderer.render_page('pagina de registro.tpl', error=None)

    @route('/logout')
    def logout(self):
        request.session.clear()
        redirect('/login')


    # Decorador para rotas que precisem de login
    def login_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.is_logged_in():
                redirect('/login')
            return func(*args, **kwargs)
        return wrapper

    # Decorador para rotas que precisem de um usuário administrador
    def admin_required(self, func):
        def wrapper(*args, **kwargs):
            if self.get_user_role() == 'admin':
                return func(*args, **kwargs)
            else:
                print("Acesso negado: usuário não é um administrador.")
                redirect('/login')
                return None
        return wrapper