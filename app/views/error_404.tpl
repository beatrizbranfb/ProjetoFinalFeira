<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venda Online</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/">Início</a>
            % if defined('user_id') and user_id:
                <a href="/cart">Carrinho</a>
                % if defined('user_role') and user_role == 'employee':
                    <a href="/products/add">Adicionar Produto</a>
                % end
                <a href="/logout">Sair</a>
            % else:
                <a href="/login">Login</a>
                <a href="/register">Registrar</a>
            % end
        </nav>
    </header>
        <div class="container">
            % if defined('error') and error:
                <p class="error">{{error}}</p>
            % end
            {{!base}}
        </div>
</body>
</html>
    <h1>Página Não Encontrada (404)</h1>
<p>{{message if defined('message') else 'A página que você solicitou não foi encontrada.'}}</p>
<p><a href="/">Voltar para a página inicial</a></p>