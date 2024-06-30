from conexao_mysql import testando_conexão, criando_cursor
import mysql.connector


connection = testando_conexão()
while not connection:
    try_again = input('falha na conexão, deseja tentar novamente? (s/n)')
    if try_again == 's':
        connection = testando_conexão()
    else:
        print('Encerrando programa')
        break

if connection:
    conn, cursor = criando_cursor()
else:
    pass


################ REGISTRO E AUTENTICAÇÃO DO USUÁRIO ###############
logged_user = False

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
    username = input('insira seu nome de usuario: ')
    password = input('insira sua senha: ')
    select_query = 'SELECT * FROM usuario WHERE username = %s AND password = %s'
    values = (username, password)
    cursor.execute(select_query, values)
    result = cursor.fetchall()
    if result:
        logged_user = True
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
def fetch_all_items(): 
    try:
        select_query = "SELECT * FROM item"
        cursor.execute(select_query)
        resultados = cursor.fetchall()
        print('Itens encontrados:')
        for linha in resultados:
            print(linha)
        return print()
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        return

@login_required
def inserir_item():
    name = input('insira o item: ')
    quantity = input('insira a quantidade: ')
    try:
        insert_query = "INSERT INTO item (name, quantity) VALUES (%s, %s)"
        valores_insert = (name, quantity)
        cursor.execute(insert_query, valores_insert)
        conn.commit()  # Confirma a inserção
        print("Registro inserido com sucesso.")
        return
    except mysql.connector.Error as err:
        print("Erro ao inserir registro no banco de dados:", err)
        return

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
