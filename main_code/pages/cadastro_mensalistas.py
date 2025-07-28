import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.cache_resource.clear()
st.cache_data.clear()
conn = st.connection("gsheets", type=GSheetsConnection)
dats = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='craques_mensalistas')
# dats = dats.dropna(how="all")


st.set_page_config(page_title="Balanceador de Times", layout="centered")
st.title("CADASTRO MENSALISTAS")

form = st.form(key="Mensalistas",  clear_on_submit=True)

with form:
    input_name = st.text_input("Nome do craque:", placeholder="Insira o nome do craque")
    input_status = st.selectbox("Status", options=["ATIVO", "INATIVO"])

    submit = form.form_submit_button("CADASTRO FEITO!")

    if submit:
        subs = dats
        if not input_name:
            st.error('AE BURRÃO COLOCA O NOME DO CARA!')
        else:
            if input_name in dats['nome_do_craque'].tolist():

                if input_status in dats.loc[dats['nome_do_craque']==input_name]['status'].to_list():
                    st.error('CRAQUE JÁ ESTÁ CADASTRADO')
                else:
                    subs.loc[subs['nome_do_craque']==input_name, 'status'] = input_status
                    conn.update(worksheet='craques_mensalistas', data = subs)
                    st.success('STATUS DO CRAQUE ALTERADO')

            else:
                st.success('CRAQUE CADASTRADO')
                new_data= {'nome_do_craque': [input_name], 'status': [input_status]}
                df = pd.DataFrame.from_dict(new_data)

                subs = pd.concat([dats, df], ignore_index=False)
                conn.update(worksheet='craques_mensalistas', data = subs)
                st.text("E LISTA ATUALIZADA")

                # dats = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0")
            st.dataframe(subs[subs['status']=='ATIVO'])


