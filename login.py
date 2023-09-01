# login.py
import streamlit as st
import jwt
import datetime

# Leitura da chave secreta a partir do arquivo
with open("https://raw.githubusercontent.com/scooby75/bck75/main/secret_key.txt", "r") as key_file:
    SECRET_KEY = key_file.read().strip()

# Dicionário de usuários (substitua por um banco de dados em produção)
users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "usuario3": {"password": "senha3", "profile": 1}
}

def create_token(username):
    # Crie um token JWT com o nome de usuário e uma data de expiração
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_credentials(username, password):
    # Verifique se o nome de usuário e a senha correspondem aos registros (substitua por um banco de dados em produção)
    if username in users and users[username]["password"] == password:
        return True
    return False

def login_page():
    st.title("Login Simples")

    if st.button("Login"):
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")

        # Verifique as credenciais do usuário
        if verify_credentials(username, password):
            # Se as credenciais estiverem corretas, crie um token JWT
            token = create_token(username)
            st.success("Login bem-sucedido!")

            # Guarde o token em algum lugar seguro (por exemplo, em um cookie ou variável global)
            return token  # Retorna o token JWT
        else:
            st.error("Credenciais inválidas. Faça login novamente.")
