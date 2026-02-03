from datetime import datetime
import logging
from psycopg import sql
from psycopg.rows import dict_row

from src.errors.mainErrors import AppError, BadRequest
from src.internal.main_database import Repository
from src.errors.databaseErrors import databaseErrors

logger = logging.getLogger(__name__)

class ListAppointmentsRepository(Repository):
    def list_all_appointments_db(self, offset, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    offset = offset * 10

                    query = sql.SQL("""
                    SELECT id, client_id, client_name, user_name, service_name, date, time_begin, status, price, duration
                    FROM appointments
                    WHERE {field} = %s
                    LIMIT %s OFFSET %s
                    """).format(field=self.role_column)

                    count = sql.SQL("SELECT COUNT(*) AS total FROM appointments WHERE {field} = %s").format(field=self.role_column)

                    cursor.execute(query, (id, 10, int(offset)))
                    results = cursor.fetchall()
                    if not results:
                        return {
                        'total': 0,
                        'appointments': []
                        }

                    cursor.execute(count, (id,))
                    count_query = cursor.fetchone()
                    if not count_query:
                        total = 0
                    else:
                        total = count_query['total']

                    appointments_list = []
                    for result in results:
                        result['date'] = result['date'].isoformat()
                        result['time_begin'] = result['time_begin'].isoformat()[:5]
                        appointments_list.append(result)

                    data = {
                        'appointments': appointments_list,
                        'total': total
                    }

                    return data

        except Exception as e:
            raise databaseErrors(e)
            

    def list_filter_appointments_db(self, offset, id, field_type, field):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    column_name = sql.SQL(field_type)
                    field = field.lower()

                    query = sql.SQL("""
                    SELECT id, client_id, client_name, user_name, service_name, date, time_begin, status, price, duration
                    FROM appointments
                    WHERE {0} = %s
                    AND {1} = %s
                    LIMIT %s OFFSET %s
                    """).format(self.role_column, column_name)

                    count = sql.SQL(
                "SELECT COUNT(*) AS total FROM appointments WHERE {0} = %s AND {1} = %s"
                    ).format(self.role_column, column_name)

                    cursor.execute(query, (id, field, 10, int(offset)))
                    results = cursor.fetchall()
                    if not results:
                        return {
                        'total': 0,
                        'appointments': []
                        }

                    cursor.execute(count, (id, field.lower()))
                    count_query = cursor.fetchone()
                    if not count_query:
                        total = 0
                    else:
                        total = count_query['total']

                    appointments_list = []
                    for result in results:
                        result['date'] = result['date'].isoformat()
                        result['time_begin'] = result['time_begin'].isoformat()[:5]
                        appointments_list.append(result)

                    data = {
                        'appointments': appointments_list,
                        'total': total
                    }

                    return data

        except Exception as e:
            raise databaseErrors(e)


    def list_filter_time_appointments_db(self, offset, id, date_value):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    interval = sql.SQL(date_value)
                    if date_value == 'day':
                        where_value = sql.SQL("""
                                            date >= date_trunc({type_field}, CURRENT_DATE)
                                            AND date < date_trunc({type_field}, CURRENT_DATE) + INTERVAL '1 {interval}'
                                            """).format(
                                                type_field=date_value,
                                                interval=interval
                                            )
                    else:
                        where_value = sql.SQL("""
                                            date >= date_trunc({type_field}, CURRENT_DATE)
                                            AND date < date_trunc({type_field}, CURRENT_DATE) + INTERVAL '1 {interval}'
                                            """).format(
                                                type_field=date_value,
                                                interval=interval
                                            )

                    query = sql.SQL("""
                    SELECT id, client_id, client_name, user_name, service_name, date, time_begin, status, price, duration
                    FROM appointments
                    WHERE {0} = %s
                    AND {1}
                    ORDER BY date, time_begin
                    LIMIT %s OFFSET %s
                    """).format(self.role_column, where_value)

                    count = sql.SQL(
                "SELECT COUNT(*) AS total FROM appointments WHERE {0} = %s AND {1}"
                    ).format(self.role_column, where_value)

                    # logger.debug(count.as_string(conn))
                    cursor.execute(query, (id, 10, int(offset)))
                    results = cursor.fetchall()
                    if not results:
                        return {
                        'total': 0,
                        'appointments': []
                        }

                    cursor.execute(count, (id,))
                    count_query = cursor.fetchone()
                    if not count_query:
                        total = 0
                    else:
                        total = count_query['total']

                    appointments_list = []
                    for result in results:
                        result['date'] = result['date'].isoformat()
                        result['time_begin'] = result['time_begin'].isoformat()[:5]
                        appointments_list.append(result)

                    data = {
                        'appointments': appointments_list,
                        'total': total
                    }

                    return data

        except Exception as e:
            raise databaseErrors(e)

class GetUniqueAppointmentRepository(Repository):
    def get_unique_appointment_db(self, appointment_id, user_id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    query = sql.SQL("""
                    SELECT id, client_name, user_name, service_name, date, time_begin, status, price, status, obs
                    FROM appointments
                    WHERE {0} = %s
                    AND id = %s
                    """).format(self.role_column)

                    # logger.debug(count.as_string(conn))
                    cursor.execute(query, (user_id, appointment_id))
                    result = cursor.fetchone()
                    if not result:
                        raise BadRequest(message='Nao foi possivel concluir a operaçao')

                    raw_date = result['date'] = result['date'].isoformat()
                    date_obj = datetime.fromisoformat(raw_date)
                    formated_date = date_obj.strftime('%d-%m-%Y')
                    formated_time = result['time_begin'] = result['time_begin'].isoformat()[:5] if result['time_begin'] else None

                    data = {
                        'name': result['client_name'],
                        'service': result['service_name'],
                        'raw_date': raw_date,
                        'date': formated_date,
                        'hour': formated_time,
                        'price': int(result['price']) / 100,
                        'status': result['status'].title(),
                        'obs': result['obs']
                    }

                    return data

        except Exception as e:
            raise databaseErrors(e)

class DeleteAppointmentRepository(Repository):
    def delete_appointment_db(self, appointment_id, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("DELETE FROM appointments WHERE id = %s and {0} = %s").format(self.role_column)

                    cursor.execute(query, (appointment_id, id))
                    conn.commit()
                    if cursor.rowcount <= 0:
                        raise AppError(message='Erro ao deletar usuário')

                    response = 'Agendamento excluído com sucesso'
                    return response

        except Exception as e:
            raise databaseErrors(e)

class UpdateAppointmentRepository(Repository):
    def update_appointment_status_db(self, appointment_id, status, id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = sql.SQL("UPDATE appointments SET status = %s WHERE id = %s and {0} = %s RETURNING id").format(self.role_column)

                    cursor.execute(query, (status, appointment_id, id))
                    updated = cursor.fetchone()
                    if not updated:
                        raise AppError(message='Agendamento não encontrado', status=404)

                    conn.commit()

                    response = 'Status do agendamento atualizado com sucesso'
                    return response

        except Exception as e:
            raise databaseErrors(e)
