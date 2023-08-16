import streamlit as st

def app():
    # URL do arquivo CSV
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

# Carregar o arquivo CSV em um dataframe
    df = pd.read_csv(url)

# Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'Rodada': 'Round',
    }, inplace=True)

# Função para extrair o número do texto "ROUND N"
    def extrair_numero_round(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

# Aplicando a função para extrair o número do "Round" e criando uma nova coluna "Round_Num"
    df["Round_Num"] = df["Round"].apply(extrair_numero_round)

# Filtrando os jogos com valores de "FT_Odd_H" entre 1.40 e 2.0 e "Round_Num" maior ou igual a 10
    eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Round_Num"] >= 10)]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    eventos_raros_df = eventos_raros_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Casa")
    st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
    st.dataframe(eventos_raros_df)

# Adicionar botão de download do dataframe filtrado em formato CSV
    #csv_file = eventos_raros_df.to_csv(index=False)
    #st.download_button(label="Download CSV", data=csv_file, file_name="eventos_raros_casa.csv", mime="text/csv")

####

# Filtrando os jogos com valores de "FT_Odd_A" entre 1.40 e 2.0 e "Round_Num" maior ou igual a 10
    eventos_raros2_df = df[(df["FT_Odd_A"] >= 1.71) & (df["FT_Odd_A"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Round_Num"] >= 10)]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    eventos_raros2_df = eventos_raros2_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Visitante")
    st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
    st.dataframe(eventos_raros2_df)

# Adicionar botão de download do dataframe filtrado em formato CSV
    #csv_file = eventos_raros2_df.to_csv(index=False)
    #st.download_button(label="Download CSV", data=csv_file, file_name="eventos_raros_visitante.csv", mime="text/csv")

    #####

    # Filtrando os jogos com valores de "FT_Odd_H" eh menor que 1.50 e "Round_Num" maior ou igual a 10
    lay0x2_df = df[(df["FT_Odd_H"] <= 1.50) & (df["Round_Num"] >= 10)]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    lay0x2_df = lay0x2_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("Lay 0x2")
    st.text("Apostar em Lay 0x2, Odd máxima 50")
    st.dataframe(lay0x2_df)

# Adicionar botão de download do dataframe filtrado em formato CSV
    #csv_file = lay0x2_df.to_csv(index=False)
    #st.download_button(label="Download CSV", data=csv_file, file_name="eventos_raros_lay0x2.csv", mime="text/csv")

#####

# Filtrando os jogos com valores de "FT_Odd_H" eh menor que 1.50 e "Round_Num" maior ou igual a 10
    layzebraht_df = df[
    (df["FT_Odd_H"] >= 1.01) & (df["FT_Odd_H"] <= 1.7) &
    (df["FT_Odd_A"] >= 5.5) & (df["FT_Odd_A"] <= 10) &
    (df["Round_Num"] >= 10)
    ]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    layzebraht_df = layzebraht_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Zebra HT")
    st.text("Apostar em Lay visitante, Odd máxima 6")
    st.dataframe(layzebraht_df)

# Adicionar botão de download do dataframe filtrado em formato CSV
    #csv_file = layzebraht_df.to_csv(index=False)
    #st.download_button(label="Download CSV", data=csv_file, file_name="eventos_raros_layzebraht.csv", mime="text/csv")

    ####

# URL to the CSV file
    #url = "https://github.com/futpythontrader/YouTube/blob/main/Jogos_do_Dia_FlashScore/2023-08-03_Jogos_do_Dia_FlashScore.csv?raw=true"
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

# Load the CSV data from the URL into a DataFrame
    df = pd.read_csv(url)
    
# Check if any "home" team is present in top_over_05HT_casa
    matches_over_05 = df[df["Home"].isin(top_over_05HT_casa)]

# Create df.over05 with the matches where the "home" team is in top_over_05HT_casa
    df_over05 = matches_over_05.copy()

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    df_over05 = df_over05[colunas_desejadas]

# Display the DataFrame df.over05
    st.subheader("Back Over 05HT")
    st.dataframe(df_over05)

##### HA -0,25 ######

    # URL to the CSV file
    #url = "https://github.com/futpythontrader/YouTube/blob/main/Jogos_do_Dia_FlashScore/2023-08-03_Jogos_do_Dia_FlashScore.csv?raw=true"
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"

    # Load the CSV data from the URL into a DataFrame
    df = pd.read_csv(url)

    # Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'Rodada': 'Round',
    }, inplace=True)

# Função para extrair o número do texto "ROUND N"
    def extrair_numero_round(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

# Aplicando a função para extrair o número do "Round" e criando uma nova coluna "Round_Num"
    df["Round_Num"] = df["Round"].apply(extrair_numero_round)

    
# Filtrando os jogos com valores de "FT_Odd_A" entre 1.40 e 2.0 e "Round_Num" maior ou igual a 10
    ha_df = df[
        (df["FT_Odd_H"] <= 1.90) &
        (df["Odds_DuplaChance_1X"] <= 1.25) &
        (df["PPG_Home"] >= 2) &
        (df["PPG_Away"] <= 1.50) &
        (df["Round_Num"] >= 10)
    ]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    ha_df = ha_df[colunas_desejadas]

# Exibir o dataframe "Eventos Raros"
    st.subheader("HA -0.25")
    st.text("Apostar em HA -0.25 casa, Odd minima 1.50")
    st.dataframe(ha_df)
    