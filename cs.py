import streamlit as st
import pandas as pd
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

    # Carregar os dados do arquivo CSV em um DataFrame
    df = pd.read_csv(url)

    # Filtrar jogos com round maior ou igual a 10
    df = df[df['Rodada'] >= 10]

    # Filtrar jogos com home menor ou igual a 1.90
    df = df[(df['FT_Odd_H'] >= 1.40) & (df['FT_Odd_H'] <= 2.4)]

    # Filtrar jogos com home menor ou igual a 1.90
    df = df[(df['FT_Odd_Under25'] <= 2)]

    # Placares para os quais você deseja calcular a probabilidade
    placares = ['1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x1', '3x2', '3x3', '1x3', '2x3']

    # Lista para armazenar as linhas dos resultados
    linhas_resultados = []

    # Iterar sobre os jogos e calcular as probabilidades para cada placar
    for index, row in df.iterrows():
        # Calcular as médias de gols esperados para cada time e o total esperado
        lambda_home = row['XG_Home']
        lambda_away = row['XG_Away']
        lambda_total = row['Average Goals']

        # Calcular as probabilidades usando a distribuição de Poisson
        probabilidades = []
        total_prob = 0  # Total de probabilidade para normalização

        for placar in placares:
            placar_split = placar.split('x')
            gols_home = int(placar_split[0])
            gols_away = int(placar_split[1])

            prob_home = poisson.pmf(gols_home, lambda_home)
            prob_away = poisson.pmf(gols_away, lambda_away)
            prob_total = poisson.pmf(gols_home + gols_away, lambda_total)

            # Aplicar o ajuste de zero inflado para placares "estranhos"
            if (lambda_home < gols_home) or (lambda_away < gols_away):
                prob_placar = prob_home * prob_away * prob_total * 1.50
            else:
                prob_placar = prob_home * prob_away * prob_total

            total_prob += prob_placar
            probabilidades.append(prob_placar)

        # Normalizar as probabilidades para que a soma seja 100%
        probabilidades = [prob / total_prob for prob in probabilidades]

        # Criar uma linha para o resultado deste jogo
        linha_resultado = {
            'Date': row['Date'],
            'Hora': row['Hora'],
            'Pais': row['Pais'],  # Adicionando a coluna "Pais"
            'Liga': row['Liga'],  # Adicionando a coluna "Liga"
            'Home': row['Home'],
            'Away': row['Away'],
            'FT_Odd_H': row['FT_Odd_H'],
            'FT_Odd_D': row['FT_Odd_D'],
            'FT_Odd_A': row['FT_Odd_A']
        }

        for i, placar in enumerate(placares):
            linha_resultado[placar] = round(probabilidades[i] * 100, 2)

        linhas_resultados.append(linha_resultado)

    # Criar um novo DataFrame com os resultados
    resultado_df = pd.DataFrame(linhas_resultados)

    # Iniciar aplicativo Streamlit
    st.subheader("Probabilidade de Placar")

    # Lista para armazenar os placares mais prováveis
    placares_provaveis = []

    # Loop para exibir os detalhes e a tabela apenas para jogos com probabilidade entre 14% e 20%
    for index, row in resultado_df.iterrows():
        # Criar um DataFrame temporário apenas com as probabilidades para o jogo atual
        prob_game_df = resultado_df[placares].iloc[[index]]

        # Selecionar os 6 placares mais prováveis em ordem decrescente de probabilidade
        top_scores = prob_game_df.iloc[0].nlargest(6)

        # Verificar se a probabilidade do placar mais provável está entre 14% e 20%
        if (top_scores.max() >= 14.0) and (top_scores.max() <= 20.0):
            details1 = f"**Hora:** {row['Hora']}  |  {row['Pais']} - {row['Liga']}  |  {row['Home']} vs {row['Away']}"
            details2 = f"**Odd Casa:** {row['FT_Odd_H']} |  **Odd Empate:** {row['FT_Odd_D']} |  **Odd Visitante:** {row['FT_Odd_A']}"
            
            # Formatar as probabilidades em porcentagem com número inteiro
            top_scores_formatted = top_scores.apply(lambda x: f"{int(x)}%")

            # Verificar se há algum "None" nas probabilidades
            if not top_scores_formatted.isnull().any():
                # Adicionar os placares mais prováveis a uma lista
                placares_provaveis.append(top_scores_formatted.to_frame(name=row['Home'] + ' vs ' + row['Away']))

    # Concatenar os DataFrames da lista em um único DataFrame com os placares como colunas
    if placares_provaveis:
        placares_df = pd.concat(placares_provaveis, axis=1)

        # Transpor o DataFrame para que os placares se tornem colunas
        placares_df = placares_df.transpose()

        # Formatar e exibir o DataFrame com os placares como colunas
        st.dataframe(placares_df)

# Chamar a função para executar o aplicativo
cs_page()
