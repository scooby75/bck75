import streamlit as st

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

