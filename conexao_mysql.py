import mysql.connector
import os


# Configurações de conexão
config = {
    'user': 'usuario',
    'password': 'senha@',
    'host': 'host',  # ou 'localhost' se estiver usando port forwarding
    'database': 'database',
    'raise_on_warnings': True
}

def testando_conexão():
    try:
        # limpando o terminal
        os.system('cls')

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
        return True
    except mysql.connector.Error as err:
        print("Erro ao conectar ao MySQL:", err)

def criando_cursor():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        return conn, cursor


    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
