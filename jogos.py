import streamlit as st
import pandas as pd
import datetime as dt

def jogos_do_dia_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

@st.cache_data(ttl=dt.timedelta(hours=24))
def load_base():
    # url = "https://github.com/futpythontrader/YouTube/blob/main/Jogos_do_Dia_FlashScore/2023-08-03_Jogos_do_Dia_FlashScore.csv?raw=true"
    url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"
    data_jogos = pd.read_csv(url)

    # Rename the columns
    data_jogos.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'Rodada': 'Round',
    }, inplace=True)

    return data_jogos

df2 = load_base()

# Filtrar Odds
# Aplicar o filtro ao DataFrame df2
filtered_df2 = df2[
    (df2['FT_Odd_H'].between(odd_casa_ft_min, odd_casa_ft_max)) &
    (df2['FT_Odd_D'].between(odd_casa_empate_min, odd_casa_empate_max)) &
    (df2['FT_Odd_A'].between(odd_fora_ft_min, odd_fora_ft_max)) &
    (df2['FT_Odd_Over25'].between(odd_over25_ft_min, odd_over25_ft_max)) &
    (df2['FT_Odd_BTTS_Yes'].between(odd_btts_min, odd_btts_max))
]

# Exibir o DataFrame filtrado apenas no tab9
with tab7:
    # Select the specific columns to display in the "Jogos Filtrados" table
    columns_to_display = [
        'Date', 'Time', 'League', 'Home', 'Away', 'Round', 'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A', 'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes' 
    ]
    st.dataframe(filtered_df2[columns_to_display])

# Créditos
st.text("Desenvolvido por Lyssandro Silveira")
st.markdown("Fale Comigo [link](https://t.me/Lyssandro)")
