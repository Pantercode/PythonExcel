from pathlib import Path
import streamlit as st
import pandas as pd
import streamlit as st

def show_page():
    st.markdown("## Página 1")
    st.write("Conteúdo da Página 1")


Pasta_datasets = Path(__file__).parent.parent /'datasets'

caminho = Pasta_datasets / 'vendas.xlsx'

df_vendas = pd.read_excel(caminho, decimal=',')

st.dataframe(df_vendas)





















