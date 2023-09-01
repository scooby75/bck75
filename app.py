import streamlit as st
from login import login_page, perform_logout
from jogos import jogos_do_dia_page
from cs import cs_page
from predict import predict_page
from ha_025 import ha_025_page
from lay_zebra import lay_zebra_page
from zebra_ft import zebra_ft_page
from scalping import scalping_page
from bck_home import bck_home_page
from bck_away import bck_away_page
from bck_league_home import bck_league_home_page
from goleada import goleada_page
from h2h import h2h_page
from session_state import get_or_create_session_state

def main():
    # Obtém ou cria o estado da sessão
    session_state = get_or_create_session_state()

    if not hasattr(session_state, 'logged_in'):
        session_state.logged_in = False

    if not session_state.logged_in:
        login_page()
    else:
        # Initialize user_profile attribute if not present
        if not hasattr(session_state, 'user_profile'):
            session_state.user_profile = 1  # Initialize with a default value

        # Barra lateral com imagem e informações
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.header("Football Data Analysis")

        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {session_state.username}")
        if st.sidebar.button("Logout", key="logout_button"):
            perform_logout(session_state)  # Chame perform_logout em vez de logout

        # Mapeia a seleção do usuário para as páginas
        pages = {
            "Jogos do Dia": (jogos_do_dia_page, 1),
            "Análise Home": (bck_home_page, 3),
            "Análise Away": (bck_away_page, 3),
            "Análise Liga": (bck_league_home_page, 3),
            "Dutching CS": (cs_page, 2),
            "HA": (ha_025_page, 2),
            "H2H": (h2h_page, 2),
            "Lay Goleada": (goleada_page, 3),
            "Lay Zebra HT": (lay_zebra_page, 2),
            "Predict": (predict_page, 3),
            "Lay Zebra FT": (zebra_ft_page, 2),
            "Scalping": (scalping_page, 3)
        }

        # Caixa de seleção para diferentes páginas
        selected_tab = st.sidebar.selectbox("Selecione uma aba", list(pages.keys()))

        # Exibe o conteúdo da página selecionada, considerando as permissões do perfil
        user_profile = session_state.user_profile

        if selected_tab in pages:
            page_function, required_profile = pages[selected_tab]
            if user_profile is not None and user_profile >= required_profile:
                page_function()

if __name__ == "__main__":
    main()
