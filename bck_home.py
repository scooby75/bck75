import streamlit as st
import pandas as pd

def bck_home_page():
    ##### PÁGINA BCK HOME ######
    tab0, tab1, tab2, tab3 = st.tabs(["Partidas Filtradas", "Desempenho", "Away", "League"])

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
        filtered_df = bck_home_df[
            (bck_home_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
            (bck_home_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
            (bck_home_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True) &
            (bck_home_df['Home'].isin(selected_home) if selected_home else True) &
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
            "Date", "League", "Season", "Round", "Home", "Away",
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
        data_ht = {'Performance': [f"{performance_home_ht:.2f}%"], 'Amostra': [tamanho_amostra_ht]}
        df_resultado_ht = pd.DataFrame(data_ht)

        # Exibindo o resultado
        st.subheader('Desempenho da Equipe HT')
        st.dataframe(df_resultado_ht)

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
        data_ft = {'Performance': [f"{performance_home_ft:.2f}%"], 'Amostra': [tamanho_amostra_ft]}
        df_resultado_ft = pd.DataFrame(data_ft)

        # Exibindo o resultado do desempenho da equipe FT
        st.subheader('Desempenho da Equipe FT')
        st.dataframe(df_resultado_ft)

    ##### Top Back Casa ####

    # Group the filtered DataFrame by 'Home' (Home Team) and calculate the cumulative sum of 'Profit'
        df_home_profit = filtered_df.groupby('Home')['profit_home'].cumsum()

    # Add the 'Profit_acumulado' column to the filtered DataFrame
        filtered_df['profit_home_acumulado'] = df_home_profit

    # Filter the DataFrame to include only rows where 'Profit_acumulado' is greater than 1
        filtered_home_profit = filtered_df[filtered_df['profit_home_acumulado'] >= 3]

    # Group the filtered DataFrame by 'Home' (Home Team) and calculate the total profit for each home team
        home_team_total_profit = filtered_home_profit.groupby('Home')['profit_home_acumulado'].last()

    # Sort the home_team_total_profit DataFrame in descending order of profit
        home_team_total_profit_sorted = home_team_total_profit.sort_values(ascending=False)

    # Display the table with total profit by home team in descending order
        st.subheader("Top Back Casa")
        st.text("Serão exibidas apenas as Equipes que acumulam pelo menos 3und de lucro")
        st.dataframe(home_team_total_profit_sorted)
        
        
    with tab2:
        st.write("dados")

    with tab3:
        st.write("dados")

# Execute the function to create the page
bck_home_page()

