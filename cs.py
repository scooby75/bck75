import streamlit as st
import pandas as pd
from scipy.stats import poisson

def calculate_probabilities(row):
    lambda_home = row['XG_Home_Pre']
    lambda_away = row['XG_Away_Pre']
    
    placares = ['0x0', '1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x2', '3x3', '4x0', '4x1', '4x2', '4x3', '4x4', '5x0', '5x1', '5x2', '5x3']

    probabilidades = []
    total_prob = 0

    for placar in placares:
        gols_home, gols_away = map(int, placar.split('x'))

        prob_home = poisson.pmf(gols_home, lambda_home)
        prob_away = poisson.pmf(gols_away, lambda_away)

        if (lambda_home < gols_home) or (lambda_away < gols_away):
            prob_placar = prob_home * prob_away * 0.7
        else:
            prob_placar = prob_home * prob_away 

        total_prob += prob_placar
        probabilidades.append(prob_placar)

    probabilidades = [prob / total_prob for prob in probabilidades]
    return probabilidades

def main():
    st.subheader("Probabilidade de Placar")
    
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return
    
    df = df[df['Rodada'] >= 10]
    df = df[(df['FT_Odds_H'] >= 2) & (df['FT_Odds_A'] >= 2)]
     
    # Filtrar jogos com home menor ou igual a 1.80
    df = df[(df['FT_Odds_Under25'] <= 1.80)]

    # Filtrar jogos com XG entre 1 e 1.6
    df = df[(df['XG_Home_Pre'] >= 1) & (df['XG_Home_Pre'] <= 1.6)]
    df = df[(df['XG_Away_Pre'] >= 1) & (df['XG_Away_Pre'] <= 1.6)]

    st.write("Exibindo as probabilidades para os jogos selecionados:")
    for index, row in df.iterrows():
        probabilidades = calculate_probabilities(row)

        st.write(f"**Hora:** {row['Time']} | **Home:** {row['Home']} | **Away:** {row['Away']}")
        st.write(f"**Odd Casa:** {row['FT_Odds_H']} | **Odd Empate:** {row['FT_Odds_D']} | **Odd Visitante:** {row['FT_Odds_A']}")

        prob_game_df = pd.DataFrame([probabilidades], columns=placares)
        top_placares = prob_game_df.T.nlargest(8, 0)[0].index
        prob_game_df = prob_game_df[top_placares]

        formatted_df = prob_game_df.applymap(lambda x: f"{x * 100:.1f}%")
        st.dataframe(formatted_df)

if __name__ == "__main__":
    main()

