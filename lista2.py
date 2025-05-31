import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

itens = []

def salvar_button():
    item = item_entry.get()
    if item.strip() !=  '':
        itens.append(item)
        itens.sort()
        itens_combobox = ttk.Combobox(windows_software, values=itens)
        itens_combobox.grid(row=3,column=0,padx=5,pady=5)
        itens_combobox.set('Conteúdo de itens')
        item_entry.delete(0,tk.END)
    else:
        messagebox.showinfo('Atenção','Digite algo no campo item!')

windows_software = tk.Tk()
windows_software.title('Teste de Lista')
windows_software.geometry('800x600')

#Label
item_label = ttk.Label(windows_software, text='Digite um item: ', background='White', foreground='Black')
item_label.grid(row=0,column=0,padx=5,pady=5)
item_entry = ttk.Entry(windows_software,justify='center')
item_entry.grid(row=0,column=1,padx=5,pady=5)
item_button = ttk.Button(windows_software, text='Salvar', command=salvar_button)
item_button.grid(row=2,column=0,padx=5,pady=5)

#Combo de Itens
itens_combobox = ttk.Combobox(windows_software, values=itens)
itens_combobox.grid(row=3,column=0,padx=5,pady=5)
itens_combobox.set('Conteúdo de itens')


windows_software.mainloop()