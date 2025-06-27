from app.models.user import User, AdminUser
import json, uuid


class UserRecord():

    def __init__(self):
        self.__all_users = {'user_accounts': [], 'admin_accounts': []}
        self.__authenticated_users = {}
        self.read('user_accounts')
        self.read('admin_accounts')

    def read(self, database):
        account_class = AdminUser if (database == 'admin_accounts') else User
        try:
            with open(f"app/controllers/db/{database}.json", "r") as fjson:
                user_data = json.load(fjson)
                self.__all_users[database] = [account_class(**user) for user in user_data]
        except FileNotFoundError:
            if database == 'user_accounts':
                self.__all_users[database].append(account_class(0,'GuestUser', '000000', 'a@gmail.com'))
            else:
                self.__all_users[database].append(account_class(0,'AdminUser', '000000', 'admin@gmail.com', permissions=['admin']))

    def __write(self, database):
        try:
            with open(f"app/controllers/db/{database}.json", "w") as fjson:
                user_data=[vars(user) for user in self.__all_users[database]]
                json.dump(user_data, fjson)
                print(f'Arquivo gravado (Usuário)')
        except FileNotFoundError:
            print('Não gravou o arquivo (Usuário)')

    def setUser(self, user_id, username, password, email=None, permissions=None):
        for account_type in ['user_accounts', 'admin_accounts']:
            for user in self.__all_users[account_type]:
                if user_id == user.id:
                    user.password= password
                    user.email = email
                    user.permissions = permissions
                    print(f'O usuário {username} foi editado com sucesso.')
                    self.__write(account_type)
                    return username
        print('O método setUser foi chamado, porém sem sucesso.')
        return None

    def removeUser(self, user):
        for account_type in ['user_accounts', 'admin_accounts']:
            if user in self.__all_users[account_type]:
                print(f'O usuário {"(admin) " if account_type == "admin_accounts" else ""}{user.username} foi encontrado no cadastro.')
                self.__all_users[account_type].remove(user)
                print(f'O usuário {"(admin) " if account_type == "admin_accounts" else ""}{user.username} foi removido do cadastro.')
                self.__write(account_type)
                return user.username
        print(f'O usuário {user.username} não foi identificado!')
        return None
    
    def book(self, username, password, email=None, permissions=None):
        account_type = 'admin_accounts' if permissions else 'user_accounts'
        account_class = AdminUser if permissions else User
        new_user = account_class \
        (len(self.__all_users[account_type]) + 1, username, password, email, permissions) \
            if permissions else account_class \
            (len(self.__all_users[account_type]) + 1, username, password, email)
        self.__all_users[account_type].append(new_user)
        self.__write(account_type)
        return new_user.username

    def getUserAccount(self):
        return self.__all_users['user_accounts']
    
    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None
        
    def getUserByUsername(self, username):
        for account_type in ['user_accounts', 'admin_accounts']:
            for user in self.__all_users[account_type]:
                if user.username == username:
                    return user
        return None

    def getAutenticatedUsers(self):
        return self.__authenticated_users

    def checkUser(self, username, password):
        for account_type in ['user_accounts', 'admin_accounts']:
            for user in self.__all_users[account_type]:
                if username == user.username and password == user.password:
                    session_id = str(uuid.uuid4())
                    self.__authenticated_users[username] = user
                    print(f'O usuário {username} foi autenticado com sucesso.')
                    return session_id
        print('Usuário ou senha inválidos!')
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    def update_users_list(self):
        self.read('user_accounts')
        self.read('admin_accounts')
