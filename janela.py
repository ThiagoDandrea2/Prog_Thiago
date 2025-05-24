#Windows - janela para software grafico
#label (Text, font, foreground, background, width, height)-> saída
#Entry (font, foreground, background, show, justify) -> entrada
#Button (text) -> ação

import tkinter as tk
from tkinter import messagebox

#Criando função
def mensagem_usuario():
    messagebox.showinfo('ATENÇÃO!!', f'Bem vindo ao software {nome_entrada.get()}')

# variavéis para configuração do espaçamento
valor_pad_x = 20
valor_pad_y = 20

#Inicio da janela e configuração
janela_principal = tk.Tk()
janela_principal.title('Minha primeira Janela')
janela_principal.geometry('1024x768')
janela_principal.config(bg="white")

#Configuração dos textos em tela
label_frase = tk.Label(janela_principal,text='Hello World!', bg='green', fg ='white', font=['Jokerman', 36])
label_frase.pack(padx=valor_pad_x,pady=valor_pad_y)
label_segunda_frase = tk.Label(janela_principal, text='Seja Bem-Vindo', bg='Blue', fg='White', font=['Jokerman', 24])
label_segunda_frase.pack(padx=valor_pad_x,pady=valor_pad_y)

#Configuração da entrada
label_entrada = tk.Label(janela_principal, text='Digite seu nome: ', font=['Jokerman', 16])
label_entrada.pack(padx=valor_pad_x,pady=valor_pad_y)
nome_entrada = tk.Entry(janela_principal, bg='black', fg='white', font=['Jokerman', 14],)
nome_entrada.pack(padx=valor_pad_x,pady=valor_pad_y)

#Configurando botão
save_button = tk.Button(janela_principal,text='Salvar', bg='green', font=['Jokerman', 14], command=mensagem_usuario)
#save_button = tk.Button(janela_principal,text='Salvar', bg='green', font=['Jokerman', 14], command=lambda: messagebox.showinfo('ATENÇÃO!!', f'Bem vindo ao software {nome_entrada.get()}'))
save_button.pack(padx=valor_pad_x,pady=valor_pad_y)


# Definição para manutenção da abertura de janela
janela_principal.mainloop()