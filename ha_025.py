# ha_025.py

import streamlit as st
import pandas as pd

from session_state import SessionState

def ha_025_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
        
    ##### HA -0.25 ######

    # Load the data
    #@st.cache_data(ttl=86400.0)  # 24 hours in seconds
    def load_base():
        import pandas as pd

        # Carregue os dados diretamente da URL
        url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
        ha_df = pd.read_csv(url)

        # Defina os critérios para HA -0.25 e HA +0.25
        crit_ha_025 = (ha_df['FT_Odd_H'] >= 1.61) & (ha_df['FT_Odd_H'] <= 2.20)
        crit_ha_plus_025 = (ha_df['FT_Odd_H'] >= 2.61) & (ha_df['FT_Odd_H'] <= 3.20)

        # Defina os critérios para seleção de equipes e ligas
        equipes_desejadas = [
            "Ind. Rivadavia",
            "Machida",
            "Nagoya Grampus",
            "Botafogo RJ",
            "Stjarnan",
            "Lanus",
            "Vitoria",
            "Start",
            "2 de Mayo",
            "Fernando de la Mora",
            "Utsikten",
            "Vega Real",
            "FC Gomel",
            "Deportivo Maipu",
            "Viking",
            "Jeonbuk",
            "Agropecuario",
            "San Marcos de Arica",
            "Samgurali",
            "Gremio",
            "Cobreloa",
            "Manta",
            "Rosario Central",
            "Recoleta",
            "Hacken",
            "Termez Surkhon",
            "Macara",
            "Cobh Ramblers",
            "Ulsan Hyundai",
            "Fredrikstad",
            "Nacional Potosi",
            "Bucheon FC 1995",
            "FK Panevezys",
            "Pohang"
        ]


        ligas_desejadas = [
            "ARGENTINA - PRIMERA NACIONAL",
            "JAPAN - J2 LEAGUE",
            "BRAZIL - SERIE A",
            "ICELAND - BESTA DEILD KARLA",
            "ARGENTINA - LIGA PROFESIONAL",
            "BRAZIL - SERIE B",
            "NORWAY - OBOS-LIGAEN",
            "PARAGUAY - DIVISION INTERMEDIA",
            "PARAGUAY - DIVISION INTERMEDIA",
            "SWEDEN - SUPERETTAN",
            "DOMINICAN REPUBLIC - LDF",
            "BELARUS - VYSSHAYA LIGA",
            "ARGENTINA - PRIMERA NACIONAL",
            "NORWAY - ELITESERIEN",
            "SOUTH KOREA - K LEAGUE 1",
            "ARGENTINA - PRIMERA NACIONAL",
            "CHILE - PRIMERA B",
            "GEORGIA - CRYSTALBET EROVNULI LIGA",
            "BRAZIL - SERIE A",
            "CHILE - PRIMERA B",
            "ECUADOR - SERIE B",
            "ARGENTINA - LIGA PROFESIONAL",
            "PARAGUAY - DIVISION INTERMEDIA",
            "SWEDEN - ALLSVENSKAN",
            "UZBEKISTAN - SUPER LEAGUE",
            "ECUADOR - SERIE B",
            "IRELAND - DIVISION 1",
            "SOUTH KOREA - K LEAGUE 1",
            "NORWAY - OBOS-LIGAEN",
            "BOLIVIA - DIVISION PROFESIONAL",
            "SOUTH KOREA - K LEAGUE 2",
            "LITHUANIA - A LYGA",
            "SOUTH KOREA - K LEAGUE 1"
        ]

        # Aplique as regras corretas de acordo com os critérios
        ha_df['Aposta'] = ''

        # Para HA -0.25
        ha_df.loc[crit_ha_025, 'Aposta'] = 'HA -0.25 casa, Odd minima 1.35'

        # Para HA +0.25
        ha_df.loc[crit_ha_plus_025, 'Aposta'] = 'HA +0.25 casa, Odd minima 1.70'

        # Aplique os critérios de seleção para equipes e ligas
        ha_df_filtered = ha_df[(ha_df['Home'].isin(equipes_desejadas)) & (ha_df['League'].isin(ligas_desejadas))]

        # Selecione apenas as colunas desejadas
        colunas_desejadas = ["Date", "Time", "League", "Home", "Away", "Aposta"]
        ha_df_filtered = ha_df_filtered[colunas_desejadas]

        # Exiba o DataFrame resultante
        st.subheader("Apostas em HA -0.25 e HA +0.25")
        st.dataframe(ha_df_filtered)

    # Chamar a função para iniciar o aplicativo
    ha_025_page()

    

