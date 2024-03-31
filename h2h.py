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

    # Adicionar um slider para selecionar o intervalo de odds home
    min_odd_home, max_odd_home = st.slider("Selecione o intervalo de odds para a equipe da casa:", min_value=1.0, max_value=10.0, value=(1.0, 2.0), step=0.01)

    # Adicionar um slider para selecionar o intervalo de odds away
    min_odd_away, max_odd_away = st.slider("Selecione o intervalo de odds para a equipe visitante:", min_value=1.0, max_value=10.0, value=(1.0, 2.0), step=0.01)

    # Definir os intervalos de Odd
    odd_intervals = [(1.01, 1.30), (1.31, 1.50), (1.51, 1.70), (1.71, 1.90), (1.91, 2.1), (2.11, 2.3), (2.31, 2.5), (2.51, 2.7), (2.71, 3), (3.01, 3.5), (3.51, 4), (4.01, 4.50), (4.51, 5.5), (5.51, 6.5), (6.51, 7.5)]

    # Filtrar os jogos correspondentes às equipes selecionadas e ao intervalo de odds
    matching_games = data.loc[(data['Home'] == home_team) & 
                              (data['Away'] == away_team) & 
                              (data['FT_Odd_H'] >= min_odd_home) & 
                              (data['FT_Odd_H'] <= max_odd_home) &
                              (data['FT_Odd_A'] >= min_odd_away) & 
                              (data['FT_Odd_A'] <= max_odd_away)]

    if not matching_games.empty:
        st.subheader("Últimos confrontos h2h:")
        st.dataframe(matching_games[['Date', 'Season', 'League', 'Home', 'Away', 'Resultado_FT', 'Placar_FT', 'FT_Odd_H', 'FT_Odd_A']])

        # Filtrar os últimos jogos da equipe da casa com base no intervalo de odds
        ultimos_jogos_casa = matching_games.loc[(matching_games['Home'] == home_team)].sort_values(by='Date', ascending=False).head(5)

        # Verificar se a coluna 'Resultado_FT' está presente no DataFrame
        if 'Resultado_FT' in ultimos_jogos_casa.columns:
            # Calcular o número de vitórias da equipe da casa
            vitorias = ultimos_jogos_casa.loc[ultimos_jogos_casa['Resultado_FT'] == 'H', 'Resultado_FT'].count()
        else:
            # Definir vitorias como 0 caso a coluna não esteja presente
            vitorias = 0

        # Calcular as estatísticas de vitórias, empates e derrotas
        empates = ultimos_jogos_casa.loc[ultimos_jogos_casa['Resultado_FT'] == 'D', 'Resultado_FT'].count()
        derrotas = ultimos_jogos_casa.loc[ultimos_jogos_casa['Resultado_FT'] == 'A', 'Resultado_FT'].count()

        # Criar um DataFrame com as estatísticas
        stats_casa = pd.DataFrame({
            'Estatísticas': ['Vitórias', 'Empates', 'Derrotas'],
            'Total': [vitorias, empates, derrotas]
        })

        # Calcular a média de gols marcados (Home) nas últimas 5 partidas
        media_gols_feitos_casa = ultimos_jogos_casa['FT_Goals_H'].mean()

        # Calcular a média de gols tomados (Home) nas últimas 5 partidas
        media_gols_tomados_casa = ultimos_jogos_casa['FT_Goals_A'].mean()

        # Criar um DataFrame com os valores calculados para a equipe da casa
        stats_gols_casa = pd.DataFrame({
            'Equipe da Casa': [home_team],
            'Gols Feitos (Home)': [media_gols_feitos_casa],
            'Gols Tomados (Home)': [media_gols_tomados_casa]
        })

        st.subheader(f"Stats Desempenho - {home_team}")
        st.dataframe(stats_casa)

        st.subheader(f"Stats Gols - {home_team}")
        st.dataframe(stats_gols_casa)

        # Filtrar os últimos jogos da equipe visitante com base no intervalo de odds
        ultimos_jogos_visitante = matching_games.loc[(matching_games['Away'] == away_team)].sort_values(by='Date', ascending=False).head(5)

        # Calcular as estatísticas de vitórias, empates e derrotas para a equipe visitante
        if not ultimos_jogos_visitante.empty and 'Resultado_FT' in ultimos_jogos_visitante.columns:
            vitorias_visitante = ultimos_jogos_visitante.loc[ultimos_jogos_visitante['Resultado_FT'] == 'A', 'Resultado_FT'].count()
            empates_visitante = ultimos_jogos_visitante.loc[ultimos_jogos_visitante['Resultado_FT'] == 'D', 'Resultado_FT'].count()
            derrotas_visitante = ultimos_jogos_visitante.loc[ultimos_jogos_visitante['Resultado_FT'] == 'H', 'Resultado_FT'].count()
        else:
            vitorias_visitante = 0
            empates_visitante = 0
            derrotas_visitante = 0

        # Criar um DataFrame com as estatísticas para a equipe visitante
        stats_visitante = pd.DataFrame({
            'Estatísticas': ['Vitórias', 'Empates', 'Derrotas'],
            'Total': [vitorias_visitante, empates_visitante, derrotas_visitante]
        })

        # Calcular a média de gols marcados (Away) nas últimas 5 partidas
        media_gols_feitos_visitante = ultimos_jogos_visitante['FT_Goals_A'].mean()

        # Calcular a média de gols tomados (Away) nas últimas 5 partidas
        media_gols_tomados_visitante = ultimos_jogos_visitante['FT_Goals_H'].mean()

        # Criar um DataFrame com os valores calculados para a equipe visitante
        stats_gols_visitante = pd.DataFrame({
            'Equipe Visitante': [away_team],
            'Gols Feitos (Away)': [media_gols_feitos_visitante],
            'Gols Tomados (Away)': [media_gols_tomados_visitante]
        })

        st.subheader(f"Stats Desempenho - {away_team}")
        st.dataframe(stats_visitante)

        st.subheader(f"Stats Gols - {away_team}")
        st.dataframe(stats_gols_visitante)
    else:
        st.write("Nenhum jogo correspondente encontrado.")

# Chamar a função para iniciar o aplicativo
h2h_page()
