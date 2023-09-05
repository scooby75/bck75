# bck_home.py

import pandas as pd
import numpy as np
import streamlit as st
import base64

from datetime import datetime, timedelta  
from session_state import SessionState

def bck_home_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
    #else:
        #st.write("Acesso concedido!")  # Debug
         
    ##### PÁGINA BCK HOME ######
    tab0, tab1, tab2, tab3, tab4 = st.tabs(["Partidas Filtradas", "Desempenho HT", "Desempenho FT", "Backtesting Mercado", "Placar"])

    with tab0:
        # Carregar os dados
        @st.cache_data(ttl=28800.0)  # 24 horas em segundos
        def load_base():
            url = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
            df = pd.read_csv(url)
            return df
        
        # Chamar a função para carregar os dados
        bck_home_df = load_base()

        

        # Filtros interativos
        st.header("Filtros")

        # Organize filters into columns
        col1, col2, col3 = st.columns(3)

        # Filter by League, Season, Round, Home
        with col1:
            all_leagues = "Todos"
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_home_df['League'].unique()))

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_home_df['Round'].unique()))

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_home_df['Season'].unique()))
        
            home_teams = bck_home_df['Home'].unique()  # Get unique teams from 'Home' column
            selected_home = st.multiselect("Selecionar Mandante", home_teams)

            # PPG_Home filter
            min_rank_home = st.number_input("Rank Mínimo (Home)", min_value=1.0, key="min_rank_home")
            max_rank_home = st.number_input("Rank Máximo (Home)", max_value=50.0, key="max_rank_home")

        # Filter for Odd_Home and Odd_Away range
        with col2:
            odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0)
            odd_h_max = st.number_input("Odd_Home Máximo", value=10.0)

            odd_a_min = st.number_input("Odd_Away Mínimo", value=0.0)
            odd_a_max = st.number_input("Odd_Away Máximo", value=10.0)
        
            odd_draw_min = st.number_input("Odd_Empate Mínimo", value=0.0)
            odd_draw_max = st.number_input("Odd_Empate Máximo", value=10.0)

        # Filter for Over_05HT (HT_Odd_Over05) range and Over_25FT (FT_Odd_Over25)
        with col3:
            over_05ht_min = st.number_input("Over_05HT Mínimo", value=0.0)
            over_05ht_max = st.number_input("Over_05HT Máximo", value=10.0)

            over_25ft_min = st.number_input("Over_25FT Mínimo", value=0.0)
            over_25ft_max = st.number_input("Over_25FT Máximo", value=10.0)
        
            btts_yes_min = st.number_input("BTTS_Yes Mínimo", value=0.0)
            btts_yes_max = st.number_input("BTTS_Yes Máximo", value=10.0)

        # Remover espaços em branco dos nomes das colunas
        bck_home_df.columns = bck_home_df.columns.str.strip()

        # Apply filters
        filtered_df = bck_home_df[     
            (bck_home_df['League'].isin(selected_leagues) | (all_leagues in selected_leagues)) &
            (bck_home_df['Season'].isin(selected_seasons) | (all_seasons in selected_seasons)) &
            ((bck_home_df['Round'].isin(selected_rounds)) if all_rounds not in selected_rounds else True) &
            ((bck_home_df['Home'].isin(selected_home)) if selected_home else True) &
            (bck_home_df['Rank_Home'] >= min_rank_home) & 
            (bck_home_df['Rank_Home'] <= max_rank_home) & 
            (bck_home_df['FT_Odd_H'] >= odd_h_min) &
            (bck_home_df['FT_Odd_H'] <= odd_h_max) &
            (bck_home_df['FT_Odd_A'] >= odd_a_min) &
            (bck_home_df['FT_Odd_A'] <= odd_a_max) &
            (bck_home_df['FT_Odd_D'] >= odd_draw_min) &
            (bck_home_df['FT_Odd_D'] <= odd_draw_max) &
            (bck_home_df['HT_Odd_Over05'] >= over_05ht_min) &
            (bck_home_df['HT_Odd_Over05'] <= over_05ht_max) &
            (bck_home_df['FT_Odd_Over25'] >= over_25ft_min) &
            (bck_home_df['FT_Odd_Over25'] <= over_25ft_max) &
            (bck_home_df['Odd_BTTS_Yes'] >= btts_yes_min) &
            (bck_home_df['Odd_BTTS_Yes'] <= btts_yes_max)
        ]

        # Display selected columns from the filtered data
        selected_columns = [
            "Date", "League", "Season", "Round", 'Rank_Home', "Home", "Away",
            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "HT_Odd_Over05", "FT_Odd_Over25", "Odd_BTTS_Yes", "Placar_HT", "Placar_FT"
        ]
        st.dataframe(filtered_df[selected_columns])

    with tab1:
        
        # Calculando a quantidade de vezes que "Home" ganhou
        quantidade_vitorias_home_ht = len(filtered_df[filtered_df['Resultado_HT'] == 'H'])

        # Calculando o total de jogos no intervalo HT
        total_jogos_home_ht = len(filtered_df)

        # Calculando a performance de "Home"
        if total_jogos_home_ht > 0:
            performance_home_ht = (quantidade_vitorias_home_ht / total_jogos_home_ht) * 100
        else:
            performance_home_ht = 0

        # Arredondando a performance para 2 casas decimais e garantindo que não seja maior que 100%
        performance_home_ht = min(performance_home_ht, 100)
        performance_home_ht = round(performance_home_ht, 2)

        # Calculando o tamanho da amostra
        tamanho_amostra_ht = total_jogos_home_ht

        # Criando o novo DataFrame
        data_ht = {'Winrate': [f"{performance_home_ht:.2f}%"], 'Amostra': [tamanho_amostra_ht]}
        df_resultado_ht = pd.DataFrame(data_ht)

        # Exibindo o resultado
        st.subheader('Desempenho da Equipe HT')
        st.dataframe(df_resultado_ht)        

  
    #### TOP Equipes HT - Casa ####

        # Função para formatar os valores da média de gols com duas casas decimais
        def format_decimal(value):
            return "{:.2f}".format(value)

        # Agrupando por Temporada (Season), Liga (League) e Equipe (Home) e calculando a média de gols e o total de jogos
        grouped_data = filtered_df.groupby(['Season', 'League', 'Home']).agg(
            Total_Goals=pd.NamedAgg(column='HT_Goals_H', aggfunc='sum'),
            Total_Matches=pd.NamedAgg(column='Home', aggfunc='size')
        )

        # Filtrando as equipes que tiveram pelo menos 5 jogos na mesma Season e mesma League
        grouped_data = grouped_data[grouped_data['Total_Matches'] >= 5]

        # Resetando o índice para criar um novo DataFrame
        top_over_05HT_casa = grouped_data.reset_index()

        # Calculando a média de gols por jogo para cada equipe, considerando todas as partidas Home
        top_over_05HT_casa['Média Gols HT'] = top_over_05HT_casa['Total_Goals'] / top_over_05HT_casa['Total_Matches']

        # Formatando a coluna de média de gols com duas casas decimais e tratando possíveis erros
        try:
            top_over_05HT_casa['Média Gols HT'] = top_over_05HT_casa['Média Gols HT'].apply(format_decimal)
        except Exception as e:
        # Em caso de erro, preencher a coluna com valor vazio
            top_over_05HT_casa['Média Gols HT'] = ''

        # Renomeando as colunas
        top_over_05HT_casa = top_over_05HT_casa.rename(columns={
            'Season': 'Temporada',
            'League': 'Liga',
            'Total_Goals': 'Total Gols HT',
            'Total_Matches': 'Total de Partidas',
            'Média Gols HT': 'Média Gols HT'
        })

        # Ordenando a tabela pela coluna 'Média Gols HT' em ordem decrescente
        top_over_05HT_casa = top_over_05HT_casa.sort_values(by='Média Gols HT', ascending=False)

        # Verificar se a equipe selecionada está disponível na lista de opções de equipes
        if 'selected_team' not in st.session_state or not st.session_state.selected_team:
            selected_team = "All"
        else:
            selected_team = st.session_state.selected_team

        if 'selected_seasons' not in st.session_state or not st.session_state.selected_seasons:
            selected_seasons = "All"
        else:
            selected_seasons = st.session_state.selected_seasons

        if selected_team != "All" and selected_team not in team_options:
            st.error("Equipe selecionada não está disponível.")
        elif selected_seasons != "All" and selected_seasons not in top_over_05HT_casa['Temporada'].unique():
            st.error("Temporada selecionada não está disponível.")
        else:
        # Filtrar o DataFrame original para a equipe selecionada, se aplicável
            if selected_team != "All":
                filtered_df_over_05HT = filtered_df_over_05HT[filtered_df_over_05HT['Home'] == selected_team]

        # Filtrar o DataFrame original para a temporada selecionada, se aplicável
            if selected_seasons != "All":
                top_over_05HT_casa = top_over_05HT_casa[top_over_05HT_casa['Temporada'] == selected_seasons]

        # Selecionando as 10 equipes com maior média de gols
            top_10_teams = top_over_05HT_casa.head(10)

        # Exibindo a nova tabela "Top Over 05HT - Casa" com Streamlit e ajustando o tamanho da fonte
            st.subheader("Top Over 05HT - Casa")
            st.dataframe(top_10_teams)
        
        
    with tab2:
          ##### Desempenho da Equipe FT ######

        # Calculando a quantidade de vezes que "Home" ganhou no intervalo FT
        quantidade_vitorias_home_ft = len(filtered_df[filtered_df['Resultado_FT'] == 'H'])

        # Calculando o total de jogos no intervalo FT
        total_jogos_home_ft = len(filtered_df)

        # Calculando a performance de "Home" no intervalo FT
        if total_jogos_home_ft > 0:
            performance_home_ft = (quantidade_vitorias_home_ft / total_jogos_home_ft) * 100
        else:
            performance_home_ft = 0

        # Arredondando a performance para 2 casas decimais e garantindo que não seja maior que 100%
        performance_home_ft = min(performance_home_ft, 100)
        performance_home_ft = round(performance_home_ft, 2)

        # Calculando o tamanho da amostra
        tamanho_amostra_ft = total_jogos_home_ft

        # Criando o novo DataFrame para o desempenho da equipe FT
        data_ft = {'Winrate': [f"{performance_home_ft:.2f}%"], 'Amostra': [tamanho_amostra_ft]}
        df_resultado_ft = pd.DataFrame(data_ft)

        # Exibindo o resultado do desempenho da equipe FT
        st.subheader('Desempenho da Equipe FT')
        st.dataframe(df_resultado_ft)

     ##### Desempenho Geral - Casa ####

        # Group the filtered dataframe by home team (equipe da casa) and calculate cumulative sum of 'Profit'
        df_home_profit = filtered_df.groupby('Home')['profit_home'].sum().reset_index()

        # Group the filtered dataframe by home team (equipe da casa) and calculate cumulative sum of 'Profit'
        df_home_profit = filtered_df.groupby(['Season', 'Home'])['profit_home'].sum().reset_index()

        # Create a pivot table of profit/loss by home team for the selected season
        home_team_profit_loss_pivot = df_home_profit.pivot_table(index="Home", columns="Season", values="profit_home")

        # Display the table with profit/loss by home team (pivot table)
        st.subheader("Desempenho Geral - Equipe da Casa")
        st.text("Serão exibidas todas as Equipes que se enquadraram no(s) filtro(s) de Odd")
        st.dataframe(home_team_profit_loss_pivot)

    ##### Top Back Casa ####

        # Group the filtered DataFrame by 'Home' (Home Team) and calculate the cumulative sum of 'Profit'
        df_home_profit = filtered_df.groupby('Home')['profit_home'].cumsum()

        # Add the 'Profit_acumulado' column to the filtered DataFrame
        filtered_df['profit_home_acumulado'] = df_home_profit

        # Filter the DataFrame to include only rows where 'Profit_acumulado' is greater than 1
        filtered_home_profit = filtered_df[filtered_df['profit_home_acumulado'] >= 3]

        # Group the filtered DataFrame by 'Home' (Home Team) and calculate the total profit for each home team
        home_team_total_profit = filtered_home_profit.groupby(['Home', 'League'])['profit_home_acumulado'].last().reset_index()

        # Sort the home_team_total_profit DataFrame in descending order of profit
        home_team_total_profit_sorted = home_team_total_profit.sort_values(by='profit_home_acumulado', ascending=False)

        # Display the table with total profit by home team in descending order
        st.subheader("Top Back Casa")
        st.text("Serão exibidas apenas as Equipes que acumulam pelo menos 3und de lucro")
        st.dataframe(home_team_total_profit_sorted)

        # Download button for CSV
        #csv_file = home_team_total_profit_sorted.to_csv(index=False, encoding='utf-8-sig')
        #b64 = base64.b64encode(csv_file.encode()).decode()
        #st.markdown(f'<a href="data:file/csv;base64,{b64}" download="top_back_casa.csv">Download CSV</a>', unsafe_allow_html=True)

    ########## Faixa de Odd Mais Lucrativa

        st.subheader("Odds Mais Lucrativas")

        # Defina as faixas de odd
        faixas_de_odd = [(1.01, 1.20), (1.21, 1.40), (1.41, 1.60), (1.61, 1.80), (1.81, 2.00), 
                         (2.01, 2.20), (2.21, 2.40), (2.41, 2.60), (2.61, 2.80), (2.81, 3.00),
                         (3.01, 3.20), (3.21, 3.40), (3.41, 3.60), (3.61, 3.80), (3.81, 4.00)]

        # Crie uma função para mapear a faixa de odd com base no valor da odd
        def encontrar_faixa(odd):
            for faixa in faixas_de_odd:
                if faixa[0] <= odd <= faixa[1]:
                    return f"{faixa[0]:.2f} - {faixa[1]:.2f}"
            return "Outras"

        # Adicione uma coluna "faixa_de_odd" ao seu DataFrame original (filtered_df)
        filtered_df["faixa_de_odd"] = filtered_df["FT_Odd_H"].apply(encontrar_faixa)

        # Crie o DataFrame "Faixa De Odds Mais Lucrativas" agrupando e somando por faixa de odd
        faixa_de_odds_mais_lucrativas = filtered_df.groupby("faixa_de_odd")["profit_home"].sum().reset_index()

        # Renomeie a coluna "profit_home" para algo mais descritivo, se desejar
        faixa_de_odds_mais_lucrativas = faixa_de_odds_mais_lucrativas.rename(columns={"profit_home": "Soma Profit Home"})

        # Exiba o DataFrame "Odds Mais Lucrativas"
        st.dataframe(faixa_de_odds_mais_lucrativas)


    with tab3:

################################################################################3        

    ##### Calculo Win/Loss Over Back Casa FT ####

        # Create a new DataFrame for the "Back Casa FT" table
        df_back_casa_ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_FT"] == "H"])
        num_loss = len(filtered_df[filtered_df["Resultado_FT"].isin(["A", "D"])])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Back Casa FT" table ####
        df_back_casa_ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Back Casa FT" table
        st.subheader("Back Casa FT")
        st.dataframe(df_back_casa_ft)
    with tab3:
    
    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_home'].sum()

    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

###### ADD Gráfico com Resultado Back FT #####

    #st.subheader("Desempenho Geral do Filtro")
        
        # Converter a coluna 'Date' para o tipo datetime e formatar como "DD/MM/YYYY"
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d/%m/%Y')

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_FT'] = filtered_df['profit_home'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_FT', use_container_width=True)

##########################################################################################

            ##### Calculo Win/Loss OverLay Zebra FT ####

        # Create a new DataFrame for the "Lay Zebra FT" table
        df_lay_zebra_ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_FT"].isin(["H", "D"])])
        num_loss = len(filtered_df[filtered_df["Resultado_FT"] == "A"])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Back Casa FT" table ####
        df_lay_zebra_ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Back Casa FT" table
        st.subheader("Lay Zebra FT")
        st.dataframe(df_lay_zebra_ft)
    with tab3:
    
    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_lay_away'].sum()

    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

###### ADD Gráfico com Resultado Lay Zebra FT #####

    #st.subheader("Desempenho Geral do Filtro")
        
        # Converter a coluna 'Date' para o tipo datetime e formatar como "DD/MM/YYYY"
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d/%m/%Y')

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_Zebra'] = filtered_df['profit_lay_away'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_Zebra', use_container_width=True)
        

###########################################################################################        

    ##### Calculo Win/Loss Over Back Casa HT ####

        # Create a new DataFrame for the "Back Casa HT" table
        df_back_casa_ht = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_HT"] == "H"])
        num_loss = len(filtered_df[filtered_df["Resultado_HT"].isin(["A", "D"])])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Back Casa FT" table ####
        df_back_casa_ht.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Back Casa HT" table
        st.subheader("Back Casa HT")
        st.dataframe(df_back_casa_ht)
    
###########################################################################################################
        
    ##### Calculo Win/Loss Lay Zebra HT ####

          # Create a new DataFrame for the "Lay Zebra FT" table
        df_lay_zebra_ht = pd.DataFrame(columns=["Win", "Loss", "Odd Lay"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_HT"] != "A"])
        num_loss = len(filtered_df[filtered_df["Resultado_HT"] == "A"])

       # Calculate win and loss percentages
        total_games = num_win + num_loss

        if total_games == 0:
        # Handle the case when there are no games in the dataset
            win_percentage = 0
            loss_percentage = 0
        else:
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100

        # Calculate the fair odds with 2 decimal places
        if loss_percentage == 0:
            fair_odd = 0  # Since all games are wins, fair odds cannot be calculated
        else:
            fair_odd = round(100 / loss_percentage, 2)
            
        # Add the data to the "Lay Zebra HT" table
            df_lay_zebra_ht.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]
            
        # Display the "Lay Zebra FT" table
            st.subheader("Lay Zebra HT")
            st.dataframe(df_lay_zebra_ht)

#################################################################################################3        

##### Calculo Win/Loss Over 05HT ####

        # Create a new DataFrame for the "Over 05HT" table
        df_over05ht = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["HT_Goals_H"] + filtered_df["HT_Goals_A"]) >= 1])
        num_loss = len(filtered_df[(filtered_df["HT_Goals_H"] + filtered_df["HT_Goals_A"]) == 0])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Over 05HT" table ####
        df_over05ht.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Over 05HT" table
        st.subheader("Over 05HT")
        st.dataframe(df_over05ht)

       ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_over05HT'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

       ###### ADD Gráfico Over 05HT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_OV05HT'] = filtered_df['profit_over05HT'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_OV05HT', use_container_width=True)

##### Calculo Win/Loss Under 05HT ####

        # Create a new DataFrame for the "Under 05HT" table
        df_under05ht = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["HT_Goals_H"] + filtered_df["HT_Goals_A"]) == 0])
        num_loss = len(filtered_df[(filtered_df["HT_Goals_H"] + filtered_df["HT_Goals_A"]) >= 1])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Under 05HT" table ####
        df_under05ht.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Under 05HT" table
        st.subheader("Under 05HT")
        st.dataframe(df_under05ht)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_under05HT'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Under 05HT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_U05HT'] = filtered_df['profit_under05HT'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_U05HT', use_container_width=True)

########################################################################################        

##### Calculo Win/Loss Over 15FT ####

        # Create a new DataFrame for the "Over 15FT" table
        df_over15ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 1])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 1])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Over 15FT" table ####
        df_over15ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Over 15FT" table
        st.subheader("Over 15FT")
        st.dataframe(df_over15ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_over15'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

          ###### ADD Gráfico Over 15FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_O15FT'] = filtered_df['profit_over15'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_O15FT', use_container_width=True)

##### Calculo Win/Loss Under 15FT ####

        # Create a new DataFrame for the "Under 15FT" table
        df_under15ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 1])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 1])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Under 15FT" table ####
        df_under15ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Under 15FT" table
        st.subheader("Under 15FT")
        st.dataframe(df_under15ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_under15'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

        ###### ADD Gráfico Under 15FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_U15FT'] = filtered_df['profit_under15'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_U15FT', use_container_width=True)

###############################################################################3
        
##### Calculo Win/Loss Over 25FT ####

        # Create a new DataFrame for the "Over 25FT" table
        df_over25ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 2])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 2])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Over 25FT" table ####
        df_over25ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Over 25FT" table
        st.subheader("Over 25FT")
        st.dataframe(df_over25ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_over25'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Over 25FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_O25FT'] = filtered_df['profit_over25'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_O25FT', use_container_width=True)

##### Calculo Win/Loss Under 25FT ####

        # Create a new DataFrame for the "Under 25FT" table
        df_under25ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 2])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 2])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Under 25FT" table ####
        df_under25ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Under 25FT" table
        st.subheader("Under 25FT")
        st.dataframe(df_under25ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_under25'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

   ###### ADD Gráfico Under 25FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_U25FT'] = filtered_df['profit_under25'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_U25FT', use_container_width=True)

##########################################################################        

##### Calculo Win/Loss Over 35FT ####

        # Create a new DataFrame for the "Over 35FT" table
        df_over35ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 3])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 3])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Over 35FT" table ####
        df_over35ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Over 35FT" table
        st.subheader("Over 35FT")
        st.dataframe(df_over35ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_over35'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Over 35FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_O35FT'] = filtered_df['profit_over35'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_O35FT', use_container_width=True)

##### Calculo Win/Loss Under 35FT ####

        # Create a new DataFrame for the "Under 35FT" table
        df_under35ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 3])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 3])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Under 35FT" table ####
        df_under35ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Under 35FT" table
        st.subheader("Under 35FT")
        st.dataframe(df_under35ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_under35'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

   ###### ADD Gráfico Under 35FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_U35FT'] = filtered_df['profit_under35'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_U35FT', use_container_width=True)
   
#########################################################3

##### Calculo Win/Loss Over 45FT ####

        # Create a new DataFrame for the "Over 45FT" table
        df_over45ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 4])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 4])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Over 45FT" table ####
        df_over45ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Over 45FT" table
        st.subheader("Over 45FT")
        st.dataframe(df_over45ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_over45'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Over 45FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_O45FT'] = filtered_df['profit_over45'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_O45FT', use_container_width=True)

##### Calculo Win/Loss Under 45FT ####

        # Create a new DataFrame for the "Under 45FT" table
        df_under45ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) <= 4])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] + filtered_df["FT_Goals_A"]) > 4])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if win_percentage != 0:
            fair_odd = round(100 / win_percentage, 2)
        else:
        # Handle the case when win_percentage is zero
            fair_odd = 0

        #### Add the data to the "Under 45FT" table ####
        df_under45ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Under 45FT" table
        st.subheader("Under 45FT")
        st.dataframe(df_under45ft)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_under45'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

   ###### ADD Gráfico Under 45FT #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_U45FT'] = filtered_df['profit_under45'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_U45FT', use_container_width=True)

#########################################################

##### Calculo Win/Loss Lay 0x1 ####

        # Create a new DataFrame for the "Lay 0x1" table
        df_lay_01 = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] != 0) | (filtered_df["FT_Goals_A"] != 1)])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] == 0) & (filtered_df["FT_Goals_A"] == 1)])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if loss_percentage != 0:
            fair_odd = round(100 / loss_percentage, 2)
        else:
        # Handle the case when loss_percentage is zero
            fair_odd = 0

        #### Add the data to the "Lay 0x1" table ####
        df_lay_01.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Lay 0x1" table
        st.subheader("Lay 0x1")
        st.dataframe(df_lay_01)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_Lay_0x1'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Lay 0x1 #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_Lay_01'] = filtered_df['profit_Lay_0x1'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_Lay_01', use_container_width=True)

#########################################################

##### Calculo Win/Loss Lay 1x0 ####

        # Create a new DataFrame for the "Lay 1x0" table
        df_lay_10 = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] != 1) | (filtered_df["FT_Goals_A"] != 0)])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] == 1) & (filtered_df["FT_Goals_A"] == 0)])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if loss_percentage != 0:
            fair_odd = round(100 / loss_percentage, 2)
        else:
        # Handle the case when loss_percentage is zero
            fair_odd = 0

        #### Add the data to the "Lay 1x0" table ####
        df_lay_10.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Lay 1x0" table
        st.subheader("Lay 1x0")
        st.dataframe(df_lay_10)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_Lay_1x0'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Lay 1x0 #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_Lay_10'] = filtered_df['profit_Lay_1x0'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_Lay_10', use_container_width=True)

#########################################################

##### Calculo Win/Loss Lay 1x2 ####

        # Create a new DataFrame for the "Lay 1x2" table
        df_lay_12 = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] != 1) | (filtered_df["FT_Goals_A"] != 2)])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] == 1) & (filtered_df["FT_Goals_A"] == 2)])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if loss_percentage != 0:
            fair_odd = round(100 / loss_percentage, 2)
        else:
        # Handle the case when loss_percentage is zero
            fair_odd = 0

        #### Add the data to the "Lay 1x2" table ####
        df_lay_12.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Lay 1x2" table
        st.subheader("Lay 1x2")
        st.dataframe(df_lay_12)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_Lay_1x2'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Lay 1x2 #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_Lay_12'] = filtered_df['profit_Lay_1x2'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_Lay_12', use_container_width=True)

#########################################################

##### Calculo Win/Loss Lay 2x1 ####

        # Create a new DataFrame for the "Lay 2x1" table
        df_lay_21 = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[(filtered_df["FT_Goals_H"] != 2) | (filtered_df["FT_Goals_A"] != 1)])
        num_loss = len(filtered_df[(filtered_df["FT_Goals_H"] == 2) & (filtered_df["FT_Goals_A"] == 1)])
        total_games = num_win + num_loss

        # Check if total_games is not zero before performing division
        if total_games != 0:
        # Calculate win and loss percentages
            win_percentage = (num_win / total_games) * 100
            loss_percentage = (num_loss / total_games) * 100
        else:
        # Handle the case when total_games is zero
            win_percentage = 0
            loss_percentage = 0

        # Calculate the fair odds with 2 decimal places
        if loss_percentage != 0:
            fair_odd = round(100 / loss_percentage, 2)
        else:
        # Handle the case when loss_percentage is zero
            fair_odd = 0

        #### Add the data to the "Lay 1x2" table ####
        df_lay_21.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Lay 2x1" table
        st.subheader("Lay 2x1")
        st.dataframe(df_lay_21)

    ###### Calculo Lucro/Prejuízo ####

    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_Lay_2x1'].sum()
            
    # Calcular o ROI
            total_de_jogos = len(filtered_df)
            roi = (lucro_total / total_de_jogos) * 100
    
    # Arredondar os valores para duas casas decimais
            lucro_total = round(lucro_total, 2)
            roi = round(roi, 2)
    
    # Exibir os resultados usando st.write()
            st.write(f"Lucro/Prejuízo: {lucro_total} Und em {total_de_jogos} jogos")
            st.write(f"Yield: {roi}%")
        else:
    # Exibir mensagem de DataFrame vazio
            st.write("Nenhum dado disponível. O DataFrame está vazio.")

    ###### ADD Gráfico Lay 2x1 #####   

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_Lay_21'] = filtered_df['profit_Lay_2x1'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_Lay_21', use_container_width=True)

################ Placar FT ##########################
    
    with tab4:
        # Agrupe os placares em categorias
        placares_especificados = ['0 x 0', '0 x 1', '0 x 2', '0 x 3', 
                                  '1 x 0', '2 x 0', '3 x 0', 
                                  '1 x 1', '1 x 2', '1 x 3', 
                                  '2 x 1', '2 x 2', '2 x 3', 
                                  '3 x 1', '3 x 2', '3 x 3']
        
        goleada_casa = ['4 x 0', '4 x 1', '4 x 2', '4 x 3', '5 x 0', '5 x 1', '5 x 2', '5 x 3', '5 x 4',
                        '6 x 0', '6 x 1', '6 x 2', '6 x 3', '6 x 4', '6 x 5',
                        '7 x 0', '7 x 1', '7 x 2', '7 x 3', '7 x 4', '7 x 5', '7 x 6']

        goleada_visitante = ['0 x 4', '1 x 4', '2 x 4', '3 x 4',
                             '0 x 5', '1 x 5', '2 x 5', '3 x 5', '4 x 5',
                             '0 x 6', '1 x 6', '2 x 6', '3 x 6', '4 x 6', '5 x 6',
                             '0 x 7', '1 x 7', '2 x 7', '3 x 7', '4 x 7', '5 x 7', '6 x 7']

        # Função para categorizar os resultados
        def categorize_result(result):
            if result in placares_especificados:
                return "Placar Comum"
            elif result in goleada_casa:
                return "Goleada Casa"
            elif result in goleada_visitante:
                return "Goleada Visitante"
            else:
                return "Outros"

      # Supondo que filtered_df seja o DataFrame que você possui
        filtered_df['Categoria'] = filtered_df['Placar_FT'].apply(categorize_result)

# Calcular as contagens das categorias
        contagem_categorias = filtered_df['Categoria'].value_counts()

# Calcular as contagens dos placares específicos
        contagem_placares_especificos = filtered_df[filtered_df['Categoria'] == 'Placar Comum']['Placar_FT'].value_counts()

# Exibir os resultados de placar mais comuns
        
        st.subheader("Placares Mais Comuns no FT")
        st.dataframe(contagem_categorias.rename_axis('Categoria').reset_index(name='Contagem de Categorias'), width=400)
        st.dataframe(contagem_placares_especificos.rename_axis('Placar').reset_index(name='Total'), width=400)

        
        # Supondo que 'Temporada' seja a coluna que contém o ano da temporada
        temporadas = filtered_df['Season'].unique()

        
        contagem_placares_por_temporada = {}

        for temporada in temporadas:
        # Filtrar o DataFrame para a temporada atual
            filtered_temporada = filtered_df[filtered_df['Season'] == temporada]
    
       # Calcular as contagens dos placares específicos para a temporada atual
            contagem_placares_temporada = filtered_temporada[filtered_temporada['Categoria'] == 'Placar Comum']['Placar_FT'].value_counts()
    
        # Adicionar as contagens ao dicionário, usando a temporada como chave
            contagem_placares_por_temporada[temporada] = contagem_placares_temporada

        # Criar um DataFrame a partir do dicionário
        df = pd.DataFrame(contagem_placares_por_temporada)

        # Configurar o Streamlit para exibir os dados
        st.subheader("Placares Mais Comuns por Temporada")

        # Exibir o DataFrame usando st.dataframe
        st.dataframe(df, width=400)

################ Placar HT ##########################

        # Agrupe os placares em categorias
        placares_especificados_ht = ['0 x 0', '0 x 1', '0 x 2', '0 x 3', 
                                  '1 x 0', '2 x 0', '3 x 0', 
                                  '1 x 1', '1 x 2', '1 x 3', 
                                  '2 x 1', '2 x 2', '2 x 3', 
                                  '3 x 1', '3 x 2', '3 x 3']
        
        goleada_casa_ht = ['4 x 0', '4 x 1', '4 x 2', '4 x 3', '5 x 0', '5 x 1', '5 x 2', '5 x 3', '5 x 4',
                        '6 x 0', '6 x 1', '6 x 2', '6 x 3', '6 x 4', '6 x 5',
                        '7 x 0', '7 x 1', '7 x 2', '7 x 3', '7 x 4', '7 x 5', '7 x 6']

        goleada_visitante_ht = ['0 x 4', '1 x 4', '2 x 4', '3 x 4',
                             '0 x 5', '1 x 5', '2 x 5', '3 x 5', '4 x 5',
                             '0 x 6', '1 x 6', '2 x 6', '3 x 6', '4 x 6', '5 x 6',
                             '0 x 7', '1 x 7', '2 x 7', '3 x 7', '4 x 7', '5 x 7', '6 x 7']

        # Função para categorizar os resultados
        def categorize_result(result):
            if result in placares_especificados_ht:
                return "Placar Comum"
            elif result in goleada_casa_ht:
                return "Goleada Casa"
            elif result in goleada_visitante_ht:
                return "Goleada Visitante"
            else:
                return "Outros"

      # Supondo que filtered_df seja o DataFrame que você possui
        filtered_df['Categoria'] = filtered_df['Placar_HT'].apply(categorize_result)

# Calcular as contagens das categorias
        contagem_categorias_ht = filtered_df['Categoria'].value_counts()

# Calcular as contagens dos placares específicos
        contagem_placares_especificos_ht = filtered_df[filtered_df['Categoria'] == 'Placar Comum']['Placar_HT'].value_counts()

# Exibir os resultados de placar mais comuns
        
        st.subheader("Placares Mais Comuns no HT")
        st.dataframe(contagem_categorias_ht.rename_axis('Categoria').reset_index(name='Contagem de Categorias'), width=400)
        st.dataframe(contagem_placares_especificos_ht.rename_axis('Placar').reset_index(name='Total'), width=400)

        
        # Supondo que 'Temporada' seja a coluna que contém o ano da temporada
        temporadas = filtered_df['Season'].unique()

        
        contagem_placares_por_temporada_ht = {}

        for temporada in temporadas:
        # Filtrar o DataFrame para a temporada atual
            filtered_temporada_ht = filtered_df[filtered_df['Season'] == temporada]
    
        # Calcular as contagens dos placares específicos para a temporada atual
            contagem_placares_temporada_ht = filtered_temporada_ht[filtered_temporada_ht['Categoria'] == 'Placar Comum']['Placar_HT'].value_counts()
    
        # Adicionar as contagens ao dicionário, usando a temporada como chave
            contagem_placares_por_temporada_ht[temporada] = contagem_placares_temporada_ht

        # Criar um DataFrame a partir do dicionário
        df = pd.DataFrame(contagem_placares_por_temporada_ht)

        # Configurar o Streamlit para exibir os dados
        st.subheader("Placares Mais Comuns HT por Temporada")

        # Exibir o DataFrame usando st.dataframe
        st.dataframe(df, width=400)


# Execute a função para criar a página
bck_home_page()
