# h2h.py

import streamlit as st
import pandas as pd

from session_state import SessionState

def h2h_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Carregar o arquivo CSV
    data = pd.read_csv('https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true')

    st.subheader("Análise h2h")

    # Solicitar ao usuário as equipes "Home" e "Away" usando selectbox
    home_teams = data['Home'].unique()
    away_teams = data['Away'].unique()

    home_team = st.selectbox("Selecione a equipe Home:", home_teams)
    away_team = st.selectbox("Selecione a equipe Away:", away_teams)

    # Definir os intervalos de Odd
    odd_intervals = [(1.01, 1.30), (1.31, 1.50), (1.51, 1.70), (1.71, 1.90), (1.91, 2.1), (2.11, 2.3), (2.31, 2.5), (2.51, 2.7), (2.71, 3), (3.01, 3.5), (3.51, 4), (4.01, 4.50), (4.51, 5.5), (5.51, 6.5), (6.51, 7.5)]

    # Filtrar os resultados para as equipes selecionadas
    home_team_wins = data[(data['Resultado_FT'] == 'H') & (data['Home'] == home_team) & (data['Away'] == away_team)]
    away_team_wins = data[(data['Resultado_FT'] == 'A') & (data['Home'] == home_team) & (data['Away'] == away_team)]
    draws = data[(data['Resultado_FT'] == 'D') & (data['Home'] == home_team) & (data['Away'] == away_team)]

    # Contar o número de partidas vencidas por cada equipe
    home_team_wins_count = len(home_team_wins)
    away_team_wins_count = len(away_team_wins)
    draws_count = len(draws)

    # Criar um DataFrame para exibir os valores
    result_data = pd.DataFrame({
        'Equipe': ['Home', 'Away', 'Empates'],
        'Número de Vitórias': [home_team_wins_count, away_team_wins_count, draws_count]
    })

    st.dataframe(result_data)

    # Encontrar o placar mais comum (Placar_FT) apenas para as equipes selecionadas
    filtered_data = data[(data['Home'] == home_team) & (data['Away'] == away_team)]
    if not filtered_data.empty:
        most_common_score = filtered_data['Placar_FT'].value_counts().idxmax()
        st.write(f'Placar mais comum: {most_common_score}')
    else:
        st.write("Nenhum jogo correspondente encontrado.")

    # Agrupar por intervalo de Odd e encontrar o placar mais comum em cada intervalo
    for lower_bound, upper_bound in odd_intervals:
        odd_group = data[(data['FT_Odd_H'] >= lower_bound) & (data['FT_Odd_H'] <= upper_bound) & (data['Home'] == home_team) & (data['Away'] == away_team)]

        if not odd_group.empty:
            most_common_score_in_group = odd_group['Placar_FT'].value_counts().idxmax()
            st.write(f'Intervalo de Odd: [{lower_bound:.2f}, {upper_bound:.2f}): Placar mais comum: {most_common_score_in_group}')
        
    
    # Filtrar os jogos correspondentes às equipes selecionadas
    matching_games = data[(data['Home'] == home_team) & (data['Away'] == away_team)]

    if not matching_games.empty:
        st.write("Jogos correspondentes:")
        st.dataframe(matching_games[['Date', 'Season', 'League', 'Home', 'Away', 'Resultado_FT', 'Placar_FT', 'FT_Odd_H']])
    else:
        st.write("Nenhum jogo correspondente encontrado.")

# Chamar a função para iniciar o aplicativo
h2h_page()

