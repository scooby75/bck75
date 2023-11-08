import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from session_state import SessionState

def bck_dia_home_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 3  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    ##### PÁGINA BCK DIA ######
    tab0, tab1 = st.columns(2)  # Changed from st.tabs to st.columns

    with tab0:
        # Carregar os dados
        @st.cache_data(ttl=28800.0)  # 24 horas em segundos
        def load_base():
            url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/BD_Geral_Rank_Dia_Semana.csv"
            df = pd.read_csv(url)
            return df

        # Chamar a função para carregar os dados
        bck_dia_home_df = load_base()

        # Filtros interativos
        st.header("Filtros")

        # Organize filters into columns
        col1, col2, col3 = st.columns(3)

        # Filter by League, Season, Round, Home
        with col1:
            all_leagues = "Todos"
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_home_df['League'].unique())

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_home_df['Round'].unique()))

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_home_df['Season'].unique())
        
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

        # Filter for PPG and Day
        with col3:
            # PPG_Home filter
            min_rank_home = st.number_input("Rank Mínimo (Home)", min_value=1.0, max_value=50.0, value=1.0, key="min_rank_home")
            max_rank_home = st.number_input("Rank Máximo (Home)", min_value=1.0, max_value=50.0, value=50.0, key="max_rank_home")

            # Filter by "dia_semana"
            all_dias_semana = "Todos"
            selected_dias_semana = st.multiselect("Selecionar Dia da Semana", [all_dias_semana] + list(bck_dia_home_df['dia_semana'].unique())

        # Remover espaços em branco dos nomes das colunas
        bck_dia_home_df.columns = bck_dia_home_df.columns.str.strip()

        # Apply filters
        filtered_df = bck_dia_home_df[
            (bck_dia_home_df['League'].isin(selected_leagues) | (all_leagues in selected_leagues)) &
            (bck_dia_home_df['Season'].isin(selected_seasons) | (all_seasons in selected_seasons)) &
            ((bck_dia_home_df['Round'].isin(selected_rounds)) if all_rounds not in selected_rounds else True) &
            ((bck_dia_home_df['Home'].isin(selected_home)) if selected_home else True) &
            (bck_dia_home_df['Rank_Home'] >= min_rank_home) &
            (bck_dia_home_df['Rank_Home'] <= max_rank_home) &
            (bck_dia_home_df['FT_Odd_H'] >= odd_h_min) &
            (bck_dia_home_df['FT_Odd_H'] <= odd_h_max) &
            (bck_dia_home_df['FT_Odd_A'] >= odd_a_min) &
            (bck_dia_home_df['FT_Odd_A'] <= odd_a_max) &
            (bck_dia_home_df['FT_Odd_D'] >= odd_draw_min) &
            (bck_dia_home_df['FT_Odd_D'] <= odd_draw_max) &
            (bck_dia_home_df['dia_semana'].isin(selected_dias_semana) | (all_dias_semana in selected_dias_semana))
        ]

        # Display selected columns from the filtered data
        selected_columns = ["Date", "League", "Season", "Round", 'Rank_Home', "Home", "Away",
                            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "dia_semana", "Placar_HT", "Placar_FT"]
        st.dataframe(filtered_df[selected_columns])

    with tab1:
        # Define a function to calculate profit for a given day of the week
        def calculate_profit_by_day(filtered_df, day_of_week):
            # Filter the DataFrame for the given day of the week
            day_filtered_df = filtered_df[filtered_df['dia_semana'] == day_of_week]

            # Filter matches for Casa (H), Empate (D), and Visitante (A) outcomes
            casa_matches = day_filtered_df[day_filtered_df['Resultado_FT'] == 'H']
            empate_matches = day_filtered_df[day_filtered_df['Resultado_FT'] == 'D']
            visitante_matches = day_filtered_df[day_filtered_df['Resultado_FT'] == 'A']

            # Calculate profit for each outcome
            profit_casa = casa_matches['FT_Odd_H'].astype(float).sum()
            profit_empate = empate_matches['FT_Odd_D'].astype(float).sum()
            profit_visitante = visitante_matches['FT_Odd_A'].astype(float).sum()

            return profit_casa, profit_empate, profit_visitante

        # Define the list of days of the week
        days_of_week = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']

        # Create a table to display profit for each day of the week
        st.header("Análise por Dia da Semana")
        for day in days_of_week:
            profit_casa, profit_empate, profit_visitante = calculate_profit_by_day(filtered_df, day)

            st.subheader(day.capitalize())
            st.write("Casa:", profit_casa)
            st.write("Empate:", profit_empate)
            st.write("Visitante:", profit_visitante)

# Execute the function to create the page
bck_dia_home_page()
