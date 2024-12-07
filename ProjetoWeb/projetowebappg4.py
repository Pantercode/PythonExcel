import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import timedelta, datetime
import os

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Definindo a comissão
COMISSAO = 0.08

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

# Seleção de datas no sidebar
data_max = df_vendas.index.date.max()
data_min = df_vendas.index.date.min()

st.sidebar.header("Filtros")

data_inicio = st.sidebar.date_input(
    'Data Inicial',
    data_max - timedelta(days=7),
    min_value=data_min,
    max_value=data_max
)

data_final = st.sidebar.date_input(
    'Data Final',
    data_max,
    min_value=data_min,
    max_value=data_max
)

# Validação das datas
if data_inicio > data_final:
    st.sidebar.error("A data inicial não pode ser posterior à data final.")
    st.stop()

# Filtrando os dados de vendas no período selecionado
df_vendas_periodo = df_vendas[
    (df_vendas.index.date >= data_inicio) & 
    (df_vendas.index.date <= data_final)
]

# Título da página
st.title("📊 Dashboard de Vendas")

# Seção de Números Gerais
st.header("Números Gerais")

col1, col2 = st.columns(2)

valor_vendas = df_vendas_periodo['preco'].sum()
valor_vendas_str = f"R$ {valor_vendas:,.2f}"
col1.metric('Valor de Vendas no Período', valor_vendas_str)

qtd_vendas = df_vendas_periodo['preco'].count()
col2.metric('Quantidade de Vendas no Período', qtd_vendas)

st.markdown("---")

# Identificando a principal filial
if not df_vendas_periodo.empty:
    principal_filial = df_vendas_periodo['filial'].value_counts().idxmax()
    st.header(f"🏆 Principal Filial: {principal_filial}")

    # Filtrando vendas da principal filial
    df_filial = df_vendas_periodo[df_vendas_periodo['filial'] == principal_filial]

    col3, col4 = st.columns(2)

    valor_vendas_filial = df_filial['preco'].sum()
    valor_vendas_filial_str = f"R$ {valor_vendas_filial:,.2f}"
    col3.metric('Valor de Vendas da Filial', valor_vendas_filial_str)

    qtd_vendas_filial = df_filial['preco'].count()
    col4.metric('Quantidade de Vendas da Filial', qtd_vendas_filial)
else:
    st.info("Nenhuma venda encontrada no período selecionado.")

st.markdown("---")

# Exibindo os dataframes (opcional)
with st.expander("🔍 Mostrar Dados Filtrados"):
    st.dataframe(df_vendas_periodo)

with st.expander("📂 Mostrar Todas as Vendas"):
    st.dataframe(df_vendas)

with st.expander("🛍️ Mostrar Produtos"):
    st.dataframe(df_produtos)

# Opcional: Exibir gráficos
st.header("📈 Gráficos")

# Gráfico de Vendas ao Longo do Tempo
st.subheader("Vendas ao Longo do Tempo")
vendas_diarias = df_vendas_periodo['preco'].resample('D').sum()
st.line_chart(vendas_diarias)

# Gráfico de Vendas por Filial
st.subheader("Vendas por Filial")
vendas_filial = df_vendas_periodo.groupby('filial')['preco'].sum().sort_values(ascending=False)
st.bar_chart(vendas_filial)
