import streamlit as st
import pandas as pd
from scipy.stats import poisson
from session_state import SessionState
from datetime import datetime
import io

def cs_page():
    # Initialize session state
    session_state = SessionState()

    # Set the user profile value after creating the instance
    session_state.user_profile = 2  # Or any other desired value

    # Check if the user has permission to access the page
    if session_state.user_profile < 2:
        st.error("You do not have permission to access this page. Please upgrade your plan!!")
        return

    # URL of the CSV file with match data
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"

    # Load data from the CSV file into a DataFrame
    df = pd.read_csv(url)

    # Filter out games with 'Liga' containing 'Reserve' or 'Women'
    df = df[~df['Liga'].str.contains('Reserve|Women', case=False)]

    # Define a list of substrings to check for in 'Home' and 'Away' columns
    exclude_substrings = ['U16', 'U17', 'U18', 'U19', 'U20', 'U21']

    # Filter out games with 'Home' or 'Away' containing any of the specified substrings
    df = df[~df['Home'].str.contains('|'.join(exclude_substrings), case=False) & ~df['Away'].str.contains('|'.join(exclude_substrings), case=False)]

    # Specify the score outcomes to calculate probabilities for
    placares = ['1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2']

    # List of dictionaries to store the results of all the day's matches
    linhas_resultados = []

    # Iterate over the matches and calculate probabilities for each score outcome
    for index, row in df.iterrows:
        # ... (rest of your code, calculating probabilities and storing results)

    # Continue with the rest of your code

# Call the function to run the application
cs_page()
