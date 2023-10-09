import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import poisson
from session_state import SessionState

def cs_page():
    # Initialize the session state
    session_state = SessionState()

    # Set the user_profile value after creating the instance
    session_state.user_profile = 2  # Or any other desired value

    # Check if the user has permission to access the page
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # URL of the CSV file with game data
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"
    df = pd.read_csv(url)

    # Define desired scores
    placares = [(i, j) for i in range(8) for j in range(8)]

    # Filter out matches that do not contain specific strings in the "Home" or "Away" columns
    df = df[~df['Home'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False) & ~df['Away'].str.contains(r'(U21|U19|U20|U16|U23|U18)', case=False)]

    # Initialize a list to store match information
    partidas_info = []

    # Calculate probabilities for each match using Poisson
    for index, row in df.iterrows():
        date = row['Date']
        hora = row['Hora']
        liga = row['Liga']
        home_team = row['Home']
        away_team = row['Away']
        odd_casa = row['FT_Odd_H']
        odd_empate = row['FT_Odd_D']
        odd_visitante = row['FT_Odd_A']

        # Calculate goal probabilities for each team
        prob_home = poisson.pmf(np.arange(0, 8), row['XG_Home'])
        prob_away = poisson.pmf(np.arange(0, 8), row['XG_Away'])

        # Calculate the probability of each possible score
        probabilidade_partida = np.outer(prob_home, prob_away)

        # Sort the scores based on probabilities
        placares_classificados = sorted(
            [(i, j, probabilidade_partida[i][j]) for i in range(8) for j in range(8)],
            key=lambda x: x[2],
            reverse=True
        )

        # Calculate the probability of score 1
        probabilidade_placar_1 = placares_classificados[0][2] * 100  # In percentage

        # Check if the probability of score 1 is between 15% and 21%
        if 15 <= probabilidade_placar_1 <= 21:
            # Store match information and probabilities
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
                probabilidade_percentual = round(probabilidade * 100, 2)  # Round to 2 decimal places and convert to percentage
                partida_info[f'Prob {idx + 1}'] = f"{i}x{j} ({probabilidade_percentual}%)"

            partidas_info.append(partida_info)

    # Create a DataFrame with match information
    partidas_df = pd.DataFrame(partidas_info)

    # Display the table with all information using st.dataframe
    st.subheader("Dutching CS")
    st.dataframe(partidas_df)

    # Export the DataFrame to a CSV file when the button is clicked
    if st.button("Export CSV"):
        # Export the DataFrame to a CSV file
        partidas_df.to_csv('dutching_cs.csv', index=False)
        st.write("Arquivo CSV gerado com sucesso.")

# Call the function to run the application
cs_page()

