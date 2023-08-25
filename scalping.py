import streamlit as st
import pandas as pd
import re
from session_state import SessionState

def scalping_page():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=3)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Definir URLs para os arquivos CSV
    url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true'
    url_momento_gol_home = 'https://github.com/scooby75/bdfootball/blob/main/scalping_home.csv?raw=true'
    url_momento_gol_away = 'https://github.com/scooby75/bdfootball/blob/main/scalping_away.csv?raw=true'

    try:
        # Carregar dados CSV
        jogosdodia = pd.read_csv(url_jogosdodia)
        momento_gol_home = pd.read_csv(url_momento_gol_home)
        momento_gol_away = pd.read_csv(url_momento_gol_away)

        # Lógica de mesclagem e filtragem de dados
        jogos_filtrados_home = jogosdodia.merge(momento_gol_home, left_on=['Home', 'ROUND'], right_on=['Equipe', 'ROUND'])
        jogos_filtrados_away = jogosdodia.merge(momento_gol_away, left_on=['Away', 'ROUND'], right_on=['Equipe', 'ROUND'])
        jogos_filtrados = jogos_filtrados_home.merge(jogos_filtrados_away, on=['Date', 'Home', 'Away'], suffixes=('_home', '_away'))

        # Filtrar jogos com critérios específicos
        filtered_games = jogos_filtrados[
            (jogos_filtrados['0_15_mar_home'] == 0) & (jogos_filtrados['0_15_sofri_home'] == 0) &
            (jogos_filtrados['0_15_mar_away'] == 0) & (jogos_filtrados['0_15_sofri_away'] == 0)
        ]

        # Selecionar colunas relevantes e renomear
        result_df = filtered_games[['Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home', 'FT_Odd_Over25_home', 'ROUND']]
        result_df.columns = ['Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Over25', 'Rodada']

        # Extraindo apenas os números da coluna 'Rodada'
        result_df['Rodada'] = result_df['Rodada'].str.extract('(\d+)')

        # Filtrar jogos com ROUND >= 5
        result_df = result_df[result_df['Rodada'].astype(int) >= 5]

        # Streamlit App
        st.subheader("Lay Over 25FT")
        st.text("Apostar em Lay Over 25FT e fechar posição com 3% ou 5min de exposição.")
        st.dataframe(result_df)

    except Exception as e:
        st.error("Ocorreu um erro: " + str(e))

# Chamar a função para iniciar o aplicativo Streamlit
scalping_page()


