import streamlit as st
from login import login_page, logout
from jogos import jogos_do_dia_page
from cs import cs_page
from tips import tips_page

def main():
    # Verifica se o estado de sessão "logged_in" já existe
    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    # Verifica se o usuário está logado ou não
    if not st.session_state.logged_in:
        login_page()
    else:
        # Barra lateral com imagem e informações
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.header("Football Data Analysis")  # Corrigido "Footbal" para "Football"

        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {st.session_state.username}")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()

        # Cria abas para diferentes páginas
        tab0, tab1, tab2 = st.sidebar.beta_columns(3)
        if tab0.button("Jogos do Dia"):
            jogos_do_dia_page()
        if tab1.button("CS"):
            cs_page()
        if tab2.button("Tips"):
            tips_page()

if __name__ == "__main__":
    main()
