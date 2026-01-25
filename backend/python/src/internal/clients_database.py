from datetime import datetime
import logging

from psycopg import sql
from psycopg.rows import dict_row

from src.internal.main_database import Repository
from src.errors.databaseErrors import databaseErrors

from src.errors.clientsErrors import ClientNotFound, DuplicateClientError
from src.errors.mainErrors import AppError, BadRequest

logger = logging.getLogger(__name__)

def IfNull(valor, default='N/A'):
    if not valor:
        return default

    return valor

class ListClientsRepository(Repository):
    def get_clients_db(self, id, offset):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("""SELECT clientId, nome, email, telefone, last_contact, status, resp_name
                    FROM contacts
                    WHERE {field} = %s LIMIT %s OFFSET %s""").format(field=self.role_column)
                    count = sql.SQL("SELECT COUNT(*) AS total FROM contacts WHERE {field} = %s").format(field=self.role_column)

                    cursor.execute(query, (id, 10, int(offset)))
                    results = cursor.fetchall()

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

    def search_clients_db(self, user_id, text):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    query = sql.SQL("""
                    SELECT 
                        c.clientid,
                        c.nome
                    FROM contacts c
                    LEFT JOIN contacts_address a ON a.clientid = c.clientid
                    WHERE c.{field} = %s
                    AND search ILIKE '%%' || %s || '%%';""").format(field=self.role_column)

                    cursor.execute(query, (user_id, text))
                    result = cursor.fetchall()

                    return result

        except Exception as e:
            raise databaseErrors(e)

class GetContact(Repository):
    def get_unique_contact_db(self, contactId, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    # Define a query e a executa
                    query = sql.SQL(''' SELECT c.nome, c.email, c.telefone, c.cpf, c.visitas, c.gasto, c.obs,
                                a.rua, a.bairro, a.cidade, a.numero FROM contacts c LEFT JOIN contacts_address a
                                on c.clientid = a.clientId WHERE c.clientid = %s AND c.{0} = %s
                                ''').format(self.role_column)

                    cursor.execute(query, (contactId, id))

                    # Retorna o resultado da query
                    result = cursor.fetchone()
                    if not result:
                        raise ClientNotFound()

                    return result

        # Registra qualquer erro com a consulta
        except Exception as e:
            raise databaseErrors(e)

class InsertContact(Repository):
    def insert_new_contact_db(self, data):
        # Valida se o id recebido é uma string
        id = data['userid']
        if not (id, str):
            raise BadRequest(field=id)

        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    contact_fields = [
                        'userid', 'contactID', 'nome', 'email', 'status',
                        'telefone', 'visitas', 'gasto', 'obs', 'respName',
                        'bussinesId', 'cpf'
                    ]
                    
                    info_values = tuple(data.get(field) for field in contact_fields)


                    # Define a query e a executa
                    queryContacts = """INSERT INTO contacts (
                        userid, clientid, nome, email, last_contact, status,
                        telefone, visitas, gasto, obs, resp_name, bussines_id, cpf
                    )
                    VALUES (
                        %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (telefone) DO NOTHING
                    RETURNING clientid;"""

                    cursor.execute(queryContacts, info_values)
                    resultContacts = cursor.fetchone()
                    if not resultContacts:
                        raise DuplicateClientError(message='Cliente já cadastrado!')
                    conn.commit()

                    adress_fields = [
                        'contactID', 'rua', 'bairro', 'cidade', 'numero'
                    ]
                    adress_values = tuple(data.get(field) for field in adress_fields)
                    
                    queryAdress = """
                    INSERT INTO contacts_address (
                        clientid, rua, bairro, cidade, numero
                    )
                    VALUES (
                        %s, %s, %s, %s, %s
                    );"""
                    cursor.execute(queryAdress, adress_values)
                    conn.commit()

                    contact = ', '.join(str(data.get(field, '')) for field in contact_fields)
                    address = ', '.join(str(data.get(field, '')) for field in adress_fields)
                    search = f'{contact}, {address}'.lower()
                    client_id = data.get('contactID')

                    query = "UPDATE contacts SET search = %s WHERE clientid = %s RETURNING clientid;"
                    cursor.execute(query, (search, client_id))
                    result = cursor.fetchone()
                    if not result:
                        raise AppError(logger_message='Erro ao inserir campo search')
                    conn.commit()

                    return 'Cliente cadastrado com sucesso!'

        # Registra qualquer erro com a consulta
        except Exception as e:
            return databaseErrors(e)

class SetContact(Repository):
    def delete_contact_db(self, client_id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query_1 = 'DELETE FROM contacts_address WHERE clientid = %s'
                    query_2 = 'DELETE FROM contacts WHERE clientid = %s'

                    cursor.execute(query_1, (client_id,))
                    conn.commit()
                    
                    cursor.execute(query_2, (client_id,))
                    conn.commit()
                    if cursor.rowcount <= 0:
                        raise AppError(message='Erro ao deletar contato da tabela contatos')

                    return 'Usuário excluído com sucesso'

        except Exception as e:
            raise databaseErrors(e)

    def update_contact_db(self, id, body):
        try:
            with self.db_pool.get_connection() as conn:
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
                    return 'Usuário atualizado com sucesso'

        except Exception as e:
            raise databaseErrors(e)
