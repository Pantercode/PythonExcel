import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import timedelta, datetime
import os
import streamlit as st

def show_page():
    st.markdown("## Página 5")
    st.write("Conteúdo da Página 5")


# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Definindo a comissão
COMISSAO = 0.08

Colunas_analises = ['filial','produto','vendedor','cliente','forma_pagamento']
Colunas_numericas =['preco','comissao']
Funcao_agg = {'soma':'sum',
              'contagem':'count',
              'media':'mean',
              'mediana':'median',
              'desvio_padrao':'std',
              'minimo':'min',
              'maximo':'max',}

# Função para obter o caminho dos datasets
def obter_caminho_datasets():
    try:
        return Path(__file__).parent.parent / 'datasets'
    except NameError:
        caminho_atual = Path.cwd()
        datasets_path = caminho_atual / 'datasets'
        if datasets_path.exists():
            return datasets_path
        else:
            st.warning("Não foi possível determinar automaticamente o caminho da pasta 'datasets'. Por favor, selecione manualmente.")
            selecionado = st.sidebar.text_input("Caminho da pasta 'datasets'", value="")
            if selecionado:
                caminho_personalizado = Path(selecionado)
                if caminho_personalizado.exists():
                    return caminho_personalizado
                else:
                    st.error("O caminho especificado não existe. Por favor, verifique e tente novamente.")
            st.stop()

# Buscando o caminho das pastas
pasta_datasets = obter_caminho_datasets()

# Verificando se a pasta datasets existe
if not pasta_datasets.exists():
    st.error(f"Pasta 'datasets' não encontrada em {pasta_datasets}")
    st.stop()

# Função para carregar dados com cache para melhorar a performance
@st.cache_data
def carregar_dados(pasta_datasets):
    try:
        df_vendas = pd.read_excel(
            pasta_datasets / 'vendas.xlsx',
            decimal=',',
            index_col=0,
            parse_dates=True
        )
    except FileNotFoundError:
        st.error("Arquivo 'vendas.xlsx' não encontrado na pasta 'datasets'.")
        st.stop()

    try:
        df_filiais = pd.read_csv(
            pasta_datasets / 'filiais.csv',
            sep=';',
            decimal=',',
            index_col=0
        )
    except FileNotFoundError:
        st.error("Arquivo 'filiais.csv' não encontrado na pasta 'datasets'.")
        st.stop()

    try:
        df_produtos = pd.read_csv(
            pasta_datasets / 'produtos.csv',
            sep=';',
            decimal=',',
            index_col=0
        )
    except FileNotFoundError:
        st.error("Arquivo 'produtos.csv' não encontrado na pasta 'datasets'.")
        st.stop()

    # Removendo vírgulas da coluna 'id'
    if 'id_venda' in df_vendas.columns:
        df_vendas['id_venda'] = df_vendas['id_venda'].astype(str).str.replace(',', '', regex=False)
        # Se necessário, converte para int
        # df_vendas['id_venda'] = df_vendas['id_venda'].astype(int)
    else:
        st.warning("A coluna 'id_venda' não foi encontrada em df_vendas.")

    # Renomeando coluna 'nome' para 'produto'
    df_produtos = df_produtos.rename(columns={'nome': 'produto'})

    # Resetando o índice para 'data'
    df_vendas = df_vendas.reset_index()

    # Merge entre vendas e produtos
    df_vendas = pd.merge(
        left=df_vendas,
        right=df_produtos,
        on='produto',
        how='left'
    )

    # Definindo 'data' como índice
    df_vendas = df_vendas.set_index('data')

    # Calculando a comissão
    df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

    return df_vendas, df_filiais, df_produtos

# Carregando os dados
df_vendas, df_filiais, df_produtos = carregar_dados(pasta_datasets)


indice_dinamico = st.sidebar.multiselect('Selecione os índices:',Colunas_analises)

colunas_filtradas = [c for c in Colunas_analises if c not in indice_dinamico]

coluna_dinamica = st.sidebar.multiselect('Selecione os colunas:',Colunas_numericas)


valor_analise = st.sidebar.selectbox("Selecione o valor de analise: ",Colunas_numericas)
                                     

metricas_analise = st.sidebar.selectbox("Selecione o valor a métrica: ",
                                     list(Funcao_agg.keys()))

if len(indice_dinamico) > 0 and len(coluna_dinamica) > 0:
    metricas = Funcao_agg[metricas_analise]
    vendas_dinamicas = pd.pivot_table(df_vendas,
                                        index=indice_dinamico,
                                        columns=coluna_dinamica, 
                                        values=valor_analise,
                                        aggfunc=metricas)
vendas_dinamicas['Total Geral'] = vendas_dinamicas.sum(axis=1)
vendas_dinamicas.loc['Total Geral'] = vendas_dinamicas.sum(axis=0).tolist()
st.dataframe(vendas_dinamicas)
#st.dataframe(df_produtos)