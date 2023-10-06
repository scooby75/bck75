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

    # Criar duas colunas, col1 e col2
    col1, col2 = st.columns(2)

    # Em col1, exibir o DataFrame result_data
    with col1:
        st.dataframe(result_data)

    # Em col2, exibir as informações sobre o intervalo de Odd e o placar mais comum
    with col2:
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
        st.subheader("Últimos confrontos h2h:")
        st.dataframe(matching_games[['Date', 'Season', 'League', 'Home', 'Away', 'Resultado_FT', 'Placar_FT', 'FT_Odd_H']])
    else:
        st.write("Nenhum jogo correspondente encontrado.")

    # Selecionar as 5 últimas partidas da equipe da casa
    ultimos_jogos_casa = data[(data['Home'] == home_team)].sort_values(by='Unnamed: 0', ascending=False).head(5)[['Date', 'Time', 'League', 'Season', 'Home', 'Away', 'Placar_HT', 'Placar_FT']]

    # Exibir o novo DataFrame para a equipe da casa
    st.subheader("Últimos Jogos - Equipe da Casa")
    st.dataframe(ultimos_jogos_casa, width=800)

    # Selecionar as 5 últimas partidas da equipe da casa
    ultimos_jogos_casa = data[data['Home'] == home_team].sort_values(by='Unnamed: 0', ascending=False).head(5)

    # Calcular as estatísticas de vitórias, empates e derrotas
    vitorias = ultimos_jogos_casa[ultimos_jogos_casa['Resultado_FT'] == 'H']['Resultado_FT'].count()
    empates = ultimos_jogos_casa[ultimos_jogos_casa['Resultado_FT'] == 'D']['Resultado_FT'].count()
    derrotas = ultimos_jogos_casa[ultimos_jogos_casa['Resultado_FT'] == 'A']['Resultado_FT'].count()

    # Criar um DataFrame com as estatísticas
    stats_casa = pd.DataFrame({
        'Estatísticas': ['Vitórias', 'Empates', 'Derrotas'],
        'Total': [vitorias, empates, derrotas]
    })

    # Selecionar as 5 últimas partidas da equipe da casa
    ultimos_jogos_casa = data[data['Home'] == home_team].sort_values(by='Unnamed: 0', ascending=False).head(5)

    # Calcular a média de gols marcados (Home) nas últimas 5 partidas
    media_gols_feitos = ultimos_jogos_casa['FT_Goals_H'].mean()

    # Calcular a média de gols tomados (Home) nas últimas 5 partidas
    media_gols_tomados = ultimos_jogos_casa['FT_Goals_A'].mean()

    # Criar um DataFrame com os valores calculados
    stats_gols = pd.DataFrame({
        'Equipe da Casa': [home_team],
        'Gols Feitos (Home)': [media_gols_feitos],
        'Gols Tomados (Home)': [media_gols_tomados]
    })

    # Criar duas colunas, col1 e col2
    col3, col4 = st.columns(2)

    # Em col3, exibir st.dataframe(stats_casa)
    with col3:
        st.subheader("Stats Desempenho")
        st.dataframe(stats_casa)

    # Em col4, exibir st.dataframe(stats_gols)
    with col4:
        st.subheader("Stats Gols")
        st.dataframe(stats_gols)

    # Selecionar as 5 últimas partidas da equipe visitante
    ultimos_jogos_visitante = data[(data['Away'] == away_team)].sort_values(by='Unnamed: 0', ascending=False).head(5)[['Date', 'Time', 'League', 'Season', 'Home', 'Away', 'Placar_HT', 'Placar_FT']]

    # Exibir o novo DataFrame para a equipe visitante
    st.subheader("Últimos Jogos - Equipe Visitante")
    st.dataframe(ultimos_jogos_visitante, width=800)

        # Selecionar as 5 últimas partidas da equipe visitante
    ultimos_jogos_visitante = data[data['Away'] == away_team].sort_values(by='Unnamed: 0', ascending=False).head(5)

    # Calcular as estatísticas de vitórias, empates e derrotas
    vitorias = ultimos_jogos_visitante[ultimos_jogos_visitante['Resultado_FT'] == 'A']['Resultado_FT'].count()
    empates = ultimos_jogos_visitante[ultimos_jogos_visitante['Resultado_FT'] == 'D']['Resultado_FT'].count()
    derrotas = ultimos_jogos_visitante[ultimos_jogos_visitante['Resultado_FT'] == 'H']['Resultado_FT'].count()

    # Criar um DataFrame com as estatísticas
    stats_casa = pd.DataFrame({
        'Estatísticas': ['Vitórias', 'Empates', 'Derrotas'],
        'Total': [vitorias, empates, derrotas]
    })

    # Selecionar as 5 últimas partidas da equipe visitante
    ultimos_jogos_visitante = data[data['Away'] == away_team].sort_values(by='Unnamed: 0', ascending=False).head(5)

    # Calcular a média de gols marcados (Away) nas últimas 5 partidas
    media_gols_feitos = ultimos_jogos_visitante['FT_Goals_A'].mean()

    # Calcular a média de gols tomados (Away) nas últimas 5 partidas
    media_gols_tomados = ultimos_jogos_visitante['FT_Goals_H'].mean()

    # Criar um DataFrame com os valores calculados
    stats_gols = pd.DataFrame({
        'Equipe Visitante': [away_team],
        'Gols Feitos (Away)': [media_gols_feitos],
        'Gols Tomados (Away)': [media_gols_tomados]
    })

    # Criar duas colunas, col5 e col6
    col5, col6 = st.columns(2)

    # Em col1, exibir st.dataframe(stats_casa)
    with col5:
        st.subheader("Stats Desempenho")
        st.dataframe(stats_casa)

    # Em col2, exibir st.dataframe(stats_gols)
    with col6:
        st.subheader("Stats Gols")
        st.dataframe(stats_gols)

# Chamar a função para iniciar o aplicativo
h2h_page()
