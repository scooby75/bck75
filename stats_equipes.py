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
    
    total_partidas = ultimas_partidas.shape[0
    
    # Mapear os valores nas colunas 'Resultado_FT' e 'Resultado_HT' para os resultados correspondentes
    mapeamento_resultados = {'H': 'Vitória', 'D': 'Empate', 'A': 'Away'}
    
    ultimas_partidas['Resultado_FT'] = ultimas_partidas['Resultado_FT'].map(mapeamento_resultados)
    ultimas_partidas['Resultado_HT'] = ultimas_partidas['Resultado_HT'].map(mapeamento_resultados)
    
    # Contar as ocorrências de cada resultado
    vitorias_FT = ultimas_partidas['Resultado_FT'].eq('Vitória').sum()
    empates_FT = ultimas_partidas['Resultado_FT'].eq('Empate').sum()
    derrotas_FT = ultimas_partidas['Resultado_FT'].eq('Away').sum()  # Alterado de 'Derrota' para 'Away'
    
    vitorias_HT = ultimas_partidas['Resultado_HT'].eq('Vitória').sum()
    empates_HT = ultimas_partidas['Resultado_HT'].eq('Empate').sum()
    derrotas_HT = ultimas_partidas['Resultado_HT'].eq('Away').sum()  # Alterado de 'Derrota' para 'Away'
    
    # Subheaders e estatísticas em FT e HT
    col1, col2 = st.columns(2)
    
    with col2:
        st.subheader("Resultados em FT:")
        total_resultados_FT = vitorias_FT + empates_FT + derrotas_FT
        if total_resultados_FT > 0:
            porcentagem_vitorias_FT = int((vitorias_FT / total_resultados_FT) * 100)
            porcentagem_empates_FT = int((empates_FT / total_resultados_FT) * 100)
            porcentagem_derrotas_FT = int((derrotas_FT / total_resultados_FT) * 100)
        else:
            porcentagem_vitorias_FT = 0
            porcentagem_empates_FT = 0
            porcentagem_derrotas_FT = 0

        st.dataframe({
            'Vitórias': [vitorias_FT],
            'Empates': [empates_FT],
            'Derrotas': [derrotas_FT],
            'Porcentagem (%)': [
                f"{porcentagem_vitorias_FT}%",
                f"{porcentagem_empates_FT}%",
                f"{porcentagem_derrotas_FT}%"
            ]
        })

    with col1:
        st.subheader("Resultados em HT:")
        total_resultados_HT = vitorias_HT + empates_HT + derrotas_HT
        if total_resultados_HT > 0:
            porcentagem_vitorias_HT = int((vitorias_HT / total_resultados_HT) * 100)
            porcentagem_empates_HT = int((empates_HT / total_resultados_HT) * 100)
            porcentagem_derrotas_HT = int((derrotas_HT / total_resultados_HT) * 100)
        else:
            porcentagem_vitorias_HT = 0
            porcentagem_empates_HT = 0
            porcentagem_derrotas_HT = 0

        st.dataframe({
            'Vitórias': [vitorias_HT],
            'Empates': [empates_HT],
            'Derrotas': [derrotas_HT],
            'Porcentagem (%)': [
                f"{porcentagem_vitorias_HT}%",
                f"{porcentagem_empates_HT}%",
                f"{porcentagem_derrotas_HT}%"
            ]
        })
    
    # Calcular a média de gols feitos e tomados no HT
    media_gols_feitos_HT = ultimas_partidas['HT_Goals_H'].mean()
    media_gols_tomados_HT = ultimas_partidas['HT_Goals_A'].mean()
    
    # Calcular a média de gols feitos e tomados no FT
    media_gols_feitos_FT = ultimas_partidas['FT_Goals_H'].mean()
    media_gols_tomados_FT = ultimas_partidas['FT_Goals_A'].mean()
    
    # Adicionar as médias ao DataFrame
    ultimas_partidas['Média_Gols_Feitos_HT'] = media_gols_feitos_HT
    ultimas_partidas['Média_Gols_Tomados_HT'] = media_gols_tomados_HT
    ultimas_partidas['Média_Gols_Feitos_FT'] = media_gols_feitos_FT
    ultimas_partidas['Média_Gols_Tomados_FT'] = media_gols_tomados_FT
    
    # Exibir as médias em uma tabela
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Média de Gols HT:")
        st.dataframe({
            'Gols Feitos HT': [media_gols_feitos_HT],
            'Gols Tomados HT': [media_gols_tomados_HT]
        })

    with col4:
        st.subheader("Média de Gols FT:")
        st.dataframe({
            'Gols Feitos FT': [media_gols_feitos_FT],
            'Gols Tomados FT': [media_gols_tomados_FT]
        })

# Execute a função para criar a página
stats_equipes_page()
