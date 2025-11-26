import logging
from dotenv import load_dotenv

import os
import psycopg2
import psycopg2.pool

from ..validation import CreateError
load_dotenv()

# Captura o nome do arquivo para registro dos logs
logger = logging.getLogger(__name__)

# Encapsulamento das credenciais do banco de dados Postgres
DatabaseConfig = {
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASS'),
    "port": os.getenv('DB_PORT'),
}

# Inicializa uma variável global para o pool de conexões
connectionPool = None

def CreatePool():
    global connectionPool
    try:
        # Cria o pool com ThreadedConnectionPool
        connectionPool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            **DatabaseConfig
        )

        logger.debug("Pool de conexões Criado")

    except (Exception, psycopg2.DatabaseError):
        logger.exception("Erro ao criar pool de conexões")
        # em caso de erro retorna o pool como None
        connectionPool = None

# Função para listar todos os clientes
def GetClients(id):
    # Valida se existe um pool criado
    if not connectionPool:
        logger.error("Pool de Conexões não inicializado", exc_info=True)
        return CreateError(500, "Erro interno do servidor")

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error("Valor id em GetClients precisa ser uma string")
        return CreateError(400, "Formato inválido")

    conn = None
    cursor = None

    try:
        # Coleta a conexão
        conn = connectionPool.getconn()
        logger.debug("Conexão obtida do pool")

        cursor = conn.cursor()

        query = "SELECT clientId, nome, email, telefone, last_contact, status FROM contacts WHERE userId = %s"
        cursor.execute(query, (id,))

        results = cursor.fetchall()
        # Validação em caso de não existência de contatos
        if not results:
            return None

        # Cria uma lista com os clientes registrados e retorna como resposta
        # Lista já no formato aceito pelo frontend
        clientes = []

        for result in results:
            dateFrmt = result[4].strftime("%d-%m-%Y")

            data = {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "phone": result[3],
                "status": result[5],
                "last_contact": dateFrmt
            }

            clientes.append(data)

        return clientes

    except Exception:
        logger.error("Erro ao listar clientes para a página principal", exc_info=True)
        return None

    finally:
        if conn:
            if cursor:
                cursor.close()
            connectionPool.putconn(conn)
            logger.debug("Conexão devolvida ao pool")
        
