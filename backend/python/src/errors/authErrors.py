from .mainErrors import AppError

import logging
import jwt

def jwtErrors(e):
    maps = {
        jwt.ExpiredSignatureError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com assinatura expirada', status=401),
        jwt.InvalidSignatureError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com assinatura inválida', status=401),
        jwt.InvalidTokenError: lambda: UnauthorizedSession(logger_message='Tentativa de acesso com token inválido', status=401),
        jwt.DecodeError: lambda: UnauthorizedSession(logger_message='Erro ao verificar sessão', status=401),
    }

    for errType, funcError in maps.items():
        if isinstance(e, errType):
            raise funcError()

    raise AppError(logger_level=logging.DEBUG)

class UnauthorizedSession(AppError):
    code = 'UNAUTHORIZED_SESSION'
    message = 'Sessão não autorizada'
    status = 401

class UserNotPermited(AppError):
    code = 'UNAUTHORIZED_USER'
    message = 'Usuário não autorizado'
    status = 403
