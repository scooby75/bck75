# stats_equipes.py

import streamlit as st
import pandas as pd

def stats_equipes_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
    # else:
    #     st.write("Acesso concedido!")  # Debug

    # Carregue os dados do CSV
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/BD_Geral.csv"
    df = pd.read_csv(url)

    # Título da página
    st.title("Análise de Resultados de Futebol")

    # Escolha a equipe que deseja analisar usando um seletor
    equipe_escolhida = st.selectbox("Escolha a equipe:", df['Home'].unique())

    # Escolha a liga que deseja analisar usando um seletor
    liga_escolhida = st.selectbox("Escolha a liga:", df['League'].unique())

    # Solicite ao usuário o número de partidas a serem analisadas
    num_partidas = st.slider("Número de partidas a analisar:", min_value=1, max_value=len(df), value=3)

    # Filtre o DataFrame com base nas escolhas do usuário
    df_equipe_liga = df[(df['Home'] == equipe_escolhida) & (df['League'] == liga_escolhida)]

    # Organize as partidas com base na coluna 'Unnamed: 0' do maior para o menor
    df_equipe_liga = df_equipe_liga.sort_values(by='Unnamed: 0', ascending=False)

    # Exiba as últimas N partidas selecionadas em uma tabela
    partidas_recentes = df_equipe_liga[['Date', 'League', 'Home', 'Away', 'Placar_HT', 'Placar_FT']].head(num_partidas)
    st.header("Partidas mais recentes:")
    st.dataframe(partidas_recentes, index=False)

    # Calcular as estatísticas das últimas N partidas selecionadas
    ultimas_partidas = df_equipe_liga.head(num_partidas).copy()

    total_partidas = ultimas_partidas.shape[0]

    vitorias_FT = ultimas_partidas['Resultado_FT'].eq('Vitória').sum()
    empates_FT = ultimas_partidas['Resultado_FT'].eq('Empate').sum()
    derrotas_FT = ultimas_partidas['Resultado_FT'].eq('Derrota').sum()

    vitorias_HT = ultimas_partidas['Resultado_HT'].eq('Vitória').sum()
    empates_HT = ultimas_partidas['Resultado_HT'].eq('Empate').sum()
    derrotas_HT = ultimas_partidas['Resultado_HT'].eq('Derrota').sum()

    # Exibir as estatísticas
    st.header("Estatísticas:")
    st.write("Resultados em FT:")
    st.write(f"Vitórias: {vitorias_FT} ({(vitorias_FT / total_partidas * 100):.2f}%)")
    st.write(f"Empates: {empates_FT} ({(empates_FT / total_partidas * 100):.2f}%)")
    st.write(f"Derrotas: {derrotas_FT} ({(derrotas_FT / total_partidas * 100):.2f}%)")

    st.write("Resultados em HT:")
    st.write(f"Vitórias: {vitorias_HT} ({(vitorias_HT / total_partidas * 100):.2f}%)")
    st.write(f"Empates: {empates_HT} ({(empates_HT / total_partidas * 100):.2f}%)")
    st.write(f"Derrotas: {derrotas_HT} ({(derrotas_HT / total_partidas * 100):.2f}%)")

# Execute a função para criar a página
stats_equipes_page()
