import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
from ortools.sat.python import cp_model



def atualizar_estrelas():
    conn = st.connection("gsheets", type=GSheetsConnection)
    star_point = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/131DjAiFO7f-hPTJX9rN8SksNL53z_UGOjh9ScmL-eKM/edit?gid=0#gid=0", worksheet='estrelas')
    columns_voted = star_point.columns[1:]

    columns_opt = ['craque', 'hab', 'atq', 'dfs', 'cod']
    opt_data = []
    for i in ['Alex', 'Biagio GK', 'Baitolas']:
        columns_aux = [s for s in columns_voted if i.lower() in s.lower()]
        df_aux = star_point[columns_aux]
        hab = round(df_aux[df_aux[f'hab{i}']!='nao conhece'][f'hab{i}'].mean(), 2)
        atq = round(df_aux[df_aux[f'atq{i}']!='nao conhece'][f'atq{i}'].mean(), 2)
        dfs = round(df_aux[df_aux[f'dfs{i}']!='nao conhece'][f'dfs{i}'].mean(), 2)
        cod = round(df_aux[df_aux[f'cod{i}']!='nao conhece'][f'cod{i}'].mean(), 2)

        opt_data.append([i,hab, atq, dfs, cod])

    opt_df = pd.DataFrame(data=opt_data, columns=columns_opt)
    opt_df['min_star'] = opt_df.iloc[:, -4:].min(axis=1)
    
    opt_df['nota_final'] = (round((opt_df['min_star'] + opt_df['hab'] + opt_df['atq'] + opt_df['dfs'] + opt_df['cod'])/5, 2)).astype(int)

    conn.update(worksheet='estrelas_otimizado', data = opt_df)


def sortear_times(df, num_times=3, max_por_time=7):
    model = cp_model.CpModel()
    n = len(df)
    nomes = df['craque'].tolist()
    pontuacoes = df['nota_final'].tolist()

    # Criar variáveis binárias: x[i][t] = 1 se jogador i está no time t
    x = [
        [model.NewBoolVar(f'x_{i}_{t}') for t in range(num_times)]
        for i in range(n)
    ]

    # Cada jogador deve estar em exatamente um time
    for i in range(n):
        model.Add(sum(x[i][t] for t in range(num_times)) == 1)

    # Se max_por_time não foi definido, assume divisão uniforme
    if max_por_time is None:
        max_por_time = (n + num_times - 1) // num_times

    # Restrição: cada time com no máximo `max_por_time` jogadores
    for t in range(num_times):
        model.Add(sum(x[i][t] for i in range(n)) <= max_por_time)

    # Soma das pontuações por time
    soma_por_time = [
        model.NewIntVar(0, int(sum(pontuacoes) * 100), f'soma_time_{t}')
        for t in range(num_times)
    ]

    for t in range(num_times):
        model.Add(soma_por_time[t] == sum(
            int(pontuacoes[i] * 100) * x[i][t] for i in range(n)
        ))

    # Variável de diferença máxima entre os times
    max_diff = model.NewIntVar(0, int(sum(pontuacoes) * 100), 'max_diff')

    for t1 in range(num_times):
        for t2 in range(t1 + 1, num_times):
            diff = model.NewIntVar(0, int(sum(pontuacoes) * 100), f'diff_{t1}_{t2}')
            model.Add(diff >= soma_por_time[t1] - soma_por_time[t2])
            model.Add(diff >= soma_por_time[t2] - soma_por_time[t1])
            model.Add(diff <= max_diff)

    # Minimizar a maior diferença entre as somas dos times
    model.Minimize(max_diff)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        dados = []
        for i in range(n):
            for t in range(num_times):
                if solver.Value(x[i][t]) == 1:
                    dados.append({
                        'craque': nomes[i],
                        'nota_final': pontuacoes[i],
                        'time': f'Time {t + 1}'
                    })
        df_resultado = pd.DataFrame(dados)
        return df_resultado
    else:
        print("❌ Não foi possível encontrar uma solução viável.")
        return None