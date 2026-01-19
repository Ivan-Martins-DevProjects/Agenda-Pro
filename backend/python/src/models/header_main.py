from dataclasses import dataclass
import logging
from typing import Any

from src.errors.authErrors import UnauthorizedSession, UserNotPermited
from src.errors.mainErrors import AppError
from src.security.jwt import AuthServices

logger = logging.getLogger(__name__)
@dataclass
class AuthHeader:
    req_data: Any
    scope: str
    user: Any | None = None
    AccessID: Any | None = None

    def check_token(self):
        token = self.req_data.headers.get('Authorization')
        if not token:
            raise UnauthorizedSession('Sessão não encontrada')

        check = AuthServices(token)
        self.user = check.Autenticar()
        if not self.user:
            raise AppError(logger_message='Erro ao extrair classe User do token')

        return self.user

    def has_permission(self):
        if self.user == None:
            raise AppError(logger_message="Classe user não encontrada")

        permitted = self.user.is_permitted(self.scope)
        if permitted is False:
            raise UserNotPermited()

        self.AccessID = self.user.true_id()
        return self.AccessID
