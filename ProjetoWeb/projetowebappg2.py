from pathlib import Path
import pandas as pd
import streamlit as st

# Buscando o caminho das pastas
pasta_datasets = Path(__file__).parent.parent / 'datasets'

# Lendo os datasets
df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', sep=';', decimal=',', index_col=0)

# Criando uma lista com as colunas do DataFrame
colunas = list(df_vendas.columns)

# Criando um selector para as colunas na sidebar
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:', colunas, colunas)

# Dividindo a barra lateral em duas colunas
col1, col2 = st.sidebar.columns(2)

# Criando um selectbox para escolher uma coluna (excluindo 'id_vendedor')
col_filtro = col1.selectbox('Selecione a coluna para filtro', [c for c in colunas if c != 'id_venda'])

# Criando um selectbox no segundo painel para selecionar um valor baseado na coluna escolhida
valor_filtro = col_filtro_valor = col2.selectbox('Selecione outro valor', list(df_vendas[col_filtro].unique()))

statusFiltrar = col1.button('Filtra')
statuslimpar = col2.button('Limpar Filtro')


if statusFiltrar:
    # Exibindo os dados filtrados no dataframe
    st.dataframe(df_vendas.loc[df_vendas[col_filtro] == valor_filtro, colunas_selecionadas])
elif  statuslimpar: 
    # Limpando o filtro
     st.dataframe(df_vendas[colunas_selecionadas] ,height=800)

else:
    # Limpando o filtro
     st.dataframe(df_vendas[colunas_selecionadas] ,width=800)


