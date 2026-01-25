from dataclasses import dataclass
from typing import Any

from src.errors.mainErrors import AppError
from src.models.clients import User

@dataclass
class ControlHandler:
    req_ctx: Any

    @property
    def req_data(self) -> Any:
        return self.req_ctx.req_data

    @property
    def controler(self) -> Any:
        return self.req_ctx.controler

    @property
    def user(self) -> User:
        return self.req_ctx.user

    def __post_init__(self) -> None:
        if not self.req_ctx:
            raise AppError(logger_message='Contexto da requisição não recebido')
