import streamlit as st
from login import login_page, logout
from jogos import jogos_do_dia_page
from cs import cs_page
from tips import tips_page

def main():
    # Configuração da página
    st.set_page_config(page_title="Análise de Dados de Futebol", layout="wide")

    # Verifica se o estado de sessão "logged_in" já existe
    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    # Verifica se o usuário está logado ou não
    if not st.session_state.logged_in:
        login_page()
    else:
        # Barra lateral com imagem e informações
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.markdown("por Lyssandro Silveira")

        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {st.session_state.username}")
        st.sidebar.button("Logout", key="logout_button", on_click=logout)

        # Cria abas para diferentes páginas
        st_tabs = st.tabs(["Jogos do Dia", "CS", "Tips"])
        if st_tabs == "Jogos do Dia":
            jogos_do_dia_page()
        elif st_tabs == "CS":
            cs_page()
        elif st_tabs == "Tips":
            tips_page()

if __name__ == "__main__":
    main()
