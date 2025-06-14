import streamlit as st
import pandas as pd
import emoji

st.title(emoji.emojize('🧑‍💻 Software de Gestão 🧑‍💻'))
# nome = st.text_input('Qual seu nome: ')

# if nome != '':
#     st.write(f'Olá, como vai {nome}')

if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame({
        'Nome':[],
        'Idade':[]
    
})

nome = st.text_input('Qual seu nome: ')
idade = st.number_input('Qual sua idade: ', min_value=0, step=1)

if st.button('Adicionar'):
    if nome:
        novo = pd.DataFrame({'Nome':[nome], 'Idade':[idade]})
        st.session_state.dados = pd.concat(
            [st.session_state.dados, novo],
            ignore_index=True
        )
        st.success('Adicionando')
        st.balloons()
    else:
        st.warning('Digite um nome')

st.dataframe(st.session_state.dados)