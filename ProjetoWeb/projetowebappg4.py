from pathlib import Path
import pandas as pd
import streamlit as st
from datetime import timedelta, datetime
# Buscando o caminho das pastas
comissao = 0.08

pasta_datasets = Path(__file__).parent.parent / 'datasets'

# Lendo os datasets
df_vendas = pd.read_excel(pasta_datasets / 'vendas.xlsx', decimal=',', index_col=0,parse_dates=True)

# Lendo os datasets de filia
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', sep=';', decimal=',',index_col=0)


# Lendo os datasets produtos
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', sep=';', decimal=',',index_col=0)


df_produtos = df_produtos.rename(columns={'nome':'produto'})
df_vendas = df_vendas.reset_index()
#Merge
df_vendas= pd.merge(left= df_vendas, 
                           right=df_produtos,
                            on= 'produto',
                            how='left')
df_vendas = df_vendas.set_index('data')

df_vendas['comissao'] = df_vendas['preco'] * comissao

st.dataframe(df_vendas)
st.dataframe(df_produtos)

data_default = df_vendas.index.date.max()
data_inicio = st.sidebar.date_input('Data Inicial', data_default - timedelta(days=7) )
data_final = st.sidebar.date_input('Data Final', data_default )
