import mysql.connector
from conexao_mysql import conn, cursor
import bcrypt
import getpass


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

################ REGISTRO E AUTENTICAÇÃO DO USUÁRIO ###############
# Classe de sessão do usuário
class UserSession:
    def __init__(self):
        self.logged_user = False
        self.user_id = None
    
    def login(self):
        if self.logged_user:
            return print('Você já está logado! Se quiser fazer o login em outra conta, por favor, faça o logout')
        else:
            username = input('insira seu nome de usuario: ')
            password = getpass.getpass('insira sua senha: ')
            # vai buscar a senha hasheada do usuário
            select_query_password = 'SELECT password FROM usuario WHERE username = %s'
            cursor.execute(select_query_password, (username,))
            result_passwd = cursor.fetchone()
            if result_passwd:
                stored_password = result_passwd[0]
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                # verifica se as senhas coincidem
                if check_password(stored_password, password):
                    select_query = 'SELECT * FROM usuario WHERE username = %s'
                    cursor.execute(select_query, (username,))
                    result = cursor.fetchone()
                    self.logged_user = True
                    self.user_id = result[0]
                    return print('Bem vindo, {}!'.format(username))
                else:
                    print('Usuário ou senha inválidos!')
            else:
                print('Usuário ou senha inválidos!')
    
    def logout(self):
        # Lógica de logout
        user_query = "SELECT username FROM usuario WHERE idusuario = %s"
        values = (self.user_id,)
        cursor.execute(user_query, values)
        result = cursor.fetchone()
        print(f'até a próxima {result[0]}! Bye')
        self.logged_user = False
        return
    
    
# Registrar-se
def user_register(username, password):
    if username and password:
        hash_pwd = hash_password(password)
        insert_query_has_itens = 'INSERT INTO usuario (username, password) VALUES (%s, %s)'
        values = (username, hash_pwd)
        cursor.execute(insert_query_has_itens, values)
        conn.commit()
        print('Usuário registrado com sucesso!')
        print()
        print(f'Bem vindo, {values[0]}! faça login para começar a utilizar o seu app!')
        print()
    else:
        print('Valores inválidos para a criação do usuário!')



################ INTERAÇÕES COM O BD ###################
# busca todos os itens da tabela
sessao_usuario = UserSession()

# verificar se o usuário tá logado
def login_required(func): 
    def wrapper(*args, **kwargs):
        if not sessao_usuario.logged_user:
            print('Você precisa estar logado para utilizar esta funcionanlidade.')
            sessao_usuario.login()
            if not sessao_usuario.logged_user:
                return
        return func(*args, **kwargs)
    return wrapper

@login_required
def get_all_user_items():
    user_id = sessao_usuario.user_id
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
    user_id = sessao_usuario.user_id
    try:
        cursor.execute("""INSERT INTO item (name, quantity, usuario_idusuario) VALUES (%s, %s, %s)""", (name, quantity, user_id))
        conn.commit()  # Confirma a inserção
        print("Registro inserido com sucesso.")
        return
    except mysql.connector.Error as err:
        print("Erro ao inserir registro no banco de dados:", err)
        return

# atualizar o nome do item
@login_required
def atualizar_quantidade():
    user_id = sessao_usuario.user_id
    nome = input('insira o nome do item que deseja alterar a quantidade: ')
    buscar_item = 'SELECT * FROM item WHERE name = %s'
    cursor.execute(buscar_item, (nome,))
    resultado = cursor.fetchone()
    if resultado:
        quantidade_atualizada = input('insira quantidade atualizada: ')
        try:
            update_query = "UPDATE item SET quantity = %s WHERE name = %s AND usuario_idusuario = %s"
            valores_update = (quantidade_atualizada, nome, user_id)
            cursor.execute(update_query, valores_update)
            conn.commit()  # Confirma a atualização
            print("Registro atualizado com sucesso.")
        except mysql.connector.Error as err:
            print("Erro ao atualizar o registro:", err)
            return
    else:
        print('insira valores válidos.')

# excluir item
@login_required
def excluir_item_por_id():
    user_id = sessao_usuario.user_id
    excluir_nome = input('insira o nome do item que deseja excluir: ')
    buscar_item = 'SELECT * FROM item WHERE name = %s'
    cursor.execute(buscar_item, (excluir_nome,))
    resultado = cursor.fetchone()
    if resultado:
        try:
            select_query = "SELECT name FROM item WHERE name = %s AND usuario_idusuario = %s"
            values = (excluir_nome, user_id)
            cursor.execute(select_query, values)
            resultado = cursor.fetchall()
            confirmacao = input(f'Voce tem certeza que deseja excluir o seguinte item: {resultado[0][0]}? [y/n]', )
            if confirmacao == 'y':
                delete_query = "DELETE FROM item WHERE name = %s AND usuario_idusuario = %s"
                cursor.execute(delete_query, values) # -> lembre-se sempre de passar uma tupla no 'values'
                conn.commit()  # Confirma a exclusão
                print("Registro deletado com sucesso.")
                return
        except mysql.connector.Error as err:
            print("Erro ao deletar o registro:", err)
            return
    else:
        print('insira valores válidos.')