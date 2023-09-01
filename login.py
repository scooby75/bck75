# login.py
import streamlit as st
import datetime
from session_state import get_or_create_session_state

# Initialize session state
session_state = get_or_create_session_state()

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 1},
    "blamim": {"password": "lamim23", "profile": 3},
    "mrodrigues": {"password": "mrodrigues23", "profile": 3},
    "user3": {"password": "password3", "profile": 3}
}

def perform_login(username, password):
    if username in valid_users and valid_users[username]["password"] == password:
        session_state.login_successful = True
        session_state.username = username
        session_state.login_time = datetime.datetime.now()
        session_state.user_profile = valid_users[username]["profile"]
        return True
    else:
        return False

def perform_logout():
    session_state.login_successful = False
    session_state.username = None
    session_state.login_time = None
    session_state.user_profile = None

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
    st.title("Análise de Dados de Futebol")

    if session_state.login_successful:
        st.success(f"Bem-vindo, {session_state.username}! | Perfil: {session_state.user_profile}")
        logout_button = st.button("Sair")
        if logout_button:
            perform_logout()
    else:
        with st.form("formulario_login"):
            # Mova a criação do widget 'username' para cima da atribuição do 'username'
            username = st.text_input("Usuário", key="username", help="Digite seu nome de usuário", **{"autocomplete": "username"})
            password = st.text_input("Senha", type="password", key="password", help="Digite sua senha", **{"autocomplete": "current-password"})
            
            # Agora, você pode atribuir 'username' a 'session_state' antes do widget ser criado
            session_state.username = username

            login_button = st.form_submit_button("Entrar")

            if login_button:
                if perform_login(username, password):
                    st.success(f"Bem-vindo, {username}!")
                else:
                    st.error("Falha ao fazer login. Verifique seu nome de usuário e senha.")

# Main application
if __name__ == "__main__":
    login_page()
