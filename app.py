import streamlit as st
from login import login_page, logout
from jogos import jogos_do_dia_page
from cs import cs_page
from goleada import goleada_page
from ha_025 import ha_025_page
from lay_zebra import lay_zebra_page
from predict import predict_page
from scalping import scalping_page
from zebra_ft import zebra_ft_page

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
        st.sidebar.header("Football Data Analysis")

        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {st.session_state.username}")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()

        # Caixa de seleção para diferentes páginas
        selected_tab = st.sidebar.selectbox("Selecione uma aba", ["Jogos do Dia", "Dutching", "HA", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "Predict", "Scalping"])

        # Exibe o conteúdo da página selecionada
        if selected_tab == "Jogos do Dia":
            jogos_do_dia_page()
        elif selected_tab == "Dutching":
            cs_page()
        elif selected_tab == "HA":
            ha_025_page()
        elif selected_tab == "Lay Goleada":
            goleada_page()
        elif selected_tab == "Lay Zebra HT":
            lay_zebra_page()
        elif selected_tab == "Predict":
            predict_page()
        elif selected_tab == "Lay Zebra FT":
            zebra_ft_page()
        elif selected_tab == "Lay Zebra FT":
            scalping_ft_page()

if __name__ == "__main__":
    main()
