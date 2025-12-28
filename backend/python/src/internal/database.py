from datetime import datetime
import logging
from dotenv import load_dotenv

import os
import psycopg
from psycopg import errors, sql
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from ..validation import CreateError, CreateResponse
load_dotenv()

# Captura o nome do arquivo para registro dos logs
logger = logging.getLogger(__name__)

# Encapsulamento das credenciais do banco de dados Postgres
DatabaseConfig = os.getenv('POSTGRES_URL', 'postgres')

# Map de erros para um except mais bem tratado
DatabaseErrorMap = {
    errors.UniqueViolation:             (409, 'Usuário já cadastrado'),
    errors.ForeignKeyViolation:         (400, 'Chave estrangeira inválida'),
    errors.NotNullViolation:            (400, 'Campo obrigatório faltando'),
    errors.CheckViolation:              (400, 'Violação de regra CHECK'),
    errors.NumericValueOutOfRange:      (400, 'Valor numérico fora do limite'),
    errors.InvalidTextRepresentation:   (400, 'Tipo de dado inválido'),
    errors.UndefinedColumn:             (400, 'Tipo de dado inválido')
}

def IfNull(valor, default='N/A'):
    if not valor:
        return default

    return valor

# Função que lida com os exeptions, associando-os ao item relativo dentro do map de erros
def HandleExceptions(e):
    for errType, (status, message) in DatabaseErrorMap.items():
        if isinstance(e, errType):
            return  CreateError(status, message)

    if isinstance(e, psycopg.DatabaseError):
        return  CreateError(500, 'Erro interno do servidor')

    return  CreateError(500, 'Erro inesperado')

# Inicializa uma variável global para o pool de conexões
connectionPool = None

def CreatePool():
    global connectionPool
    try:
        # Cria o pool com ThreadedConnectionPool
        connectionPool = ConnectionPool(
            conninfo=DatabaseConfig,
            min_size=1,
            max_size=10,
        )

        logger.debug('Pool de conexões Criado')

    except (Exception, psycopg.DatabaseError):
        logger.exception('Erro ao criar pool de conexões')
        # em caso de erro retorna o pool como None
        connectionPool = None

def RequestPermissionsDB(id):
    # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        logger.error('Valor id em CheckPermission precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
            # Obtém a conexão do pool de conexões
                logger.debug('Conexão obtida do pool')

                # Define a query e a executa
                query = 'SELECT * FROM roles WHERE user_id = %s'
                cursor.execute(query, (id,))

                # Retorna o resultado da query
                result = cursor.fetchone()
                return CreateResponse(result, 200)

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro ao checar permissão do usuário')
        return HandleExceptions(e)

# Função para listar todos os clientes
def GetClients(id, role, offset):
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
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                # Coleta a conexão
                logger.debug('Conexão obtida do pool')

                query = """SELECT clientId, nome, email, telefone, last_contact, status, resp_name
                FROM contacts
                WHERE userid = %s LIMIT %s OFFSET %s"""
                count = "SELECT COUNT(*) AS total FROM contacts WHERE userid = %s"

                if role == 'admin':
                    query ="""SELECT clientId, nome, email, telefone, last_contact, status, resp_name
                FROM contacts
                WHERE bussines_id = %s LIMIT %s OFFSET %s"""
                    count = "SELECT COUNT(*) AS total FROM contacts WHERE bussines_id = %s"

                cursor.execute(query, (id, 10, int(offset)))
                results:list = cursor.fetchall()

                clientes: list[dict] = []

                response = {
                    'total': 0,
                    'clientes': []
                }

                # Validação em caso de não existência de contatos
                if not results:
                    return response
                # Cria uma lista com os clientes registrados e retorna como resposta
                # Lista já no formato aceito pelo frontend
                chaves = [
                    'id', 'name', 'email', 'phone', 'last_contact','status', 'resp'
                ]


                for result in results:
                    data = {}
                    for i, chave in enumerate(chaves):
                        valor = IfNull(result[i])
                        if chave == 'last_contact' and isinstance(valor, datetime):
                            valor = valor.strftime('%d-%m-%Y')
                        data[chave] = valor
               
                    clientes.append(data)

                cursor.execute(count, (id,))
                count_query = cursor.fetchone()
                if not count_query:
                    total = 0
                else:
                    total = count_query[0]

                response = {
                    'total': total,
                    'clientes': clientes
                }

                return response

    except Exception as e:
        logger.error('Erro com a função GetClients', exc_info=True)
        return HandleExceptions(e)


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
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                # Obtém a conexão do pool de conexões
                logger.debug('Conexão obtida do pool')
                
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
                result = cursor.fetchone()
                if not result:
                    return CreateError(404, 'Nenhum contato encontrado')

                response = CreateResponse(result, 200)

                return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro com a função GetUniqueContact')
        return HandleExceptions(e)

        
def InsertNewContactDB(data):
     # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    # Valida se o id recebido é uma string
    if not isinstance(data['userid'], str):
        logger.error('Valor id em InsertNewContactDB precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                logger.debug('Conexão obtida do pool')
                
                userid = data['userid']
                clientId = data['contactID']
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
                    last_contact,
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
                    %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (telefone) DO NOTHING
                RETURNING clientid;"""

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
                resultContacts = cursor.fetchone()

                if not resultContacts:
                    logger.error('Usuário já cadastrado')
                    return CreateError(409, 'Usuário já cadastrado')
                conn.commit()

                cursor.execute(queryAdress, (
                    clientId, rua, bairro, cidade, numero,)
                )
                conn.commit()

                data = {
                    "id" : clientId
                }

                response = CreateResponse(200, data)

                return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        logger.exception('Erro com a função GetUniqueContact')
        return HandleExceptions(e)

def UpdateContactDB(id, body):
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    if not isinstance(id, str):
        logger.error('Valor id em UpdateContactDB precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                Contacts = [
                    'telefone', 'cpf', 'nome', 'gasto', 'email', 'visitas'
                ]
                data = {
                    key : value
                    for key, value in body.items() if key in Contacts
                }
                    
                values = tuple( value for value in data.values())
                assignments = [
                    sql.SQL('{0} = {1}').format(sql.Identifier(key), sql.Placeholder())
                    for key in data.keys()
                ]
                fields = sql.SQL(', ').join(assignments)

                query = sql.SQL('UPDATE contacts SET {fields} WHERE clientid = %s RETURNING clientid').format(
                    fields=fields
                )
                cursor.execute(query, values + (id,))

                results = cursor.fetchone()
                if not results:
                    logger.info('Usuário já cadastrado')
                    return CreateError(409, 'Outro usuário já possui essas informações')

                conn.commit()
                return CreateResponse(201, 'Usuário atualizado com sucesso')

    except Exception as e:
        logger.error('Erro com a função UpdateContactDB', exc_info=True)
        return HandleExceptions(e)

def DeleteContactDB(id):
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    if not isinstance(id, str):
        logger.error('Valor id em InsertNewContactDB precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                query_1 = 'DELETE FROM contacts_address WHERE clientid = %s'
                query_2 = 'DELETE FROM contacts WHERE clientid = %s'

                cursor.execute(query_1, (id,))
                conn.commit()
                
                cursor.execute(query_2, (id,))
                conn.commit()
                if cursor.rowcount <=0:
                    logger.error('Erro ao deletar contato da tabela contatos')
                    return CreateError(500, 'Erro interno do servidor')

                return CreateResponse(200, 'Usuário excluído com sucesso')

    except Exception as e:
        logger.exception('Erro com a função DeleteContactDB')
        return HandleExceptions(e)



def SearchContactDB(id, text, role):
    if not connectionPool:
        logger.error('Pool de Conexões não inicializado', exc_info=True)
        return CreateError(500, 'Erro interno do servidor')

    if not isinstance(id, str):
        logger.error('Valor id em InsertNewContactDB precisa ser uma string')
        return CreateError(400, 'Formato inválido')

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if role == 'admin':
                    query = """
                    SELECT 
                        c.clientid,
                        c.nome
                    FROM contacts c
                    LEFT JOIN contacts_address a ON a.clientid = c.clientid
                    WHERE c.bussines_id = %s
                      AND (
                            c.nome ILIKE '%%' || %s || '%%'
                         OR a.rua ILIKE '%%' || %s || '%%'
                         OR a.bairro ILIKE '%%' || %s || '%%'
                         OR a.cidade ILIKE '%%' || %s || '%%'
                         OR a.numero::text ILIKE '%%' || %s || '%%'
                      );
                """
                else:
                    query = """
                    SELECT 
                        c.clientid,
                        c.nome
                    FROM contacts c
                    LEFT JOIN contacts_address a ON a.clientid = c.clientid
                    WHERE c.userid = %s
                      AND (
                            c.nome ILIKE '%%' || %s || '%%'
                         OR a.rua ILIKE '%%' || %s || '%%'
                         OR a.bairro ILIKE '%%' || %s || '%%'
                         OR a.cidade ILIKE '%%' || %s || '%%'
                         OR a.numero::text ILIKE '%%' || %s || '%%'
                      );
                """

                cursor.execute(query, (id, text, text, text, text, text))
                result = cursor.fetchall()

                if not result:
                    return CreateResponse([], 200)

                return CreateResponse(result, 200)

    except Exception as e:
        logger.exception('Erro ao buscar termo de pesquisa na função SearchContactDB')
        return HandleExceptions(e)

