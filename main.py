import streamlit as st
from streamlit_option_menu import option_menu
from login import app as login_app
from cs import app as cs_app
from tips import app as tips_app

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

    @staticmethod
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Football Data Analysis ',
                options=['Conta', 'CS', 'Tips'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "Conta":
            login_app()
        if app == "CS":
            cs_app()
        if app == "Tips":
            tips_app()

# Criar uma instância de MultiApp
multi_app = MultiApp()

# Adicionar os aplicativos à instância
multi_app.add_app("Conta", login_app)
multi_app.add_app("CS", cs_app)
multi_app.add_app("Tips", tips_app)

# Executar o aplicativo selecionado
multi_app.run()

         


