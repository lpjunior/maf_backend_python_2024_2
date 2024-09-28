# Escreva um programa que verifique se um número é par ou ímpar.
numero = int(input('Digite um número: '))

# print((numero % 2 == 0) ? 'O número é par!' : 'O número é ímpar!')
# operador ternário, substitui o if else
# O Python não tem operador ternário, mas pode ser feito da seguinte forma:

if numero % 2 == 0:
    print('O número é par!')
else:
    print('O número é ímpar!')

# Desenvolva um algoritmo que peça oa usuário sua idade e retorne se ele pode votar ou não.
idade = int(input('Digite sua idade: ')) 
# input sempre retorna uma string, por isso é necessário converter para int

if idade >= 16: # estrutura de decisão composta
    print('Você pode votar!')
else:
    print('Você não pode votar!')