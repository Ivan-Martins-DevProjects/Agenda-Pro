from functools import cached_property
import logging
from dataclasses import dataclass
from typing import Any

from src.errors.mainErrors import AppError
from src.internal.main_database import DatabasePool
from src.models.clients import ClientsRepository
from src.models.header_main import AuthHeader
from src.models.appointments import AppointmentsControl, AppointmentsRepository
from src.models.services import ServicesRepository

logger = logging.getLogger(__name__)

@dataclass
class Header:
    req_data: Any
    scope: str
    db_pool: DatabasePool
    controler: Any | None = None
    
    @cached_property
    def _auth(self) -> Any:
        return AuthHeader(self.req_data, self.scope)

    @cached_property
    def user(self) -> Any:
        return self._auth.check_token(self.db_pool)

    @cached_property
    def access_id(self) -> str:
        return self._auth.has_permission()

@dataclass
class AppointmentsHeader(Header):
    def __post_init__(self):
        self.controler = AppointmentsRepository(
            db_pool=self.db_pool,
            role=self.user.Role,
            access_id=self.access_id
        )
        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")

@dataclass
class ServicesHeader(Header):
    def __post_init__(self):
        self.controler = ServicesRepository(
            db_pool=self.db_pool,
            role=self.user.Role,
            access_id=self.access_id
        )
        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")

@dataclass
class ClientsHeader(Header):
    def __post_init__(self):
        self.controler = ClientsRepository(
            db_pool=self.db_pool,
            role=self.user.Role,
            access_id=self.access_id,
        )

        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")
