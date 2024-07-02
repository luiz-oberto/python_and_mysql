import mysql.connector
from conexao_mysql import conn, cursor

################ REGISTRO E AUTENTICAÇÃO DO USUÁRIO ###############
logged_user = False
user_id = None

# Registrar-se
def user_register(username, password):
    if username and password:
        insert_query_has_itens = 'INSERT INTO usuario (username, password) VALUES (%s, %s)'
        values = (username, password)
        cursor.execute(insert_query_has_itens, values)
        conn.commit()
        print('Usuário registrado com sucesso!')
        print()
        print(f'Bem vindo, {values[0]}! faça login para começar a utilizar o seu app!')
        print()
    else:
        print('Valores inválidos para a criação do usuário!')

# Fazer login
def login():
    global logged_user
    global user_id
    if logged_user:
        return print('Você já está logado! Se quiser fazer o login em outra conta, por favor, faça o logout')
    else:
        username = input('insira seu nome de usuario: ')
        password = input('insira sua senha: ')
        select_query = 'SELECT * FROM usuario WHERE username = %s AND password = %s'
        values = (username, password)
        cursor.execute(select_query, values)
        result = cursor.fetchall()
        if result:
            logged_user = True
            user_id = result[0][0]
            print()
            print('Usuário autenticado com sucesso!')
            return print()
        else:
            print()
            print('Usuário ou senha inválidos!')
            return 

# verificar se o usuário tá logado
def login_required(func): 
    def wrapper(*args, **kwargs):
        global logged_user
        if not logged_user:
            print('Você precisa estar logado para utilizar esta funcionanlidade.')
            login()
            if not logged_user:
                return
        return func(*args, **kwargs)
    return wrapper

# logout
@login_required
def logout():
    global logged_user
    global user_id
    user_query = "SELECT username FROM usuario WHERE idusuario = %s"
    values = (user_id,)
    cursor.execute(user_query, values)
    result = cursor.fetchone()    
    print(f'até a próxima {result[0]}! Bye')
    logged_user = False
    return


################ INTERAÇÕES COM O BD ###################
# busca todos os itens da tabela
@login_required
def get_all_user_items():
    global user_id
    try:
        select_query ="""
            SELECT item.name AS item, item.quantity AS quantidade
            FROM usuario
            INNER JOIN item ON usuario.idusuario = item.usuario_idusuario
            WHERE usuario.idusuario = %s
            """
        cursor.execute(select_query, (user_id,))
        resultados = cursor.fetchall()
        print('Itens encontrados:')
        print('|  nome  quantidade')
        for linha in resultados:
            print(f'|  {linha[0]}    {linha[1]}')
        return print()
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        return

# inserir itens
@login_required
def inserir_item():
    name = input('insira o item: ')
    quantity = input('insira a quantidade: ')
    global user_id
    try:
        cursor.execute("""INSERT INTO item (name, quantity, usuario_idusuario) VALUES (%s, %s, %s)""", (name, quantity, user_id))
        conn.commit()  # Confirma a inserção
        print("Registro inserido com sucesso.")
        return
    except mysql.connector.Error as err:
        print("Erro ao inserir registro no banco de dados:", err)
        return

# atualizar o nome do item
# OBS: colocar a opção de alterar quantidade
@login_required
def atualizar_bd_name():
    nome = input('insira o nome do item que deseja alterar: ')
    new_name = input('insira novo nome: ')
    if nome and new_name:
        try:
            update_query = "UPDATE item SET name = %s WHERE name = %s"
            valores_update = (new_name, nome)
            cursor.execute(update_query, valores_update)
            conn.commit()  # Confirma a atualização
            print("Registro atualizado com sucesso.")
            return
        except mysql.connector.Error as err:
            print("Erro ao atualizar o registro:", err)
            return
    else:
        print('insira valores válidos.')

# excluir item
@login_required
def excluir_item_por_id():
    nome = input('insira o nome do item que deseja excluir: ')
    global user_id
    try:
        select_query = "SELECT name FROM item WHERE name = %s AND usuario_idusuario = %s"
        values = (nome, user_id)
        cursor.execute(select_query, values)
        resultado = cursor.fetchall()
        confirmacao = input(f'Voce tem certeza que deseja excluir o seguinte item: {resultado[0][0]} [y/n]', )
        if confirmacao == 'y':
            delete_query = "DELETE FROM item WHERE name = %s AND usuario_idusuario = %s"
            cursor.execute(delete_query, values) # -> lembre-se sempre de passar uma tupla no 'values'
            conn.commit()  # Confirma a exclusão
            print("Registro deletado com sucesso.")
            return
    except mysql.connector.Error as err:
        print("Erro ao deletar o registro:", err)
        return
