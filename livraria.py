import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import emoji
import json
import os

ARQUIVO_JSON = "livros_cadastrados.json"

def salvar_em_json():
    """Salva a lista de livros no arquivo JSON"""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(livros, f, ensure_ascii=False, indent=4)

def carregar_do_json():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Remove possíveis duplicatas (se houver corrupção no arquivo)
            seen = set()
            return [livro for livro in dados if not (livro['livro_ISBN'] in seen or seen.add(livro['livro_ISBN']))]
    return []

livros = carregar_do_json()

def limpar_tela():
    book_title_entry.delete(0, tk.END)
    book_autor_entry.delete(0, tk.END)
    book_pages_entry.delete(0, tk.END)
    book_year_entry.delete(0, tk.END)
    book_gen_entry.delete(0, tk.END)
    book_edit_entry.delete(0, tk.END)
    book_isbn_entry.delete(0, tk.END)

def confirmar_limpeza():
    """Pede confirmação antes de limpar os campos"""
    resposta = messagebox.askyesno(
        "Confirmar Limpeza",
        "Tem certeza que deseja limpar todos os campos?",
        icon='warning'
    )
    if resposta:
        limpar_tela()

def salvar_livro():
       
    novo_isbn = book_isbn_entry.get().strip()
    
    if not novo_isbn:
        messagebox.showerror('Erro', 'O ISBN é obrigatório!')
        return
    
    if isbn_existe(novo_isbn):
        messagebox.showerror('Erro', 'Este ISBN já está cadastrado para outro livro!')
        book_isbn_entry.focus()
        return
          
    livro = {
        'titulo_livro': book_title_entry.get(),
        'autor_livro': book_autor_entry.get(),
        'paginas_livro': book_pages_entry.get(),
        'livro_publi': book_year_entry.get(),
        'livro_genero': book_gen_entry.get(),
        'editora_livro': book_edit_entry.get(),
        'livro_ISBN': novo_isbn  # Usando o ISBN já validado
    }
    
    livros.append(livro)
    salvar_em_json()
    messagebox.showinfo('Sucesso', 'Livro cadastrado!')
    limpar_tela()
    atualizar_tabela()

def isbn_existe(isbn):
    """Verifica se o ISBN já está cadastrado"""
    return any(livro['livro_ISBN'] == isbn for livro in livros)

def validar_isbn(event):
    isbn = book_isbn_entry.get()
    if isbn_existe(isbn):
        book_isbn_entry.config(foreground='red')
    else:
        book_isbn_entry.config(foreground='black')


def atualizar_tabela():
    # Limpa a tabela atual
    for item in tabela.get_children():
        tabela.delete(item)
    
    # Preenche com os livros da lista
    for livro in livros:
        tabela.insert(
            "",
            "end",
            values=(
                livro["titulo_livro"],
                livro["autor_livro"],
                livro["paginas_livro"],
                livro["livro_publi"],
                livro["livro_genero"],
                livro["editora_livro"],
                livro["livro_ISBN"],
            ),
        )

def excluir_livro():
    item_selecionado = tabela.selection()
    
    if not item_selecionado:
        messagebox.showwarning('Aviso', 'Nenhum livro selecionado para deletar!')
        return
    
    # Obtém todos os valores da linha selecionada
    valores = tabela.item(item_selecionado, 'values')
    titulo_livro = valores[0]  # O título está na primeira coluna
    
    # Confirmação antes de excluir
    resposta = messagebox.askyesno(
        'Confirmar Exclusão', 
        f'Tem certeza que deseja deletar o livro:\n"{titulo_livro}"?'
    )
    
    if resposta:
        # Remove da lista livros (comparando pelo ISBN que está na coluna 6)
        for livro in livros:
            if livro['livro_ISBN'] == valores[6]:
                livros.remove(livro)
                break
        
        # Remove da tabela
        tabela.delete(item_selecionado)
        
        # Salva as alterações no JSON
        salvar_em_json()
        
        messagebox.showinfo('Sucesso', 'Livro removido com sucesso!')
     
def localizar_livro():
    termo_busca = search_entry.get().strip().lower()  # Pega o termo digitado
    
    if not termo_busca:
        messagebox.showwarning("Aviso", "Digite um termo para buscar!")
        return
    
    # Limpa a tabela atual
    for item in tabela.get_children():
        tabela.delete(item)
    
    # Filtra os livros que correspondem ao termo (em título, autor ou ISBN)
    livros_encontrados = [
        livro for livro in livros
        if (termo_busca in livro["titulo_livro"].lower() or
            termo_busca in livro["autor_livro"].lower() or
            termo_busca in livro["livro_ISBN"].lower())
    ]
    
    if not livros_encontrados:
        messagebox.showinfo("Resultado", "Nenhum livro encontrado!")
        return
    
    # Preenche a tabela com os resultados
    for livro in livros_encontrados:
        tabela.insert(
            "",
            "end",
            values=(
                livro["titulo_livro"],
                livro["autor_livro"],
                livro["paginas_livro"],
                livro["livro_publi"],
                livro["livro_genero"],
                livro["editora_livro"],
                livro["livro_ISBN"],
            ),
        )


vlr_x = 5
vlr_y = 5
fonte = ['Calibri', 18]
largura_titulo = 50
largura_label = 40 

software_window = tk.Tk()
software_window.title(emoji.emojize('📚Cadastro de Livro📚'))
software_window.geometry('1260x675')
software_window.config(background='lightgray')

software_window_new = tk.Frame(software_window)
software_window_new.grid(row=11, column=0, padx=vlr_x,pady=vlr_y)

title_label = ttk.Label(software_window, text=emoji.emojize('📚📚 Cadastro de Livros 1.0 📚📚'), font=fonte, width=largura_titulo, background='lightgray', foreground='black')
title_label.grid(row=0, rowspan=2, column=0, columnspan=4, padx=10,pady=10)

#Digite o título do Livro
book_title_label = ttk.Label(software_window,text=emoji.emojize('📔Digite o titulo do livro📔: '), font=fonte, width=largura_label, background='lightgray', foreground='black')
book_title_label.grid(row=2, column=0, padx=vlr_x,pady=vlr_y)
book_title_entry = ttk.Entry(software_window, justify='center')
book_title_entry.grid(row=2,column=1,padx=vlr_x,pady=vlr_y)

#Digite o nome do autor
book_autor_label = ttk.Label(software_window, text=emoji.emojize('🧐Digite o nome do autor🧐'), font=fonte,width=largura_label, background='lightgray', foreground='black')
book_autor_label.grid(row=2,column=2,padx=vlr_x,pady=vlr_y)
book_autor_entry = ttk.Entry(software_window, justify='center')
book_autor_entry.grid(row=2,column=3, padx=vlr_x,pady=vlr_y)

#Digite o Quantidade de paginas
book_pages_label = ttk.Label(software_window,text=emoji.emojize('📖Quantidade de paginas do livro📖: '), font=fonte,width=largura_label, background='lightgray', foreground='black')
book_pages_label.grid(row=3,column=0,padx=vlr_x,pady=vlr_y)
book_pages_entry = ttk.Entry(software_window, justify='right')
book_pages_entry.grid(row=3,column=1,padx=vlr_x,pady=vlr_y)

#Digite o ano da publicação
book_year_label = ttk.Label(software_window, text=emoji.emojize('📅Digite o ano da publicação📅: '), font=fonte, width=largura_label, background='lightgray', foreground='black')
book_year_label.grid(row=3,column=2, padx=vlr_x,pady=vlr_y)
book_year_entry = ttk.Entry(software_window,justify='right')
book_year_entry.grid(row=3,column=3,padx=vlr_x,pady=vlr_y)

#Digite o genero
book_gen_label = ttk.Label(software_window,text=emoji.emojize('🔬Digite o genêro do livro🔬: '), font=fonte, width=largura_label, background='lightgray', foreground='black')
book_gen_label.grid(row=4,column=0,padx=vlr_x,pady=vlr_y)
book_gen_entry = ttk.Entry(software_window, justify='center')
book_gen_entry.grid(row=4,column=1,padx=vlr_x,pady=vlr_y)

#Digite a editora
book_edit_label = ttk.Label(software_window, text=emoji.emojize('📰Digite a editora📰: '), font=fonte, width=largura_label, background='lightgray', foreground='black')
book_edit_label.grid(row=4,column=2,padx=vlr_x,pady=vlr_y)
book_edit_entry = ttk.Entry(software_window, justify='center')
book_edit_entry.grid(row=4,column=3,padx=vlr_x,pady=vlr_y)

#Digite o ISBN
book_isbn_label = ttk.Label(software_window,text=emoji.emojize('⚠ Digite o ISBN ⚠'), font=fonte,width=largura_label, background='lightgray', foreground='black')
book_isbn_label.grid(row=5,column=0, columnspan=1, padx=vlr_x,pady=vlr_y)
book_isbn_entry = ttk.Entry(software_window, justify='right', width=100)
book_isbn_entry.grid(row=5,column=2, columnspan=4, padx=vlr_x,pady=vlr_y)

#Criando Botão Salvar
book_save_button = ttk.Button(software_window, text=emoji.emojize('✅ Salvar'), command=salvar_livro)
book_save_button.grid(row=7, column=0, padx=vlr_x,pady=vlr_y)

#Criando Botão Excluir
book_del_button = ttk.Button(software_window, text=emoji.emojize('❌ Deletar'), command=excluir_livro)
book_del_button.grid(row=7, column=1,padx=vlr_x,pady=vlr_y)

#Criando Botão Excluir
book_clean_button = ttk.Button(software_window, text=emoji.emojize('🧹 Zerar Campos'), command=confirmar_limpeza, style='danger.TButton')
book_clean_button.grid(row=7, column=2,padx=vlr_x,pady=vlr_y, sticky='ew')
style = ttk.Style()
style.configure('danger.TButton', foreground='black', background="#fc031c")

#Criando Botão Localizar
# Campo de busca (adicionar após os botões existentes)
search_frame = ttk.Frame(software_window)
search_frame.grid(row=6, column=0, columnspan=4, pady=10, sticky="ew")

search_label = ttk.Label(search_frame, text=emoji.emojize("🔎 Buscar por (Título/Autor/ISBN):"), font=fonte, background='lightgray', foreground='black')
search_label.pack(side="left", padx=5)

search_entry = ttk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=5, expand=True, fill="x")

search_button = ttk.Button(
    search_frame,
    text="Buscar",
    command=localizar_livro  # Função que vamos criar
)
search_button.pack(side="left", padx=5)

def limpar_busca():
    search_entry.delete(0, "end")  # Limpa o campo de busca
    # Recarrega todos os livros na tabela
    for item in tabela.get_children():
        tabela.delete(item)
    for livro in livros:
        tabela.insert(
            "",
            "end",
            values=(
                livro["titulo_livro"],
                livro["autor_livro"],
                livro["paginas_livro"],
                livro["livro_publi"],
                livro["livro_genero"],
                livro["editora_livro"],
                livro["livro_ISBN"],
            ),
        )

# Adicione o botão ao search_frame
clear_search_button = ttk.Button(
    search_frame,
    text="Limpar Busca",
    command=limpar_busca
)
clear_search_button.pack(side="left", padx=5)


# Configurando o grid para expansão
software_window.grid_rowconfigure(8, weight=1)  # Linha onde a tabela ficará
software_window.grid_columnconfigure(0, weight=1)
software_window.grid_columnconfigure(1, weight=1)
software_window.grid_columnconfigure(2, weight=1)
software_window.grid_columnconfigure(3, weight=1)

# Frame para a tabela
frame_tabela = tk.Frame(software_window, borderwidth=2, relief="groove")
frame_tabela.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configurando o grid dentro do frame
frame_tabela.grid_rowconfigure(0, weight=1)
frame_tabela.grid_columnconfigure(0, weight=1)

# Criando a tabela
tabela = ttk.Treeview(frame_tabela, columns=('Titulo', 'Autor', 'Paginas', 'Ano', 'Gênero', 'Editora', 'ISBN'), show='headings')

# Configurando as colunas
tabela.heading('Titulo', text='Título')
tabela.heading('Autor', text='Autor')
tabela.heading('Paginas', text='Páginas')
tabela.heading('Ano', text='Ano Publicação')
tabela.heading('Gênero', text='Gênero')
tabela.heading('Editora', text='Editora')
tabela.heading('ISBN', text='ISBN')

# Definindo largura das colunas
tabela.column('Titulo', width=150)
tabela.column('Autor', width=120)
tabela.column('Paginas', width=80, anchor='center')
tabela.column('Ano', width=100, anchor='center')
tabela.column('Gênero', width=100)
tabela.column('Editora', width=120)
tabela.column('ISBN', width=120)

# Adicionando scrollbars
scroll_vertical = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
scroll_horizontal = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tabela.xview)
tabela.configure(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

# Posicionando os widgets
tabela.grid(row=0, column=0, sticky="nsew")
scroll_vertical.grid(row=0, column=1, sticky="ns")
scroll_horizontal.grid(row=1, column=0, sticky="ew")



#Provando que o livro foi removido

atualizar_tabela()

software_window.mainloop()