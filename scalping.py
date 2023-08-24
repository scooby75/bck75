import streamlit as st
import pandas as pd

def scalping_page():
    # Carregar arquivos CSV via URL
    url_jogosdodia = '/content/Jogos_do_Dia_FS.csv'
    url_momento_gol_home = '/content/scalping_home.csv'
    url_momento_gol_away = '/content/scalping_away.csv'

    jogosdodia = pd.read_csv(url_jogosdodia)
    momento_gol_home = pd.read_csv(url_momento_gol_home)
    momento_gol_away = pd.read_csv(url_momento_gol_away)

    # Filtrar jogos em que 0-15_mar e 0-15_sofri seja == 0 em ambos os DataFrames
    jogos_filtrados_home = jogosdodia.merge(momento_gol_home, left_on='Home', right_on='Equipe')
    jogos_filtrados_away = jogosdodia.merge(momento_gol_away, left_on='Away', right_on='Equipe')

    jogos_filtrados = jogos_filtrados_home.merge(jogos_filtrados_away, on=['Date', 'Home', 'Away'], suffixes=('_home', '_away'))

    filtered_games = jogos_filtrados[
        (jogos_filtrados['0_15_mar_home'] == 0) & (jogos_filtrados['0_15_sofri_home'] == 0) &
        (jogos_filtrados['0_15_mar_away'] == 0) & (jogos_filtrados['0_15_sofri_away'] == 0)
    ]

    # Selecionar colunas relevantes
    result_df = filtered_games[['Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home', 'FT_Odd_Over25_home']]

    # Renomear colunas
    result_df.columns = ['Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Over25']

    # Streamlit App
    st.title("Jogos Filtrados")
    st.dataframe(result_df)

# Call the function to start the Streamlit app
scalping_page()

