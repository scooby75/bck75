import streamlit as st
import pandas as pd
import datetime as dt

def jogos_do_dia_page():
    st.set_page_config(page_title="Football Data Analysis", layout="wide")
    
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

    # Debug: Exibir as primeiras linhas do DataFrame
    st.write("Primeiras linhas do DataFrame:")
    st.write(df2.head())

    # Debug: Verificar se as colunas especificadas estão presentes
    st.write("Colunas do DataFrame:")
    st.write(df2.columns)

    # Select the specific columns to display in the "Jogos Filtrados" table
    columns_to_display = [
        'Date', 'Time', 'League', 'Home', 'Away', 'Round', 'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A', 'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes' 
    ]
    st.write("Tabela de Dados:")
    st.write(df2[columns_to_display])

    # Créditos
    st.text("Desenvolvido por Lyssandro Silveira")
    st.markdown("Fale Comigo [link](https://t.me/Lyssandro)")

# Run the Streamlit app
if __name__ == '__main__':
    jogos_do_dia_page()
