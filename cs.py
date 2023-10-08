import streamlit as st
import pandas as pd
from scipy.stats import poisson

from session_state import SessionState

def cs_page():
    # Initialize the session state
    session_state = SessionState()

    # Set the user profile value after session state creation
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

    # Filter games with home odds between 1.40 and 2.4
    df = df[(df['FT_Odd_H'] >= 1.40) & (df['FT_Odd_H'] <= 2.4)]

    # Filter games with under 2.5 goals odds less than or equal to 2
    df = df[(df['FT_Odd_Under25'] <= 2)]

    # Scores for which you want to calculate the probability
    placares = ['0x0', '1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x1', '3x2', '3x3', '1x3', '2x3']

    # List to store the result rows
    linhas_resultados = []

    # Iterate over the games and calculate probabilities for each score
    for index, row in df.iterrows():
        # Calculate expected goal averages for each team and total expected
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

            # Apply zero-inflation adjustment for "odd" scores
            if (lambda_home < gols_home) or (lambda_away < gols_away):
                prob_placar = prob_home * prob_away * prob_total * 1.50
            else:
                prob_placar = prob_home * prob_away * prob_total

            total_prob += prob_placar
            probabilidades.append(prob_placar)

        # Normalize probabilities to sum up to 100%
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
            linha_resultado[placar] = round(probabilidades[i] * 100, 2)

        linhas_resultados.append(linha_resultado)

    # Create a new DataFrame with the results
    resultado_df = pd.DataFrame(linhas_resultados)

    # Initialize Streamlit app
    st.subheader("Probabilidade de Placar")

    # Sort the DataFrame by the highest probability score outcomes and select the top 8
    top_8_scores = resultado_df[placares].apply(lambda x: x.str.rstrip('%').astype(float)).max(axis=1).nlargest(8).index

    for index in top_8_scores:
        # Create a temporary DataFrame with probabilities for the current game
        prob_game_df = resultado_df[placares].iloc[[index]]

        # Select the most probable score
        placar_mais_provavel = prob_game_df.idxmax(axis=1).values[0]

        # Get the probability of the most probable score
        probabilidade_mais_provavel = prob_game_df.loc[index, placar_mais_provavel]

        # Check if the probability is greater than or equal to 16%
        if probabilidade_mais_provavel >= 16.0:
            # Display match details and odds
            details1 = f"**Hora:** {resultado_df.at[index, 'Hora']}  |  **Home:** {resultado_df.at[index, 'Home']}  |  **Away:** {resultado_df.at[index, 'Away']}"
            details2 = f"**Odd Casa:** {resultado_df.at[index, 'FT_Odd_H']} |  **Odd Empate:** {resultado_df.at[index, 'FT_Odd_D']} |  **Odd Visitante:** {resultado_df.at[index, 'FT_Odd_A']}"
            st.write(details1)
            st.write(details2)

            # Format and display the table
            formatted_df = prob_game_df.applymap(lambda x: f"{x:.1f}%")
            st.dataframe(formatted_df)

# Call the function to run the application
cs_page()
