import streamlit as st
import datetime

# Variável global para armazenar as informações de login
logged_in_user = None

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 1},
    "blamim": {"password": "lamim23", "profile": 3},
    "mrodrigues": {"password": "mrodrigues23", "profile": 3},
    "user3": {"password": "password3", "profile": 3}
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    global logged_in_user
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            logged_in_user = username  # Armazena o usuário logado na variável global
        else:
            st.error("Credenciais inválidas.")

def logout():
    global logged_in_user
    logged_in_user = None  # Limpa o usuário logado
