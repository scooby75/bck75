import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

# Importe a função do arquivo cs.py
import cs

cred = credentials.Certificate("football-data-analysis-29975-firebase-adminsdk-ejqyp-bd278ebaff.json")
firebase_admin.initialize_app(cred)

def app():
    # Usernm = []
    st.title('Bem Vindo :red[Football Data Analysis]:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    # Resto do seu código de autenticação...

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

    # Chame a função ap() para exibir o seu conteúdo
    ap()

    # Chame a função show_cs_page() do módulo cs
    cs.show_cs_page()
