
lista_de_livros = []

livro = {
    'titulo_livro'   : 'Programação Python',
    'autor_livro'   : 'Nilo Ney Coutinho Menezes',
    'paginas_livro' :  328,
    'livro_publi'   :  2019,
    'livro_genero'  : 'Técnico',
    'editora_livro' : 'Novatec',
    'livro_ISBN'    : '978-85-7522-718-3'
}


lista_de_livros.append(livro)
print(lista_de_livros)

livro = {
    'titulo_livro'   : 'Aonde a gente vai, papai?',
    'autor_livro'   : 'Jean-Louis Fournier',
    'paginas_livro' :  158,
    'livro_publi'   :  2009,
    'livro_genero'  : 'Drama',
    'editora_livro' : 'Intriseca',
    'livro_ISBN'    : '978-85-98078-50-2'
}

lista_de_livros.append(livro)
print(lista_de_livros)

print(f'O titulo do primeiro livro é {lista_de_livros[0]['titulo_livro']} e o titulo do segundo livro é {lista_de_livros[1]['titulo_livro']}')

# print(f'O titulo do livro é {livro['titulo_livro']}')
# print(f'O autor do livro é {livro['autor_livro']}')
# print(f'A quantidade de paginas é {livro['paginas_livro']}')
# print(f'O ano da publicação foi {livro['livro_publi']}')
# print(f'O genero do livro é {livro['livro_genero']}')
# print(f'A editora que publicou é {livro['editora_livro']}')
# print(f'O código ISBN é {livro['livro_ISBN']}')
