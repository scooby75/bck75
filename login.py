# login.py
import streamlit as st
import jwt
import datetime
import requests

# URL do arquivo secreto no GitHub
SECRET_KEY_URL = "https://raw.githubusercontent.com/scooby75/bck75/main/secret_key.txt"

# Faça uma solicitação HTTP para obter a chave secreta
response = requests.get(SECRET_KEY_URL)

if response.status_code == 200:
    SECRET_KEY = response.text.strip()  # Lê o conteúdo da resposta
else:
    st.error("Erro ao obter a chave secreta do GitHub")

# Dicionário de usuários (substitua por um banco de dados em produção)
users = {
    "lsilveira": "senha123",
    "usuario3": "senha3"
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
    stored_password = users.get(username)
    return stored_password == password

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

            # Guarde o token em algum lugar seguro (por exemplo, em um cookie ou em uma variável de sessão)
            st.write(f"Token JWT: {token}")

# Main application
if __name__ == "__main__":
    login_page()
