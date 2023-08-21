import streamlit as st
import pandas as pd
import re

def lay_zebra_page():
    # Load Zebra HT Data
    st.subheader("Lay Zebra HT")
    st.text("Apostar em Lay visitante, Odd máxima 6")

    # URL for the CSV file
    url = "https://github.com/scooby75/bdfootball/blob/main/2023-08-22_Jogos_do_Dia_FS.csv?raw=true"
    
    # Load CSV data into a DataFrame
    df = pd.read_csv(url)
    
    # Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'ROUND': 'Rodada',
    }, inplace=True)
    
    # Function to extract round numbers from text
    def extrair_numero_rodada(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None
    
    # Apply the function to extract round numbers and create a new column "Rodada_Num"
    df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)
    
    # Filter matches with conditions
    layzebraht_df = df[
        (df["FT_Odd_H"] >= 1.01) & (df["FT_Odd_H"] <= 1.7) &
        (df["FT_Odd_A"] >= 5.5) & (df["FT_Odd_A"] <= 10) &
        (df["Rodada_Num"] >= 10)
    ]
    
    # Select desired columns: Date, Time, League, Home, and Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    layzebraht_df = layzebraht_df[colunas_desejadas]
    
    # Display the "Lay Zebra HT" DataFrame
    st.dataframe(layzebraht_df)

# Call the function to start the Streamlit app
lay_zebra_page()


    
