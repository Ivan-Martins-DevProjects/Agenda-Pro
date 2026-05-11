import logging

from dataclasses import dataclass

from typing import Any

from psycopg import sql
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.errors.mainErrors import AppError, BadRequest
from src.errors.databaseErrors import databaseErrors

logger = logging.getLogger(__name__)


@dataclass
class DatabasePool:
    conninfo: Any
    min_size: int = 1
    max_size: int = 10
    pool: Any | None = None

    def __post_init__(self):
        try:
            # Cria o pool com ThreadedConnectionPool
            self.pool = ConnectionPool(
                conninfo=self.conninfo,
                min_size=self.min_size,
                max_size=self.max_size,
            )
            logger.debug('Pool de conexões Criado')

        except Exception as e:
            self.pool = None
            raise databaseErrors(e)

    def get_connection(self):
        if not self.pool:
            raise AppError(logger_message='Pool de conexões não inicializado')

        return self.pool.connection()

@dataclass
class Repository:
    params: tuple

    @property
    def db_pool(self):
        return self.params[1]

    @property
    def role(self):
        return self.params[0]

    @property
    def role_column(self):
        if self.role == 'admin':
            return sql.Identifier('bussines_id')
        elif self.role == 'user':
            return sql.Identifier('user_id')
        else:
            raise BadRequest(field='Role')

class RoleRepository(Repository):
    def get_permissions_by_user_id(self, user_id):
        try:
            with self.db_pool.get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    # Define a query e a executa
                    query = 'SELECT * FROM roles WHERE user_id = %s'
                    cursor.execute(query, (user_id,))

                    # Retorna o resultado da query
                    result = cursor.fetchone()
                    return result

        # Registra qualquer erro com a consulta
        except Exception as e:
            raise databaseErrors(e)

