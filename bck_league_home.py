# bck_league_home.py

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta  

from session_state import SessionState

def bck_league_home_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
        
    ##### PÁGINA BCK LEAGUE HOME ######

    tab0, tab1, tab2, tab3 = st.tabs(["Partidas Filtradas", "Análise Geral", "Top Ligas", "Placar"])

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
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_league_home_df['League'].unique()), key="selected_leagues_leagues")

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_league_home_df['Round'].unique()), key="selected_rounds_leagues")

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_league_home_df['Season'].unique()), key="selected_seasons_leagues")

            home_teams = bck_league_home_df['Home'].unique()  # Get unique teams from 'Home' column
            #selected_home = st.multiselect("Selecionar Mandante", home_teams, key="selected_home")

        # Filter for Odd_Home and Odd_Away range
        with col2:
            odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0, key="odd_h_min_leagues")
            odd_h_max = st.number_input("Odd_Home Máximo", value=10.0, key="odd_h_max_leagues")

            odd_a_min = st.number_input("Odd_Away Mínimo", value=0.0, key="odd_a_min_leagues")
            odd_a_max = st.number_input("Odd_Away Máximo", value=10.0, key="odd_a_max_leagues")
    
            odd_draw_min = st.number_input("Odd_Empate Mínimo", value=0.0, key="odd_draw_min_leagues")
            odd_draw_max = st.number_input("Odd_Empate Máximo", value=10.0, key="odd_draw_max_leagues")

        # Filter for Over_05HT (HT_Odd_Over05) range and Over_25FT (FT_Odd_Over25)
        with col3:
            
            over_05ht_min = st.number_input("Over_05HT Mínimo", value=0.0, key="over_05ht_min_leagues")
            over_05ht_max = st.number_input("Over_05HT Máximo", value=10.0, key="over_05ht_max_leagues")

            over_25ft_min = st.number_input("Over_25FT Mínimo", value=0.0, key="over_25ft_min_leagues")
            over_25ft_max = st.number_input("Over_25FT Máximo", value=10.0, key="over_25ft_max_leagues")

            btts_yes_min = st.number_input("BTTS_Yes Mínimo", value=0.0, key="btts_yes_min_leagues")
            btts_yes_max = st.number_input("BTTS_Yes Máximo", value=10.0, key="btts_yes_max_leagues")

        # Apply filters
        filtered_df = bck_league_home_df[
            (bck_league_home_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
            (bck_league_home_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
            (bck_league_home_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True) &
            #(bck_league_home_df['Home'].isin(selected_home) if selected_home else True) &
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
        
        # Agrupar o DataFrame filtrado pela Liga e calcular a soma cumulativa do 'Lucro' tanto em casa quanto fora
	    profit_home_by_season_league = filtered_df.groupby(['Season', 'League'])[['profit_home', 'profit_away']].sum().reset_index()

	    # Criar uma tabela dinâmica do lucro/prejuízo combinado das equipes da casa e fora para a temporada selecionada
	    profit_home_by_season_league_pivot = profit_home_by_season_league.pivot_table(index="League", columns="Season", values=["profit_home", "profit_away"])

	    # Exibir a tabela com o lucro/prejuízo combinado das equipes da casa e fora (tabela dinâmica)
	    st.subheader("Back Casa - Desempenho por Liga")
	    st.text("Serão exibidas todas as equipes que atenderam aos critérios de filtro de Odds")
	    st.dataframe(profit_home_by_season_league_pivot, width=800)


        ####################################################        
        # back visitante agrupado por liga
        profit_away_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_away'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_away_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_away', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Back Visitante - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

        

    ####################################################        
        # back empate agrupado por liga
        profit_draw_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_draw'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_draw_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_draw', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Back Empate - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    

    ####################################################        
        # Over 05HT agrupado por liga
        profit_ov05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over05HT', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 05HT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

   

    ####################################################        
        # Over U5HT agrupado por liga
        profit_u05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under05HT', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 05HT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ####################################################        
        # Over 15FT agrupado por liga
        profit_ov15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over15', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 15FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Under 15FT agrupado por liga
        profit_u15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under15', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 15FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Over 25FT agrupado por liga
        profit_ov25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over25', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 25FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Under 25FT agrupado por liga
        profit_u25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under25', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 25FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Over 35FT agrupado por liga
        profit_ov35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over35', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 35FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Under 35FT agrupado por liga
        profit_u35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under35', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 35FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Over 45FT agrupado por liga
        profit_ov45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over45', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Over 45FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

    ##################################################        
        # Under 45FT agrupado por liga
        profit_u45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under45', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Under 45FT - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)
        

    ##################################################        
        # Lay 0x1 agrupado por liga
        profit_lay01_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_0x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay01_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_0x1', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 0x1 - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

     ##################################################        
        # Lay 1x0 agrupado por liga
        profit_lay10_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x0'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay10_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x0', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 1x0 - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

       ##################################################        
        # Lay 1x2 agrupado por liga
        profit_lay12_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x2'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay12_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x2', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 1x2 - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)

        ##################################################        
        # Lay 2x1 agrupado por liga
        profit_lay21_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_2x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay21_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_2x1', aggfunc='sum')

        # Display profit/loss by Season and League with Season as columns and League as rows
        st.subheader("Lay 2x1 - Desempenho por Liga")
        st.dataframe(pivot_table, width=800)
    
    with tab2:

        ####################################################        
        # Top back casa agrupado por liga
        profit_home_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_home'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_home_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_home', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Back Casa - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top back visitante agrupado por liga
        profit_away_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_away'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_away_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_away', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Back Visitante - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top back empate agrupado por liga
        profit_draw_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_draw'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_draw_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_draw', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Back Empate - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Over 05HT agrupado por liga
        profit_ov05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over05HT', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Over 05HT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Under 05HT agrupado por liga
        profit_u05ht_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under05HT'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u05ht_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under05HT', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Under 05HT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Over 15FT agrupado por liga
        profit_ov15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over15', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Over 15FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Under 15FT agrupado por liga
        profit_u15ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under15'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u15ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under15', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Under 15FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Over 25FT agrupado por liga
        profit_ov25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over25', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Over 25FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Under 25FT agrupado por liga
        profit_u25ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under25'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u25ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under25', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Under 25FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Over 35FT agrupado por liga
        profit_ov35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over35', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Over 35FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Under 35FT agrupado por liga
        profit_u35ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under35'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u35ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under35', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Under 35FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Over 45FT agrupado por liga
        profit_ov45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_over45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_ov45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_over45', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Over 45FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Under 45FT agrupado por liga
        profit_u45ft_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_under45'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_u45ft_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_under45', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()

        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Under 45FT - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Lay 0x1 agrupado por liga
        profit_lay01_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_0x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay01_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_0x1', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Lay 0x1 - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Lay 1x0 agrupado por liga
        profit_lay10_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x0'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay10_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x0', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Lay 1x0 - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Lay 1x2 agrupado por liga
        profit_lay12_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_1x2'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay12_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_1x2', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Lay 1x2 - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

        ####################################################        
        # Top Lay 2x1 agrupado por liga
        profit_lay21_by_season_league = filtered_df.groupby(['Season', 'League'])['profit_Lay_2x1'].sum()

        # Use a função pivot_table para reorganizar os dados
        pivot_table = profit_lay21_by_season_league.reset_index().pivot_table(index='League', columns='Season', values='profit_Lay_2x1', aggfunc='sum')

        # Filtrar as ligas que tiveram lucro em todas as temporadas
        profitable_leagues = pivot_table[pivot_table.gt(0).all(axis=1)]

        # Calcular o lucro acumulado nas temporadas lucrativas
        cumulative_profit = profitable_leagues.cumsum()
        
        # Exibir o lucro acumulado por liga nas temporadas lucrativas
        st.subheader("Top Lay 2x1 - Desempenho por Liga")
        st.dataframe(cumulative_profit, width=800)

################ Placar ##########################
    
    with tab3:
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

  
        
        
# Execute the function to create the page
bck_league_home_page()


