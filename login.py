# login.py

import streamlit as st
import datetime

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 1},
    "user3": {"password": "password3", "profile": 3}
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now()
            st.session_state.user_profile = valid_users[username]["profile"]  # Store user profile
        else:
            st.error("Credenciais inválidas.")

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("login_time", None)
    st.session_state.pop("user_profile", None)  # Clear user profile on logout
