from .mainErrors import AppError, InvalidField

from psycopg import errors
import logging

def databaseErrors(e):
    maps = {
        errors.UniqueViolation:             lambda: InvalidField(message='Usuário já cadastrado'),
        errors.ForeignKeyViolation:         lambda: AppError(logger_message='Chave estrangeira inválida', logger_level=logging.error),
        errors.NotNullViolation:            lambda: AppError(logger_message='Campo obrigatório faltando', logger_level=logging.error),
        errors.NumericValueOutOfRange:      lambda: AppError(logger_message='Valor numérico fora de range', logger_level=logging.error),
        errors.InvalidTextRepresentation:   lambda: AppError(logger_message='Tipo de valor inválido', logger_level=logging.error),
        errors.UndefinedColumn:             lambda: AppError(logger_message='Coluna indefinida', logger_level=logging.error)
}

    for errType, funcType in maps.items():
        if isinstance(e, errType):
            raise funcType()
        elif isinstance(e, AppError):
            raise e

    raise AppError(logger_message='Erro interno do servidor', logger_level=logging.error)
