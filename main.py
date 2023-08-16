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
    st.session_state.sync()  # Sincroniza o estado da sessão
    if not st.session_state.is_logged_in:
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.button("Entrar")

        if login_button:
            # Faça a validação do login aqui
            # Se as credenciais estiverem corretas, defina is_logged_in como True
            if username == "usuario" and password == "senha":
                st.session_state.is_logged_in = True
            else:
                st.error("Credenciais inválidas")

def main():
    login()

    if st.session_state.is_logged_in:
        app.run()

if __name__ == "__main__":
    app = MultiApp()
    app.add_app("Conta", test.app)  # Substitua test.app pela função apropriada do seu aplicativo
    
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=230", use_column_width=True)
    main()

