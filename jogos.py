# jogos.py

import streamlit as st
import pandas as pd
from session_state import SessionState
import datetime as dt

def jogos_do_dia_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Define o valor de user_profile após a criação da instância
    session_state.user_profile = 1  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 1:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=23200.0)  # 24 hours in seconds
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
        data_jogos = pd.read_csv(url)
        return data_jogos

    df2 = load_base()

    # Define colunas a serem exibidas
    columns_to_display = [
        'Date', 'Hora', 'Liga', 'Rodada', 'Home', 'Away', 'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A',
        'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes', 'XG_Home', 'XG_Away', 'Media_Gols', 'AVG_05HT',
        'AVG_15FT', 'AVG_25FT', 'PPG_Home', 'PPG_Away', 'Real_Prob_Home', 'Real_Prob_Draw', 'Real_Prob_Away'
    ]

    # Cria filtros para colunas selecionadas
    filter_values = {}
    filter_columns = [
        ('FT Odds Home', 'selected_ft_odd_h'),
        ('FT Odds Draw', 'selected_ft_odd_d'),
        ('FT Odds Away', 'selected_ft_odd_a'),
        ('FT Odds Over 2.5', 'selected_ft_odd_over25'),
        ('FT Odds Under 2.5', 'selected_ft_odd_under25'),
        ('FT Odds BTTS Yes', 'selected_ft_odd_btts_yes'),
        ('Rodada', 'selected_rodada'),
        ('PPG Home', 'selected_ppg_h'),
        ('PPG Away', 'selected_ppg_a'),
        ('XG Home', 'selected_hg_home'),
        ('XG Away', 'selected_hg_away'),
        ('Média de Gols', 'selected_Media_Gols'),
        ('AVG_05HT', 'selected_AVG_05HT'),
        ('AVG_15FT', 'selected_AVG_15FT'),
        ('AVG_25FT', 'selected_AVG_25FT'),
        ('AVG_BTTS_Yes', 'selected_AVG_BTTS_Yes'),
    ]

    # Cria entradas de número para condições de filtro
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        selected_ft_odd_h_min = st.number_input("FT Odds Home (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_h_max = st.number_input("FT Odds Home (max)", selected_ft_odd_h_min, 15.0, 15.0)
        selected_ft_odd_d_min = st.number_input("FT Odds Draw (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_d_max = st.number_input("FT Odds Draw (max)", selected_ft_odd_d_min, 15.0, 15.0)
        selected_ft_odd_a_min = st.number_input("FT Odds Away (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_a_max = st.number_input("FT Odds Away (max)", selected_ft_odd_a_min, 15.0, 15.0)

    with col2:
        selected_ft_odd_over25_min = st.number_input("FT Odds Over 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_over25_max = st.number_input("FT Odds Over 2.5 (max)", selected_ft_odd_over25_min, 10.0, 10.0)
        selected_ft_odd_under25_min = st.number_input("FT Odds Under 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_under25_max = st.number_input("FT Odds Under 2.5 (max)", selected_ft_odd_under25_min, 10.0, 10.0)
        selected_ft_odd_btts_yes_min = st.number_input("FT Odds BTTS Yes (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_btts_yes_max = st.number_input("FT Odds BTTS Yes (max)", selected_ft_odd_btts_yes_min, 10.0, 10.0)

    with col3:
        selected_rodada_min = st.number_input("Rodada (min)", 0.0, 50.0, 1.0)
        selected_rodada_max = st.number_input("Rodada (max)", 0.0, 50.0, 50.0)
        selected_ppg_home_min = st.number_input("PPG Home (min)", 0.0, 3.0, 0.0)
        selected_ppg_home_max = st.number_input("PPG Home (max)", 0.0, 3.0, 3.0)
        selected_ppg_away_min = st.number_input("PPG Away (min)", 0.0, 3.0, 0.0)
        selected_ppg_away_max = st.number_input("PPG Away (max)", 0.0, 3.0, 3.0)

    with col4:
        selected_hg_home_min = st.number_input("XG Home (min)", 0.0, 10.0, 0.0)
        selected_hg_home_max = st.number_input("XG Home (max)", 0.0, 10.0, 10.0)
        selected_hg_away_min = st.number_input("XG Away (min)", 0.0, 10.0, 0.0)
        selected_hg_away_max = st.number_input("XG Away (max)", 0.0, 10.0, 10.0)
        selected_Media_Gols_min = st.number_input("Média de Gols (min)", 0.0, 10.0, 0.0)
        selected_Media_Gols_max = st.number_input("Média de Gols (max)", 0.0, 10.0, 10.0)

    with col5:
        selected_AVG_05HT_min = st.number_input("AVG 05HT (min)", 0.0, 100.0, 0.0)
        selected_AVG_05HT_max = st.number_input("AVG 05HT (max)", 0.0, 100.0, 100.0)
        selected_AVG_15FT_min = st.number_input("AVG 15FT (min)", 0.0, 100.0, 0.0)
        selected_AVG_15FT_max = st.number_input("AVG 15FT (max)", 0.0, 100.0, 100.0)
        selected_AVG_25FT_min = st.number_input("AVG 25FT (min)", 0.0, 100.0, 0.0)
        selected_AVG_25FT_max = st.number_input("AVG 25FT (max)", 0.0, 100.0, 100.0)
        selected_AVG_BTTS_Yes_min = st.number_input("AVG BTTS Yes (min)", 0.0, 100.0, 0.0)
        selected_AVG_BTTS_Yes_max = st.number_input("AVG BTTS Yes (max)", 0.0, 100.0, 100.0)

    # Aplica filtros ao DataFrame
    filtered_data = df2[
        (df2['FT_Odd_H'] >= selected_ft_odd_h_min) &
        (df2['FT_Odd_H'] <= selected_ft_odd_h_max) &
        (df2['FT_Odd_D'] >= selected_ft_odd_d_min) &
        (df2['FT_Odd_D'] <= selected_ft_odd_d_max) &
        (df2['FT_Odd_A'] >= selected_ft_odd_a_min) &    
        (df2['FT_Odd_A'] <= selected_ft_odd_a_max) &
        (df2['FT_Odd_Over25'] >= selected_ft_odd_over25_min) &
        (df2['FT_Odd_Over25'] <= selected_ft_odd_over25_max) &
        (df2['FT_Odd_Under25'] >= selected_ft_odd_under25_min) &
        (df2['FT_Odd_Under25'] <= selected_ft_odd_under25_max) &
        (df2['FT_Odd_BTTS_Yes'] >= selected_ft_odd_btts_yes_min) &
        (df2['FT_Odd_BTTS_Yes'] <= selected_ft_odd_btts_yes_max) &
        (df2['Rodada'] >= selected_rodada_min) &
        (df2['Rodada'] <= selected_rodada_max) &
        (df2['PPG_Home'] >= selected_ppg_home_min) &
        (df2['PPG_Home'] <= selected_ppg_home_max) &
        (df2['PPG_Away'] >= selected_ppg_away_min) &
        (df2['PPG_Away'] <= selected_ppg_away_max) &
        (df2['XG_Home'] >= selected_hg_home_min) &
        (df2['XG_Home'] <= selected_hg_home_max) &
        (df2['XG_Away'] >= selected_hg_away_min) &
        (df2['XG_Away'] <= selected_hg_away_max) &
        (df2['Media_Gols'] >= selected_Media_Gols_min) &
        (df2['Media_Gols'] <= selected_Media_Gols_max) &
        (df2['AVG_05HT'] >= selected_AVG_05HT_min) &
        (df2['AVG_05HT'] <= selected_AVG_05HT_max) &
        (df2['AVG_15FT'] >= selected_AVG_15FT_min) &
        (df2['AVG_15FT'] <= selected_AVG_15FT_max) &
        (df2['AVG_25FT'] >= selected_AVG_25FT_min) &
        (df2['AVG_25FT'] <= selected_AVG_25FT_max) &
        (df2['AVG_BTTS_Yes'] >= selected_AVG_BTTS_Yes_min) &
        (df2['AVG_BTTS_Yes'] <= selected_AVG_BTTS_Yes_max) 
    ]

    if not filtered_data.empty:
        sorted_filtered_data = filtered_data.sort_values(by='Hora')
        st.dataframe(sorted_filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Chama a função para exibir a aplicação web
jogos_do_dia_page()
