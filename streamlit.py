import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Título Principal")  # Título grande
st.header("Cabeçalho da Seção")  # Cabeçalho médio
st.subheader("Subseção")  # Subcabeçalho
st.write("Texto normal")  # Texto comum
st.markdown("**Markdown** suportado!")  # Permite formatação Markdown
st.code("print('Hello, Streamlit!')")  # Exibe código formatado


# Botão
if st.button("Clique aqui"):
    st.write("Botão pressionado!")

# Caixa de seleção
check = st.checkbox("Concordo com os termos")
if check:
    st.write("Aceito!")

# Radio button
opcao = st.radio("Escolha uma opção:", ["Python", "JavaScript", "Rust"])

# Selectbox
linguagem = st.selectbox("Linguagem favorita:", ["Python", "Java", "C++"])

# Slider
idade = st.slider("Idade:", 0, 100, 25)  # (min, max, default)

# Text input
nome = st.text_input("Digite seu nome:")

# Text area
bio = st.text_area("Escreva sua biografia:")

# Upload de arquivo
arquivo = st.file_uploader("Envie um arquivo:")

# DataFrame
df = pd.DataFrame({"Nome": ["Ana", "João", "Maria"], "Idade": [25, 30, 22]})
st.dataframe(df)  # Tabela interativa

# Tabela estática
st.table(df)

# Gráficos
st.line_chart(df.set_index("Nome"))  # Gráfico de linha
st.bar_chart(df.set_index("Nome"))   # Gráfico de barras

# Exibir JSON
st.json({"nome": "Streamlit", "versao": "1.0"})

# Sidebar (barra lateral)
st.sidebar.title("Menu")
st.sidebar.button("Opção 1")

# Colunas
col1, col2 = st.columns(2)
with col1:
    st.write("Coluna 1")
with col2:
    st.write("Coluna 2")

# Expanders (seções expansíveis)
with st.expander("Detalhes"):
    st.write("Conteúdo oculto que pode ser expandido.")

# Tabs (abas)
tab1, tab2 = st.tabs(["Aba 1", "Aba 2"])
with tab1:
    st.write("Conteúdo da Aba 1")
with tab2:
    st.write("Conteúdo da Aba 2")

# Spinner (carregamento)
with st.spinner("Processando..."):
    time.sleep(2)
    st.success("Concluído!")

# Barra de progresso
progresso = st.progress(0)
for i in range(100):
    time.sleep(0.05)
    progresso.progress(i + 1)

# Mensagens de status
st.error("Erro!")
st.warning("Aviso!")
st.info("Informação")
st.success("Sucesso!")