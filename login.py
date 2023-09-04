# login.py
import streamlit as st
import datetime
from session_state import get_or_create_session_state

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 3},
    "blamim": {"password": "lamim23", "profile": 3},
    "mrodrigues": {"password": "mrodrigues23", "profile": 3},
    "user3": {"password": "password3", "profile": 3}
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    
    # Add information message with a clickable link
    st.markdown("Informações sobre acesso, [clique aqui](https://t.me/Lyssandro).")
    
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            session_state = get_or_create_session_state()
            session_state.logged_in = True
            session_state.username = username
            session_state.login_time = datetime.datetime.now()
            session_state.user_profile = valid_users[username]["profile"]  # Store user profile
        else:
            st.error("Credenciais inválidas.")

def logout():
    session_state = get_or_create_session_state()
    session_state.logged_in = False
    session_state.pop("username", None)
    session_state.pop("login_time", None)
    session_state.pop("user_profile", None)  # Clear user profile on logout
