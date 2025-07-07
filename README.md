# ProjetoFinalFeira

## DIAGRAMA E RELAÇÕES UML
*Relações UML*
**Relações de Herança**
User e AdminUser:

AdminUser herda de User.

AdminUser é uma especialização de User, adicionando uma propriedade permissions e sobrescrevendo o método is_admin para retornar True.

**Relações de Associação**
Application e Classes de View (HTML templates):

A classe Application contêm métodos como render_page e login que "usam" os seus arquivos HTML correspondentes. Embora não seja uma associação direta entre classes em Python, é uma associação forte na arquitetura do sistema.

UserController e UserRecord:

UserController "tem um" uma instância de UserRecord.(self.__users = UserRecord()) no método __init__ de UserController.

UserController utiliza métodos de UserRecord para gerenciar usuários (login, registro, busca por email/username, etc.).

UserRecord e User/AdminUser:

*DIAGRAMA UML*
![Diagrama de classes](![alt text](image.png))