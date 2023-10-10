import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import poisson
from session_state import SessionState

def cs_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # URL do arquivo CSV com os dados dos jogos
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"
    
    # Extrair "País" e "Liga" da URL
    pais, liga = url.split('/')[-1].split('_')[:2]
    
    df = pd.read_csv(url)

    # Defina os placares desejados
    placares_desejados = [(1, 0), (1, 1), (0, 1), (1, 2), (1, 3), (2, 0), (0, 2), (2, 1)]  

    # Filtrar partidas que não contenham as strings "U21", "U19", "U20", "U16", "U23" ou "U18" nas colunas "Home" ou "Away"
    df = df[~df['Home'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False) & ~df['Away'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False)]

    # Inicializar uma lista para armazenar as informações das partidas
    partidas_info = []

    # Calcular as probabilidades para cada partida usando Poisson e ZIP
    for index, row in df.iterrows():
        date = row['Date']
        hora = row['Hora']
        home_team = row['Home']
        away_team = row['Away']
        odd_casa = row['FT_Odd_H']
        odd_empate = row['FT_Odd_D']
        odd_visitante = row['FT_Odd_A']

        # Parâmetros para a distribuição Poisson
        lambda_home = row['XG_Home']
        lambda_away = row['XG_Away']

        # Parâmetros para a distribuição Zero-Inflated Poisson (ZIP)
        zip_prob_zero = 0.2  # Ajuste esse valor conforme necessário
        zip_prob_non_zero = 1 - zip_prob_zero

        # Calcular as probabilidades de gols para cada equipe usando Poisson
        prob_home = poisson.pmf(np.arange(0, 8), lambda_home)
        prob_away = poisson.pmf(np.arange(0, 8), lambda_away)

        # Calcular a probabilidade de cada placar possível usando a distribuição ZIP
        probabilidade_partida = np.zeros((8, 8))

        for i in range(8):
            for j in range(8):
                if i == 0 and j == 0:
                    probabilidade_partida[i][j] = zip_prob_zero * (1 - prob_home[0]) * (1 - prob_away[0])
                else:
                    probabilidade_partida[i][j] = zip_prob_non_zero * prob_home[i] * prob_away[j]

        # Selecionar os 6 placares mais prováveis
        placares_classificados = sorted(
            [(i, j, probabilidade_partida[i][j]) for i in range(8) for j in range(8)],
            key=lambda x: x[2],
            reverse=True
        )[:6]  # Alterado para pegar apenas os 6 placares mais prováveis

        # Ajustar as probabilidades para que a soma seja igual a 100%
        soma_probabilidades = np.sum([prob for _, _, prob in placares_classificados])
        placares_classificados = [(i, j, prob / soma_probabilidades) for i, j, prob in placares_classificados]

        # Armazenar as informações da partida e probabilidades apenas para os placares desejados
        for placar_desejado in placares_desejados:
            i, j = placar_desejado
            probabilidade = [prob for _, _, prob in placares_classificados if i == _ and j == _][0] if placares_classificados else 0
            
            # Verificar se a probabilidade é maior que zero
            if probabilidade > 0:
                partida_info = {
                    'Date': date,
                    'Hora': hora,
                    'País': pais,
                    'Liga': liga,
                    'Home': home_team,
                    'Away': away_team,
                    'Placar': f"{i}x{j}",
                    'Odd Casa': odd_casa,
                    'Odd Empate': odd_empate,
                    'Odd Visitante': odd_visitante,
                    'Probabilidade': probabilidade,  # Ajustar o formato da probabilidade conforme necessário
                }
                partidas_info.append(partida_info)

    # Criar um DataFrame com as informações das partidas
    partidas_df = pd.DataFrame(partidas_info)

    # Ordenar o DataFrame pelos placares mais prováveis (do maior para o menor)
    partidas_df = partidas_df.sort_values(by='Probabilidade', ascending=False)

    # Exibir a tabela com todas as informações usando st.dataframe
    st.subheader("Probabilidades de Placares Desejados (do maior para o menor)")
    st.dataframe(partidas_df)

    # Exportar o DataFrame para um arquivo CSV quando o botão é clicado
    if st.button("Exportar CSV"):
        # Usar BytesIO para criar um arquivo temporário em memória para download
        import io
        buffer = io.BytesIO()
        partidas_df.to_csv(buffer, index=False, encoding='utf-8-sig')
        buffer.seek(0)
        st.download_button(
            label="Baixar CSV",
            data=buffer,
            file_name=f"probabilidades_placares.csv",
            key="probabilidades_placares_csv"
        )

# Chamar a função para executar o aplicativo
cs_page()
