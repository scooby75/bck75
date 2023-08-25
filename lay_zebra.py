import streamlit as st
import pandas as pd
import re
from session_state import SessionState

def lay_zebra_page():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=2)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Carrega o dado
    url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
    df = pd.read_csv(url)
    
    # Convert the 'Hora' column to a datetime object
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert the game times to the local time zone (subtracting 3 hours)
    df['Time'] = df['Time'] - pd.to_timedelta('3 hours')

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

    # Função para extrair o número do texto "ROUND N"
    def extrair_numero_rodada(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

    # Apply the function to extract the round number and create a new column "Rodada_Num"
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
    st.subheader("Lay Zebra HT")
    st.text("Apostar em Lay visitante, Odd máxima 6")
    st.dataframe(layzebraht_df)

# Chamar a função para exibir a aplicação web
lay_zebra_page()

