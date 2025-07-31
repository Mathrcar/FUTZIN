import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
from functions.futzin_funcs import atualizar_estrelas,sortear_times
import datetime


st.cache_resource.clear()
st.cache_data.clear()
conn = st.connection("gsheets", type=GSheetsConnection)
players = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='craques_mensalistas')
players_list = players.loc[players['status']=='ATIVO']['nome_do_craque'].to_list()
hist_times = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='historico_times')


att = st.button('ATUALIZAR ESTRELAS', type='primary')

if att:
    atualizar_estrelas()



form = st.form(key="QUEM VAI JOGAR?!",  clear_on_submit=True)


with form:
    play_today = st.pills('SELECIONE OS MENSALISTAS CONFIRMADOS DE HOJE:', options=players_list, selection_mode='multi')
    
    away = st.text_area('COLOQUE OS AVULSOS COMO NO SEGUINTE EXEMPLO, 1 AVULSO POR LINHA (Mister - 5)')
    
    left, right = st.columns(2)

    qtt_times = left.selectbox('QUANTOS TIMES?', options=['', 3, 4])
    qtt_players = right.selectbox('QUANTOS POR TIME?', options=['',7,6])

    submit = form.form_submit_button("SORTEAR TIMES!")

    if submit:

        if len(play_today)==0:
            st.error('SELECIONE OS MENSALISTAS SEU ANIMAL!')
        elif qtt_times=='':
            st.error('SELECIONE QUANTOS TIMES SEU ANIMAL!')
        elif qtt_players=='':
            st.error('SELECIONE QUANTOS JOGADORES POR TIME SEU ANIMAL!')
        else:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='estrelas_otimizado')
            df = df.loc[df['craque'].isin(play_today)][['craque', 'nota_final']]
    
            df_aux = ''
            players = ''
            if away!='':

                linhas = away.split('\n')
                dados = [linha.split('-') for linha in linhas]
                df_aux = pd.DataFrame(dados, columns=['craque', 'nota_final'])
                df_aux['nota_final'] = df_aux['nota_final'].astype(int)
                players = pd.concat([df_aux, df], ignore_index=False)

            else:
                players = df

            times = sortear_times(players, num_times=qtt_times, max_por_time=qtt_players)
            times['dia_do_jogo'] = datetime.datetime.now().strftime('%Y-%m-%d')
            
            hist_times_new = pd.concat([hist_times, times], ignore_index=False)

            conn.update(worksheet='historico_times', data = hist_times_new)

            times_list = set(times['time'].to_list())

            for t in times_list:
                taux = times.loc[times['time']==t]
                st.title(t)
                col = st.columns(taux.shape[0])
                for i in range(0, taux.shape[0]):
                    try:
                        col[i].image(f'main_code/fotos_craques/{taux["craque"].iloc[i]}.png', width=100)
                    except:
                        col[i].image('main_code/fotos_craques/Mister.png', width=100)
                    col[i].write(f'{taux["craque"].iloc[i]} - {int(taux["nota_final"].iloc[i])}')