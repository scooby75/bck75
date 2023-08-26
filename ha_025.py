import streamlit as st
import pandas as pd
import re

def ha_025_page():
    ##### HA -0.25 ######

    # Load the data
    #@st.cache_data(ttl=86400.0)  # 24 hours in seconds
    def load_base():
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
    df = load_base()

    # Filtrando os jogos 
    ha_df = df[
        (df["FT_Odd_H"] <= 1.90) &
        (df["DC_1X"] <= 1.25) &
        (df["HA"] <= 1.7) &
        (df["Rodada_Num"] >= 10)
    ]

    # Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    ha_df = ha_df[colunas_desejadas]

    # Exibir o dataframe "Eventos Raros"
    st.subheader("HA -0.25")
    st.text("Apostar em HA -0.25 casa, Odd minima 1.40")
    st.dataframe(ha_df)

# Chamar a função para iniciar o aplicativo
ha_025_page()

    

