import streamlit as st
import pandas as pd
import re

def tips_page():
    # URL do arquivo CSV
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

        # Filtrando os jogos com valores de "FT_Odd_H" eh menor que 1.50 e "Round_Num" maior ou igual a 10
    lay0x2_df = df[(df["FT_Odd_H"] <= 1.50) & (df["Round_Num"] >= 10)]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    lay0x2_df = lay0x2_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("Lay 0x2")
    st.text("Apostar em Lay 0x2, Odd máxima 50")
    st.dataframe(lay0x2_df)

# Chamar a função para iniciar o aplicativo
tips_page()

    
