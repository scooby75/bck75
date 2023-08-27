import streamlit as st
import pandas as pd

def bck_league_home_page():
    ##### PÁGINA BCK LEAGUE HOME ######

    tab0, tab1, tab2, tab3 = st.tabs(["Partidas Filtradas", "Desempenho HT", "Desempenho FT", "Backtesting Mercado"])

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

####################################################        
        # back casa agrupado por liga
        profit_home_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_home'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_home_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_home', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Back Casa - Desempenho por Liga")
        st.dataframe(pivot_table)

        ####################################################        
        # back visitante agrupado por liga
        profit_away_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_away'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_away_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_away', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Back Visitante - Desempenho por Liga")
        st.dataframe(pivot_table)

    ####################################################        
        # back empate agrupado por liga
        profit_draw_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_draw'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_draw_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_draw', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Back Empate - Desempenho por Liga")
        st.dataframe(pivot_table)

    ####################################################        
        # Over 05HT agrupado por liga
        profit_ov05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over05HT', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 05HT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ####################################################        
        # Over U5HT agrupado por liga
        profit_u05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under05HT', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 05HT - Desempenho por Liga")
        st.dataframe(pivot_table)

     ####################################################        
        # Over 15FT agrupado por liga
        profit_ov15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over15', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 15FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Under 15FT agrupado por liga
        profit_u15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under15', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 15FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Over 25FT agrupado por liga
        profit_ov25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over25', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 25FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Under 25FT agrupado por liga
        profit_u25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under25', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 25FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Lay 0x1 agrupado por liga
        profit_lay01_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_0x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay01_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_0x1', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 0x1 - Desempenho por Liga")
        st.dataframe(pivot_table)

        
        
    with tab2:
          ##### Desempenho da Equipe FT ######
        st.write("Profit/Loss for Home Team (grouped by League)")
        
    with tab3:

################################################################################3        

    ##### Calculo Win/Loss Over Back Casa FT ####

         st.write("Profit/Loss for Home Team (grouped by League)")
        
# Execute the function to create the page
bck_league_home_page()

