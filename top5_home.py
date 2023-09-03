import streamlit as st
import pandas as pd
import re
from session_state import SessionState

def top5_home_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Carrega o dado
    # Carregar o arquivo CSV a partir da URL
    url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
    df = pd.read_csv(url)

    # Renomear as colunas
    df = df.rename(columns={'Home': 'Equipe', 'League': 'Liga', 'Rank_Home': 'Posição Casa', 'Round': 'Rodada', 'profit_home': 'Lucro Acumulado'})

    # Filtrar as equipes com Round >= 10
    df = df[df['Round'] >= 10]

    # Classificar o DataFrame por Posição Casa
    df.sort_values(by='Posição Casa', inplace=True)

    # Criar um dicionário para armazenar os 5 melhores times de cada liga
    top5_teams_by_league = {}

    # Iterar pelas ligas únicas no DataFrame
    for league in df['Liga'].unique():
        # Filtrar o DataFrame para a liga específica
        league_df = df[df['Liga'] == league]

        # Obter os 5 primeiros times da liga com base na Posição Casa
        top5_teams = league_df.head(5)

        # Armazenar os resultados no dicionário
        top5_teams_by_league[league] = top5_teams

    # Mostrar os resultados usando st.dataframe
    for league, top5_teams in top5_teams_by_league.items():
        st.subheader(f"Top 5 times da liga {league}")
        st.dataframe(top5_teams[['Equipe', 'Liga', 'Posição Casa', 'Rodada', 'Lucro Acumulado']], index=False)

# Chamar a função para exibir a aplicação web
top5_home_page()
