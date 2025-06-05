<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feira Login</title>
    <style>
        * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    background: linear-gradient(135deg, #d0ebff, #f0faff);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    background: #ffffffcc;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    max-width: 400px;
    width: 90%;
}

header h1 {
    color: #1e3a8a;
    font-size: 2em;
    margin-bottom: 10px;
}

header p {
    color: #3b82f6;
    margin-bottom: 20px;
}


.buttons .btn {
    display: block;
    text-decoration: none;
    margin: 10px 0;
    padding: 12px 0;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.3s ease;
}

.btn {
    background: #3b82f6;
    color: #fff;
}

.btn:hover {
    background: #2563eb;
}

.btn.outline {
    background: transparent;
    color: #3b82f6;
    border: 2px solid #3b82f6;
}

.btn.outline:hover {
    background: #3b82f6;
    color: #fff;
}

    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Bem-vindo à Feira</h1>
            <p>Por favor, faça login ou crie uma conta.</p>
        </header>

        <div class="buttons">
            <a href="#" class="btn">Entrar</a>
            <a href="#" class="btn outline">Criar Conta</a>
        </div>
    </div>
</body>
</html>