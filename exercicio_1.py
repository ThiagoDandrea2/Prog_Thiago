import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk

#Função botão
def soma():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) + float(entrada_numero_2.get())):.2f}')

def subtrair():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) - float(entrada_numero_2.get())):.2f}')

def multiplicar():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) * float(entrada_numero_2.get())):.2f}')

def dividir():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) / float(entrada_numero_2.get())):.2f}')

def divisao_inteira():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) // float(entrada_numero_2.get())):.2f}')

def modulo():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) % float(entrada_numero_2.get())):.2f}')

def exponenciacao():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) ** float(entrada_numero_2.get())):.2f}')

#Definição de Pad's
valor_pad_x = 18
valor_pad_y = 18

#Abertura da Janela
programa = tk.Tk()
programa.title('Calculadora 1.0')
programa.geometry('1024x900')
programa.config(bg='grey')

#Configuração da Calculadora

#Titulo
calculadora = ttk.Label(programa, text='Calculadora 1.0', font=['Jokerman', 32], background='White', justify='center')
calculadora.pack(padx=valor_pad_x,pady=valor_pad_y)

#Pedindo Primeiro Numero:
primeiro_numero = ttk.Label(programa,text="Digite o primeiro numero: ", font=['Jokerman', 16], background='Blue', justify='center')
primeiro_numero.pack(padx=valor_pad_x,pady=valor_pad_y)
entrada_numero_1 = ttk.Entry(programa)
entrada_numero_1.pack(padx=valor_pad_x,pady=valor_pad_y)

#Pedindo Segundo Numero:
segundo_numero = ttk.Label(programa,text='Digite o segundo Número: ', font=['Jokerman', 16], background= 'yellow', justify='center')
segundo_numero.pack(padx=valor_pad_x,pady=valor_pad_y)
entrada_numero_2 = ttk.Entry(programa)
entrada_numero_2.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o Botão de Soma
somar_botao = ttk.Button(programa,text='Somar', command=soma)
somar_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#criando o Botão de Subtração
sub_botao = ttk.Button(programa, text='Subtrair', command=subtrair)
sub_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o botão de Multiplicar
mult_botao = ttk.Button(programa, text='Multiplicar', command=multiplicar)
mult_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o botão de divisão
div_botao = ttk.Button(programa, text='Divisão', command=dividir)
div_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o botão de divisão inteiro
div_int_botao = ttk.Button(programa, text='Divisão(Inteiro)', command=divisao_inteira)
div_int_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o botão de Módulo
modulo_botao = ttk.Button(programa,text='Módulo', command=modulo)
modulo_botao.pack(padx=valor_pad_x,pady=valor_pad_y)

#Criando o botão da Exponenciação
expo_botao = ttk.Button(programa, text='Exponenciação', command=exponenciacao)
expo_botao.pack(padx=valor_pad_x,pady=valor_pad_y)


#Programa em Loop
programa.mainloop()