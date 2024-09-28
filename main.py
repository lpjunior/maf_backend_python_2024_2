# Estrutura de decisão
# Calculo de salário de um vendedor de veículos com possível prémio quando é aniversário do funcionário.
# salario = float(input('Digite seu salário: '))
# numeroDeCarrosVendidos = int(input('Digite o número de vendas: '))
# eAniversario = input('É seu aniversário? (S/N): ').upper()
# 
# bonus = 100 * numeroDeCarrosVendidos
# 
# salario += bonus
# 
# if eAniversario == 'S':
#     premio = 100
#     salario += premio
# 
# print(f'Seu salário é de R${salario:.2f}')

# Estrutura de dados (lista)
# lista de alunos do curso de desenvolvimento backend com Python

alunos = ["Jorge", "Matheus", "Antonio", "Diogo", "Guilherme", "Everton", "Lucas", "Jod"]
alunos.append("Gabriela")
alunos.append("Pedro")
print(alunos)
print(len(alunos))
alunos.sort()
print(alunos)

# len(), append(), remove(), sort()

# Estrutura de repetição
# for, while

## FOR
for i in range(10): # for each
    print(i)

# Interando sobre uma string
nome = "Luis"
for letra in nome:
    print(letra)

# Interando sobre uma lista    
for aluno in alunos:
    print(aluno)

# Interando sobre um dicionário
aluno = { "nome": "Luis", "idade": 20, "curso": "ADS" }
for chave in aluno:
    print(f"{chave}: {aluno[chave]}")
    
## WHILE
contador = 0
while contador < 10:
    print(contador)
    contador += 1
    
# Loop infinito
soma = 0
while True:
    print("Loop infinito")
    soma += 1
    if soma == 10: # controle de fluxo
        print("Saindo do loop infinito")
        break
        
print(f"Soma: {soma}")

# Funções
# Existem 2 tipos de funções que são com retorno e sem retorno

# Funções com retorno
def soma(a, b):
    return a + b

resultado = soma(2, 3)
print(resultado)

# Funções sem retorno
def imprimir_mensagem(msg="Olá, mundo!"):
    print(msg)

imprimir_mensagem("Olá, Luis!")


# Exercícios

# 1. Crie uma função que receba uma lista de números e retorne a soma de todos os números.

def soma_lista(numeros):
    return sum(numeros)

lista = [1, 2, 3, 4, 5]
resultado = soma_lista(lista)
print(resultado)

print(soma_lista([1, 2, 3, 4, 5]))