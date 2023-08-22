import pandas as pd
import numpy as np
import streamlit as st

def cs_page():
    # Load the CSV data from the URL into a DataFrame
    url = "https://github.com/scooby75/bdfootball/blob/main/bd%202019_2023%20com%20placar.csv?raw=true"
    bdgeral = pd.read_csv(url)

    # Calculate the average goals scored and conceded at home (Home)
    df_media_gols_home = bdgeral.groupby('Home').agg({'FT_Goals_H': 'mean', 'FT_Goals_A': 'mean'}).reset_index()
    df_media_gols_home.rename(columns={'FT_Goals_H': 'Mean_Goals_Home', 'FT_Goals_A': 'Mean_Goals_Away'}, inplace=True)

    # Calculate the average goals scored and conceded away from home (Away)
    df_media_gols_away = bdgeral.groupby('Away').agg({'FT_Goals_A': 'mean', 'FT_Goals_H': 'mean'}).reset_index()
    df_media_gols_away.rename(columns={'FT_Goals_A': 'Mean_Goals_Away', 'FT_Goals_H': 'Mean_Goals_Home'}, inplace=True)

    # Load the CSV data from another URL into a DataFrame
    url = "https://github.com/scooby75/bdfootball/blob/main/2023-08-22_Jogos_do_Dia_FS.csv?raw=true"
    jogosdodia = pd.read_csv(url)

    # Merge the filtered games with the calculated mean goals data
    jogos_filtrados = jogosdodia.merge(df_media_gols_home, left_on='Home', right_on='Home')
    jogos_filtrados = jogos_filtrados.merge(df_media_gols_away, left_on='Away', right_on='Away')

    # Function to calculate the probability of a certain number of goals using the Poisson distribution
    def poisson_prob(mean, k):
        return (np.exp(-mean) * mean ** k) / np.math.factorial(k)

    # List to store the results for display
    results = []

    # Predict the 6 most probable scores for each game
    for index, row in jogos_filtrados.iterrows():
        home_team = row['Home']
        away_team = row['Away']
        home_mean_goals = row['Mean_Goals_Home_x']
        away_mean_goals = row['Mean_Goals_Away_x']

        predicted_scores = []
        for home_goals in range(7):
            for away_goals in range(7):
                home_prob = poisson_prob(home_mean_goals, home_goals)
                away_prob = poisson_prob(away_mean_goals, away_goals)
                total_prob = home_prob * away_prob
                predicted_scores.append((home_goals, away_goals, total_prob))

        # Sort the predicted scores by probability in descending order
        predicted_scores.sort(key=lambda x: x[2], reverse=True)

        # Add the results to the list
        for i in range(6):
            results.append({'Jogo': f"{home_team} vs {away_team}",
                            'Placar': f"{predicted_scores[i][0]} - {predicted_scores[i][1]}",
                            'Probabilidade': predicted_scores[i][2]})

    # Display the results using Streamlit
    st.write(pd.DataFrame(results))

# Call the function to execute the app
cs_page()
