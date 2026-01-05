import logging
from datetime import datetime
from dotenv import load_dotenv

import os
from psycopg import sql
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from ..errors.databaseErrors import databaseErrors
from ..errors.clientsErrors import ClientNotFound, DuplicateClientError
from ..errors.mainErrors import AppError, InvalidField, handle_exception
from ..errors.servicesErrors import DuplicateServiceError, ServiceNotFound

load_dotenv()

# Captura o nome do arquivo para registro dos logs
logger = logging.getLogger(__name__)

# Encapsulamento das credenciais do banco de dados Postgres
DatabaseConfig = os.getenv('POSTGRES_URL', 'postgres')

def IfNull(valor, default='N/A'):
    if not valor:
        return default

    return valor

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

    except Exception as e:
        # em caso de erro retorna o pool como None
        connectionPool = None
        raise databaseErrors(e)

def RequestPermissionsDB(id):
    # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        raise InvalidField('id')

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
            # Obtém a conexão do pool de conexões
                logger.debug('RequestPermissionsDB Acionado')

                # Define a query e a executa
                query = 'SELECT * FROM roles WHERE user_id = %s'
                cursor.execute(query, (id,))

                # Retorna o resultado da query
                result = cursor.fetchone()
                return result

    # Registra qualquer erro com a consulta
    except Exception as e:
        raise databaseErrors(e)

# Função para listar todos os clientes
def GetClients(id, role, offset):
    # Valida se existe um pool criado
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        raise InvalidField('ID do cliente')

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                # Coleta a conexão
                if role == 'admin':
                    query ="""SELECT clientId, nome, email, telefone, last_contact, status, resp_name
                FROM contacts
                WHERE bussines_id = %s LIMIT %s OFFSET %s"""
                    count = "SELECT COUNT(*) AS total FROM contacts WHERE bussines_id = %s"
                elif role == 'user':
                    query = """SELECT clientId, nome, email, telefone, last_contact, status, resp_name
                    FROM contacts
                    WHERE userid = %s LIMIT %s OFFSET %s"""
                    count = "SELECT COUNT(*) AS total FROM contacts WHERE userid = %s"

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
        raise databaseErrors(e)


def GetUniqueContact(contactId, id, role):
    # Valida se o Pool de Conexões foi criado
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )
    # Valida se o id recebido é uma string
    if not isinstance(id, str):
        raise InvalidField(field='id')

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
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
                    raise ClientNotFound()

                response = {
                    'data': result
                }
                return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        raise databaseErrors(e)
        
def InsertNewContactDB(data):
     # Valida se o Pool de Conexões foi criado
    if not connectionPool:
         raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    # Valida se o id recebido é uma string
    id = data['userid']
    if not (id, str):
        raise InvalidField(field=id)

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
                    raise DuplicateClientError(message=resultContacts)

                conn.commit()

                cursor.execute(queryAdress, (
                    clientId, rua, bairro, cidade, numero,)
                )
                conn.commit()

                data = {
                    "id" : clientId
                }

                response = {
                    'data': data
                }

                return response

    # Registra qualquer erro com a consulta
    except Exception as e:
        return handle_exception(e)

def UpdateContactDB(id, body):
    if not connectionPool:
         raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    if not isinstance(id, str):
        raise InvalidField(field=id)
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
                    raise DuplicateClientError()

                conn.commit()
                return {
                    'data': 'Usuário cadastrado com sucesso',
                }

    except Exception as e:
        raise databaseErrors(e)

def DeleteContactDB(id):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    if not isinstance(id, str):
        raise InvalidField(field=id)

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                query_1 = 'DELETE FROM contacts_address WHERE clientid = %s'
                query_2 = 'DELETE FROM contacts WHERE clientid = %s'

                cursor.execute(query_1, (id,))
                conn.commit()
                
                cursor.execute(query_2, (id,))
                conn.commit()
                if cursor.rowcount <= 0:
                    raise AppError(message='Erro ao deletar contato da tabela contatos')

                data = {
                    'data': 'Usuário excluído com sucesso'
                }
                return data

    except Exception as e:
        raise databaseErrors(e)



def SearchContactDB(id, text, role):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    if not isinstance(id, str):
        raise InvalidField(field=id)

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
                            OR c.email ILIKE '%%' || %s || '%%'
                            OR c.cpf ILIKE '%%' || %s || '%%'
                            OR c.telefone ILIKE '%%' || %s || '%%'
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
                            OR c.email ILIKE '%%' || %s || '%%'
                            OR c.cpf ILIKE '%%' || %s || '%%'
                            OR c.telefone ILIKE '%%' || %s || '%%'
                            OR a.rua ILIKE '%%' || %s || '%%'
                            OR a.bairro ILIKE '%%' || %s || '%%'
                            OR a.cidade ILIKE '%%' || %s || '%%'
                            OR a.numero::text ILIKE '%%' || %s || '%%'
                      );
                """

                cursor.execute(query, (id, text, text, text, text, text, text, text, text))
                result = cursor.fetchall()

                if not result:
                    return {
                        'data': []
                    }

                return {
                    'data': result
                }

    except Exception as e:
        raise databaseErrors(e)
#############################################################################

def list_services_db(offset, id, role):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    conn = None
    cursor = None

    offset = offset - 1
    if offset < 0:
        offset = 0

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if role == 'admin':
                    query ="""SELECT id, title, description, price, duration
                FROM services
                WHERE bussines_id = %s LIMIT %s OFFSET %s"""
                    count = "SELECT COUNT(*) AS total FROM services WHERE bussines_id = %s"
                elif role == 'user':
                    query = """SELECT id, title, description, price, duration
                    FROM services
                    WHERE userid = %s LIMIT %s OFFSET %s"""
                    count = "SELECT COUNT(*) AS total FROM services WHERE userid = %s"

                cursor.execute(query, (id, 10, int(offset)))
                services = cursor.fetchall()

                response = {
                    'total': 0,
                    'services': []
                }
                if not services:
                    return {
                        'data': response
                    }

                cursor.execute(count, (id,))
                count_query = cursor.fetchone()
                if not count_query:
                    total = 0
                else:
                    total = count_query['total']

                services_list= []
                for result in services:
                    services_list.append(result)

                data = {
                    'services': services_list,
                    'total': total
                }

                return {
                    'data': data
                }

    except Exception as e:
        return databaseErrors(e)

def insert_service_db(data):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                userId = data['userId']
                bussinesId = data['bussinesId']
                id = data['id']
                respName = data['respName']
                title = data['title']
                description = data['description']
                Unpackprice = int(data['price'])
                price = int(Unpackprice * 10)
                duration = data.get('duration')

                query = """
                INSERT INTO services (id, user_id, bussines_id, title, description, price, duration, resp_name)
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (title) DO NOTHING
                RETURNING id
                """

                cursor.execute(query, (id, userId, bussinesId, title, description, price, duration, respName))

                result = cursor.fetchone()
                if not result:
                    raise DuplicateServiceError()

                conn.commit()

                response = {
                    'data': result[0]
                }
                return response

    except Exception as e:
        raise databaseErrors(e)

def delete_service(serviceId):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor() as cursor:
                query = """DELETE FROM services WHERE id = %s"""

                cursor.execute(query, (serviceId,))
                conn.commit()
                if cursor.rowcount <= 0:
                    raise AppError(message='Erro ao deletar usuário')

                response = 'Usuário excluído com sucesso'
                return response

    except Exception as e:
        raise databaseErrors(e)


def get_unique_service_db(serviceId, AccessID, role):
    if not connectionPool:
        raise AppError(
            status=500,
            logger_message='Pool de conexões não inicializado'
        )

    conn = None
    cursor = None

    try:
        with connectionPool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                if role == 'admin':
                    query = """
                    SELECT title, description, price, duration FROM services
                    WHERE id = %s AND bussines_id = %s
                    """
                else:
                    query = """
                    SELECT title, description, price, duration FROM services
                    WHERE id = %s AND user_id = %s
                    """

                cursor.execute(query, (serviceId, AccessID))
                result = cursor.fetchone()
                if not result:
                    raise ServiceNotFound()

                return {
                    'data': result
                }

    except Exception as e:
        raise databaseErrors(e)
