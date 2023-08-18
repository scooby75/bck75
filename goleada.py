import streamlit as st
import pandas as pd
import re

def goleada_page():
    # URL do arquivo CSV
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

    # Carregar o arquivo CSV em um dataframe
    df = pd.read_csv(url)

    # Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'Rodada': 'Round',
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

    # Filtrando os jogos com valores de "FT_Odd_H" entre 1.40 e 2.0 e "Round_Num" maior ou igual a 10
    eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Round_Num"] >= 10)]

    # Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    eventos_raros_df = eventos_raros_df[colunas_desejadas]

    # Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Casa")
    st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
    st.dataframe(eventos_raros_df)

    # ... Repetir o padrão para outras seções ...

# Chamar a função para iniciar o aplicativo
tips_page()

    
