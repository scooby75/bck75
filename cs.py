import streamlit as st
import pandas as pd
from scipy.stats import poisson

from session_state import SessionState

def cs_page():
    # ... Código anterior ...

    # Criar um DataFrame vazio para armazenar as probabilidades de placar
    resultado_df = pd.DataFrame(columns=placares)

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

        # Adicionar as probabilidades deste jogo como uma nova linha no DataFrame
        resultado_df.loc[index] = probabilidades

    # Adicionar colunas de informações do jogo ao DataFrame resultado_df
    resultado_df['Hora'] = df['Hora']
    resultado_df['Home'] = df['Home']
    resultado_df['Away'] = df['Away']
    resultado_df['FT_Odd_H'] = df['FT_Odd_H']
    resultado_df['FT_Odd_D'] = df['FT_Odd_D']
    resultado_df['FT_Odd_A'] = df['FT_Odd_A']

    # Iniciar aplicativo Streamlit
    st.subheader("Probabilidade de Placar")

    # Exibir as informações dos jogos em colunas
    for index, row in resultado_df.iterrows():
        st.write(f"**Hora:** {row['Hora']}  |  **Home:** {row['Home']}  |  **Away:** {row['Away']}")
        st.write(f"**Odd Casa:** {row['FT_Odd_H']} |  **Odd Empate:** {row['FT_Odd_D']} |  **Odd Visitante:** {row['FT_Odd_A']}")

        # Formatar e exibir as probabilidades de placar em colunas
        formatted_df = pd.DataFrame(row[placares], index=placares, columns=['Probabilidade'])
        formatted_df['Probabilidade'] = formatted_df['Probabilidade'].apply(lambda x: f"{x*100:.2f}%")
        st.dataframe(formatted_df)

# Chamar a função para executar o aplicativo
cs_page()
