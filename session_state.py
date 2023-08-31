import streamlit as st

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Função para obter ou criar o estado da sessão
def get_or_create_session_state():
    if not hasattr(st, "session_state"):
        st.session_state = SessionState()
    return st.session_state
