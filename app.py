import streamlit as st
import datetime
from SessionState import SessionState  # Importa a biblioteca SessionState

# Dados de exemplo para simular o login (substitua por um mecanismo seguro em um ambiente de produção)
valid_users = {
    "lsilveira": "senha123",
    "usuario2": "senha456"
}

def login_page(session):
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=280)
    st.title("Football Data Analysis")
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")  # Criar botão de login

    if login_button:  # Verificar se o botão foi clicado
        if username in valid_users and valid_users[username] == password:
            session.logged_in = True
            session.username = username  # Armazena o nome de usuário
            session.login_time = datetime.datetime.now()
        else:
            st.error("Credenciais inválidas.")

def jogos_do_dia_page():
    st.title("Jogos do Dia")
    # Coloque aqui a lógica e o conteúdo da página de jogos do dia

def cs_page():
    st.title("CS")
    # Coloque aqui a lógica e o conteúdo da página de CS

def tips_page():
    st.title("Tips")
    # Coloque aqui a lógica e o conteúdo da página de Tips

def main():
    st.set_page_config(page_title="Football Data Analysis", layout="wide")
    session_state = SessionState.get(logged_in=False)  # Inicializa o estado da sessão

    if not session_state.logged_in:
        login_page(session_state)
    else:
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.markdown("by Lyssandro Silveira")

        st.sidebar.write(f"Logado como: {session_state.username}")  # Mostra o nome do usuário na barra lateral
        st.sidebar.button("Logout", key="logout_button", on_click=logout)  # Botão de logout na barra lateral

        st_tabs = st.tabs(["Jogos do Dia", "CS", "Tips"])
        if st_tabs == "Jogos do Dia":
            jogos_do_dia_page()
        elif st_tabs == "CS":
            cs_page()
        elif st_tabs == "Tips":
            tips_page()

def logout():
    session_state = SessionState.get()
    session_state.logged_in = False
    session_state.username = None
    session_state.login_time = None

if __name__ == "__main__":
    main()
