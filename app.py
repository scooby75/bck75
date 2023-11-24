# app.py

import streamlit as st
from login import login_page, logout
from jogos import jogos_do_dia_page
from cs import cs_page
from predict import predict_page
from bck_home import bck_home_page
from bck_away import bck_away_page
from bck_league_home import bck_league_home_page
from h2h import h2h_page
from last4 import last4_page
from stats_equipes import stats_equipes_page
from stats_away import stats_away_page
from tips import tips_page
from value_bets import value_bets_page
from bck_dia_home import bck_dia_home_page

from session_state import get_or_create_session_state
from session_state import SessionState

def main():
    # Inicialize o estado da sessão (session_state) usando um dicionário
    session_state = st.session_state

    # Defina os atributos iniciais do estado da sessão, se não existirem
    if not hasattr(session_state, 'logged_in'):
        session_state.logged_in = False

    if not hasattr(session_state, 'username'):
        session_state.username = None

    if not hasattr(session_state, 'user_profile'):
        session_state.user_profile = 1  # Inicialize com um valor padrão

    if not session_state.logged_in:
        login_page()
    else:
        # Barra lateral com imagem e informações
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.header("Football Data Analysis")

        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {session_state.username}")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()

        # Caixa de seleção para diferentes páginas
        selected_tab = st.sidebar.selectbox("Selecione uma aba", ["Jogos do Dia", "Análise Home", "Análise Away", "Análise Liga", "Análise Dia", "Desempenho Equipes - Casa", "Desempenho Equipes - Visitante", "Dutching CS",  "H2H", "Last4", "Predict", "Tips", "Value Bets"])

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
        elif selected_tab == "Desempenho Equipes - Casa" and user_profile >= 3:
            stats_equipes_page()
        elif selected_tab == "Desempenho Equipes - Visitante" and user_profile >= 3:
            stats_away_page()           
        elif selected_tab == "Dutching CS" and user_profile >= 2:
            cs_page()
        elif selected_tab == "H2H" and user_profile >= 2:
            h2h_page()
        elif selected_tab == "Last4" and user_profile >= 2:
            last4_page()
        elif selected_tab == "Predict" and user_profile >= 2:
            predict_page()
        elif selected_tab == "Tips" and user_profile >= 1:
            tips_page()
        elif selected_tab == "Value Bets" and user_profile >= 2:
            value_bets_page()
        elif selected_tab == "Análise Dia" and user_profile >= 4:
            bck_dia_home_page()
        
       

if __name__ == "__main__":
    main()
