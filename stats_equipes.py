import streamlit as st
import pandas as pd

from session_state import SessionState

def stats_equipes_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
        
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/BD_Geral.csv"
    df = pd.read_csv(url)

    st.subheader("Análise Desempenho das Equipes")

    equipe_escolhida = st.selectbox("Escolha a equipe:", df['Home'].unique())
    liga_escolhida = st.selectbox("Escolha a liga:", df['League'].unique())
    num_partidas = st.slider("Número de partidas a analisar:", min_value=3, max_value=min(8, len(df)), value=3)

    df_equipe_liga = df[(df['Home'] == equipe_escolhida) & (df['League'] == liga_escolhida)]
    df_equipe_liga = df_equipe_liga.sort_values(by='Unnamed: 0', ascending=False)

    st.subheader("Partidas mais recentes:")
    partidas_recentes = df_equipe_liga[['Date', 'League', 'Home', 'Away', 'Placar_HT', 'Placar_FT']].head(num_partidas)
    partidas_recentes = partidas_recentes.reset_index(drop=True)
    st.dataframe(partidas_recentes)

    ultimas_partidas = df_equipe_liga.head(num_partidas).copy()
    total_partidas = ultimas_partidas.shape[0]

    mapeamento_resultados = {'H': 'Vitória', 'D': 'Empate', 'A': 'Away'}

    ultimas_partidas['Resultado_FT'] = ultimas_partidas['Resultado_FT'].map(mapeamento_resultados)
    ultimas_partidas['Resultado_HT'] = ultimas_partidas['Resultado_HT'].map(mapeamento_resultados)

    vitorias_FT = ultimas_partidas['Resultado_FT'].eq('Vitória').sum()
    empates_FT = ultimas_partidas['Resultado_FT'].eq('Empate').sum()
    derrotas_FT = ultimas_partidas['Resultado_FT'].eq('Away').sum()

    vitorias_HT = ultimas_partidas['Resultado_HT'].eq('Vitória').sum()
    empates_HT = ultimas_partidas['Resultado_HT'].eq('Empate').sum()
    derrotas_HT = ultimas_partidas['Resultado_HT'].eq('Away').sum()

    st.subheader("Desempenho HT:")
    st.write(f"Vitórias HT: {vitorias_HT} ({(vitorias_HT / total_partidas * 100):.2f}%)")
    st.write(f"Empates HT: {empates_HT} ({(empates_HT / total_partidas * 100):.2f}%)")
    st.write(f"Derrotas HT: {derrotas_HT} ({(derrotas_HT / total_partidas * 100):.2f}%)")

    st.subheader("Desempenho FT:")
    st.write(f"Vitórias FT: {vitorias_FT} ({(vitorias_FT / total_partidas * 100):.2f}%)")
    st.write(f"Empates FT: {empates_FT} ({(empates_FT / total_partidas * 100):.2f}%)")
    st.write(f"Derrotas FT: {derrotas_FT} ({(derrotas_FT / total_partidas * 100):.2f}%)")

    media_gols_feitos_HT = ultimas_partidas['HT_Goals_H'].mean()
    media_gols_tomados_HT = ultimas_partidas['HT_Goals_A'].mean()
    
    media_gols_feitos_FT = ultimas_partidas['FT_Goals_H'].mean()
    media_gols_tomados_FT = ultimas_partidas['FT_Goals_A'].mean()
    
    st.subheader("Média de Gols HT:")
    st.write(f"Gols Feitos HT: {media_gols_feitos_HT:.2f}")
    st.write(f"Gols Tomados HT: {media_gols_tomados_HT:.2f}")

    st.subheader("Média de Gols FT:")
    st.write(f"Gols Feitos FT: {media_gols_feitos_FT:.2f}")
    st.write(f"Gols Tomados FT: {media_gols_tomados_FT:.2f}")

    partidas_com_gols = ultimas_partidas[ultimas_partidas['Goals_Minutes_Home'] != '[]']

    medias_por_partida = []

    for index, partida in partidas_com_gols.iterrows():
        minutos_gols = [int(minuto) for minuto in partida['Goals_Minutes_Home'].strip('[]').split(', ')]
        media_partida = sum(minutos_gols) / len(minutos_gols)
        medias_por_partida.append(media_partida)

    if medias_por_partida:
        media_equipe = sum(medias_por_partida) / len(medias_por_partida)

        st.subheader("Média de Tempo de Gol da Equipe (Home):")
        st.write(f"{media_equipe:.2f} minutos")

    rank_home_partida_mais_recente = df_equipe_liga.iloc[0]['Rank_Home']

    st.subheader("Rank Home")
    st.write(rank_home_partida_mais_recente)

# Execute the function to create the page
stats_equipes_page()
