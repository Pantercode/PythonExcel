import streamlit as st
from projetowebappg1 import show_page as page1
from projetowebappg2 import show_page as page2
from projetowebappg3 import show_page as page3
from projetowebappg4 import show_page as page4
from projetowebappg5 import show_page as page5
from projetowebappg6 import show_page as page6

# Adicionando imagem na barra lateral
st.sidebar.image(r'C:\Users\marcell.oliveira\Desktop\pythoexcel\PythonExcel\ProjetoWeb\1652501565743.jpg', caption='Marcell Felipe')

# Adicionando link na barra lateral
st.sidebar.markdown('Desenvolvido por [Marcell Felipe](https://www.linkedin.com/in/marcell-felipe-de-paula-oliveira-219525199/)')

# Menu de navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha a página:", 
                        ["Home", "Página 1", "Página 2", "Página 3", "Página 4", "Página 5", "Página 6"])

# Página principal
if page == "Home":
    st.markdown("# Página Inicial")
    st.write("Bem-vindo ao aplicativo principal. Use o menu lateral para navegar.")

# Chamando as funções das páginas
elif page == "Página 1":
    page1()

elif page == "Página 2":
    page2()

elif page == "Página 3":
    page3()

elif page == "Página 4":
    page4()

elif page == "Página 5":
    page5()

elif page == "Página 6":
    page6()
