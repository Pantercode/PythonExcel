from pathlib import Path
import pandas as pd
import streamlit as st
from datetime import datetime
# Buscando o caminho das pastas
pasta_datasets = Path(__file__).parent.parent / 'datasets'

# Lendo os datasets
df_vendas = pd.read_excel(pasta_datasets / 'vendas.xlsx', decimal=',', index_col=0)

# Lendo os datasets de filia
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', sep=';', decimal=',')


# Lendo os datasets produtos
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', sep=';', decimal=',')

# Adicionando coluna com a cidade e estado
df_filiais['Cidade/Estado'] = df_filiais['cidade']+ '/' + df_filiais['estado']

#criand lista do concatendo
lista_filiais = df_filiais['Cidade/Estado'] .to_list()
# barra de seleçao filial
filial_selecionada = st.sidebar.selectbox('Selecione a Filial:', 
                                          lista_filiais)
# barra de seleçao vendedor
lista_vendedores = df_filiais.loc[df_filiais['Cidade/Estado'] == filial_selecionada, 'vendedores'].iloc[0]

lista_vendedores = lista_vendedores.strip('][').replace("'", '').split(', ') 

vendedor_selecionada = st.sidebar.selectbox('Selecione o Vendedor:', 
                                          lista_vendedores)

#criand lista do produtos
lista_produtos= df_produtos['nome'] .to_list()

produtos_selecionada = st.sidebar.selectbox('Selecione o Produto:', 
                                          lista_produtos)


nome_cliente = st.sidebar.text_input('Nome Cliente:')


genero_selecionada = st.sidebar.selectbox('Selecione o Genero:' , 
                                          ['Masculino', 'Feminino'])


forma_de_pagamento_selecionada = st.sidebar.selectbox('Selecione a forma de Pagamento:' , 
                                          ['boleto', 'pix','credito','Debito'])

if st.sidebar.button('Adicionar nova Venda'):
    lista_adicionar = [df_vendas['id_venda'].max() + 1,
                   filial_selecionada,
                   vendedor_selecionada,
                   produtos_selecionada,
                   nome_cliente,
                   genero_selecionada,
                   forma_de_pagamento_selecionada]
    df_vendas.loc[datetime.datetime.now()] = lista_adicionar
    df_vendas.to_csv(pasta_datasets / 'vendas.csv', sep=';')
    st.success('Venda adicionada com sucesso!')


st.dataframe(df_vendas,height=600, width=1200)


