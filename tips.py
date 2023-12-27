import pandas as pd
import numpy as np
import streamlit as st
import base64
import re
import datetime as dt
import requests
import csv
import io
import plotly.express as px



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
    substrings_para_excluir = ['U16', 'U17', 'U18', 'U19', 'U20', '21', 'U22', 'U23', 'Women']
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
        tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Resultados", "HA", "Lay 0x2", "Lay Goleada", "Lay Zebra HT", "Drakito", "BTTS Sim", "Scalping", "Scalping HT"])

        with tab1:
            # Use df aqui para a aba "HA"
            st.subheader("HA -0.25")
            st.text("Apostar em HA -0.25 casa, Odd mínima 1.40")

            # Carregue os dados do CSV da URL
            url_df2 = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Apostas_HA.csv"
            df2 = pd.read_csv(url_df2)
        
            # Selecionar as colunas desejadas
            colunas_desejadas = ["Data", "Hora", "Liga", "Home", "Away"]
            ha_df = df2[colunas_desejadas]
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
            # Use df aqui para a aba "Lay 0x2"
            st.subheader("Lay 0x2")
            st.text("Apostar em Lay 0x2, Odd Maxima 50")
            lay_02_ft = df[
                (df["FT_Odd_A"] >= 6) & (df["FT_Odd_A"] <= 10)
            ]
            colunas_desejadas = ["Date", "Hora", "Pais", "Liga", "Home", "Away"]
            lay_02_ft = lay_02_ft[colunas_desejadas]
            st.dataframe(lay_02_ft, width=800)

            # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
            data_atual = datetime.now().strftime("%d-%m-%Y")

            # Criar um link para download do CSV
            csv_lay_02_ft = lay_02_ft.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Baixar CSV",
                data=csv_lay_02_ft,
                file_name=f"lay_02_ft_{data_atual}.csv",
                key="lay_02_ft_csv"
            )

        with tab3:
        
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

        with tab4:
            # Use df aqui para a aba "Lay Zebra HT"
            st.subheader("Lay Zebra HT")
            st.text("Apostar em Lay visitante, Odd máxima 6")
            layzebraht_df = df[
                (df["FT_Odd_H"] >= 1.21) & (df["FT_Odd_H"] <= 1.6) &
                (df["FT_Odd_A"] >= 4) & (df["FT_Odd_A"] <= 10) &
                (df["PPG_Home"] >= 2.4) &
                (df["Rodada"] >= 8)
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

        with tab5:
            
            # Definir URLs para os arquivos CSV
            url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true'
            url_momento_gol_home = 'https://github.com/scooby75/bdfootball/blob/main/scalping_home.csv?raw=true'
            
            try:
                # Carregar dados CSV
                jogosdodia = pd.read_csv(url_jogosdodia)
                momento_gol_home = pd.read_csv(url_momento_gol_home)
            
                # Lógica de mesclagem e filtragem de dados
                jogos_filtrados_home = jogosdodia.merge(momento_gol_home, left_on='Home', right_on='Equipe')
            
                # Adicionar condições para filtrar os jogos em url_jogosdodia
                jogos_filtrados_home = jogos_filtrados_home[
                    (jogos_filtrados_home['FT_Odd_H'] >= 1.40) &
                    (jogos_filtrados_home['FT_Odd_H'] <= 2) &
                    (jogos_filtrados_home['FT_Odd_A'] >= 4) &
                    (jogos_filtrados_home['FT_Odd_A'] <= 10) &
                    (jogos_filtrados_home['Home'] == jogos_filtrados_home['Equipe']) &
                    (jogos_filtrados_home['16_30_mar'] >= 4)
                ]
            
                # Selecionar colunas relevantes e renomear
                result_df = jogos_filtrados_home[['Hora','Pais', 'Liga', 'Home', 'Away', 'FT_Odd_H', 'FT_Odd_A']]
                result_df.columns = ['Hora','Pais', 'Liga', 'Home', 'Away', 'FT_Odd_H_home', 'FT_Odd_A_home']
            
                # Streamlit App
                st.subheader("Drakito")
                st.text("Entrar após o primeiro gol e fechar a posição no segundo gol ou término do HT")
                st.dataframe(result_df, width=800)
            
                # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
                data_atual = datetime.now().strftime("%d-%m-%Y")
            
                # Criar um link para download do CSV
                csv_link_drakito = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Baixar CSV",
                    data=csv_link_drakito,
                    file_name=f"drakito_{data_atual}.csv",
                    key="drakito_csv"
                )
            
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
        
        with tab6:
            
            # Use df aqui para a aba "BTTS Sim"
            st.subheader("BTTS Sim")
            st.text("Apostar em Ambas Marcam Sim, Odd mínima 1.6")
                    
            # Lista de ligas para apostar
            ligas_para_apostar = [
                "3. Liga MSFL",
                "K League 1",
                "Super Liga",
                "3. Liga CFL",
                "Regionalliga West",
                "3 Liga Group 3",
                "Damallsvenskan",
                "National Division",
                "3 Liga Group 1",
                "Division 2 Vastra Gotaland",
                "1 Lyga",
                "Regionalliga Ost",
                "Division 2 Sodra Gotaland",
                "Southern League Premier Central",
                "Southern League Premier South",
                "Eerste Divisie"

            ]
        
            btts_yes_df = df[
                (df["FT_Odd_Over25"] <= 1.7) & 
                (df["FT_Odd_BTTS_Yes"] <= 1.7) &
                (df["XG_Home"] >= 1.5) & 
                (df["XG_Away"] >= 1.5) &
                (df["Rodada"] >= 10) &
                (df["Liga"].isin(ligas_para_apostar))  # Adiciona a condição para apostar nas ligas desejadas
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
    
        with tab7:
            # Definir URLs para os arquivos CSV            
            url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true'
        
            # Carregar dados CSV
            jogosdodia = pd.read_csv(url_jogosdodia)
        
            # Filtrar jogos com critérios específicos
            filtered_games = jogosdodia[
                (jogosdodia['FT_Odd_H'] >= 1.80) & (jogosdodia['FT_Odd_A'] >= 1.80) & (jogosdodia['AVG_25FT'] <= 50)
            ]
        
            try:
                # Selecionar colunas relevantes e renomear
                result_df = filtered_games[['Date', 'Hora', 'Pais', 'Liga', 'Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Under05', 'FT_Odd_Over25', 'AVG_25FT']]
                result_df.columns = ['Date', 'Hora', 'Pais', 'Liga', 'Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Under05', 'FT_Odd_Over25', 'AVG_25FT']
        
                # Streamlit App
                st.subheader("Scalping Gols")
                #st.text("Realizar scalping pós gol e fechar posição com 3% ou 5min de exposição.")
                st.dataframe(result_df, width=800)
        
                # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
                data_atual = datetime.now().strftime("%d-%m-%Y")
        
                # Criar um link para download do CSV
                csv_link_scalping = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Baixar CSV",
                    data=csv_link_scalping,
                    file_name=f"scalping_gols_{data_atual}.csv",
                    key="scalping_csv"
                )
        
            except Exception as e:
                st.error("Ocorreu um erro: " + str(e))
        
        with tab8:
        

            # Definir URLs para os arquivos CSV
            url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/bd_fts_bruto.csv?raw=true'
            url_momento_gol_home = 'https://github.com/scooby75/bdfootball/blob/main/scalping_home.csv?raw=true'
            url_momento_gol_away = 'https://github.com/scooby75/bdfootball/blob/main/scalping_away.csv?raw=true'

            try:
                # Carregar dados CSV
                jogosdodia = pd.read_csv(url_jogosdodia)
                momento_gol_home = pd.read_csv(url_momento_gol_home)
                momento_gol_away = pd.read_csv(url_momento_gol_away)

                # Lógica de mesclagem e filtragem de dados
                jogos_filtrados_home = jogosdodia.merge(momento_gol_home, left_on='Home Team', right_on='Equipe')
                jogos_filtrados_away = jogosdodia.merge(momento_gol_away, left_on='Away Team', right_on='Equipe')

                # Adicionar condições para filtrar os jogos
                condicoes_filtragem = (
                    (jogosdodia['Country'] != 'Esports') &
                    (jogosdodia['League'] != 'U21 League') &
                    (jogosdodia['League'] != 'UEFA U21 Championship Qualification') &
                    (jogosdodia['Odds_Home_Win'].between(2, 10)) &
                    (jogosdodia['Odds_Away_Win'].between(2, 10)) &
                    #(jogosdodia['Under25 Average'].between(75, 100))
                    (jogosdodia['Under45 Average'].between(90, 100)) &
                    (jogos_filtrados_home['Home Team'] == jogos_filtrados_home['Equipe']) &
                    (jogos_filtrados_away['Away Team'] == jogos_filtrados_away['Equipe']) &
                    (jogos_filtrados_home['46_60_mar'] <= 1) &
                    (jogos_filtrados_home['46_60_sofri'] <= 1) &
                    (jogos_filtrados_home['61_75_mar'] <= 1) &
                    (jogos_filtrados_home['61_75_sofri'] <= 1) &
                    (jogos_filtrados_away['46_60_mar'] <= 1) &
                    (jogos_filtrados_away['46_60_sofri'] <= 1) &
                    (jogos_filtrados_away['61_75_mar'] <= 1) &
                    (jogos_filtrados_away['61_75_sofri'] <= 1) 
                )

                jogosdodia = jogosdodia[condicoes_filtragem]

                # Selecionar colunas relevantes e renomear
                result_df = jogosdodia[['Country', 'League', 'Home Team', 'Away Team', 'Odds_Home_Win', 'Odds_Away_Win', 'Odds_Over25']]
                result_df.columns = ['Country', 'League', 'Home Team', 'Away Team', 'Odds_Home_Win', 'Odds_Away_Win', 'Odds_Over25']

                # Streamlit App
                st.subheader("Scalping HT")
                st.dataframe(result_df, width=800)

                # Obter a data atual no formato desejado (por exemplo, "DD-MM-YYYY")
                #data_atual = datetime.now().strftime("%d-%m-%Y")

                # Criar um link para download do CSV
                csv_link_scalping_ht = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Baixar CSV",
                    data=csv_link_scalping_ht,
                    file_name=f"Scalping_HT_{data_atual}.csv",
                    key="scalping_ht_csv"
                )

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

             
        with tab0:
                 
            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_ha_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)
            
            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_HA'] = pd.to_numeric(df['Profit_HA'].str.replace(',', '.'), errors='coerce')
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Cálculo do Lucro/Prejuízo
            profit = round(df['Profit_HA'].sum(), 2)
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)
            
            # Adicione a nova coluna "Partidas" com a quantidade total de jogos
            df['Eventos'] = len(df)  # O comprimento do DataFrame é a quantidade total de jogos           
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("HA -0,25")
            st.text("A partir de 16/09/2023")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div style="text-align: center;"> Partidas </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(len(df)), unsafe_allow_html=True)
            
            # Adicione um gráfico de linha usando Plotly

            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Filter the DataFrame to include data from 16.09.2023 onwards
            start_date = '2023-09-16'
            df_filtered = df[df['Date'] >= start_date]

            # Sum the 'Profit' column and group by day ('Date')
            cumulative_profit = df.groupby('Date')['Profit_HA'].sum().cumsum().reset_index()

            # Display a line chart using Plotly
            fig = px.line(cumulative_profit, x='Date', y='Profit_HA', title='Lucro Acumulado HA -0,25', labels={'L/P': 'L/P (Und)'})
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)
            

############### Lay 0 x 2 ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/lay_02_ft_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)

            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_FT_02'] = df['Profit_FT_02'].str.replace(',', '.').astype(float)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate FT'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_FT_02'] = pd.to_numeric(df['Profit_FT_02'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = round(df['Profit_FT_02'].sum(), 2)
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)

            # Adicione a nova coluna "Partidas" com a quantidade total de jogos
            df['Partidas'] = len(df)  # O comprimento do DataFrame é a quantidade total de jogos
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Lay 0x2")
            st.text("A partir de 04/11/2023")
            
            col19, col20, col21, col22 = st.columns(4)
            
            with col19:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col20:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col21:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)

            with col22:
                st.markdown('<div style="text-align: center;"> Partidas </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(len(df)), unsafe_allow_html=True)

            # Adicione um gráfico de linha usando Plotly

            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Filter the DataFrame to include data from 16.09.2023 onwards
            start_date = '2023-09-16'
            df_filtered = df[df['Date'] >= start_date]

            # Sum the 'Profit' column and group by day ('Date')
            cumulative_profit = df.groupby('Date')['Profit_FT_02'].sum().cumsum().reset_index()

            # Display a line chart using Plotly
            fig = px.line(cumulative_profit, x='Date', y='Profit_FT_02', title='Lucro Acumulado Lay 0x2', labels={'L/P': 'L/P (Und)'})
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)


############### Lay Goleada Visitante ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_lay_goleada_visitante_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)

            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Goleada'] = df['Profit_Goleada'].str.replace(',', '.').astype(float)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Goleada'] = pd.to_numeric(df['Profit_Goleada'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = round(df['Profit_Goleada'].sum(), 2)
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)

            # Adicione a nova coluna "Partidas" com a quantidade total de jogos
            df['Partidas'] = len(df)  # O comprimento do DataFrame é a quantidade total de jogos
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Lay Goleada Visitante")
            st.text("A partir de 16/09/2023")
            
            col7, col8, col9, col10 = st.columns(4)
            
            with col7:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col8:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col9:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)

            with col10:
                st.markdown('<div style="text-align: center;"> Partidas </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(len(df)), unsafe_allow_html=True)
            
            # Adicione um gráfico de linha usando Plotly

            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Filter the DataFrame to include data from 16.09.2023 onwards
            start_date = '2023-09-16'
            df_filtered = df[df['Date'] >= start_date]

            # Sum the 'Profit' column and group by day ('Date')
            cumulative_profit = df.groupby('Date')['Profit_Goleada'].sum().cumsum().reset_index()

            # Display a line chart using Plotly
            fig = px.line(cumulative_profit, x='Date', y='Profit_Goleada', title='Lucro Acumulado Lay Goleada Visitante', labels={'L/P': 'L/P (Und)'})
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)

############### Lay Visitante HT ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_lay_zebra_ht_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)

            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Visitante_HT'] = df['Profit_Visitante_HT'].str.replace(',', '.').astype(float)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Visitante_HT'] = pd.to_numeric(df['Profit_Visitante_HT'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = round(df['Profit_Visitante_HT'].sum(), 2)
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)

            # Adicione a nova coluna "Partidas" com a quantidade total de jogos
            df['Partidas'] = len(df)  # O comprimento do DataFrame é a quantidade total de jogos
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("Lay Visitante HT")
            st.text("A partir de 16/09/2023")
            
            col10, col11, col12, col13 = st.columns(4)
            
            with col10:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col11:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col12:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)

            with col13:
                st.markdown('<div style="text-align: center;"> Partidas </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(len(df)), unsafe_allow_html=True)

                        # Adicione um gráfico de linha usando Plotly

            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Filter the DataFrame to include data from 16.09.2023 onwards
            start_date = '2023-09-16'
            df_filtered = df[df['Date'] >= start_date]

            # Sum the 'Profit' column and group by day ('Date')
            cumulative_profit = df.groupby('Date')['Profit_Visitante_HT'].sum().cumsum().reset_index()

            # Display a line chart using Plotly
            fig = px.line(cumulative_profit, x='Date', y='Profit_Visitante_HT', title='Lucro Acumulado Away HT', labels={'L/P': 'L/P (Und)'})
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)


############### BTTS ##########################

            # Baixe o arquivo CSV do GitHub usando a URL fornecida
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/tips_btts_geral.csv"
            response = requests.get(url)
            csv_data = StringIO(response.text)

            # Carregue os dados do CSV em um DataFrame do Pandas
            df = pd.read_csv(csv_data)

            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Btts'] = df['Profit_Btts'].str.replace(',', '.').astype(float)
            
            # Cálculo do Winrate com 2 casas decimais e formato de porcentagem
            winrate = (df['Winrate'] * 100).mean()  # Média dos Winrates em formato de porcentagem
            winrate_formatted = "{:.2f}%".format(winrate)
            
            # Conversão da coluna "Profit" para um tipo numérico (float)
            df['Profit_Btts'] = pd.to_numeric(df['Profit_Btts'], errors='coerce')
            
            # Cálculo do Lucro/Prejuízo
            profit = round(df['Profit_Btts'].sum(), 2)
            
            # Cálculo da Odd Justa com 2 casas decimais
            odd_justa = round(100 / winrate, 2)

            # Adicione a nova coluna "Partidas" com a quantidade total de jogos
            df['Partidas'] = len(df)  # O comprimento do DataFrame é a quantidade total de jogos
            
            # Exiba os resultados no Streamlit em três colunas separadas com centralização
            st.subheader("BTTS Sim")
            st.text("A partir de 16/09/2023")
            
            col16, col17, col18, col19 = st.columns(4)
            
            with col16:
                st.markdown('<div style="text-align: center;"> Winrate </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(winrate_formatted), unsafe_allow_html=True)
            
            with col17:
                st.markdown('<div style="text-align: center;"> Profit </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(profit), unsafe_allow_html=True)
            
            with col18:
                st.markdown('<div style="text-align: center;"> Odd Justa </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{:.2f}</div>'.format(odd_justa), unsafe_allow_html=True)

            with col19:
                st.markdown('<div style="text-align: center;"> Partidas </div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align: center;">{}</div>'.format(len(df)), unsafe_allow_html=True)

            # Adicione um gráfico de linha usando Plotly

            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

            # Filter the DataFrame to include data from 16.09.2023 onwards
            start_date = '2023-09-16'
            df_filtered = df[df['Date'] >= start_date]

            # Sum the 'Profit' column and group by day ('Date')
            cumulative_profit = df.groupby('Date')['Profit_Btts'].sum().cumsum().reset_index()

            # Display a line chart using Plotly
            fig = px.line(cumulative_profit, x='Date', y='Profit_Btts', title='Lucro Acumulado BTTS Sim', labels={'L/P': 'L/P (Und)'})
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig)


# Chama a função tips_page() no início do código para criar a página
tips_page()
