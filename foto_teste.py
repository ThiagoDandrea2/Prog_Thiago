import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Funções dos botões
def soma():
    messagebox.showinfo('RESULTADO!!', f'O resultado da soma é {(float(entrada_numero_1.get()) + float(entrada_numero_2.get())):.2f}')

def subtrair():
    messagebox.showinfo('RESULTADO!!', f'O resultado da subtração é {(float(entrada_numero_1.get()) - float(entrada_numero_2.get())):.2f}')

def multiplicar():
    messagebox.showinfo('RESULTADO!!', f'O resultado da multiplicação é {(float(entrada_numero_1.get()) * float(entrada_numero_2.get())):.2f}')

def dividir():
    messagebox.showinfo('RESULTADO!!', f'O resultado da divisão é {(float(entrada_numero_1.get()) / float(entrada_numero_2.get())):.2f}')

def divisao_inteira():
    messagebox.showinfo('RESULTADO!!', f'O resultado da divisão inteira é {(float(entrada_numero_1.get()) // float(entrada_numero_2.get())):.2f}')

def modulo():
    messagebox.showinfo('RESULTADO!!', f'O resultado do módulo é {(float(entrada_numero_1.get()) % float(entrada_numero_2.get())):.2f}')

def exponenciacao():
    messagebox.showinfo('RESULTADO!!', f'O resultado da exponenciação é {(float(entrada_numero_1.get()) ** float(entrada_numero_2.get())):.2f}')

# Definição de Pad's
valor_pad_x = 18
valor_pad_y = 18

# Abertura da Janela
programa = tk.Tk()
programa.title('Calculadora 1.0')
programa.geometry('1024x900')

# Carregar e configurar a imagem de fundo
try:
    # Substitua 'background.jpg' pelo caminho da sua imagem
    background_image = Image.open('calculadora.jpg')
    background_image = background_image.resize((1024, 900), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Criar um canvas para a imagem de fundo
    canvas = tk.Canvas(programa, width=1024, height=900, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    
    # Criar um frame principal com fundo semi-transparente
    main_frame = tk.Frame(canvas, bg='#000000', bd=0)  # Cor preta com transparência
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Adicionar retângulo semi-transparente para melhor legibilidade
    canvas.create_rectangle(50, 50, 974, 850, fill='black', stipple='gray50', outline='')
    
except Exception as e:
    print(f"Erro ao carregar imagem de fundo: {e}")
    # Fallback se a imagem não carregar
    programa.config(bg='grey')
    main_frame = tk.Frame(programa, bg='grey')
    main_frame.pack(fill="both", expand=True)

# Configuração da Calculadora com melhor contraste

# Titulo (com fundo escuro semi-transparente)
calculadora = tk.Label(main_frame, text='Calculadora 1.0', font=('Jokerman', 32), 
                      bg='#333333', fg='white', justify='center')  # Cinza escuro
calculadora.pack(padx=valor_pad_x, pady=valor_pad_y)

# Pedindo Primeiro Numero:
primeiro_numero = tk.Label(main_frame, text="Digite o primeiro numero: ", 
                          font=('Jokerman', 16), bg='#333333', fg='white', justify='center')
primeiro_numero.pack(padx=valor_pad_x, pady=valor_pad_y)
entrada_numero_1 = ttk.Entry(main_frame)
entrada_numero_1.pack(padx=valor_pad_x, pady=valor_pad_y)

# Pedindo Segundo Numero:
segundo_numero = tk.Label(main_frame, text='Digite o segundo Número: ', 
                         font=('Jokerman', 16), bg='#333333', fg='white', justify='center')
segundo_numero.pack(padx=valor_pad_x, pady=valor_pad_y)
entrada_numero_2 = ttk.Entry(main_frame)
entrada_numero_2.pack(padx=valor_pad_x, pady=valor_pad_y)

# Criando os botões (com estilo para melhor visibilidade)
style = ttk.Style()
style.configure('TButton', font=('Arial', 12), background='#444444', foreground='black')
style.map('TButton', background=[('active', '#555555')])

somar_botao = ttk.Button(main_frame, text='Somar', command=soma)
somar_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

sub_botao = ttk.Button(main_frame, text='Subtrair', command=subtrair)
sub_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

mult_botao = ttk.Button(main_frame, text='Multiplicar', command=multiplicar)
mult_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

div_botao = ttk.Button(main_frame, text='Divisão', command=dividir)
div_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

div_int_botao = ttk.Button(main_frame, text='Divisão(Inteiro)', command=divisao_inteira)
div_int_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

modulo_botao = ttk.Button(main_frame, text='Módulo', command=modulo)
modulo_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

expo_botao = ttk.Button(main_frame, text='Exponenciação', command=exponenciacao)
expo_botao.pack(padx=valor_pad_x, pady=valor_pad_y)

# Garantir que a imagem não seja coletada pelo garbage collector
programa.background_photo = background_photo

# Programa em Loop
programa.mainloop()