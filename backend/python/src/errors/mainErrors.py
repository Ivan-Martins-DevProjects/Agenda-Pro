import logging

logger = logging.getLogger(__name__)

import logging

class AppError(Exception):
    code = 'APP_ERROR'
    default_message = 'Erro na Aplicação'
    default_logger_message = 'Erro interno'
    default_logger_level = logging.WARNING
    default_status = 500

    def __init__(self, message=None, logger_message=None, logger_level=None, status=None) -> None:
        self.message = message or self.default_message
        self.logger_message = logger_message or self.default_logger_message
        self.logger_level = logger_level or self.default_logger_level
        self.status = status or self.default_status

        super().__init__(self.message)

def handle_exception(e: Exception):
    if isinstance(e, AppError):
        if e.logger_level:
            logger.log(e.logger_level, str(e.logger_message), exc_info=e)

        return {
            'error': e.message,
            'code': e.code,
            'status': e.status
        }

    else:
        logger.exception('Erro insesperado')
        return {
            'error': 'Erro interno',
            'status': 500
        }

class InvalidField(AppError):
    default_message = 'Campo inválido'
    default_logger_level = None
    default_logger_message = None

    code = 'INVALID_FIELD'
    status = 400

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

    code = 'NULLABLE_FIELD'
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

    code = 'BAD_REQUEST'
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
