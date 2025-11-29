import logging
from dotenv import load_dotenv

import os
import psycopg2
import psycopg2.pool
from psycopg2 import errors

from src.validation.errors import CreateResponse

from ..validation import CreateError
load_dotenv()

# Captura o nome do arquivo para registro dos logs
logger = logging.getLogger(__name__)

# Encapsulamento das credenciais do banco de dados Postgres
DatabaseConfig = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'port': os.getenv('DB_PORT'),
}

# Map de erros para um except mais bem tratado
DatabaseErrorMap = {
    errors.UniqueViolation:             (400, 'Registro duplicado'),
    errors.ForeignKeyViolation:         (400, 'Chave estrangeira inválida'),
    errors.NotNullViolation:            (400, 'Campo obrigatório faltando'),
    errors.CheckViolation:              (400, 'Violação de regra CHECK'),
    errors.NumericValueOutOfRange:      (400, 'Valor numérico fora do limite'),
    errors.InvalidTextRepresentation:   (400, 'Tipo de dado inválido'),
    errors.UndefinedColumn:             (400, 'Tipo de dado inválido')
}

# Função que lida com os exeptions, associando-os ao item relativo dentro do map de erros
def HandleExceptions(e):
    for errType, (status, message) in DatabaseErrorMap.items():
        if isinstance(e, errType):
            return CreateError(status, message)

    if isinstance(e, psycopg2.DatabaseError):
        return CreateError(500, 'Erro interno do servidor')

    return CreateError(500, 'Erro inesperado')

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

        logger.debug('Pool de conexões Criado')

    except (Exception, psycopg2.DatabaseError):
        logger.exception('Erro ao criar pool de conexões')
        # em caso de erro retorna o pool como None
        connectionPool = None

# Função responsável por checar as permissões do usuário
def CheckPermission(id, permission):
    # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error('Valor id em GetClients precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        # Obtém a conexão do pool de conexões
        conn = connectionPool.getconn()
        logger.debug('Conexão obtida do pool')
        
        cursor = conn.cursor()

        # Define a query e a executa
        query = f'SELECT {permission} FROM roles WHERE user_id = %s'
        cursor.execute(query, (id,))

        # Retorna o resultado da query
        result = cursor.fetchone()
        return CreateResponse(result)

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro ao checar permissão do usuário')
        return HandleExceptions(e)
    # Garante que o cursor foi fechado e a conexão devolvida ao pool
    finally:
        if conn:
            if cursor:
                cursor.close()
            connectionPool.putconn(conn)
            logger.debug('Conexão devolvida ao pool')

# Função para listar todos os clientes
def GetClients(id, role):
    # Valida se existe um pool criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error('Valor id em GetClients precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        # Coleta a conexão
        conn = connectionPool.getconn()
        logger.debug('Conexão obtida do pool')

        cursor = conn.cursor()

        query = 'SELECT clientId, nome, email, telefone, last_contact, status, resp_name FROM contacts WHERE userId = %s'

        if role == 'admin':
            query = 'SELECT clientId, nome, email, telefone, last_contact, status, resp_name FROM contacts WHERE bussines_id = %s'

        cursor.execute(query, (id,))

        results = cursor.fetchall()
        # Validação em caso de não existência de contatos
        if not results:
            return CreateError(404, 'Contato não encontrado')

        # Cria uma lista com os clientes registrados e retorna como resposta
        # Lista já no formato aceito pelo frontend
        clientes = []

        for result in results:
            dateFrmt = result[4].strftime('%d-%m-%Y')

            data = {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3],
                'status': result[5],
                'resp': result[6],
                'last_contact': dateFrmt
            }

            clientes.append(data)

        return clientes

    except Exception as e:
        logger.error('Erro com a função GetClients', exc_info=True)
        return HandleExceptions(e)

    finally:
        if conn:
            if cursor:
                cursor.close()
            connectionPool.putconn(conn)
            logger.debug('Conexão devolvida ao pool')

def GetUniqueContact(contactId, id, role):
    # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error('Valor id em GetClients precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        # Obtém a conexão do pool de conexões
        conn = connectionPool.getconn()
        logger.debug('Conexão obtida do pool')
        
        cursor = conn.cursor()

        # Define a query e a executa
        if role == 'admin':
            query = ''' SELECT c.nome, c.email, c.telefone, c.cpf, c.visitas, c.gasto, c.obs,
                        a.rua, a.bairro, a.cidade, a.numero FROM contacts c LEFT JOIN contacts_address a
                        on c.clientid = a.clientId WHERE c.clientid = %s AND c.bussines_id = %s'''
        else:
            query = ''' SELECT c.nome, c.email, c.telefone, c.cpf, c.visitas, c.gasto, c.obs,
                        a.rua, a.bairro, a.cidade, a.numero FROM contacts c LEFT JOIN contacts_address a
                        on c.clientid = a.clientId WHERE c.clientid = %s AND c.userid = %s'''

        cursor.execute(query, (contactId, id))

        # Retorna o resultado da query
        result = cursor.fetchall()
        if not result:
            return CreateError(404, 'Nenhum contato encontrado')

        def IfNull(valor, default='N/A'):
            if not valor:
                return default

            return valor


        data = {
            'nome': IfNull(result[0][0]),
            'email': IfNull(result[0][1]),
            'telefone': IfNull(result[0][2]),
            'cpf': IfNull(result[0][3]),
            'visitas': IfNull(result[0][4]),
            'gasto': f'R${IfNull(result[0][5])},00',
            'obs': IfNull(result[0][6]),
            'rua': IfNull(result[0][7]),
            'bairro': IfNull(result[0][8]),
            'cidade': IfNull(result[0][9]),
            'numero': IfNull(result[0][10]),
        }

        response = CreateResponse(data)

        return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro com a função GetUniqueContact')
        return HandleExceptions(e)

    # Garante que o cursor foi fechado e a conexão devolvida ao pool
    finally:
        if conn:
            if cursor:
                cursor.close()
            connectionPool.putconn(conn)
            logger.debug('Conexão devolvida ao pool')

        
def InsertNewContactDB(data):
     # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error('Valor id em InsertNewContactDB precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        # Obtém a conexão do pool de conexões
        conn = connectionPool.getconn()
        logger.debug('Conexão obtida do pool')
        
        cursor = conn.cursor()

        userid = data['userid']
        clientId = data['clientId']
        nome = data['nome']
        email = data['email']
        telefone = data['telefone']
        obs = data['obs']
        respName = data['respName']
        bussinesId = data['bussinesId']
        cpf = data['cpf']
        rua = data['rua']
        bairro = data['bairro']
        cidade = data['cidade']
        numero = data['numero']

        
        # Define a query e a executa
        queryContacts = """INSERT INTO contacts (
            userid,
            clientid,
            nome,
            email,
            status,
            telefone,
            visitas,
            gasto,
            obs,
            resp_name,
            bussines_id,
            cpf
        )
        VALUES (
            %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING ID;"""

        queryAdress = """
        INSERT INTO contacts_address (
            clientid,
            rua,
            bairro,
            cidade,
            numero
        )
        VALUES (
            %s, %s, %s, %s, %s
        );"""

        cursor.execute(queryContacts, (
            userid, clientId, nome, email, 'ativo', telefone, 0, 0, obs, respName, bussinesId, cpf,)
        )
        resultContacts = cursor.fetchone[0]
        if not resultContacts:
            return CreateError(500, 'Erro interno do servidor')

        cursor.execute(queryAdress, (
            clientId, rua, bairro, cidade, numero,)
        )

        data = {
            "id" : clientId
        }

        response = CreateResponse(data)

        return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro com a função GetUniqueContact')
        return HandleExceptions(e)

    # Garante que o cursor foi fechado e a conexão devolvida ao pool
    finally:
        if conn:
            if cursor:
                cursor.close()
            connectionPool.putconn(conn)
            logger.debug('Conexão devolvida ao pool')

   
