import pandas as pd
import numpy as np
import streamlit as st
import base64
import re
import datetime as dt
import requests
import csv
import io

from datetime import datetime
from my_token import github_token

from io import StringIO
from io import BytesIO
from datetime import datetime, timedelta
from session_state import SessionState

# Função para carregar o CSV
@st.cache_data(ttl=21600.0)  # 06 horas em segundos
def load_base():
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"
    df = pd.read_csv(url)

    # Excluir linhas em que 'Home' ou 'Away' contenham substrings específicas
    substrings_para_excluir = ['U16', 'U17', 'U18', 'U19', 'U20', '21', 'U22', 'U23']
    mask = ~df['Home'].str.contains('|'.join(substrings_para_excluir), case=False) & \
           ~df['Away'].str.contains('|'.join(substrings_para_excluir), case=False)
    df = df[mask]

    # Excluir linhas em que 'League' contenha 'WOMEN'
    substring_para_excluir = 'WOMEN'
    mask = ~df['Liga'].str.contains(substring_para_excluir, case=False)
    df = df[mask]

    return df

# Função principal para criar a página de dicas
def tips_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Define o valor de user_profile após a criação da instância
    session_state.user_profile = 1  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 1:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
    else:
        # Carregar o DataFrame uma vez no início
        df = load_base()

        # ##### PÁGINA BCK HOME ######
        tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Resultados", "HA", "Back Casa HT", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "BTTS Sim", "Scalping"])

        with tab1:
            # Use df aqui para a aba "HA"
            st.subheader("HA -0.25")
            st.text("Apostar em HA -0.25 casa, Odd mínima 1.40")
            ha_df = df[
                (df["FT_Odd_H"] >= 1.40) & (df["FT_Odd_H"] <= 2.00) & 
                (df["DC_1X"] <= 1.3) &
                (df["PPG_Home"] >= 1.8) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            ha_df = ha_df[colunas_desejadas]
            st.dataframe(ha_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_ha = ha_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_ha,
                file_name=f"handicap_asiatico_{data_atual}.csv",
                key="handicap_asiatico_csv"
            )

        with tab2:
            # Use df aqui para a aba "Back Casa HT"
            st.subheader("Back Casa HT")
            st.text("Apostar em Back Casa HT, Odd Mínima 1.90")
            back_casa_ht = df[
                (df["FT_Odd_H"] >= 1.01) & (df["FT_Odd_H"] <= 1.7) &
                (df["FT_Odd_A"] >= 5.5) & (df["FT_Odd_A"] <= 10) &
                (df["PPG_Home"] >= 1.8) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            back_casa_ht = back_casa_ht[colunas_desejadas]
            st.dataframe(back_casa_ht, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_back_casa_ht = back_casa_ht.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_back_casa_ht,
                file_name=f"back_casa_ht_{data_atual}.csv",
                key="back_casa_ht_csv"
            )

        with tab3:
            # Use df aqui para a aba "Lay Goleada"
            st.subheader("Lay Goleada")
            st.text("Apostar em Lay Goleada, Odd Máxima 4.0")
            lay_goleada = df[
                (df["FT_Odd_H"] >= 1.10) & (df["FT_Odd_H"] <= 2.00) &
                (df["FT_Odd_A"] >= 1.10) & (df["FT_Odd_A"] <= 2.00) &
                (df["PPG_Home"] >= 2) & (df["PPG_Away"] >= 2) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            lay_goleada = lay_goleada[colunas_desejadas]
            st.dataframe(lay_goleada, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_lay_goleada = lay_goleada.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_lay_goleada,
                file_name=f"lay_goleada_{data_atual}.csv",
                key="lay_goleada_csv"
            )

        with tab4:
            # Use df aqui para a aba "Lay Zebra HT"
            st.subheader("Lay Zebra HT")
            st.text("Apostar em Lay Zebra HT, Odd Máxima 6.0")
            lay_zebra_ht = df[
                (df["FT_Odd_H"] >= 1.10) & (df["FT_Odd_H"] <= 3.00) &
                (df["FT_Odd_A"] >= 1.10) & (df["FT_Odd_A"] <= 3.00) &
                (df["PPG_Home"] <= 1.2) & (df["PPG_Away"] <= 1.2) &
                (df["HTHG"] <= 0.5) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            lay_zebra_ht = lay_zebra_ht[colunas_desejadas]
            st.dataframe(lay_zebra_ht, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_lay_zebra_ht = lay_zebra_ht.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_lay_zebra_ht,
                file_name=f"lay_zebra_ht_{data_atual}.csv",
                key="lay_zebra_ht_csv"
            )

        with tab5:
            # Use df aqui para a aba "Lay Zebra FT"
            st.subheader("Lay Zebra FT")
            st.text("Apostar em Lay Zebra FT, Odd Máxima 6.0")
            lay_zebra_ft = df[
                (df["FT_Odd_H"] >= 1.10) & (df["FT_Odd_H"] <= 3.00) &
                (df["FT_Odd_A"] >= 1.10) & (df["FT_Odd_A"] <= 3.00) &
                (df["PPG_Home"] <= 1.2) & (df["PPG_Away"] <= 1.2) &
                (df["HTHG"] <= 1.5) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            lay_zebra_ft = lay_zebra_ft[colunas_desejadas]
            st.dataframe(lay_zebra_ft, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_lay_zebra_ft = lay_zebra_ft.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_lay_zebra_ft,
                file_name=f"lay_zebra_ft_{data_atual}.csv",
                key="lay_zebra_ft_csv"
            )

        with tab6:
            # Use df aqui para a aba "BTTS Sim"
            st.subheader("BTTS Sim")
            st.text("Apostar em BTTS Sim, Odd Mínima 1.60")
            btts_sim = df[
                (df["FT_Odd_BTTS_Yes"] >= 1.60) &
                (df["PPG_Home"] >= 1.2) & (df["PPG_Away"] >= 1.2) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            btts_sim = btts_sim[colunas_desejadas]
            st.dataframe(btts_sim, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_btts_sim = btts_sim.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_btts_sim,
                file_name=f"btts_sim_{data_atual}.csv",
                key="btts_sim_csv"
            )

if __name__ == '__main__':
    tips_page()
