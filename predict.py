import streamlit as st
import pandas as pd
import datetime as dt

def predict_page(perfil_usuario):
    if perfil_usuario == 1:  # Verifica o nível de acesso do usuário
        st.warning("Você não tem acesso a esta funcionalidade.")
        return
        
    st.subheader("Filtro Preditivo")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=dt.timedelta(hours=24))
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/Predict.csv?raw=true"
        data_jogos = pd.read_csv(url)

        # Rename the columns
        data_jogos.rename(columns={
            'Vitoria_H': 'Prob_Vitoria_Home',
            'Vitoria_A': 'Prob_Vitoria_Away',
            'Over25_H': 'Prob_Over25_Home',
            'Over25_A': 'Prob_Over25_Away',
            'MediaGols_H': 'Media_Gols_H',
            'MediaGols_A': 'Media_Gols_A',
            'PPG_H': 'PPG_H',
            'PPG_A': 'PPG_A',
        }, inplace=True)

        return data_jogos

    df2 = load_base()

    # Create number inputs for filter conditions
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        prob_vitoria_home_min = st.number_input("Prob Vitória Home (min)", 0, 100, 0)
        prob_vitoria_home_max = st.number_input("Prob Vitória Home (max)", prob_vitoria_home_min, 100, 100)
        prob_vitoria_away_min = st.number_input("Prob Vitória Away (min)", 0, 100, 0)
        prob_vitoria_away_max = st.number_input("Prob Vitória Away (max)", prob_vitoria_away_min, 100, 100)

    with col2:
        prob_over25_home_min = st.number_input("Prob Over 2.5 Home (min)", 0, 100, 0)
        prob_over25_home_max = st.number_input("Prob Over 2.5 Home (max)", prob_over25_home_min, 100, 100)
        prob_over25_away_min = st.number_input("Prob Over 2.5 Away (min)", 0, 100, 0)
        prob_over25_away_max = st.number_input("Prob Over 2.5 Away (max)", prob_over25_away_min, 100, 100)

    with col3:
        media_gols_h_min = st.number_input("Média Gols H (min)", 0.0, 10.0, 0.0)
        media_gols_h_max = st.number_input("Média Gols H (max)", media_gols_h_min, 10.0, 10.0)
        media_gols_a_min = st.number_input("Média Gols A (min)", 0.0, 10.0, 0.0)
        media_gols_a_max = st.number_input("Média Gols A (max)", media_gols_a_min, 10.0, 10.0)

    with col4:
        ppg_h_min = st.number_input("PPG H (min)", 0.0, 3.0, 0.0)
        ppg_h_max = st.number_input("PPG H (max)", ppg_h_min, 3.0, 3.0)
        ppg_a_min = st.number_input("PPG A (min)", 0.0, 3.0, 0.0)
        ppg_a_max = st.number_input("PPG A (max)", ppg_a_min, 3.0, 3.0)

    # Specify columns to display in the sorted data
    columns_to_display = [
        'Hora', 'Home', 'Away', 'Prob_Vitoria_Home', 'Prob_Vitoria_Away',
        'Prob_Over25_Home', 'Prob_Over25_Away', 'Media_Gols_H', 'Media_Gols_A', 'PPG_H', 'PPG_A'
    ]

    if not df2.empty:
        filtered_data = df2.copy()

        # Apply filters with ranges
        filtered_data = filtered_data[
            (filtered_data['Prob_Vitoria_Home'] >= prob_vitoria_home_min) &
            (filtered_data['Prob_Vitoria_Home'] <= prob_vitoria_home_max) &
            (filtered_data['Prob_Vitoria_Away'] >= prob_vitoria_away_min) &
            (filtered_data['Prob_Vitoria_Away'] <= prob_vitoria_away_max) &
            (filtered_data['Prob_Over25_Home'] >= prob_over25_home_min) &
            (filtered_data['Prob_Over25_Home'] <= prob_over25_home_max) &
            (filtered_data['Prob_Over25_Away'] >= prob_over25_away_min) &
            (filtered_data['Prob_Over25_Away'] <= prob_over25_away_max) &
            (filtered_data['Media_Gols_H'] >= media_gols_h_min) &
            (filtered_data['Media_Gols_H'] <= media_gols_h_max) &
            (filtered_data['Media_Gols_A'] >= media_gols_a_min) &
            (filtered_data['Media_Gols_A'] <= media_gols_a_max) &
            (filtered_data['PPG_H'] >= ppg_h_min) &
            (filtered_data['PPG_H'] <= ppg_h_max) &
            (filtered_data['PPG_A'] >= ppg_a_min) &
            (filtered_data['PPG_A'] <= ppg_a_max) &
            (filtered_data['GP_H'] >= 5)
        ]

        # Sort the filtered data by 'Hora'
        filtered_data = filtered_data.sort_values(by='Hora')

        # Display the filtered data
        st.dataframe(filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Determinar o valor do perfil_usuario com base na lógica de autenticação ou gerenciamento de perfil
perfil_usuario = 1  # Substitua pelo valor real obtido da lógica de autenticação

# Chamar a função para executar o app
predict_page(perfil_usuario)



