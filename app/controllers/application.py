from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'login': self.login,
            'criar_conta': self.criar_conta,
            'helper': self.helper
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/index.html',)
    
    def login(self):
        return template('app/views/login.tpl',)
    
    def criar_conta(self):
        return template('app/views/criar_conta.tpl',)
    

