import streamlit as st
import pandas as pd
import io
import requests

from session_state import SessionState

def last4_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    tab0, tab1 = st.tabs(["Análise", "Jogos do Dia"])

    with tab0:
        # Fazer o download do arquivo CSV da URL
        url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/last4_geral.csv"
        response = requests.get(url)
        data = response.content.decode("utf-8")

        # Carregar o CSV em um dataframe
        df = pd.read_csv(io.StringIO(data))

        # Renomear as colunas
        df.rename(columns={'W': 'Vitórias', 'D': 'Empates', 'L': 'Derrotas', 'GF': 'Gols_Feitos', 'GA': 'Gols_Tomados', 'GD': 'Saldo_Gols'}, inplace=True)

        # Filtrar as equipes com pelo menos 4 vitórias para o "Top Equipes"
        top_equipes = df[(df['Vitórias'] + df['Empates']) >= 6]

        # Filtrar as equipes com pelo menos 4 derrotas para o "Piores Equipes"
        piores_equipes = df[(df['Derrotas'] + df['Empates']) >= 7]
        
        # Filtrar as equipes com 4 vitórias para o "Top Equipes"
        #top_equipes = df[df['Vitórias'] == 4]

        # Filtrar as equipes com 0 vitórias para o "Piores Equipes"
        #piores_equipes = df[df['Vitórias'] == 0]

        # Criar um aplicativo Streamlit
        st.subheader("Análise das últimas 4  Partidas")

        # Adicionar uma barra de consulta para selecionar equipes
        equipes_selecionadas = st.multiselect("Selecione as equipes", df["Equipe"].unique())

        # Filtrar as equipes selecionadas
        equipes_filtradas = df[df["Equipe"].isin(equipes_selecionadas)]

        # Exibir o dataframe com as equipes selecionadas
        st.subheader("Equipes Selecionadas:")
        st.dataframe(equipes_filtradas[["Equipe", "Vitórias", "Empates", "Derrotas", "Gols_Feitos", "Gols_Tomados", "Saldo_Gols"]])

        # Exibir "Top Equipes" em uma tabela interativa
        st.subheader("Top Equipes:")
        st.text("Serão exibidas todas as equipes que ganharam as últimas 4 partidas jogando em casa ou fora na mesma Liga")
        st.dataframe(top_equipes[["Equipe", "Vitórias", "Empates", "Derrotas", "Gols_Feitos", "Gols_Tomados", "Saldo_Gols"]])

        # Exibir "Piores Equipes" em uma tabela interativa
        st.subheader("Piores Equipes:")
        st.text("Serão exibidas todas as equipes que perderam as últimas 4 partidas jogando em casa ou fora na mesma Liga")
        st.dataframe(piores_equipes[["Equipe", "Vitórias", "Empates", "Derrotas", "Gols_Feitos", "Gols_Tomados", "Saldo_Gols"]])

    with tab1:
        # Lê o arquivo CSV "last4_geral.csv" e seleciona as colunas "Equipe" e "W"
        url1 = "https://raw.githubusercontent.com/scooby75/bdfootball/main/last4_geral.csv"
        equipe_df = pd.read_csv(url1)

        # Lê o arquivo CSV "Jogos_do_Dia_FS.csv" e seleciona as colunas relevantes
        url2 = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"
        partidas_df = pd.read_csv(url2, usecols=["Date", "Hora", "Liga", "Home", "Away", "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "Rodada"])

        # Filtro para selecionar apenas as linhas em que a coluna "Rodada" seja >= 8
        partidas_df = partidas_df[partidas_df["Rodada"] >= 8]

        # Filtro para selecionar apenas as linhas em que a coluna "FT_Odd_H" seja <= 1.90
        partidas_df = partidas_df[partidas_df["FT_Odd_H"] <= 1.90]

        # Merge dos DataFrames com base na coluna "Home"
        merged_df = pd.merge(partidas_df, equipe_df, left_on="Home", right_on="Equipe", suffixes=("_partida", "_equipe"))

        # Encontra os nomes que coincidem entre as duas colunas
        nomes_coincidentes = merged_df[merged_df["W"].isin([0, 4])]

        # Filtra os resultados com W + D >= 6 (Melhores Equipes)
        melhores_equipes = nomes_coincidentes[(nomes_coincidentes["W"] + nomes_coincidentes["D"]) >= 6].head(800)

        # Filtra os resultados com L + D >= 7 (Piores Equipes)
        piores_equipes = nomes_coincidentes[(nomes_coincidentes["L"] + nomes_coincidentes["D"]) >= 7].head(800)

        # Função para destacar o time em verde
        def highlight_green(s):
            return f"<span style='color:green'>{s}</span>"

        # Apresenta os resultados em DataFrames do Streamlit com destaque em vermelho
        st.subheader("Jogos do Dia - Melhores Equipes")
        melhores_equipes_styled = melhores_equipes[["Date", "Hora", "Liga", "Home", "Away", "FT_Odd_H", "FT_Odd_D", "FT_Odd_A"]].copy()
        melhores_equipes_styled["Home"] = melhores_equipes_styled["Home"].apply(highlight_green)
        st.write(melhores_equipes_styled.to_html(escape=False), unsafe_allow_html=True)

        # Cria um arquivo CSV temporário
        temp_csv = st.cache_data(pd.DataFrame.to_csv)(melhores_equipes_styled, index=False)

        # Adiciona um botão para fazer o download do arquivo CSV
        st.download_button(
            label="Download CSV",
            data=temp_csv,
            file_name="melhores_equipes_last4.csv",
            mime="text/csv",
        )

        st.subheader("Jogos do Dia - Piores Equipes")
        piores_equipes_styled = piores_equipes[["Date", "Hora", "Liga", "Home", "Away", "FT_Odd_H", "FT_Odd_D", "FT_Odd_A"]].copy()
        piores_equipes_styled["Home"] = piores_equipes_styled["Home"].apply(highlight_green)
        st.write(piores_equipes_styled.to_html(escape=False), unsafe_allow_html=True)

# Chamar a função para iniciar o aplicativo
last4_page()
