<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Criar Conta - Feira</title>
  <style>
    body {
      background: linear-gradient(135deg, #d0ebff, #f0faff);
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .signup-container {
      background-color: #ffffffcc;
      padding: 40px;
      border-radius: 20px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      max-width: 400px;
      width: 90%;
      text-align: center;
    }

    h2 {
      color: #1e3a8a;
      margin-bottom: 20px;
    }

    input {
      width: 100%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 8px;
    }

    .btn {
      background-color: #3b82f6;
      color: white;
      padding: 12px;
      border: none;
      width: 100%;
      border-radius: 8px;
      font-weight: bold;
      cursor: pointer;
      margin-top: 10px;
    }

    .btn:hover {
      background-color: #2563eb;
    }

    a {
      display: block;
      margin-top: 15px;
      color: #3b82f6;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="signup-container">
    <h2>Criar Conta na Feira</h2>
    <form>
      <input type="text" placeholder="Nome completo" required />
      <input type="email" placeholder="E-mail" required />
      <input type="password" placeholder="Senha" required />
      <input type="password" placeholder="Confirmar senha" required />
      <button type="submit" class="btn">Cadastrar</button>
    </form>
    <a href="/login">Já tem uma conta? Entrar</a>
  </div>
</body>
</html>
