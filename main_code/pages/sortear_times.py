import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
from functions.atualizar_estrelas import atualizar_estrelas



conn = st.connection("gsheets", type=GSheetsConnection)
players = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='craques_mensalistas')
players_list = players.loc[players['status']=='ATIVO']['nome_do_craque'].to_list()

st.button('ATUALIZAR ESTRELAS', type='primary')

if st.button:
    atualizar_estrelas()



form = st.form(key="QUEM VAI JOGAR?!",  clear_on_submit=True)


with form:
    play_today = st.pills('SELECIONE OS MENSALISTAS CONFIRMADOS DE HOJE:', options=players_list, selection_mode='multi')
    
    away = st.text_area('COLOQUE OS AVULSOS COMO NO SEGUINTE EXEMPLO, 1 AVULSO POR LINHA (Mister - 5*)')

    
    submit = form.form_submit_button("SORTEAR TIMES!")

    if submit:
        st.write(play_today)
        st.write(away)

        linhas = away.split('\n')

        dados = [linha.split('-') for linha in linhas]

        # Criar o DataFrame
        # df = pd.DataFrame(dados, columns=['nome_do_avulso', 'estrelas'])

        # st.dataframe(df)