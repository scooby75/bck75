import streamlit as st
from firebase_setup import initialize_firebase

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    auth = initialize_firebase()

    if st.button("Entrar"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login bem-sucedido!")
            return user
        except Exception as e:
            st.error("Erro no login. Verifique suas credenciais.")
            st.write(e)
    return None

