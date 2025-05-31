frutas = ['Maça','Pera','Uva','Abacate','Gato']

print(frutas[0])
print(frutas[2])
print(frutas[4])
print(frutas)
print(f'A lista contém {len(frutas)} frutas!')

frutas.append('Carambola')
frutas.append('Jaca')

print(frutas[5])
print(frutas[6])
print(frutas)
print(f'A lista contém {len(frutas)} frutas!')

#frutas.pop(4)
print(frutas[4])
frutas.remove('Gato')
print(frutas)
print(f'A lista contém {len(frutas)} frutas!')
frutas.remove('Jaca')
print(frutas)
print(f'A lista contém {len(frutas)} frutas!')

frutas[2] = 'Melancia'
print(frutas[2])
print(frutas)
print(len(frutas))

frutas.sort()
print(frutas)

for fruta in frutas:
    print(f'Suco de {fruta}')

frutas.reverse()
print(frutas)