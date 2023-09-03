# bck_home.py

import pandas as pd
import numpy as np
import streamlit as st
import base64
import re

from datetime import datetime, timedelta  
from session_state import SessionState

def tips_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    ##### PÁGINA BCK HOME ######
    tab0, tab1, tab2, tab3, tab4 = st.tabs(["HA", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "Scalping"])

    with tab0:
        @st.cache_data(ttl=86400.0)  # 24 hours in seconds
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
        st.text("Apostar em HA -0.25 casa, Odd mínima 1.40")
        st.dataframe(ha_df)

    with tab1:
        # Import statements for tab1
        import streamlit as st
        import pandas as pd
        import re

        # Classe de gerenciamento de estado da sessão
        class SessionState:
            def __init__(self):
                self.user_profile = 3

        # Função para extrair o número do texto "ROUND N"
        def extrair_numero_rodada(text):
            if isinstance(text, int):
                return text
            match = re.search(r'\d+', text)
            if match:
                return int(match.group())
            return None

        def load_base():
            url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
            df = pd.read_csv(url)  # Carregar os dados do CSV

            # Converter a coluna 'Date' para um objeto de data
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Converter a coluna 'Time' para um objeto de hora
            df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

            # Subtrair 3 horas da coluna 'Time'
            df['Time'] = df['Time'] - pd.DateOffset(hours=3)

            # Formatar a coluna 'Time' no formato HH:MM
            df['Time'] = df['Time'].dt.strftime('%H:%M')

            # Rename the columns
            df.rename(columns={
                'FT_Odd_H': 'FT_Odd_H',
                'FT_Odd_D': 'FT_Odd_D',
                'FT_Odd_A': 'FT_Odd_A',
                'FT_Odd_Over25': 'FT_Odd_Over25',
                'FT_Odd_Under25': 'FT_Odd_Under25',
                'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',        
                'ROUND': 'Rodada',
                'Time': 'Hora',
            }, inplace=True)

            # Apply the function to extract the round number and create a new column "Rodada_Num"
            df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)

            return df

        def goleada_page():
            # Inicializa o estado da sessão
            session_state = SessionState()

            # Verifica se o usuário tem permissão para acessar a página
            if session_state.user_profile < 3:
                st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
                return

            # Load the data
            df = load_base()

            # Filtrando os jogos com valores de "FT_Odd_H" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
            eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]

            # Exibir o dataframe "Eventos Raros"
            st.subheader("Lay Goleada Casa")
            st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
            display_columns = ["Date", "Hora", "League", "Home", "Away"]  # Columns to display
            st.dataframe(eventos_raros_df[display_columns])

            # Filtrando os jogos com valores de "FT_Odd_A" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
            eventos_raros2_df = df[(df["FT_Odd_A"] >= 1.71) & (df["FT_Odd_A"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]

            # Exibir o dataframe "Eventos Raros"
            st.subheader("Lay Goleada Visitante")
            st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
            st.dataframe(eventos_raros2_df[display_columns])

    with tab2:
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
            'FT_Odd_Over25': 'FT_Odd_Over25',
            'FT_Odd_Under25': 'FT_Odd_Under25',
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

    with tab3:
        # Load the data
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

        # Call the load_base function to load the data
        df = load_base()

        # Filtrando os jogos com valores de "FT_Odd_H" eh menor que 1.50 e "Round_Num" maior ou igual a 10
        layzebraft_df = df[
            (df["FT_Odd_H"] >= 1.4) & (df["FT_Odd_H"] <= 2.1) &
            (df["FT_Odd_A"] >= 5) & (df["FT_Odd_A"] <= 10) &
            (df["Rodada_Num"] >= 10)
        ]

        # Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
        colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
        layzebraft_df = layzebraft_df[colunas_desejadas]

        # Exibir o dataframe "Lay Zebra FT"
        st.subheader("Lay Zebra FT")
        st.text("Apostar em Lay visitante, Odd máxima 6")
        st.dataframe(layzebraft_df)

# Execute a função para criar a página
tips_page()
