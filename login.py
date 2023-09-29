# login.py

import streamlit as st
import datetime
from session_state import get_or_create_session_state
from user_data import valid_users  # Importe os dados dos usuários

@st.cache_resource
def initialize_session_state():
    return get_or_create_session_state()

def login_page():
    session_state = initialize_session_state()  # Inicializa o session_state
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    
    # Adicione uma mensagem de informação com um link clicável e ícone "info-circle-fill"
    st.markdown('<i class="bi bi-info-circle-fill"></i> Informações sobre acesso, [clique aqui](https://t.me/Lyssandro).', unsafe_allow_html=True)
    
    username = st.text_input("Usuário")  # Sem chave personalizada
    password = st.text_input("Senha", type="password")  # Sem chave personalizada

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            session_state.logged_in = True
            session_state.username = username
            session_state.login_time = datetime.datetime.now()
            session_state.user_profile = valid_users[username]["profile"]  # Armazena o perfil do usuário
        else:
            st.error("Credenciais inválidas.")

def logout():
    session_state = initialize_session_state()  # Inicializa o session_state
    session_state.logged_in = False
    session_state.pop("username", None)
    session_state.pop("login_time", None)
    session_state.pop("user_profile", None)  # Limpa o perfil do usuário ao fazer logout

# Execute a função para criar a página de login
login_page()
