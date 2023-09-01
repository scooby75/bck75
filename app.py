import streamlit as st
from login import login_page, logout
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
            logout()
        
        # Caixa de seleção para diferentes páginas
        selected_tab = st.sidebar.selectbox("Selecione uma aba", ["Jogos do Dia", "Análise Home", "Análise Away", "Análise Liga", "Dutching CS", "HA", "H2H", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "Predict", "Scalping"])

        # Exibe o conteúdo da página selecionada, considerando as permissões do perfil
        user_profile = session_state.user_profile  # Use session_state here
        
        if selected_tab == "Jogos do Dia" and user_profile >= 1:
            jogos_do_dia_page()
        elif selected_tab == "Análise Home" and user_profile >= 3:
            bck_home_page()
        elif selected_tab == "Análise Away" and user_profile >= 3:
            bck_away_page()
        elif selected_tab == "Análise Liga" and user_profile >= 3:
            bck_league_home_page()
        elif selected_tab == "Dutching CS" and user_profile >= 2:
            cs_page()
        elif selected_tab == "HA" and user_profile >= 2:
            ha_025_page()
        elif selected_tab == "H2H" and user_profile >= 2:
            h2h_page()
        elif selected_tab == "Lay Goleada" and user_profile == 3:
            goleada_page()
        elif selected_tab == "Lay Zebra HT" and user_profile >= 2:
            lay_zebra_page()
        elif selected_tab == "Predict" and user_profile == 3:
            predict_page()
        elif selected_tab == "Lay Zebra FT" and user_profile >= 2:
            zebra_ft_page()
        elif selected_tab == "Scalping" and user_profile == 3:
            scalping_page()

if __name__ == "__main__":
    main()
