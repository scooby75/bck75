import streamlit as st
import datetime

# Dados de exemplo para simular o login (substitua por um mecanismo seguro em um ambiente de produção)
valid_users = {
    "lsilveira": "senha123",
    "usuario2": "senha456"
}

def login_page():
    st.title("Página de Login")
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in valid_users and valid_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.login_time = datetime.datetime.now()
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
    st.set_page_config(page_title="Meu Sistema", layout="wide")
    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.write(f"Logado como: {st.session_state.username}")  # Mostra o nome do usuário na barra lateral
        st.sidebar.button("Logout", key="logout_button", on_click=logout)  # Botão de logout na barra lateral

        st_tabs = st.tabs(["Jogos do Dia", "CS", "Tips"])
        if st_tabs == "Jogos do Dia":
            jogos_do_dia_page()
        elif st_tabs == "CS":
            cs_page()
        elif st_tabs == "Tips":
            tips_page()

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("login_time", None)

if __name__ == "__main__":
    main()
