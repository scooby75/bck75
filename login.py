import streamlit as st

def app():
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        if username == "user" and password == "pass":
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

