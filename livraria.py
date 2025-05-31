import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import emoji

livros = []

def limpar_tela():
    book_title_entry.delete(0, tk.END)
    book_autor_entry.delete(0, tk.END)
    book_pages_entry.delete(0, tk.END)
    book_year_entry.delete(0, tk.END)
    book_gen_entry.delete(0, tk.END)
    book_edit_entry.delete(0, tk.END)
    book_isbn_entry.delete(0, tk.END)

def salvar_livro():
    livro = {
        'titulo_livro' : book_title_entry.get(),
        'autor_livro'  : book_autor_entry.get(),
        'paginas_livro': book_pages_entry.get(),
        'livro_publi'  : book_year_entry.get(),
        'livro_genero' : book_gen_entry.get(),
        'editora_livro': book_edit_entry.get(),
        'livro_ISBN'   : book_isbn_entry.get()
    }
    livros.append(livro)
    messagebox.showinfo('Sucesso','Livro cadastrado!')
    limpar_tela() 

def excluir_livro():
     livro = {
        'titulo_livro' : book_title_entry.get(),
        'autor_livro'  : book_autor_entry.get(),
        'paginas_livro': book_pages_entry.get(),
        'livro_publi'  : book_year_entry.get(),
        'livro_genero' : book_gen_entry.get(),
        'editora_livro': book_edit_entry.get(),
        'livro_ISBN'   : book_isbn_entry.get()
     }
     livros.remove(livro)
     messagebox.showinfo('Sucesso','Livro removido!')
     limpar_tela() 
     
# def localizar_livro():

vlr_x = 5
vlr_y = 5
fonte = ['Calibri', 18]
largura_titulo = 50
largura_label = 40 

software_window = tk.Tk()
software_window.title(emoji.emojize('📚Cadastro de Livro📚'))
software_window.geometry('1260x675')
software_window.config(background='Green')

title_label = ttk.Label(software_window, text=emoji.emojize('📚📚 Cadastro de Livros 1.0 📚📚'), font=fonte, width=largura_titulo, background='Green', foreground='White')
title_label.grid(row=0, rowspan=2, column=0, columnspan=4, padx=10,pady=10)

#Digite o título do Livro
book_title_label = ttk.Label(software_window,text=emoji.emojize('📔Digite o titulo do livro📔: '), font=fonte, width=largura_label, background='Green', foreground='White')
book_title_label.grid(row=2, column=0, padx=vlr_x,pady=vlr_y)
book_title_entry = ttk.Entry(software_window, justify='center')
book_title_entry.grid(row=2,column=1,padx=vlr_x,pady=vlr_y)

#Digite o nome do autor
book_autor_label = ttk.Label(software_window, text=emoji.emojize('🧐Digite o nome do autor🧐'), font=fonte,width=largura_label, background='Green', foreground='White')
book_autor_label.grid(row=2,column=2,padx=vlr_x,pady=vlr_y)
book_autor_entry = ttk.Entry(software_window, justify='center')
book_autor_entry.grid(row=2,column=3, padx=vlr_x,pady=vlr_y)

#Digite o Quantidade de paginas
book_pages_label = ttk.Label(software_window,text=emoji.emojize('📖Quantidade de paginas do livro📖: '), font=fonte,width=largura_label, background='Green', foreground='White')
book_pages_label.grid(row=3,column=0,padx=vlr_x,pady=vlr_y)
book_pages_entry = ttk.Entry(software_window, justify='right')
book_pages_entry.grid(row=3,column=1,padx=vlr_x,pady=vlr_y)

#Digite o ano da publicação
book_year_label = ttk.Label(software_window, text=emoji.emojize('📅Digite o ano da publicação📅: '), font=fonte, width=largura_label, background='Green', foreground='White')
book_year_label.grid(row=3,column=2, padx=vlr_x,pady=vlr_y)
book_year_entry = ttk.Entry(software_window,justify='right')
book_year_entry.grid(row=3,column=3,padx=vlr_x,pady=vlr_y)

#Digite o genero
book_gen_label = ttk.Label(software_window,text=emoji.emojize('🔬Digite o genêro do livro🔬: '), font=fonte, width=largura_label, background='Green', foreground='White')
book_gen_label.grid(row=4,column=0,padx=vlr_x,pady=vlr_y)
book_gen_entry = ttk.Entry(software_window, justify='center')
book_gen_entry.grid(row=4,column=1,padx=vlr_x,pady=vlr_y)

#Digite a editora
book_edit_label = ttk.Label(software_window, text=emoji.emojize('📰Digite a editora📰: '), font=fonte, width=largura_label, background='Green', foreground='White')
book_edit_label.grid(row=4,column=2,padx=vlr_x,pady=vlr_y)
book_edit_entry = ttk.Entry(software_window, justify='center')
book_edit_entry.grid(row=4,column=3,padx=vlr_x,pady=vlr_y)

#Digite o ISBN
book_isbn_label = ttk.Label(software_window,text=emoji.emojize('⚠ Digite o ISBN ⚠'), font=fonte,width=largura_label, background='Green', foreground='White')
book_isbn_label.grid(row=5,column=0, columnspan=1, padx=vlr_x,pady=vlr_y)
book_isbn_entry = ttk.Entry(software_window, justify='right', width=100)
book_isbn_entry.grid(row=5,column=2, columnspan=4, padx=vlr_x,pady=vlr_y)

#Criando Botão Salvar
book_save_button = ttk.Button(software_window, text=emoji.emojize('✅ Salvar'), command=salvar_livro)
book_save_button.grid(row=7, column=0, padx=vlr_x,pady=vlr_y)

#Criando Botão Excluir
book_del_button = ttk.Button(software_window, text=emoji.emojize('❌ Deletar'), command=excluir_livro)
book_del_button.grid(row=7, column=1,padx=vlr_x,pady=vlr_y)

#Criando Botão Localizar
book_search_button = ttk.Button(software_window, text=emoji.emojize('🔎 Localizar'), command='')
book_search_button.grid(row=7, column=2, padx=vlr_x,pady=vlr_y)

#Provando que o Livro foi salvo
selecao_livraria = tk.Text(software_window)
selecao_livraria.grid(row=9,rowspan=10,column=0,columnspan=4, padx=5,pady=5)

#Provando que o livro foi removido


software_window.mainloop()