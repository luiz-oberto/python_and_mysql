import mysql.connector


# Configurações de conexão
config = {
    'user': 'seu_ususario',
    'password': 'sua_senha',
    'host': 'IP_da_maquina_virtul',  # ou 'localhost' se estiver usando port forwarding
    'database': 'nome_do_banco_dados',
    'raise_on_warnings': True
}

# Carregar todas as informações do BD
def verificar_bd():
    try:
        select_query = "SELECT * FROM item"
        cursor.execute(select_query)
        resultados = cursor.fetchall()
        for linha in resultados:
            print("itens na tabela", linha)
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)

# Inserir itens no BD
def inserir_item(name=None, quantity=None):
    try:
        insert_query = "INSERT INTO item (name, quantity) VALUES (%s, %s)"
        valores_insert = (name, quantity)
        cursor.execute(insert_query, valores_insert)
        conn.commit()  # Confirma a inserção
        print("Registro inserido com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao inserir registro no banco de dados:", err)

# Atualizar itens no BD
def atualizar_bd_name(previous_name=None, new_name=None):
    try:
        update_query = "UPDATE item SET name = %s WHERE name = %s"
        valores_update = (new_name, previous_name)
        cursor.execute(update_query, valores_update)
        conn.commit()  # Confirma a atualização
        print("Registro atualizado com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao atualizar o registro:", err)

# Excluir itens do BD
def excluir_item_por_id(iditem=None):
    try:
        delete_query = "DELETE FROM item WHERE iditem = %s"
        valores_delete = (iditem)
        cursor.execute(delete_query, valores_delete)
        conn.commit()  # Confirma a exclusão
        print("Registro deletado com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao deletar o registro:", err)

# Fazendo a conexão com o DB
try:
    # Estabelecendo a conexão
    conn = mysql.connector.connect(**config)
    
    # Criando um cursor
    cursor = conn.cursor()
    
    # Executando uma consulta de teste
    cursor.execute("SELECT DATABASE();")
    
    # Obtendo o resultado
    result = cursor.fetchone()
    print("Conectado ao banco de dados:", result)
    
    # Fechando o cursor e a conexão
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print("Erro ao conectar ao MySQL:", err)

# Estabelecendo a conexão para utilização das funções
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()


except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")

# Exemplos de uso
verificar_bd()
print()
inserir_item('carne', 3)
print()
atualizar_bd_name('tomate')
print()
excluir_item_por_id()
print()
verificar_bd()

# Fechando a conexão 
cursor.close()
conn.close()