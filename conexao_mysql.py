import mysql.connector
import os


# Configurações de conexão
config = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'host': 'seu_host',  #7 ou 'localhost' se estiver usando port forwarding
    'database': 'modelo-despensa',
    'raise_on_warnings': True
}

def testando_conexão():
    try:
        # limpando o terminal
        os.system('cls')

        # Estabelecendo a conexão
        conn = mysql.connector.connect(**config)
        
        # Criando um cursor
        cursor = conn.cursor(buffered=True)
        
        # Executando uma consulta de teste
        cursor.execute("SELECT DATABASE();")
        
        # Obtendo o resultado
        result = cursor.fetchone()
        print("Conectado ao banco de dados:", result)
        
        # Fechando o cursor e a conexão
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print("Erro ao conectar ao MySQL:", err)
        return False

def criando_cursor():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)
        return conn, cursor


    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")


################### FAZENDO A CONEXÃO COM O BD ###################
connection = testando_conexão()
while not connection:
    try_again = input('falha na conexão, deseja tentar novamente? (s/n)')
    if try_again == 's':
        connection = testando_conexão()
    else:
        print('# Encerrando programa #')
        # conn e cursor devem ser None para não dar erro ao encerrar o programa.
        conn, cursor = None, None
        break

################### CRIANDO DO CURSOR ###################
if connection:
    conn, cursor = criando_cursor()
else:
    pass