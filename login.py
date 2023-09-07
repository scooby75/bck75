# login.py

import streamlit as st
import datetime
from session_state import get_or_create_session_state

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 1},
    "blamim": {"password": "lamim23", "profile": 1},
    "mrodrigues": {"password": "mrodrigues23", "profile": 3},
    "alexbadcarrel": {"password": "Badminton76", "profile": 3},
    "Ellwanger": {"password": "21ellwanger", "profile": 3}, 
    "bulquinha": {"password": "evrr1111", "profile": 1}, 
    "rafaelmax": {"password": "19cYqCqu!OpO", "profile": 1}, 
    "Eanes": {"password": "Eanes@Analysis", "profile": 2}, 
    "wagnercw": {"password": "G28M1V97@", "profile": 1}, 
    "bjales": {"password": "kisso1cc", "profile": 3}, 
    "DANIELSATOS": {"password": "140751@Ju", "profile": 3}, 
    "mmoren0": {"password": "mmoren23", "profile": 3}, 
    "gblbet": {"password": "gblbet23", "profile": 2} 
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Análise de Dados de Futebol")
    
    # Adicione uma mensagem de informação com um link clicável e ícone "info-circle-fill"
    st.markdown('<i class="bi bi-info-circle-fill"></i> Informações sobre acesso, [clique aqui](https://t.me/Lyssandro).', unsafe_allow_html=True)
    
    username = st.text_input("Usuário")  # Sem chave personalizada
    password = st.text_input("Senha", type="password")  # Sem chave personalizada

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            session_state = get_or_create_session_state()
            session_state.logged_in = True
            session_state.username = username
            session_state.login_time = datetime.datetime.now()
            session_state.user_profile = valid_users[username]["profile"]  # Armazena o perfil do usuário
        else:
            st.error("Credenciais inválidas.")

def logout():
    session_state = get_or_create_session_state()
    session_state.logged_in = False
    session_state.pop("username", None)
    session_state.pop("login_time", None)
    session_state.pop("user_profile", None)  # Limpa o perfil do usuário ao fazer logout

# Execute a função para criar a página de login
login_page()
