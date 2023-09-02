import streamlit as st

class SessionState:
    def __init__(self):
        self.logged_in = False
        self.username = None
        self.user_profile = 1

def get_or_create_session_state():
    if not hasattr(st, 'session_state'):
        st.session_state = SessionState()
    return st.session_state
