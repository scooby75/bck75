import streamlit as st
import pandas as pd

def bck_home_page():
    ##### PÁGINA BCK HOME ######

    # Criar abas
    abas = ["Filtros", "Aba 1", "Aba 2"]
    aba_atual = st.tabs(abas)

    if aba_atual == "Filtros":
        st.header("Filtros")

        # Load data
        @st.cache_data(ttl=86400.0)  # 24 horas em segundos
        def carregar_base():
            url = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
            df = pd.read_csv(url)
            return df
        
        # Chamar a função para carregar os dados
        df_bck_home = carregar_base()

        # Organizar os filtros em colunas
        col1, col2, col3 = st.columns(3)

        # Filtrar por Liga, Temporada, Rodada, Mandante
        with col1:
            todas_ligas = "Todas"
            ligas_selecionadas = st.multiselect("Selecionar Liga(s)", [todas_ligas] + list(df_bck_home['League'].unique()))

            todas_rodadas = "Todas"
            rodadas_selecionadas = st.multiselect("Selecionar Rodada(s)", [todas_rodadas] + list(df_bck_home['Round'].unique()))

            todas_temporadas = "Todas"
            temporadas_selecionadas = st.multiselect("Selecionar Temporada(s)", [todas_temporadas] + list(df_bck_home['Season'].unique()))

            mandantes = df_bck_home['Home'].unique()  # Obter mandantes únicos da coluna 'Home'
            mandante_selecionado = st.multiselect("Selecionar Mandante", mandantes)

        # Filtrar faixa de Odd_Home e Odd_Away
        with col2:
            odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0)
            odd_h_max = st.number_input("Odd_Home Máximo", value=10.0)

            odd_a_min = st.number_input("Odd_Away Mínimo", value=0.0)
            odd_a_max = st.number_input("Odd_Away Máximo", value=10.0)
            
            odd_empate_min = st.number_input("Odd_Empate Mínimo", value=0.0)
            odd_empate_max = st.number_input("Odd_Empate Máximo", value=10.0)

        # Filtrar faixa de Over_05HT (HT_Odd_Over05) e Over_25FT (FT_Odd_Over25)
        with col3:
            over_05ht_min = st.number_input("Over_05HT Mínimo", value=0.0)
            over_05ht_max = st.number_input("Over_05HT Máximo", value=10.0)

            over_25ft_min = st.number_input("Over_25FT Mínimo", value=0.0)
            over_25ft_max = st.number_input("Over_25FT Máximo", value=10.0)
            
            btts_yes_min = st.number_input("BTTS_Yes Mínimo", value=0.0)
            btts_yes_max = st.number_input("BTTS_Yes Máximo", value=10.0)

        # Aplicar filtros
        df_filtrado = df_bck_home[
            (df_bck_home['League'].isin(ligas_selecionadas) if todas_ligas not in ligas_selecionadas else True) &
            (df_bck_home['Season'].isin(temporadas_selecionadas) if todas_temporadas not in temporadas_selecionadas else True) &
            (df_bck_home['Round'].isin(rodadas_selecionadas) if todas_rodadas not in rodadas_selecionadas else True) &
            (df_bck_home['Home'].isin(mandante_selecionado) if mandante_selecionado else True) &
            (df_bck_home['FT_Odd_H'] >= odd_h_min) &
            (df_bck_home['FT_Odd_H'] <= odd_h_max) &
            (df_bck_home['FT_Odd_A'] >= odd_a_min) &
            (df_bck_home['FT_Odd_A'] <= odd_a_max) &
            (df_bck_home['FT_Odd_D'] >= odd_empate_min) &
            (df_bck_home['FT_Odd_D'] <= odd_empate_max) &
            (df_bck_home['HT_Odd_Over05'] >= over_05ht_min) &
            (df_bck_home['HT_Odd_Over05'] <= over_05ht_max) &
            (df_bck_home['FT_Odd_Over25'] >= over_25ft_min) &
            (df_bck_home['FT_Odd_Over25'] <= over_25ft_max) &
            (df_bck_home['Odd_BTTS_Yes'] >= btts_yes_min) &
            (df_bck_home['Odd_BTTS_Yes'] <= btts_yes_max)
        ]

        # Exibir colunas selecionadas dos dados filtrados
        colunas_selecionadas = [
            "Date", "League", "Season", "Round", "Home", "Away",
            "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "HT_Odd_Over05", "FT_Odd_Over25", "Odd_BTTS_Yes", "Placar_HT", "Placar_FT"
        ]
        st.dataframe(df_filtrado[colunas_selecionadas])

    elif aba_atual == "Aba 1":
        # Espaço reservado para o conteúdo da Aba 1
        st.write("Conteúdo da Aba 1 aqui.")

    elif aba_atual == "Aba 2":
        # Espaço reservado para o conteúdo da Aba 2
        st.write("Conteúdo da Aba 2 aqui.")

# Executar a função para criar a página
bck_home_page()
