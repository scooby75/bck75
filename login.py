import streamlit as st
import datetime

valid_users = {
    "lsilveira": "senha123",
    "usuario2": "senha456"
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now()
        else:
            st.error("Credenciais inválidas.")

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("login_time", None)
