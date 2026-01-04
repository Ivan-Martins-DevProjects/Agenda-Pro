from flask import message_flashed
from .mainErrors import AppError

import logging
import jwt

def jwtErrors(e):
    maps = {
        jwt.ExpiredSignatureError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com assinatura expirada'),
        jwt.InvalidSignatureError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com assinatura inválida'),
        jwt.InvalidTokenError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com token inválido'),
        jwt.DecodeError: lambda: UnauthorizedSession(logger_message='Erro ao verificar sessão')
    }

    for errType, funcError in maps.items():
        if isinstance(e, errType):
            raise funcError()

    raise AppError(logger_level=logging.DEBUG)

class UnauthorizedSession(AppError):
    code = 'UNAUTHORIZED_SESSION'
    default_message = 'Sessão não autorizada'
    status = 401

    default_logger_message = None
    default_logger_level = None

    def __init__(self, message=None, logger_message=None, logger_level=None) -> None:
        self.message = message or self.default_message
        self.logger_message = logger_message if logger_message is not None else self.default_logger_message
        self.logger_level = logger_level if logger_level is not None else self.default_logger_level

        super().__init__(message=message, status=self.status)

class UserNotPermited(AppError):
    code = 'UNAUTHORIZED_USER'
    message = 'Usuário não autorizado'
    status = 403
