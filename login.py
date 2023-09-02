# login.py
import streamlit as st
from session_state import get_or_create_session_state
from streamlit.server.server import Server
import secure

# Função para verificar se um usuário já está logado em outra sessão
def is_user_already_logged_in(username):
    all_sessions = secure.SecureCookie.load_all_sessions()
    for session in all_sessions.values():
        if "username" in session and session["username"] == username:
            return True
    return False

def set_user_cookie(username):
    session_id = Server.get_current()._session_info.session_id
    st.experimental_set_query_params(username=username, session_id=session_id)

def get_user_cookie():
    session_id = Server.get_current()._session_info.session_id
    query_params = st.experimental_get_query_params()
    return query_params.get("username")

# Lista de pares de usuário e senha válidos
valid_users = [
    {"username": "lsilveira", "password": "senha123"},
    {"username": "usuario2", "password": "senha2"},
    # Adicione mais pares de usuário e senha conforme necessário
]

def login_page():
    session_state = get_or_create_session_state()

    if session_state.logged_in:
        st.success(f"Você já está logado como {session_state.username}!")
    else:
        st.title("Login")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")

        with st.form(key="login_form"):
            st.write("Digite sua senha com segurança:")
            st.write(f'<input type="password" name="password" value="{password}" placeholder="Senha">')
            submitted = st.form_submit_button("Entrar")

        if submitted:
            # Verifique se o usuário já está logado em outra sessão
            if is_user_already_logged_in(username):
                st.error("Você já está logado em outra sessão. Faça logout antes de fazer login novamente.")
                return

            # Verifique as credenciais fornecidas com os pares válidos
            if check_credentials(username, password):
                session_state.logged_in = True
                session_state.username = username
                set_user_cookie(username)
                st.success(f"Bem-vindo, {username}!")
            else:
                st.error("Nome de usuário ou senha incorretos.")

def check_credentials(username, password):
    for user in valid_users:
        if username == user["username"] and password == user["password"]:
            return True
    return False

def logout():
    session_state = get_or_create_session_state()
    session_state.logged_in = False
    session_state.username = None
    set_user_cookie("")  # Limpa o cookie de nome de usuário
    st.info("Você foi desconectado com sucesso.")
