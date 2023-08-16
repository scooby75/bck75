import streamlit as st
from streamlit_option_menu import option_menu
import trending, test, your, about

st.set_page_config(
    page_title="Football Data Analysis",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app_names = [app["title"] for app in self.apps]
        active_app = st.selectbox("Selecione uma página:", app_names)

        for app in self.apps:
            if active_app == app["title"]:
                app["function"]()  # Chama a função do aplicativo correspondente

def login():
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        # Faça a validação do login aqui
        # Se as credenciais estiverem corretas, mostre o seletor de página
        if username == "usuario" and password == "senha":
            app.run()
        else:
            st.error("Credenciais inválidas")

def main():
    login()

if __name__ == "__main__":
    main()
