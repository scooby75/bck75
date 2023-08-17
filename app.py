import streamlit as st
from streamlit_multiselect import MultiApp
from pages import login, page1, page2, page3

# Crie uma instância do MultiApp
app = MultiApp()

# Adicione as páginas ao MultiApp
app.add_app("Login", login.app)
app.add_app("Página 1", page1.app)
app.add_app("Página 2", page2.app)
app.add_app("Página 3", page3.app)

# Execute o MultiApp
app.run()

