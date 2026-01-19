from dataclasses import dataclass
import logging
from typing import Any

logger = logging.getLogger(__name__)

import logging

class AppError(Exception):
    default_code = 'APP_ERROR'
    default_message = 'Erro na Aplicação'
    default_logger_message = 'Erro interno'
    default_logger_level = logging.WARNING
    default_status = 500

    def __init__(self, message=None, logger_message=None, logger_level=None, status=None, code=None) -> None:
        self.message = message or self.default_message
        self.logger_message = logger_message or self.default_logger_message
        self.logger_level = logger_level or self.default_logger_level
        self.status = status or self.default_status
        self.code = code or self.default_code

        super().__init__(self.message)

@dataclass
class HandleException:
    error: Any # Classe Exception ou AppError

    code: Any | None = None
    status: Any | None = None
    message: Any | None = None

    def __post_init__(self):
        e = self.error

        if isinstance(e, AppError):
            if e.logger_level:
                logger.log(e.logger_level, str(e.logger_message), exc_info=e)

            self.code = e.code
            self.status = e.status
            self.message = e.message
            
        else:
            logger.exception('Erro Inesperado')
            self.code = 'INTERNAL_SERVER_ERROR'
            self.status = 500
            self.message = 'Erro Interno'

    def generate_data(self):
        data = {
            'message': self.message,
            'code': self.code
        }
        return data

class InvalidField(AppError):
    default_message = 'Campo inválido'
    default_logger_level = None
    default_logger_message = None

    default_code = 'INVALID_FIELD'
    default_status = 400

    def __init__(self, field=None, message=None):
        if message:
            final_message = message
        elif field:
            final_message = f'{field} inválido'
        else:
            final_message = self.default_message

        super().__init__(final_message)

class NullableField(AppError):
    default_message = 'Campo vazio'
    default_logger_level = None
    default_logger_message = None

    default_code = 'NULLABLE_FIELD'
    status = 400

    def __init__(self, field=None, message=None, logger_message=None, logger_level=None):
        if message:
            final_message = message
        elif field:
            final_message = f'{field} inválido'
        else:
            final_message = self.default_message

        self.logger_message = logger_message if logger_message is not None else self.default_logger_message
        self.logger_level = logger_level if logger_level is not None else self.default_logger_level

        super().__init__(final_message)

class BadRequest(AppError):
    default_message = 'Requisição inválida'
    default_logger_level = logging.ERROR
    default_logger_message = None

    default_code = 'BAD_REQUEST'
    status = 400

    def __init__(self, field=None, message=None, logger_message=None, logger_level=None) -> None:
        if message:
            final_message = message
        elif field:
            final_message = f'{field} inválido'
        else:
            final_message = self.default_message

        self.logger_message = logger_message if logger_message is not None else self.default_logger_message
                
        self.logger_level = logger_level if logger_level is not None else self.default_logger_level


        super().__init__(final_message)
