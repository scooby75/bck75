# stats_equipes.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    # Carregue os dados do CSV
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/BD_Geral.csv"
    df = pd.read_csv(url)

    # Título da página
    st.subheader("Análise Desempenho das Equipes")

    # Escolha a equipe que deseja analisar usando um seletor
    equipe_escolhida = st.selectbox("Escolha a equipe:", df['Home'].unique())

    # Escolha a liga que deseja analisar usando um seletor
    liga_escolhida = st.selectbox("Escolha a liga:", df['League'].unique())

    # Solicite ao usuário o número de partidas a serem analisadas, limitado a 8
    num_partidas = st.slider("Número de partidas a analisar:", min_value=3, max_value=min(8, len(df)), value=3)

    # Filtre o DataFrame com base nas escolhas do usuário
    df_equipe_liga = df[(df['Home'] == equipe_escolhida) & (df['League'] == liga_escolhida)]

    # Organize as partidas com base na coluna 'Unnamed: 0' do maior para o menor
    df_equipe_liga = df_equipe_liga.sort_values(by='Unnamed: 0', ascending=False)

    # Exiba as últimas N partidas selecionadas em uma tabela
    partidas_recentes = df_equipe_liga[['Date', 'League', 'Home', 'Away', 'Placar_HT', 'Placar_FT']].head(num_partidas)
    partidas_recentes = partidas_recentes.reset_index(drop=True)  # Remover o índice
    st.subheader("Partidas mais recentes:")
    st.dataframe(partidas_recentes)

    # Calcular as estatísticas das últimas N partidas selecionadas
    ultimas_partidas = df_equipe_liga.head(num_partidas).copy()
    
    total_partidas = ultimas_partidas.shape[0]

    # Calcular as estatísticas de vitórias, empates e derrotas em FT e HT
    vitorias_FT = ultimas_partidas[ultimas_partidas['Resultado_FT'] == 'Vitória'].shape[0]
    empates_FT = ultimas_partidas[ultimas_partidas['Resultado_FT'] == 'Empate'].shape[0]
    derrotas_FT = ultimas_partidas[ultimas_partidas['Resultado_FT'] == 'Away'].shape[0]

    vitorias_HT = ultimas_partidas[ultimas_partidas['Resultado_HT'] == 'Vitória'].shape[0]
    empates_HT = ultimas_partidas[ultimas_partidas['Resultado_HT'] == 'Empate'].shape[0]
    derrotas_HT = ultimas_partidas[ultimas_partidas['Resultado_HT'] == 'Away'].shape[0]

    # Subheaders e estatísticas em FT e HT
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resultados em FT:")
        st.write(f"Vitórias: {vitorias_FT} ({(vitorias_FT / total_partidas * 100):.2f}%)")
        st.write(f"Empates: {empates_FT} ({(empates_FT / total_partidas * 100):.2f}%)")
        st.write(f"Derrotas: {derrotas_FT} ({(derrotas_FT / total_partidas * 100):.2f}%)")

    with col2:
        st.subheader("Resultados em HT:")
        st.write(f"Vitórias: {vitorias_HT} ({(vitorias_HT / total_partidas * 100):.2f}%)")
        st.write(f"Empates: {empates_HT} ({(empates_HT / total_partidas * 100):.2f}%)")
        st.write(f"Derrotas: {derrotas_HT} ({(derrotas_HT / total_partidas * 100):.2f}%)")

    # Gráficos de barras para cada partida
    st.subheader("Gráficos de barras por partida:")

    # Defina a largura de cada barra e a largura total do espaço disponível
    largura_barra = 0.2
    largura_total = len(ultimas_partidas)

    # Crie um array com os deslocamentos para posicionar as barras lado a lado
    deslocamentos = (largura_barra * (largura_total - 1)) / 2

    for i, row in ultimas_partidas.iterrows():
        resultado = row['Resultado_FT']
        cor = 'green' if resultado == 'Vitória' else ('red' if resultado == 'Away' else 'gray')

        fig, ax = plt.subplots()
        ax.barh(['Home'], [1], color=cor, height=largura_barra, left=i - deslocamentos)  # Adicione o deslocamento
        ax.set_xlim(0, 1)
        ax.axis('off')

        st.pyplot(fig)

# Execute a função para criar a página
stats_equipes_page()
