import streamlit as st
from firebase_setup import auth

def is_authenticated(user):
    return user is not None

def content_page(user):
    st.title("Página de Conteúdo")
    
    if is_authenticated(user):
        st.write("Este é o conteúdo da página após o login.")
    else:
        st.warning("Você não está autenticado. Faça login para ver