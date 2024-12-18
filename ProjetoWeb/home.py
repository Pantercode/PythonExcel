import streamlit as st

# Adicionando imagem na barra lateral
st.sidebar.image(r'C:\Users\marcell.oliveira\Desktop\pythoexcel\PythonExcel\ProjetoWeb\1652501565743.jpg', caption='Marcell Felipe')

# Adicionando link na barra lateral
st.sidebar.markdown('Desenvolvido por [Marcell Felipe](https://www.linkedin.com/in/marcell-felipe-de-paula-oliveira-219525199/)')

# Título principal
st.markdown('# Bem-vindo ao Analisador de Vendas')

# Divisor
st.divider()

# Descrição do projeto
st.markdown(
    '''
    Esse projeto tem por finalidade demonstrar toda a capacidade do Python usando Streamlit.

    Utilizaremos três principais bibliotecas para o seu desenvolvimento:

    - `pandas`: para manipulação de dados em tabelas
    - `plotly`: para geração de gráficos
    - `streamlit`: para criação desse webApp interativo que você se encontra nesse momento

    Os dados utilizados foram gerados pelo script 'gerador_de_vendas.py' que se encontra junto do código fonte do projeto. Os dados podem ser visualizados na aba de tabelas!
    '''
)
