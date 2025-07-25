from app.controllers.userRecord import UserRecord
from app.controllers.cartRecord import CartRecord
import json
import os
from datetime import datetime
from bottle import request, redirect, route, post, template
from app.controllers.application import app_renderer
from datetime import datetime

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
        self.__orders = CartRecord()
        self.pages = {
            'login': self.login,
            'register': self.register,
            'logout': self.logout,
            'profile': self.profile,
            'admin_dashboard': self.admin_dashboard,
            'admin_clientes': self.admin_clientes,
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
        all_orders = self.__orders.get_all_orders()
        all_users = self.__users.getUserAccount()
        user_map = {user.id: user.username for user in all_users}
        
        total_sales = sum(
            order.total_amount for order in all_orders if order.status == "completed"
        )

        pending_orders_count = sum(
            1 for order in all_orders if order.status == "pending"
        )

        new_clients_count = sum(
            1 for user in all_users if user.id > len(all_users) - 5
        )

        recent_sales_orders = sorted(all_orders, key=lambda o: o.order_date, reverse=True)[:5]
        recent_sales = [
            {
                'id': order.id,
                'customer_name': user_map.get(order.user_id, 'Desconhecido'),
                'date': order.order_date.strftime('%d/%m/%Y'),
                'value': order.total_amount,
                'status': order.status
            }
            for order in recent_sales_orders
        ]

        return app_renderer.render_page(
            "administrador_dashboard.html",
            total_sales=total_sales,
            new_clients_count=new_clients_count,
            pending_orders_count=pending_orders_count,
            recent_sales=recent_sales
        )

    @route('/admin_clientes')
    @admin_required
    def admin_clientes(self):
        all_users = self.__users.getUserAccount()
        all_orders = self.__orders.get_all_orders()

        user_map = {user.id: user for user in all_users}

        clients = []
        for order in all_orders:
            user = user_map.get(order.user_id)
            if not user:
                continue

            days_pending = "?"
            if order.status == 'pending':
                days_pending = (datetime.now() - order.order_date).days

            clients.append({
                "username": user.username,
                "email": user.email,
                "phone": getattr(user, "phone", "(61) 9XXXX-XXXX"),
                "address": getattr(user, "address", "Endereço não informado"),
                "order_id": order.id,
                "order_date": order.order_date.strftime("%d/%m/%Y"),
                "order_value": order.total_amount,
                "status": order.status,
                "days_pending": days_pending
            })

        return app_renderer.render_page("administrador_clientes.html", clients=clients)

    @route('/acesso_neg')
    def acesso_neg(self):
        return app_renderer.render_page('acesso_neg.html')

    @admin_required
    def update_user(self):
        user_id = request.get_cookie("user_id") 
        name = request.forms.get("name")
        email = request.forms.get("email")
        phone = request.forms.get("phone")
        address = request.forms.get("address")

        user_record = UserRecord()
        user = user_record.getUserByEmail(email)
        if user:
            user.name = name
            user.email = email
            user.phone = phone
            user.address = address
            user_record.update_users_list()

        redirect("/account")

    @route('/admin_clientes')
    @admin_required
    def admin_clientes(self):
        cart_record = CartRecord()
        user_record = UserRecord()

        all_orders = cart_record.get_all_orders()  

        query = request.query.q.strip().lower() if request.query.q else ''
        status_filter = request.query.status
        sort = request.query.sort

        clients = []

        for order in all_orders:
            if order.status in ['pending', 'delayed', 'processing']:
                user = user_record.get_user_by_id(order.user_id)
                if user:
                    client_data = {
                        'username': user.username,
                        'email': user.email,
                        'phone': user.phone,
                        'address': user.address,
                        'order_id': order.id,
                        'order_date': order.date,
                        'order_value': order.total,
                        'status': order.status,
                        'days_pending': (datetime.now() - datetime.strptime(order.date, '%Y-%m-%d')).days
                    }

                    if query and query not in client_data["username"].lower():
                        continue

                    if status_filter and client_data["status"] != status_filter:
                        continue

                    clients.append(client_data)

        if sort == "date":
            clients.sort(key=lambda x: x["order_date"])
        elif sort == "name":
            clients.sort(key=lambda x: x["username"].lower())
        elif sort == "value":
            clients.sort(key=lambda x: x["order_value"], reverse=True)

        return app_renderer.render_page(
            "administrador_clientes.html",
            clients=clients,
            request=request
        )




ctl = UserController()