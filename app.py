from conexao_mysql import connection
from system_functions import *


# Interface
while connection:
    print("1 - Verificar items")
    print("2 - Inserir item")
    print("3 - alterar quantidade")
    print("4 - Excluir item")
    print("5 - registrar usuário")
    print("6 - login")
    print("7 - logout")
    print("0 - Sair")
    escolha = input('o que voce deseja fazer? ')
    print()

    # buscar todos os itens da tabela
    if escolha == '1':
        get_all_user_items()
    # inserir itens na tabela
    elif escolha == '2':
        inserir_item()
    # atualizar itens na tabela
    elif escolha == '3':
        atualizar_quantidade()
    # excluir itens da tabela
    elif escolha == '4':
        excluir_item_por_id()
    # registrar usuário
    elif escolha == '5':
        nome = input('insira o nome do usuario: ')
        senha = input('insira a senha do usuario: ')
        user_register(nome, senha)
    # login
    elif escolha == '6':
        login()
    # logout
    elif escolha == '7':
        logout()
    # sair
    elif escolha == '0':
        print('até a próxima! Bye!')
        break
