import streamlit as st
import pandas as pd
import re

def ha_025_page():

##### HA -0,25 ######

    # URL to the CSV file
    #url = "https://github.com/futpythontrader/YouTube/blob/main/Jogos_do_Dia_FlashScore/2023-08-03_Jogos_do_Dia_FlashScore.csv?raw=true"
    url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"

    # Load the CSV data from the URL into a DataFrame
    df = pd.read_csv(url)

    # Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'ROUND': 'Round',
    }, inplace=True)

# Função para extrair o número do texto "ROUND N"
    def extrair_numero_round(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

# Aplicando a função para extrair o número do "Round" e criando uma nova coluna "Round_Num"
    df["Round_Num"] = df["Round"].apply(extrair_numero_round)

    
# Filtrando os jogos 
    ha_df = df[
        (df["FT_Odd_H"] <= 1.90) &
        (df["DC_1X"] <= 1.30) &
        (df["HA"] <= 1.7) &
        (df["Round_Num"] >= 10)
    ]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    ha_df = ha_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("HA -0.25")
    st.text("Apostar em HA -0.25 casa, Odd minima 1.50")
    st.dataframe(ha_df)

# Chamar a função para iniciar o aplicativo
ha_025_page()

    

