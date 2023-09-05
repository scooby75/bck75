import pandas as pd
import numpy as np
import streamlit as st
import base64
import re

from io import BytesIO

from datetime import datetime, timedelta
from session_state import SessionState

# Função para carregar o CSV
@st.cache_data(ttl=21600.0)  # 06 hours in seconds
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
        'FT_Odd_Over25': 'FT_Odd_Over25',
        'FT_Odd_Under25': 'FT_Odd_Under25',
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

# Função principal para criar a página de dicas
def tips_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 1  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 1:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
    else:
        # Carregar o DataFrame uma vez no início
        df = load_base()

        # ##### PÁGINA BCK HOME ######
        tab0, tab1, tab2, tab3, tab4 = st.tabs(["HA", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "Scalping"])

        with tab0:
            # Use df aqui para a aba "HA"
            st.subheader("HA -0.25")
            st.text("Apostar em HA -0.25 casa, Odd mínima 1.40")
            ha_df = df[
                (df["FT_Odd_H"] <= 1.90) &
                (df["DC_1X"] <= 1.25) &
                (df["HA"] <= 1.7) &
                (df["Rodada_Num"] >= 10)
            ]
            colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
            ha_df = ha_df[colunas_desejadas]
            st.dataframe(ha_df,width=800)

            # Criar um link para download do CSV
            csv_link = ha_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link,
                file_name="handicap_asiatico.csv",
                key="handicap_asiatico_csv"
            )


        with tab1:
            # Use df aqui para a aba "Lay Goleada"
            st.subheader("Lay Goleada Casa")
            st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
            eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]
            colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
            eventos_raros_df = eventos_raros_df[colunas_desejadas]
            st.dataframe(eventos_raros_df,width=800)

            # Criar um link para download do CSV
            csv_link = eventos_raros_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link,
                file_name="Lay_Goleada_Casa.csv",
                key="lay_goleada_casa_csv"
            )

      
            st.subheader("Lay Goleada Visitante")
            st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
            eventos_raros2_df = df[(df["FT_Odd_A"] >= 1.71) & (df["FT_Odd_A"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]
            eventos_raros2_df = eventos_raros2_df[colunas_desejadas]
            st.dataframe(eventos_raros2_df,width=800)

            # Criar um link para download do CSV
            csv_link = eventos_raros2_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link,
                file_name="Lay_Goleada_Visitante.csv",
                key="lay_goleada_visitante_csv"
            )


        with tab2:
            # Use df aqui para a aba "Lay Zebra HT"
            st.subheader("Lay Zebra HT")
            st.text("Apostar em Lay visitante, Odd máxima 6")
            layzebraht_df = df[
                (df["FT_Odd_H"] >= 1.01) & (df["FT_Odd_H"] <= 1.7) &
                (df["FT_Odd_A"] >= 5.5) & (df["FT_Odd_A"] <= 10) &
                (df["Rodada_Num"] >= 10)
            ]
            colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
            layzebraht_df = layzebraht_df[colunas_desejadas]
            st.dataframe(layzebraht_df,width=800)

            # Criar um link para download do CSV
            csv_link = layzebraht_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link,
                file_name="lay_zebra_ht.csv",
                key="lay_zebra_ht_csv"
            )


        with tab3:
            # Use df aqui para a aba "Lay Zebra FT"
            st.subheader("Lay Zebra FT")
            st.text("Apostar em Lay visitante, Odd máxima 6")
            layzebraft_df = df[
                (df["FT_Odd_H"] >= 1.4) & (df["FT_Odd_H"] <= 2.1) &
                (df["FT_Odd_A"] >= 5) & (df["FT_Odd_A"] <= 10) &
                (df["Rodada_Num"] >= 10)
            ]
            colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
            layzebraft_df = layzebraft_df[colunas_desejadas]
            st.dataframe(layzebraft_df,width=800)

            # Criar um link para download do CSV
            csv_link = layzebraft_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link,
                file_name="lay_zebra_ft.csv",
                key="lay_zebra_ft_csv"
            )


        with tab4:
            # Definir URLs para os arquivos CSV
            url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true'
            url_momento_gol_home = 'https://github.com/scooby75/bdfootball/blob/main/scalping_home.csv?raw=true'
            url_momento_gol_away = 'https://github.com/scooby75/bdfootball/blob/main/scalping_away.csv?raw=true'

            try:
                # Carregar dados CSV
                jogosdodia = pd.read_csv(url_jogosdodia)
                momento_gol_home = pd.read_csv(url_momento_gol_home)
                momento_gol_away = pd.read_csv(url_momento_gol_away)

                # Lógica de mesclagem e filtragem de dados
                jogos_filtrados_home = jogosdodia.merge(momento_gol_home, left_on='Home', right_on='Equipe')
                jogos_filtrados_away = jogosdodia.merge(momento_gol_away, left_on='Away', right_on='Equipe')
                jogos_filtrados = jogos_filtrados_home.merge(jogos_filtrados_away, on=['Date', 'Home', 'Away'], suffixes=('_home', '_away'))

                # Filtrar jogos com critérios específicos
                filtered_games = jogos_filtrados[
                    (jogos_filtrados['0_15_mar_home'] == 0) & (jogos_filtrados['0_15_sofri_home'] == 0) &
                    (jogos_filtrados['0_15_mar_away'] == 0) & (jogos_filtrados['0_15_sofri_away'] == 0)
                ]

                # Filtrar jogos com critérios específicos
                filtered_games = jogos_filtrados[
                    (jogos_filtrados['FT_Odd_H_home'] >= 1.70) & (jogos_filtrados['FT_Odd_Over25_home'] >= 2.02) 
                ]

                # Selecionar colunas relevantes e renomear
                result_df = filtered_games[['Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home', 'FT_Odd_Over25_home']]
                result_df.columns = ['Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Over25']

                # Streamlit App
                st.subheader("Lay Over 25FT")
                st.text("Apostar em Lay Over 25FT e fechar posição com 3% ou 5min de exposição.")
                st.dataframe(result_df,width=800)

                # Criar um link para download do CSV
                csv_link = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Baixar CSV",
                    data=csv_link,
                    file_name="scalping.csv",
                    key="scalping_csv"
                )


            except Exception as e:
                st.error("Ocorreu um erro: " + str(e))

# Chama a função tips_page() no início do código para criar a página
tips_page()
