import streamlit as st
import pandas as pd
import re

from session_state import SessionState

def goleada_page():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=3)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return   

    # Load the data
    def load_base(df):
        url = "https://github.com/scooby75/bdfootball/blob/main/Predict.csv?raw=true"
        df = pd.read_csv(url)  # Carregar os dados do CSV
        
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

        # Apply the function to extract the round number and create a new column "Rodada_Num"
        df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)

        return df

    # Função para extrair o número do texto "ROUND N"
    def extrair_numero_rodada(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

    # Call the load_base function to load the data
    df = load_base(df)  # Pass the df to the function

    # Filtrando os jogos com valores de "FT_Odd_H" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
    eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]

    # Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    eventos_raros_df = eventos_raros_df[colunas_desejadas]

    # Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Casa")
    st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
    st.dataframe(eventos_raros_df)

    ### Lay goleada Visitante @@@
    
    # Filtrando os jogos com valores de "FT_Odd_A" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
    eventos_raros2_df = df[(df["FT_Odd_A"] >= 1.71) & (df["FT_Odd_A"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]

    # Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    eventos_raros2_df = eventos_raros2_df[colunas_desejadas]

    # Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Visitante")
    st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
    st.dataframe(eventos_raros2_df)

# Chamar a função para iniciar o aplicativo
goleada_page()


    
