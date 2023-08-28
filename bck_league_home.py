import streamlit as st
import pandas as pd

def bck_league_home_page():
    ##### PÁGINA BCK LEAGUE HOME ######

    tab0, tab1, tab2 = st.tabs(["Partidas Filtradas", "Análise Geral", "Top Ligas"])

    with tab0:
        # Carregar os dados
        @st.cache_data(ttl=28800.0)  # 24 horas em segundos
        def load_base():
            url = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
            df = pd.read_csv(url)
            return df
        
        # Chamar a função para carregar os dados
        bck_league_home_df = load_base()

        # Filtros interativos
        st.header("Filtros")

        # Organize filters into columns
        col1, col2, col3 = st.columns(3)

        # Filter by League, Season, Round, Home
        with col1:
            
            all_leagues = "Todos"
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_league_home_df['League'].unique()), key="selected_leagues")

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_league_home_df['Round'].unique()), key="selected_rounds")

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_league_home_df['Season'].unique()), key="selected_seasons")

            home_teams = bck_league_home_df['Home'].unique()  # Get unique teams from 'Home' column
            selected_home = st.multiselect("Selecionar Mandante", home_teams, key="selected_home")

        # Filter for Odd_Home and Odd_Away range
        with col2:
            odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0, key="odd_h_min")
            odd_h_max = st.number_input("Odd_Home Máximo", value=10.0, key="odd_h_max")

            odd_a_min = st.number_input("Odd_Away Mínimo", value=0.0, key="odd_a_min")
            odd_a_max = st.number_input("Odd_Away Máximo", value=10.0, key="odd_a_max")
    
            odd_draw_min = st.number_input("Odd_Empate Mínimo", value=0.0, key="odd_draw_min")
            odd_draw_max = st.number_input("Odd_Empate Máximo", value=10.0, key="odd_draw_max")

        # Filter for Over_05HT (HT_Odd_Over05) range and Over_25FT (FT_Odd_Over25)
        with col3:
            
            over_05ht_min = st.number_input("Over_05HT Mínimo", value=0.0, key="over_05ht_min")
            over_05ht_max = st.number_input("Over_05HT Máximo", value=10.0, key="over_05ht_max")

            over_25ft_min = st.number_input("Over_25FT Mínimo", value=0.0, key="over_25ft_min")
            over_25ft_max = st.number_input("Over_25FT Máximo", value=10.0, key="over_25ft_max")

            btts_yes_min = st.number_input("BTTS_Yes Mínimo", value=0.0, key="btts_yes_min")
            btts_yes_max = st.number_input("BTTS_Yes Máximo", value=10.0, key="btts_yes_max")

        # Apply filters
        filtered_df = bck_league_home_df[
            (bck_league_home_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
            (bck_league_home_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
            (bck_league_home_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True) &
            (bck_league_home_df['Home'].isin(selected_home) if selected_home else True) &
            (bck_league_home_df['FT_Odd_H'] >= odd_h_min) &
            (bck_league_home_df['FT_Odd_H'] <= odd_h_max) &
            (bck_league_home_df['FT_Odd_A'] >= odd_a_min) &
            (bck_league_home_df['FT_Odd_A'] <= odd_a_max) &
            (bck_league_home_df['FT_Odd_D'] >= odd_draw_min) &
            (bck_league_home_df['FT_Odd_D'] <= odd_draw_max) &
            (bck_league_home_df['HT_Odd_Over05'] >= over_05ht_min) &
            (bck_league_home_df['HT_Odd_Over05'] <= over_05ht_max) &
            (bck_league_home_df['FT_Odd_Over25'] >= over_25ft_min) &
            (bck_league_home_df['FT_Odd_Over25'] <= over_25ft_max) &
            (bck_league_home_df['Odd_BTTS_Yes'] >= btts_yes_min) &
            (bck_league_home_df['Odd_BTTS_Yes'] <= btts_yes_max)
        ]

        selected_columns = [
            "Date", "League", "Season", "Round", "Home", "Away",
            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "HT_Odd_Over05", "FT_Odd_Over25", "Odd_BTTS_Yes", "Placar_HT", "Placar_FT", "profit_Lay_0x1",
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
        # Over 35FT agrupado por liga
        profit_ov35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over35', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 35FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Under 35FT agrupado por liga
        profit_u35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under35', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 35FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Over 45FT agrupado por liga
        profit_ov45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over45', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 45FT - Desempenho por Liga")
        st.dataframe(pivot_table)

    ##################################################        
        # Under 45FT agrupado por liga
        profit_u45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under45', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 45FT - Desempenho por Liga")
        st.dataframe(pivot_table)
        

    ##################################################        
        # Lay 0x1 agrupado por liga
        profit_lay01_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_0x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay01_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_0x1', aggfunc='sum')

        # Filtrar as ligas que lucraram >= 2 em todas as temporadas
        profit_threshold => 1
        profit_ligas = pivot_table[(pivot_table >= profit_threshold).all(axis=1)]

        # Exibir as ligas que atendem ao critério de lucro em todas as temporadas
        st.subheader(f"Ligas com lucro >= {profit_threshold} em todas as temporadas")
        st.dataframe(profit_ligas)

     ##################################################        
        # Lay 1x0 agrupado por liga
        profit_lay10_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x0'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay10_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x0', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 1x0 - Desempenho por Liga")
        st.dataframe(pivot_table)

       ##################################################        
        # Lay 1x2 agrupado por liga
        profit_lay12_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x2'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay12_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x2', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 1x2 - Desempenho por Liga")
        st.dataframe(pivot_table)

        ##################################################        
        # Lay 2x1 agrupado por liga
        profit_lay21_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_2x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay21_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_2x1', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 2x1 - Desempenho por Liga")
        st.dataframe(pivot_table)

    with tab2:
    ########################## top ligas ##############################

    
        ###########################################################
        # Calcula o lucro total das apostas em casa agrupadas por liga e temporada
        profit_home_by_league_season = filtered_df.groupby(['League', 'Season'])['profit_home'].sum()

        # Filtra as ligas que lucraram pelo menos 1 unidade em todas as temporadas
        profitable_leagues = profit_home_by_league_season.groupby('League').filter(lambda x: (x >= 2).all())

        # Converte o resultado filtrado em um DataFrame
        filtered_df = profitable_leagues.reset_index()

        # Cria uma tabela dinâmica para organizar os dados
        pivot_table = filtered_df.pivot_table(index='League', columns='Season', values='profit_home', aggfunc='sum')

        # Exibe a tabela dinâmica usando o Streamlit
        st.subheader("Top Back Casa")
        st.dataframe(pivot_table)

    #########################################


  


        
        
# Execute the function to create the page
bck_league_home_page()


