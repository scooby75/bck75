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

app = MultiApp()
app.add_app("Conta", test.app)  # Substitua test.app pela função apropriada do seu aplicativo
app.add_app("Tendências", trending.app)  # Substitua trending.app pela função apropriada do seu aplicativo
app.add_app("Suas Postagens", your.app)  # Substitua your.app pela função apropriada do seu aplicativo
app.add_app("Sobre", about.app)  # Substitua about.app pela função apropriada do seu aplicativo
app.run()
