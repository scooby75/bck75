import pandas as pd
import streamlit as st
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
    tab0, tab1, tab2, tab3 = st.tabs(["Partidas Filtradas", "Back Dia FT", "Placar FT", "Profit"])  

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
            selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_dia_home_df['League'].unique()))

            all_rounds = "Todos"
            selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_dia_home_df['Round'].unique()))

            all_seasons = "Todos"
            selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_dia_home_df['Season'].unique()))

            home_teams = bck_dia_home_df['Home'].unique()  # Get unique teams from 'Home' column
            selected_home = st.multiselect("Selecionar Mandante", home_teams)

            away_teams = bck_dia_home_df['Away'].unique()  # Get unique teams from 'Away' column
            selected_away = st.multiselect("Selecionar Visitante", away_teams)


        # Filter for Odd_Home and Odd_Away range
        with col2:
            odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0)
            odd_h_max = st.number_input("Odd_Home Máximo", value=20.0)

            odd_a_min = st.number_input("Odd_Away Mínimo", value=0.0)
            odd_a_max = st.number_input("Odd_Away Máximo", value=20.0)

            odd_draw_min = st.number_input("Odd_Empate Mínimo", value=0.0)
            odd_draw_max = st.number_input("Odd_Empate Máximo", value=20.0)

        # Filter for PPG and Day
        with col3:
            # PPG_Home filter
            min_rank_home = st.number_input("Rank Mínimo (Home)", min_value=1.0, max_value=50.0, value=1.0, key="min_rank_home")
            max_rank_home = st.number_input("Rank Máximo (Home)", min_value=1.0, max_value=50.0, value=50.0, key="max_rank_home")

            # Filter by "dia_semana"
            all_dias_semana = "Todos"
            selected_dias_semana = st.multiselect("Selecionar Dia da Semana", [all_dias_semana] + list(bck_dia_home_df['dia_semana'].unique()))

        # Remover espaços em branco dos nomes das colunas
        bck_dia_home_df.columns = bck_dia_home_df.columns.str.strip()

        # Apply filters
        filtered_df = bck_dia_home_df[
            (bck_dia_home_df['League'].isin(selected_leagues) | (all_leagues in selected_leagues)) &
            (bck_dia_home_df['Season'].isin(selected_seasons) | (all_seasons in selected_seasons)) &
            ((bck_dia_home_df['Round'].isin(selected_rounds)) if all_rounds not in selected_rounds else True) &
            ((bck_dia_home_df['Home'].isin(selected_home)) if selected_home else True) &
            ((bck_dia_home_df['Away'].isin(selected_away)) if selected_away else True) &
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
                            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "dia_semana", "Placar_HT", "Placar_FT", "profit_home", "profit_draw", "profit_away"]
        st.dataframe(filtered_df[selected_columns])

    with tab1:
        st.header("Back Dia FT")

        # Verifica se há resultados filtrados na tab0
        if not filtered_df.empty:
            # Agrupa por 'dia_semana' e calcula a soma para cada coluna de lucro
            df_agrupado = filtered_df.groupby('dia_semana').agg({
                'profit_home': 'sum',
                'profit_draw': 'sum',
                'profit_away': 'sum'
            }).reset_index()
            
            # Exibe o DataFrame agrupado
            st.dataframe(df_agrupado)
        else:
            st.warning("Nenhum resultado filtrado. Aplique os filtros na aba 'Partidas Filtradas.'")

    with tab2:
        st.header("Frequência Placar FT")

        # Check if there are filtered results
        if not filtered_df.empty:
            # Count the occurrences of each Placar_FT value
            placar_counts = filtered_df['Placar_FT'].value_counts()

            # Create a DataFrame to display the counts
            placar_counts_df = pd.DataFrame({'Placar_FT': placar_counts.index, 'Quantidade': placar_counts.values})

            # Display the DataFrame
            st.dataframe(placar_counts_df)
        else:
            st.warning("Nenhum resultado filtrado. Aplique os filtros na aba 'Partidas Filtradas.'")

    with tab3:
        st.header("Profit")
    
        selected_team_option = st.selectbox("Selecionar Equipe(s)", ["Ambos", "Mandante", "Visitante"])
        
        if not filtered_df.empty:
            if selected_team_option == "Mandante":
                # Check if 'Home' column exists before including it
                if 'Home' in filtered_df.columns:
                    filtered_df_team = filtered_df[['Season', 'Home', 'profit_home', 'profit_draw', 'profit_away']]
                else:
                    st.warning("A coluna 'Home' não está presente no DataFrame.")
                    filtered_df_team = pd.DataFrame()  # Create an empty DataFrame
            elif selected_team_option == "Visitante":
                # Check if 'Away' column exists before including it
                if 'Away' in filtered_df.columns:
                    filtered_df_team = filtered_df[['Season', 'Away', 'profit_home', 'profit_draw', 'profit_away']]
                else:
                    st.warning("A coluna 'Away' não está presente no DataFrame.")
                    filtered_df_team = pd.DataFrame()  # Create an empty DataFrame
            else:
                # Include 'Home' and 'Away' columns if they exist
                relevant_columns = ['Season', 'profit_home', 'profit_draw']
                if 'Home' in filtered_df.columns:
                    relevant_columns.append('Home')
                if 'Away' in filtered_df.columns:
                    relevant_columns.append('Away')
                filtered_df_team = filtered_df[relevant_columns]
    
            if not filtered_df_team.empty:
                # Group by 'Season' and 'Team' (either 'Home' or 'Away')
                group_by_columns = ['Season']
                if 'Home' in filtered_df_team.columns:
                    group_by_columns.append('Home')
                elif 'Away' in filtered_df_team.columns:
                    group_by_columns.append('Away')
    
                # Aggregate only the existing columns
                df_agrupado = filtered_df_team.groupby(group_by_columns).agg({
                    'profit_home': 'sum',
                    'profit_draw': 'sum',
                })
    
                # If 'profit_away' is present, include it in the aggregation
                if 'profit_away' in filtered_df_team.columns:
                    df_agrupado['profit_away'] = filtered_df_team['profit_away'].sum()
    
                df_agrupado = df_agrupado.reset_index()
                
                st.dataframe(df_agrupado)
            else:
                st.warning("Nenhum resultado filtrado para a opção selecionada.")
        else:
            st.warning("Nenhum resultado filtrado. Aplique os filtros na aba 'Partidas Filtradas.'")

# Execute a função principal
bck_dia_home_page()
