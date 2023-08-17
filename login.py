import streamlit as st
from streamlit.components.v1 import components

# Dicionário de usuários (você pode substituir isso por um banco de dados real)
users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

# Função para fazer o login
def login():
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        if username in users and users[username] == password:
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")

    return False

# Função para exibir o conteúdo da página após o login
def show_content():
    st.title("Conteúdo Restrito")
    st.write("Bem-vindo à página de conteúdo restrito.")
