import streamlit as st
import datetime

valid_users = {
    "lsilveira": {"senha": "senha123", "perfil": 1},
    "lamaral": {"senha": "lamaral23", "perfil": 2}
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["senha"] == password:
            perfil_usuario = valid_users[username]["perfil"]
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.perfil_usuario = perfil_usuario
            st.session_state.login_time = datetime.datetime.now()
        else:
            st.error("Credenciais inválidas.")

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("perfil_usuario", None)
    st.session_state.pop("login_time", None)
