import streamlit as st
import emoji
import json
import os
from datetime import datetime

#Arquivo JSON
dados_pacientes = 'pacientes.json'

#Função para manipular JSON
def carregar_dados():
    if os.path.exists(dados_pacientes):
        with open(dados_pacientes, 'r', encoding='utf-8') as f:
            return json.load(f)
    return{}
    
def salvar_dados(dados):
    with open(dados_pacientes,'w',encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def criar_paciente(cpf,nome,data_nascimento, sexo, endereco, telefone, email, historico_medico):
    return {
        'CPF': cpf,
        'Nome': nome,
        'Data de Nascimento' : data_nascimento,
        'Sexo' : sexo,
        'Endereço' : endereco,
        'Telefone': telefone,
        'E-Mail': email,
        'Histórico Médico': historico_medico or [],
        'Data de Cadastro': datetime.now().strftime('%d/%m/%y %H:%M:%S'),
        'Data de Atualização': datetime.now().strftime('%d/%m/%y %H:%M:%S')
    }

def initialize_session_state():
    defaults = {
        'cpf': '',
        'nome': '',
        'data_nascimento': datetime(2000, 1, 1),
        'sexo': 'Masculino',
        'endereco': '',
        'telefone': '',
        'email': '',
        'historico': ''
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def limpar_campos():
    st.session_state['cpf'] = ''
    st.session_state['nome'] = ''
    st.session_state['data_nascimento'] = datetime(2000, 1, 1)
    st.session_state['sexo'] = 'Masculino'
    st.session_state['endereco'] = ''
    st.session_state['telefone'] = ''
    st.session_state['email'] = ''
    st.session_state['historico'] = ''

def cadastrar_paciente():
    st.subheader('Cadastro de novo paciente:')

    with st.form(key='form_cadastro'):
        col1, col2 = st.columns(2)

        with col1:
            cpf = st.text_input('CPF (Somente Números)', max_chars=11, key='cpf')
            nome = st.text_input('Nome completo', key='nome')
            data_nascimento = st.date_input(
                'Data de Nascimento (DD/MM/AAAA)',
                min_value=datetime(1900, 1, 1),
                format="DD/MM/YYYY",
                key='data_nascimento'
            )
            sexo = st.selectbox('Sexo', ['Masculino', 'Feminino', 'Outro'], key='sexo')

        with col2:
            endereco = st.text_input('Endereço', key='endereco')
            telefone = st.text_input('Telefone', key='telefone')
            email = st.text_input('E-Mail', key='email')
            historico_medico = st.text_area('Histórico Médico (OPCIONAL)', key='historico')

        submit_button = st.form_submit_button('Cadastrar Paciente')

    if submit_button:
        if not cpf or not nome:
            st.error('CPF e Nome são obrigatórios')
            return

        dados = carregar_dados()

        if cpf in dados:
            st.error('Paciente já cadastrado')
            return

        paciente = criar_paciente(
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento.strftime('%d/%m/%y'),
            sexo=sexo,
            endereco=endereco,
            telefone=telefone,
            email=email,
            historico_medico=historico_medico.split('\n') if historico_medico else []
        )

        dados[cpf] = paciente
        salvar_dados(dados)

        st.success('Paciente salvo com sucesso')
        st.balloons()

      
# Clear form button with on_click callback — this is the right way to reset inputs
st.button("Limpar formulário", on_click=limpar_campos)

    
def listar_pacientes():
    st.subheader('Lista de Pacientes cadastrados')

    dados = carregar_dados()

    if not dados:
        st.info('Nenhum paciente cadastrado')
        return
    
    filtro_nome = st.text_input('Filtrar por nome: ')

    pacientes_filtrados = []

    # Filtra os pacientes pelo nome
    for cpf, paciente in dados.items():
        if filtro_nome.lower() in paciente['Nome'].lower():
            pacientes_filtrados.append((cpf, paciente))

    # Se não houver pacientes filtrados, exibe mensagem de aviso
    if not pacientes_filtrados:
        st.warning('Nenhum paciente encontrado')
        return
    
    # Exibe os pacientes filtrados
    for cpf, paciente in pacientes_filtrados:
        with st.expander(f'{paciente["Nome"]} - CPF {cpf}'):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f'*Data de Nascimento* {paciente["Data de Nascimento"]}')
                st.write(f'*Sexo* {paciente["Sexo"]}')
                st.write(f'*Endereço* {paciente["Endereço"]}')
            
            with col2:
                st.write(f'*Telefone* {paciente["Telefone"]}')
                st.write(f'*E-mail* {paciente["E-Mail"]}')
                st.write(f'*Cadastrado em* {paciente["Data de Cadastro"]}')

            if paciente["Histórico Médico"]:
                st.write(f'*Histórico Médico*')
                for item in paciente["Histórico Médico"]:
                    st.write(f'{item}')


def editar_paciente():
    st.subheader("Editar Paciente")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("Nenhum paciente cadastrado para editar.")
        return
    
    # Seleção do paciente para edição
    cpf_selecionado = st.selectbox(
        "Selecione o paciente pelo CPF",
        options=list(dados.keys()),
        format_func=lambda x: f"{dados[x]['Nome']} - {x}"
    )
    
    paciente = dados[cpf_selecionado]
    
    # Mostrar dados atuais de forma organizada
    st.write("### Dados atuais do paciente:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Nome:** {paciente['Nome']}")
        st.write(f"**CPF:** {cpf_selecionado}")
        st.write(f"**Data de Nascimento:** {paciente['Data de Nascimento']}")
        st.write(f"**Sexo:** {paciente['Sexo']}")
    
    with col2:
        st.write(f"**Endereço:** {paciente['Endereço']}")
        st.write(f"**Telefone:** {paciente['Telefone']}")
        st.write(f"**E-mail:** {paciente['E-Mail']}")
        st.write(f"**Cadastrado em:** {paciente['Data de Cadastro']}")
    
    if paciente["Histórico Médico"]:
        st.write("**Histórico Médico:**")
        for item in paciente["Histórico Médico"]:
            st.write(f"- {item}")

    # Formulário de edição (o restante da função permanece igual)
    with st.form(key="form_edicao"):
        col1, col2 = st.columns(2)
        
        with col1:
            novo_cpf = st.text_input("CPF (somente números)", value=cpf_selecionado, max_chars=11)  # Mudado para usar o CPF original
            nome = st.text_input("Nome Completo", value=paciente["Nome"])  # Corrigido para 'Nome'
            data_nascimento = st.text_input("Data de Nascimento", value=paciente["Data de Nascimento"])  # Corrigido para 'Data de Nascimento'
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(paciente["Sexo"]))  # Corrigido para 'Sexo'
        
        with col2:
            endereco = st.text_input("Endereço", value=paciente["Endereço"])  # Corrigido para 'Endereço'
            telefone = st.text_input("Telefone", value=paciente["Telefone"])  # Corrigido para 'Telefone'
            email = st.text_input("E-mail", value=paciente["E-Mail"])  # Corrigido para 'E-Mail'
            historico_medico = st.text_area("Histórico Médico", value="\n".join(paciente["Histórico Médico"]))  # Corrigido para 'Histórico Médico'
        
        submit_button = st.form_submit_button("Atualizar Paciente")
    
    # Validação e atualização
    if submit_button:
        if not novo_cpf or not nome:
            st.error("CPF e Nome são campos obrigatórios!")
            return
        
        # Verificar se o CPF foi alterado e garantir que o novo CPF não exista
        if novo_cpf != cpf_selecionado and novo_cpf in dados:
            st.error("Já existe um paciente com este novo CPF!")
            return
        
        # Se o CPF foi alterado, remover o paciente antigo
        if novo_cpf != cpf_selecionado:
            dados.pop(cpf_selecionado)
        
        # Atualizar os dados do paciente
        paciente_atualizado = {
            "CPF": novo_cpf,  # Corrigido para 'CPF' (para consistência)
            "Nome": nome,  # Corrigido para 'Nome'
            "Data de Nascimento": data_nascimento,  # Corrigido para 'Data de Nascimento'
            "Sexo": sexo,  # Corrigido para 'Sexo'
            "Endereço": endereco,  # Corrigido para 'Endereço'
            "Telefone": telefone,  # Corrigido para 'Telefone'
            "E-Mail": email,  # Corrigido para 'E-Mail'
            "Histórico Médico": historico_medico.split("\n") if historico_medico else [],  # Corrigido para 'Histórico Médico'
            "Data de Cadastro": paciente["Data de Cadastro"],  # Mantém a data de cadastro original
            "Data de Atualização": datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Atualiza a data de cadastro
        }
        
        # Salvar os dados atualizados
        dados[novo_cpf] = paciente_atualizado
        salvar_dados(dados)
        
        st.success("Paciente atualizado com sucesso!")


def excluir_paciente():
    st.subheader("Excluir Paciente")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("Nenhum paciente cadastrado para excluir.")
        return
    
    cpf_selecionado = st.selectbox(
        "Selecione o paciente pelo CPF para excluir",
        options=list(dados.keys()),
        format_func=lambda x: f"{dados[x]['Nome']} - {x}"
    )
    
    paciente = dados[cpf_selecionado]
    
    st.warning("Você está prestes a excluir o seguinte paciente:")
    
    # Mostrar dados de forma organizada em vez de JSON
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Nome:** {paciente['Nome']}")
        st.write(f"**CPF:** {cpf_selecionado}")
        st.write(f"**Data de Nascimento:** {paciente['Data de Nascimento']}")
    
    with col2:
        st.write(f"**Telefone:** {paciente['Telefone']}")
        st.write(f"**E-mail:** {paciente['E-Mail']}")
        st.write(f"**Cadastrado em:** {paciente['Data de Cadastro']}")
    
    if st.button("Confirmar Exclusão"):
        dados.pop(cpf_selecionado)
        salvar_dados(dados)
        st.success("Paciente excluído com sucesso!")

st.title(emoji.emojize('💊 Software de Cadastro pacientes'))

st.sidebar.title('Menu')
opcao = st.sidebar.radio(
    'Selecionar uma opçao:',
    ('Cadastro paciente', 'Lista paciente', 'Editar paciente','Excluir paciente')
)

# Na navegação entre páginas
if opcao == 'Cadastro paciente':
    cadastrar_paciente()
elif opcao == 'Lista paciente':
    listar_pacientes()
elif opcao == 'Editar paciente':  # Corrigido aqui
    editar_paciente()
elif opcao == 'Excluir paciente':
    excluir_paciente()

#Rodapé
st.sidebar.markdown('-')
st.sidebar.markdown('Desenvolvido por Thiago')
st.sidebar.markdown('Total de pacientes: ')