import streamlit as st

def content_page(user):
    st.title("Página de Conteúdo")
    
    if user is not None:
        st.write("Este é o conteúdo da página após o login.")
    else:
        st.warning("Você não está autenticado. Faça login para ver o conteúdo.")
