import streamlit as st
import pandas as pd

def bck_away_page():
    ##### PÁGINA BCK AWAY ######
    tab0, tab1, tab2, tab3 = st.tabs(["Partidas Filtradas", "Desempenho HT", "Desempenho FT", "Backtesting Mercado"])

    with tab0:
        # Carregar os dados
        @st.cache_data(ttl=28800.0)  # 24 horas em segundos
        def load_base():
            url = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
            df = pd.read_csv(url)
            return df
        
        # Chamar a função para carregar os dados
        bck_away_df = load_base()

        # Filtros interativos
        st.header("Filtros")

        # Organize filters into columns
        col1, col2, col3 = st.columns(3)

        # Filter by League, Season, Round, Home
        with col1:
            all_leagues = "Todos"
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_away_df['League'].unique()))

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_away_df['Round'].unique()))

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_away_df['Season'].unique()))
        
            home_teams = bck_away_df['Home'].unique()  # Get unique teams from 'Home' column
            selected_home = st.multiselect("Selecionar Mandante", home_teams)

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

        # Apply filters
        filtered_df = bck_away_df[
            (bck_away_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
            (bck_away_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
            (bck_away_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True) &
            (bck_away_df['Home'].isin(selected_home) if selected_home else True) &
            (bck_away_df['FT_Odd_H'] >= odd_h_min) &
            (bck_away_df['FT_Odd_H'] <= odd_h_max) &
            (bck_away_df['FT_Odd_A'] >= odd_a_min) &
            (bck_away_df['FT_Odd_A'] <= odd_a_max) &
            (bck_away_df['FT_Odd_D'] >= odd_draw_min) &
            (bck_away_df['FT_Odd_D'] <= odd_draw_max) &
            (bck_away_df['HT_Odd_Over05'] >= over_05ht_min) &
            (bck_away_df['HT_Odd_Over05'] <= over_05ht_max) &
            (bck_away_df['FT_Odd_Over25'] >= over_25ft_min) &
            (bck_away_df['FT_Odd_Over25'] <= over_25ft_max) &
            (bck_away_df['Odd_BTTS_Yes'] >= btts_yes_min) &
            (bck_away_df['Odd_BTTS_Yes'] <= btts_yes_max)
        ]

        # Display selected columns from the filtered data
        selected_columns = [
            "Date", "League", "Season", "Round", "Home", "Away",
            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "HT_Odd_Over05", "FT_Odd_Over25", "Odd_BTTS_Yes", "Placar_HT", "Placar_FT"
        ]
        st.dataframe(filtered_df[selected_columns])

    with tab1:
        
        # Calculando a quantidade de vezes que "Away" ganhou
        quantidade_vitorias_away_ht = len(filtered_df[filtered_df['Resultado_HT'] == 'A'])

        # Calculando o total de jogos no intervalo HT
        total_jogos_away_ht = len(filtered_df)

        # Calculando a performance de "Home"
        if total_jogos_away_ht > 0:
            performance_away_ht = (quantidade_vitorias_away_ht / total_jogos_away_ht) * 100
        else:
            performance_away_ht = 0

        # Arredondando a performance para 2 casas decimais e garantindo que não seja maior que 100%
        performance_away_ht = min(performance_away_ht, 100)
        performance_away_ht = round(performance_away_ht, 2)

        # Calculando o tamanho da amostra
        tamanho_amostra_ht = total_jogos_away_ht

        # Criando o novo DataFrame
        data_ht = {'Winrate': [f"{performance_away_ht:.2f}%"], 'Amostra': [tamanho_amostra_ht]}
        df_resultado_ht = pd.DataFrame(data_ht)

        # Exibindo o resultado
        st.subheader('Desempenho da Equipe HT')
        st.dataframe(df_resultado_ht)        

  
    #### TOP Equipes HT - Visitante ####

        # Função para formatar os valores da média de gols com duas casas decimais
        def format_decimal(value):
            return "{:.2f}".format(value)

        # Agrupando por Temporada (Season), Liga (League) e Equipe (Away) e calculando a média de gols e o total de jogos
        grouped_data = filtered_df.groupby(['Season', 'League', 'Away']).agg(
            Total_Goals=pd.NamedAgg(column='HT_Goals_H', aggfunc='sum'),
            Total_Matches=pd.NamedAgg(column='Away', aggfunc='size')
        )

        # Filtrando as equipes que tiveram pelo menos 5 jogos na mesma Season e mesma League
        grouped_data = grouped_data[grouped_data['Total_Matches'] >= 5]

        # Resetando o índice para criar um novo DataFrame
        top_over_05HT_away = grouped_data.reset_index()

        # Calculando a média de gols por jogo para cada equipe, considerando todas as partidas Away
        top_over_05HT_away['Média Gols HT'] = top_over_05HT_away['Total_Goals'] / top_over_05HT_away['Total_Matches']

        # Formatando a coluna de média de gols com duas casas decimais e tratando possíveis erros
        try:
            top_over_05HT_away['Média Gols HT'] = top_over_05HT_away['Média Gols HT'].apply(format_decimal)
        except Exception as e:
        # Em caso de erro, preencher a coluna com valor vazio
            top_over_05HT_away['Média Gols HT'] = ''

        # Renomeando as colunas
        top_over_05HT_away = top_over_05HT_away.rename(columns={
            'Season': 'Temporada',
            'League': 'Liga',
            'Total_Goals': 'Total Gols HT',
            'Total_Matches': 'Total de Partidas',
            'Média Gols HT': 'Média Gols HT'
        })

        # Ordenando a tabela pela coluna 'Média Gols HT' em ordem decrescente
        top_over_05HT_away = top_over_05HT_away.sort_values(by='Média Gols HT', ascending=False)

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
        elif selected_seasons != "All" and selected_seasons not in top_over_05HT_away['Temporada'].unique():
            st.error("Temporada selecionada não está disponível.")
        else:
        # Filtrar o DataFrame original para a equipe selecionada, se aplicável
            if selected_team != "All":
                filtered_df_over_05HT = filtered_df_over_05HT[filtered_df_over_05HT['Away'] == selected_team]

        # Filtrar o DataFrame original para a temporada selecionada, se aplicável
            if selected_seasons != "All":
                top_over_05HT_away = top_over_05HT_away[top_over_05HT_away['Temporada'] == selected_seasons]

        # Selecionando as 10 equipes com maior média de gols
            top_10_teams = top_over_05HT_away.head(10)

        # Exibindo a nova tabela "Top Over 05HT - Away" com Streamlit e ajustando o tamanho da fonte
            st.subheader("Top Over 05HT - Visitante")
            st.dataframe(top_10_teams)
        
        
    with tab2:
          ##### Desempenho da Equipe FT ######

        # Calculando a quantidade de vezes que "Home" ganhou no intervalo FT
        quantidade_vitorias_away_ft = len(filtered_df[filtered_df['Resultado_FT'] == 'A'])

        # Calculando o total de jogos no intervalo FT
        total_jogos_away_ft = len(filtered_df)

        # Calculando a performance de "Away" no intervalo FT
        if total_jogos_away_ft > 0:
            performance_away_ft = (quantidade_vitorias_away_ft / total_jogos_away_ft) * 100
        else:
            performance_away_ft = 0

        # Arredondando a performance para 2 casas decimais e garantindo que não seja maior que 100%
        performance_away_ft = min(performance_away_ft, 100)
        performance_away_ft = round(performance_away_ft, 2)

        # Calculando o tamanho da amostra
        tamanho_amostra_ft = total_jogos_away_ft

        # Criando o novo DataFrame para o desempenho da equipe FT
        data_ft = {'Winrate': [f"{performance_away_ft:.2f}%"], 'Amostra': [tamanho_amostra_ft]}
        df_resultado_ft = pd.DataFrame(data_ft)

        # Exibindo o resultado do desempenho da equipe FT
        st.subheader('Desempenho da Equipe FT')
        st.dataframe(df_resultado_ft)

     ##### Desempenho Geral - Visitante ####

        # Group the filtered dataframe by away team (equipe da casa) and calculate cumulative sum of 'Profit'
        df_away_profit = filtered_df.groupby('Away')['profit_away'].sum().reset_index()

        # Group the filtered dataframe by away team (equipe da casa) and calculate cumulative sum of 'Profit'
        df_away_profit = filtered_df.groupby(['Season', 'Away'])['profit_away'].sum().reset_index()

        # Create a pivot table of profit/loss by away team for the selected season
        away_team_profit_loss_pivot = df_away_profit.pivot_table(index="Away", columns="Season", values="profit_away")

        # Display the table with profit/loss by away team (pivot table)
        st.subheader("Desempenho Geral - Equipe Visitante")
        st.text("Serão exibidas todas as Equipes que se enquadraram no(s) filtro(s) de Odd")
        st.dataframe(home_team_profit_loss_pivot)

    ##### Top Back Visitante ####

        # Group the filtered DataFrame by 'Away' (Away Team) and calculate the cumulative sum of 'Profit'
        df_away_profit = filtered_df.groupby('AWay')['profit_away'].cumsum()

        # Add the 'Profit_acumulado' column to the filtered DataFrame
        filtered_df['profit_away_acumulado'] = df_away_profit

        # Filter the DataFrame to include only rows where 'Profit_acumulado' is greater than 1
        filtered_away_profit = filtered_df[filtered_df['profit_away_acumulado'] >= 3]

        # Group the filtered DataFrame by 'Away' (Away Team) and calculate the total profit for each home team
        away_team_total_profit = filtered_away_profit.groupby('Away')['profit_away_acumulado'].last()

        # Sort the home_team_total_profit DataFrame in descending order of profit
        away_team_total_profit_sorted = away_team_total_profit.sort_values(ascending=False)

        # Display the table with total profit by home team in descending order
        st.subheader("Top Back Visitante")
        st.text("Serão exibidas apenas as Equipes que acumulam pelo menos 3und de lucro")
        st.dataframe(away_team_total_profit_sorted)


    with tab3:

################################################################################3        

    ##### Calculo Win/Loss Over Back Visitante FT ####

        # Create a new DataFrame for the "Back Away FT" table
        df_back_away_ft = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_FT"] == "A"])
        num_loss = len(filtered_df[filtered_df["Resultado_FT"].isin(["H", "D"])])
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

        #### Add the data to the "Back Away FT" table ####
        df_back_away_ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Back AWay FT" table
        st.subheader("Back Visitante FT")
        st.dataframe(df_back_away_ft)
    
    with tab3:
    
    # Verificar se o DataFrame não está vazio
        if not filtered_df.empty:
    # Somar os valores da coluna 'profit_home' para obter o lucro total
            lucro_total = filtered_df['profit_away'].sum()

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

    # Ordenar o dataframe pela coluna Date (caso não esteja ordenado)
        filtered_df.sort_values(by='Date', inplace=True)

    # Calcular o acumulado de capital ao longo do tempo (soma cumulativa da coluna Profit)
        filtered_df['Lucro_Acumulado_FT'] = filtered_df['profit_away'].cumsum()

    # Criar o gráfico de linha com o acumulado de capital ao longo do tempo
        st.line_chart(filtered_df, x='Date', y='Lucro_Acumulado_FT', use_container_width=True)

###########################################################################################        

    ##### Calculo Win/Loss Over Back Visitante HT ####

        # Create a new DataFrame for the "Back Visitante HT" table
        df_back_away_ht = pd.DataFrame(columns=["Win", "Loss", "Odd Justa"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_HT"] == "A"])
        num_loss = len(filtered_df[filtered_df["Resultado_HT"].isin(["H", "D"])])
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

        #### Add the data to the "Back Away FT" table ####
        df_back_away_ht.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]

        # Display the "Back Away HT" table
        st.subheader("Back Away HT")
        st.dataframe(df_back_away_ht)

###################################################################################################33        

    ##### Calculo Win/Loss Lay Zebra FT ####

        # Create a new DataFrame for the "Lay Zebra FT" table
        df_lay_zebra_ft = pd.DataFrame(columns=["Win", "Loss", "Odd Lay"])

        # Calculate the number of "Win" and "Loss" occurrences
        num_win = len(filtered_df[filtered_df["Resultado_FT"] != "A"])
        num_loss = len(filtered_df[filtered_df["Resultado_FT"] == "A"])

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
            
        # Add the data to the "Lay Zebra FT" table
            df_lay_zebra_ft.loc[0] = [f"{win_percentage:.2f}%", f"{loss_percentage:.2f}%", fair_odd]
            
        # Display the "Lay Zebra FT" table
            st.subheader("Lay Zebra FT")
            st.dataframe(df_lay_zebra_ft)

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

   

# Execute the function to create the page
bck_away_page()

