from pathlib import Path
import streamlit as st
import pandas as pd


Pasta_datasets = Path(__file__).parent.parent /'datasets'

caminho = Pasta_datasets / 'vendas.xlsx'

df_vendas = pd.read_excel(caminho, decimal=',')

st.dataframe(df_vendas)





















