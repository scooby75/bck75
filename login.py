import streamlit as st

# Dicionário de usuários (você pode substituir isso por um banco de dados real)
users = {
    'lsilveira': '123456',
    'user2': 'password2',
    'user3': 'password3'
}

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
