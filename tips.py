import pandas as pd
import numpy as np
import streamlit as st
import base64
import re
import datetime as dt

from io import BytesIO

from datetime import datetime, timedelta
from session_state import SessionState

# Função para carregar o CSV
@st.cache_data(ttl=21600.0)  # 06 hours in seconds
def load_base():
    url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
    df = pd.read_csv(url)


    # Exclude rows where 'Home' or 'Away' contains specific substrings
    substrings_to_exclude = ['U16', 'U17', 'U18', 'U19', 'U20', '21', 'U22', 'U23']
    mask = ~df['Home'].str.contains('|'.join(substrings_to_exclude), case=False) & \
           ~df['Away'].str.contains('|'.join(substrings_to_exclude), case=False)
    df = df[mask]

    # Exclude rows where 'League' contains 'WOMEN'
    substring_to_exclude = 'WOMEN'
    mask = ~df['League'].str.contains(substring_to_exclude, case=False)
    df = df[mask]

    return df


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
                (df["FT_Odd_H"] <= 1.70) &
                (df["DC_1X"] <= 1.3) &
                (df["Rodada"] >= 10)
                
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
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
            eventos_raros_df = df[(df["FT_Odd_H"] >= 2) & (df["FT_Odd_H"] <= 5) & (df["FT_Odd_Over25"] >= 2.30) & (df["FT_Odd_BTTS_Yes"] <= 2) & (df["Rodada"] >= 10)]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
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
            eventos_raros2_df = df[(df["FT_Odd_A"] >= 2) & (df["FT_Odd_A"] <= 5) & (df["FT_Odd_Over25"] >= 2.30) & (df["FT_Odd_BTTS_Yes"] >= 2) & (df["Rodada"] >= 10)]
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
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
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
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
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
                    (jogos_filtrados['FT_Odd_H'] >= 1.70) & (jogos_filtrados['FT_Odd_Over25'] >= 2.02) 
                ]

                # Selecionar colunas relevantes e renomear
                result_df = filtered_games[['Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Over25']]
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
