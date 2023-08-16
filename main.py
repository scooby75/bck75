import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Initialize Firebase
cred = credentials.Certificate("football-data-analysis-29975-firebase-adminsdk-ejqyp-bd278ebaff.json")
firebase_admin.initialize_app(cred)

# Login Function
def login_app():
    st.title('Bem Vindo :red[Football Data Analysis]:')
    
    if 'user' not in st.session_state:
        st.session_state.user = None
        
    def f():
        try:
            user = auth.get_user_by_email(email)
            st.session_state.user = user
            st.success('Login successful!')
        except:
            st.warning('Login Failed')
            
    def t():
        st.session_state.user = None
        st.session_state.signed_out = True
        
    if st.session_state.user is None:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.button('Login', on_click=f)
    else:
        st.text('Logged in as: ' + st.session_state.user.email)
        st.button('Sign Out', on_click=t)

# MultiApp Class
class MultiApp:
    def __init__(self):
        self.apps = []
        
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    @staticmethod
    def run():
        app_names = [app["title"] for app in multi_app.apps]
        with st.sidebar:
            selected_app = st.selectbox('Select Module', app_names)
        
        for app in multi_app.apps:
            if selected_app == app["title"]:
                app["function"]()

# Create instance of MultiApp
multi_app = MultiApp()

# Add apps to the instance
multi_app.add_app("Login", login_app)
multi_app.add_app("Jogos do Dia", jogos_do_dia_app)
multi_app.add_app("CS", cs_app)
multi_app.add_app("Tips", tips_app)

# Run the selected app
multi_app.run()
