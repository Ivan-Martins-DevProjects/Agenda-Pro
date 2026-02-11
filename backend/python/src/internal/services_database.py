import logging
from psycopg import sql
from psycopg.rows import dict_row

from src.errors.databaseErrors import databaseErrors 
from src.errors.mainErrors import AppError
from src.errors.servicesErrors import DuplicateServiceError, ServiceNotFound
from src.internal.main_database import Repository

logger = logging.getLogger(__name__)

class ListServicesRepository(Repository):
    def list_services_db(self, offset, id):
        if offset < 0:
            offset = 0

        offset = offset * 10

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

    def list_options_services_db(self, name, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    query =sql.SQL("""SELECT id, title, price, duration
                    FROM services
                    WHERE {field} = %s
                    AND title ILIKE '%%' || %s || '%%';""").format(field=self.role_column)
                    cursor.execute(query, (id, name))
                    services = cursor.fetchall()
                    
                    return services

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
                    query = """
                    INSERT INTO services (id, user_id, bussines_id, title, description, price, duration, resp_name)
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (title) DO NOTHING
                    RETURNING id
                    """

                    logger.debug(service.price)

                    cursor.execute(query, (
                        service.id, service.userId, service.bussinesId, service.title, service.description,
                        service.price, service.duration, service.respName
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


class EditService(Repository):
    def edit_service_db(self, service, userId):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("""
                    UPDATE services
                    SET title = %s,
                        description = %s,
                        price = %s,
                        duration = %s
                    WHERE id = %s AND {0} = %s
                    """).format(self.role_column)

                    title = service.title
                    description = service.description
                    price = service.price 
                    duration = service.duration
                    service_id = service.id

                    cursor.execute(query, (title, description, price, duration, service_id, userId))
                    conn.commit()
                    confirm = cursor.rowcount
                    if confirm < 0:
                        raise AppError(
                            message='Erro ao registrar alteração no serviço',
                            logger_message='edit_service_db não alterou nenhuma row'
                        )

                    return 'Serviço atualizado com sucesso'

        except Exception as e:
            raise databaseErrors(e)

class DeleteService(Repository):
    def delete_service_db(self, service_id, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("DELETE FROM services WHERE id = %s and {0} = %s").format(self.role_column)

                    cursor.execute(query, (service_id, id))
                    conn.commit()
                    if cursor.rowcount <= 0:
                        raise AppError(message='Você não tem autorização para excluir esse serviço')

                    response = 'Serviço excluído com sucesso'
                    return response

        except Exception as e:
            raise databaseErrors(e)
