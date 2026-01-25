from psycopg import sql
from psycopg.rows import dict_row

from src.errors.databaseErrors import databaseErrors 
from src.errors.servicesErrors import DuplicateServiceError, ServiceNotFound
from src.internal.main_database import Repository

class ListServicesRepository(Repository):
    def list_services_db(self, offset, id):
        offset = offset - 1
        if offset < 0:
            offset = 0

        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    query =sql.SQL("""SELECT id, title, description, price, duration
                FROM services
                WHERE {field} = %s LIMIT %s OFFSET %s""").format(field=self.role_column)
                    count = sql.SQL(
                        "SELECT COUNT (*) AS total FROM services WHERE {field} = %s"
                    ).format(field=self.role_column)
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
            raise databaseErrors(e)

class GetService(Repository):
    def get_unique_service_db(self, service_id, user_id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    query = sql.SQL("""
                    SELECT title, description, price, duration FROM services
                    WHERE id = %s AND {field} = %s
                    """).format(field=self.role_column)

                    cursor.execute(query, (service_id, user_id))
                    result = cursor.fetchone()
                    if not result:
                        raise ServiceNotFound()

                    return {
                        'data': result
                    }

        except Exception as e:
            raise databaseErrors(e)

class InsertNewService(Repository):
    def insert_service_db(self, service):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    Unpackprice = service.price
                    price = int(Unpackprice * 10)

                    query = """
                    INSERT INTO services (id, user_id, bussines_id, title, description, price, duration, resp_name)
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (title) DO NOTHING
                    RETURNING id
                    """

                    cursor.execute(query, (
                        service.id, service.bussinesId, service.title, service.description,
                        price, service.duration, service.respName
                    ))

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

class SetContact(Repository):
    def delete_service(self, serviceId):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """DELETE FROM services WHERE id = %s"""

                    cursor.execute(query, (serviceId,))
                    conn.commit()
                    if cursor.rowcount <= 0:
                        raise AppError(message='Erro ao deletar serviço')

                    response = 'Usuário excluído com sucesso'
                    return response

        except Exception as e:
            raise databaseErrors(e)
