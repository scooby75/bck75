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
        tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["HA", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "BTTS Sim", "Scalping", "Resultados"])

        with tab0:
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

        with tab1:
            # Use df aqui para a aba "Lay Goleada Casa"
            st.subheader("Lay Goleada Casa")
            st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
            eventos_raros_df = df[(df["FT_Odd_H"] >= 2) & (df["FT_Odd_H"] <= 5) & (df["FT_Odd_Over25"] >= 2.30) & (df["FT_Odd_BTTS_Yes"] <= 2) & (df["Rodada"] >= 10)]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            eventos_raros_df = eventos_raros_df[colunas_desejadas]
            st.dataframe(eventos_raros_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_goleada_casa = eventos_raros_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_goleada_casa,
                file_name=f"lay_goleada_casa_{data_atual}.csv",
                key="lay_goleada_casa_csv"
            )

            st.subheader("Lay Goleada Visitante")
            st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
            eventos_raros2_df = df[(df["FT_Odd_A"] >= 2) & (df["FT_Odd_A"] <= 5) & (df["FT_Odd_Over25"] >= 2.30) & (df["FT_Odd_BTTS_Yes"] >= 2) & (df["Rodada"] >= 10)]
            eventos_raros2_df = eventos_raros2_df[colunas_desejadas]
            st.dataframe(eventos_raros2_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_goleada_visitante = eventos_raros2_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_goleada_visitante,
                file_name=f"lay_goleada_visitante_{data_atual}.csv",
                key="lay_goleada_visitante_csv"
            )

        with tab2:
            # Use df aqui para a aba "Lay Zebra HT"
            st.subheader("Lay Zebra HT")
            st.text("Apostar em Lay visitante, Odd máxima 6")
            layzebraht_df = df[
                (df["FT_Odd_H"] >= 1.01) & (df["FT_Odd_H"] <= 1.7) &
                (df["FT_Odd_A"] >= 5.5) & (df["FT_Odd_A"] <= 10) &
                (df["PPG_Home"] >= 1.7) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            layzebraht_df = layzebraht_df[colunas_desejadas]
            st.dataframe(layzebraht_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_zebra_ht = layzebraht_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_zebra_ht,
                file_name=f"lay_zebra_ht_{data_atual}.csv",
                key="lay_zebra_ht_csv"
            )

        with tab3:
            # Use df aqui para a aba "Lay Zebra FT"
            st.subheader("Lay Zebra FT")
            st.text("Apostar em Lay visitante, Odd máxima 6")
            layzebraft_df = df[
                (df["FT_Odd_H"] >= 1.4) & (df["FT_Odd_H"] <= 2.1) &
                (df["FT_Odd_A"] >= 5) & (df["FT_Odd_A"] <= 10) &
                (df["PPG_Home"] >= 1.7) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            layzebraft_df = layzebraft_df[colunas_desejadas]
            st.dataframe(layzebraft_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_zebra_ft = layzebraft_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_zebra_ft,
                file_name=f"lay_zebra_ft_{data_atual}.csv",
                key="lay_zebra_ft_csv"
            )

        with tab4:
            # Use df aqui para a aba "BTTS Sim"
            st.subheader("BTTS Sim")
            st.text("Apostar em Ambas Marcam Sim, Odd minima 1.6")
            btts_yes_df = df[
                (df["FT_Odd_Over25"] <= 1.7) & 
                (df["FT_Odd_BTTS_Yes"] <= 1.7) &
                (df["XG_Home"] >= 1.2) & 
                (df["XG_Away"] >= 1.2) &
                (df["Rodada"] >= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Liga", "Home", "Away"]
            btts_yes_df = btts_yes_df[colunas_desejadas]
            st.dataframe(btts_yes_df, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_link_btts = btts_yes_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_link_btts,
                file_name=f"btts_yes_{data_atual}.csv",
                key="btts_yes_csv"
            )

        with tab5:
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
                    (jogos_filtrados['0_15_mar_away'] == 0) & (jogos_filtrados['0_15_sofri_away'] == 0) &
                    (jogos_filtrados['FT_Odd_H_home'] >= 1.70) & (jogos_filtrados['FT_Odd_Over25_home'] >= 2.02) &
                    (jogos_filtrados['FT_Odd_H_away'] >= 1.70) & (jogos_filtrados['FT_Odd_Over25_away'] >= 2.02)
                ]

                # Selecionar colunas relevantes e renomear
                result_df = filtered_games[['Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home', 'FT_Odd_Over25_home',
                                            'FT_Odd_H_away', 'FT_Odd_A_away', 'FT_Odd_Over25_away']]
                result_df.columns = ['Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home', 'FT_Odd_Over25_home',
                                     'FT_Odd_H_away', 'FT_Odd_A_away', 'FT_Odd_Over25_away']

                # Streamlit App
                st.subheader("Lay Over 25FT")
                st.text("Apostar em Lay Over 25FT e fechar posição com 3% ou 5min de exposição.")
                st.dataframe(result_df, width=800)

                # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
                data_atual = datetime.now().strftime("%d-%m-%Y")

                # Criar um link para download do CSV
                csv_link_scalping = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Baixar CSV",
                    data=csv_link_scalping,
                    file_name=f"scalping_{data_atual}.csv",
                    key="scalping_csv"
                )

            except Exception as e:
                st.error("Ocorreu um erro: " + str(e))

        with tab6:
 

            # URL do arquivo Excel
            url = "https://github.com/scooby75/bdfootball/raw/main/tips_ha_geral.xltx"

            # Use a função read_excel do pandas para ler o arquivo Excel da URL
            df = pd.read_excel(url)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = df['Profit'].sum()
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Resultado HA -0,25")
            st.text("A partir de 16/09/2023")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)

############### Lay Goleada Casa ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_lay_goleada_casa_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = df['Profit'].sum()
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Lay Goleada Casa")
            st.text("A partir de 16/09/2023")
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col5:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)


############### Lay Goleada Visitante ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_lay_goleada_visitante_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = df['Profit'].sum()
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Lay Goleada Visitante")
            st.text("A partir de 16/09/2023")
            
            col6, col7, col8 = st.columns(3)
            
            with col6:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col7:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col8:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)


# Chama a função tips_page() no início do código para criar a página
tips_page()
