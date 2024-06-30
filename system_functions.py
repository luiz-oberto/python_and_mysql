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
        # criando lista
        print(f'Bem vindo, {values[0]}! Estamos criando sua listinha.')
        print()
        user_id = cursor.lastrowid
        insert_query_has_itens = "INSERT INTO has_itens (usuario_idusuario) VALUES (%s)"
        cursor.execute(insert_query_has_itens, (user_id,))
        conn.commit()
        print("Lista criada com sucesso, faça bom proveito!")
    else:
        print('Valores inválidos para a criação do usuário!')

# Fazer login
def login():
    global logged_user
    global user_id
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
    logged_user = False
    return print('deixando a sessão...')




################ INTERAÇÕES COM O BD ###################
# busca todos os itens da tabela
@login_required
def get_all_user_items():
    global user_id
    try:
        select_query ="""
            SELECT *
            FROM item
            JOIN has_itens ON item.has_itens_idhas_itens = has_itens.idhas_itens
            WHERE has_itens.usuario_idusuario = %s
            """
        cursor.execute(select_query, (user_id,))
        resultados = cursor.fetchall()
        print('Itens encontrados:')
        for linha in resultados:
            print('|  id    nome  quantidade')
            print(f'|  {linha[0]}    {linha[1]}  {linha[2]}')
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
        # obter o idhas_itens do usuário
        cursor.execute("SELECT idhas_itens FROM has_itens WHERE usuario_idusuario = %s", (user_id,))
        has_itens_id = cursor.fetchone()[0] # salva aqui o id do has_itens do usuário

        # inserir novo item na lista de itens do usuário
        cursor.execute("INSERT INTO item (name, quantity, has_itens_idhas_itens) VALUES (%s, %s, %s)", (name, quantity, has_itens_id))
        conn.commit()  # Confirma a inserção
        print("Registro inserido com sucesso.")
        return
    except mysql.connector.Error as err:
        print("Erro ao inserir registro no banco de dados:", err)
        return

# atualizar o nome do item
@login_required
def atualizar_bd_name():
    id = input('insira o id do item que deseja alterar: ')
    new_name = input('insira novo nome: ')
    if id and new_name:
        try:
            update_query = "UPDATE item SET name = %s WHERE iditem = %s"
            valores_update = (new_name, id)
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
    iditem = input('insira o id do item que deseja excluir: ')
    try:
        select_query = f"SELECT {iditem} FROM item"
        cursor.execute(select_query)
        resultado = cursor.fetchall()
        confirmacao = input(f'Voce tem certeza que deseja excluir o seguinte item: {resultado} [y/n]', )
        if confirmacao == 'y':
            delete_query = "DELETE FROM item WHERE iditem = %s"
            valores_delete = (iditem)
            cursor.execute(delete_query, valores_delete)
            conn.commit()  # Confirma a exclusão
            print("Registro deletado com sucesso.")
            return
    except mysql.connector.Error as err:
        print("Erro ao deletar o registro:", err)
        return
