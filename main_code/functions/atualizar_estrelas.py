import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection

def atualizar_estrelas():
    conn = st.connection("gsheets", type=GSheetsConnection)
    star_point = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='estrelas')
    columns_voted = star_point.columns[1:]

    columns_opt = ['craque', 'hab', 'atq', 'dfs', 'cod']
    opt_data = []
    for i in ['Alex', 'Biagio GK', 'Baitolas']:
        columns_aux = [s for s in columns_voted if i.lower() in s.lower()]
        df_aux = star_point[columns_aux]
        hab = df_aux[df_aux[f'hab{i}']!='nao conhece'][f'hab{i}'].mean()
        atq = df_aux[df_aux[f'atq{i}']!='nao conhece'][f'atq{i}'].mean()
        dfs = df_aux[df_aux[f'dfs{i}']!='nao conhece'][f'dfs{i}'].mean()
        cod = df_aux[df_aux[f'cod{i}']!='nao conhece'][f'cod{i}'].mean()

        opt_data.append([i,hab, atq, dfs, cod])

    opt_df = pd.DataFrame(data=opt_data, columns=columns_opt)
    conn.update(worksheet='estrelas_otimizado', data = opt_df)