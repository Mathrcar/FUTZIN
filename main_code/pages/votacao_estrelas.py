import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection

# st.cache_resource.clear()
# st.cache_data.clear()
conn = st.connection("gsheets", type=GSheetsConnection)
star_point = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='estrelas')
players = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='craques_mensalistas')

players_list = players.loc[players['status']=='ATIVO']['nome_do_craque'].to_list()
# dats = dats.dropna(how="all")


st.set_page_config(page_title="Balanceador de Times", layout="wide")
st.title("VOTAÇÃO DE ESTRELAS")


form = st.form(key="Diga quem está votando",  clear_on_submit=True)

rows = int(round(len(players_list)/3, 0)) + 1

i = 0


with form:
    input_name = st.selectbox("Quem é você?", options=[' ']+players_list)
    
    st.write('ATENÇÃO: ESSE FORMS NÃO SALVA SUAS RESPOSTAS, ENTÃO VALIDE SE NÃO DEIXOU PASSAR NADA! SE VOCÊ DEIXOU DE PREENCHER UM CAMPO E SUBMETER, IRÁ TER QUE RESPONDER TUDO NOVAMENTE SEU BURRO!')

    # while i < len(players_list):
    while i < 3:

        left, mid, right = st.columns(3)

        for k in [left, mid, right]:
            try:
                k = k.container(border=True)
                k.title(players_list[i])
                k.image('futzin/fotos_craques/Mister.png', width=100)
                ncl = k.checkbox('NÃO CONHEÇO', key=f'nc{players_list[i]}')
                k.write('Habilidade: Controle de bola, Passe, Chute, Drible, Domínio.')
                hab = k.feedback('stars', key = f'hab{players_list[i]}')
                k.write('Eficácia Ofensiva: Gols, Assistências, Tomada de decisão, Criação de espaço nas jogadas.')
                atq = k.feedback('stars', key = f'atq{players_list[i]}')
                k.write('Eficácia Defensiva: Marcação, Desarmes, Trabalho em equipe.')
                dfs = k.feedback('stars', key = f'dfs{players_list[i]}')
                k.write('Desempenho Físico: Velocidade, Resistência, Força, Agilidade.')
                cod = k.feedback('stars', key = f'cod{players_list[i]}')
                i = i+1
            except:
                i = i+1
                pass

    i = 0
    value_list = [input_name]
    columns = ['quem_votou']
    # while i < len(players_list):
    while i < 3:
        if st.session_state[f'nc{players_list[i]}'] == True:
            value_list.append('nao conhece')
            value_list.append('nao conhece')
            value_list.append('nao conhece')
            value_list.append('nao conhece')               
        else:
            value_list.append(st.session_state[f'hab{players_list[i]}'])
            value_list.append(st.session_state[f'atq{players_list[i]}'])
            value_list.append(st.session_state[f'dfs{players_list[i]}'])
            value_list.append(st.session_state[f'cod{players_list[i]}'])

        columns.append(f'hab{players_list[i]}')
        columns.append(f'atq{players_list[i]}')
        columns.append(f'dfs{players_list[i]}')
        columns.append(f'cod{players_list[i]}')

        i = i+1 


    submit = form.form_submit_button("LANÇA MEU VOTO AÍ!")

    if submit:
        if not input_name in players_list:
            st.error('COLOCA TEU NOME ANIMAL!')

        elif None in value_list:
            st.error('VOCÊ ESQUECEU DE DAR ALGUMA ESTRELA PARA ALGUÉM')
        else:
            df = pd.DataFrame([dict(zip(columns, value_list))])
            conn.update(worksheet='estrelas', data = df)
            st.success('FEZ UMA PRA DEUS!')