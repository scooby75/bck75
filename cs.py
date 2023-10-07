import streamlit as st
import pandas as pd
from scipy.stats import poisson

def cs_page():
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
    placares = ['0x0', '1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x2', '3x3', '4x0', '4x1', '4x2', '4x3', '4x4', '5x0', '5x1', '5x2', '5x3']

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
            'Liga': row['Liga'],
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

    # Loop para exibir os detalhes e a tabela
    for index, row in resultado_df.iterrows():
        details1 = f"**Hora:** {row['Hora']}  |  **Home:** {row['Home']}  |  **Away:** {row['Away']}"
        details2 = f"**Odd Casa:** {row['FT_Odd_H']} |  **Odd Empate:** {row['FT_Odd_D']} |  **Odd Visitante:** {row['FT_Odd_A']}"
        st.write(details1)
        st.write(details2)

        # Criar um DataFrame temporário apenas com as probabilidades para o jogo atual
        prob_game_df = resultado_df[placares].iloc[[index]]

        # Selecionar os 6 placares mais prováveis
        top_placares = prob_game_df.T.nlargest(8, index)[index].index

        # Filtrar o DataFrame temporário para incluir apenas os 6 placares mais prováveis
        prob_game_df = prob_game_df[top_placares]

        # Formatar e exibir a tabela
        formatted_df = prob_game_df.applymap(lambda x: f"{x:.1f}%")
        st.dataframe(formatted_df)

# Chamar a função para executar o aplicativo
cs_page()



