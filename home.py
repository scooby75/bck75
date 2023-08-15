import streamlit as st
from login_page import login_page
from content_page import content_page
from firebase_setup import initialize_firebase

st.set_page_config(page_title="App com Streamlit e Firebase")

# Inicializa a autenticação do Firebase
auth = initialize_firebase()

# Página de Login
if not st.session_state.logged_in:
    login_page()
    
# Páginas de Conteúdo
else:
    content_page()

