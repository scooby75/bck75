import streamlit as st
import pandas as pd
from scipy.stats import poisson

from session_state import SessionState

def cs_page():
    # Initialize session state
    session_state = SessionState()

    # Set the user_profile value after creating the instance
    session_state.user_profile = 2  # Or any other desired value

    # Check if the user has permission to access the page
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # URL of the CSV file with game data
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"

    # Load data from the CSV file into a DataFrame
    df = pd.read_csv(url)

    # Filter games with round greater than or equal to 10
    df = df[df['Rodada'] >= 10]

    # Filter games with home odds less than or equal to 1.90
    df = df[(df['FT_Odd_H'] >= 1.80) & (df['FT_Odd_A'] >= 1.80) & (df['FT_Odd_Under25'] <= 2)]

    # Scores for which you want to calculate the probability
    placares = ['1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x1', '3x2', '3x3', '1x3', '2x3']

    # List to store the result rows
    linhas_resultados = []

    # Iterate over the games and calculate probabilities for each score
    for index, row in df.iterrows():
        # Calculate expected goal averages for each team and the total expected goals
        lambda_home = row['XG_Home']
        lambda_away = row['XG_Away']
        lambda_total = row['Average Goals']

        # Calculate probabilities using the Poisson distribution
        probabilidades = []
        total_prob = 0  # Total probability for normalization

        for placar in placares:
            placar_split = placar.split('x')
            gols_home = int(placar_split[0])
            gols_away = int(placar_split[1])

            prob_home = poisson.pmf(gols_home, lambda_home)
            prob_away = poisson.pmf(gols_away, lambda_away)
            prob_total = poisson.pmf(gols_home + gols_away, lambda_total)

            # Apply zero-inflation adjustment for "strange" scores
            if (lambda_home < gols_home) or (lambda_away < gols_away):
                prob_placar = prob_home * prob_away * prob_total * 1.50
            else:
                prob_placar = prob_home * prob_away * prob_total

            total_prob += prob_placar
            probabilidades.append(prob_placar)

        # Normalize probabilities so that the sum is 100%
        probabilidades = [prob / total_prob for prob in probabilidades]

        # Create a row for the result of this game
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
            linha_resultado[f'{placar} (Probabilidade)'] = f'{round(probabilidades[i] * 100, 2)}%'

        linhas_resultados.append(linha_resultado)

    # Create a new DataFrame with the results
    resultado_df = pd.DataFrame(linhas_resultados)

    # Start the Streamlit application
    st.subheader("Dutching CS")

    # Loop to display details and the table only for games with probability between 14% and 20%
    for index, row in resultado_df.iterrows():
        # Create a temporary DataFrame with probabilities for the current game only
        prob_game_df = resultado_df[placares].iloc[[index]]

        # Select the most likely scores in descending order of probability
        top_scores = prob_game_df.iloc[0].nlargest(8)

        # Check if the probability of the most likely score is between 14% and 20%
        if (top_scores.max() >= 14.0) and (top_scores.max() <= 20.0):
            details1 = f"**Hora:** {row['Hora']}  |  **Partida:** {row['Home']} vs {row['Away']}"
            details2 = f"**Odd Casa:** {row['FT_Odd_H']} |  **Odd Empate:** {row['FT_Odd_D']} |  **Odd Visitante:** {row['FT_Odd_A']}"
            st.write(details1)
            st.write(details2)

            # Transpose the DataFrame to display probabilities in columns
            formatted_df = top_scores.to_frame(name='Probabilidade')
            formatted_df = formatted_df.transpose()  # Transpose the DataFrame
            formatted_df.columns = [f"{placar} (Probabilidade)" for placar in formatted_df.columns]

            # Display score along with probability
            scores_and_probs = formatted_df.columns.tolist()
            st.write(scores_and_probs)

            st.dataframe(formatted_df)

# Call the function to run the Streamlit application
cs_page()
