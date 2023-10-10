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
    df = pd.read_csv(url)

    # Definir os placares desejados
    placares = [(i, j) for i in range(8) for j in range(8)]

    # Filtrar partidas que não contenham as strings "U21", "U19", "U20", "U16", "U23" ou "U18" nas colunas "Home" ou "Away"
    df = df[~df['Home'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False) & ~df['Away'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False)]

    # Inicializar uma lista para armazenar as informações das partidas
    partidas_info = []

    # Calcular as probabilidades para cada partida usando Poisson
    for index, row in df.iterrows():
        date = row['Date']
        hora = row['Hora']
        liga = row['Liga']
        home_team = row['Home']
        away_team = row['Away']
        odd_casa = row['FT_Odd_H']
        odd_empate = row['FT_Odd_D']
        odd_visitante = row['FT_Odd_A']

        # Calcular as probabilidades de gols para cada equipe
        prob_home = poisson.pmf(np.arange(0, 8), row['XG_Home'])
        prob_away = poisson.pmf(np.arange(0, 8), row['XG_Away'])

        # Calcular a probabilidade de cada placar possível
        probabilidade_partida = np.outer(prob_home, prob_away)

        # Classificar os placares com base nas probabilidades
        placares_classificados = sorted(
            [(i, j, probabilidade_partida[i][j]) for i in range(8) for j in range(8)],
            key=lambda x: x[2],
            reverse=True
        )

        # Calcular a probabilidade do placar 1
        probabilidade_placar_1 = placares_classificados[0][2] * 100  # Em porcentagem

        # Verificar se a probabilidade do placar 1 está entre 15% e 21%
        if 15 <= probabilidade_placar_1 <= 21:
            # Armazenar as informações da partida e probabilidades
            partida_info = {
                'Date': date,
                'Hora': hora,
                'Liga': liga,
                'Home': home_team,
                'Away': away_team,
                'Odd Casa': odd_casa,
                'Odd Empate': odd_empate,
                'Odd Visitante': odd_visitante,
            }

            for idx, (i, j, probabilidade) in enumerate(placares_classificados[:8]):
                probabilidade_percentual = round(probabilidade * 100, 2)  # Arredonda para 2 casas decimais e converte em porcentagem
                partida_info[f'Prob {idx + 1}'] = f"{i}x{j} ({probabilidade_percentual}%)"

            partidas_info.append(partida_info)

    # Criar um DataFrame com as informações das partidas
    partidas_df = pd.DataFrame(partidas_info)

    # Exibir a tabela com todas as informações usando st.dataframe
    st.subheader("Dutching CS ")
    st.dataframe(partidas_df)

    # Exportar o DataFrame para um arquivo CSV
    partidas_df.to_csv('dutching_cs.csv', index=False)

    st.write("Arquivo CSV gerado com sucesso.")

# Chamar a função para executar o aplicativo
cs_page()
