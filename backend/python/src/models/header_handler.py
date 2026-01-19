import logging
from dataclasses import dataclass
from typing import Any

from src.errors.mainErrors import AppError
from src.models.clients import ClientsServices
from src.models.header_main import AuthHeader
from src.models.appointments import AppointmentsControl
from src.models.services import ServicesControl

logger = logging.getLogger(__name__)

@dataclass
class Header:
    req_data: Any
    scope: str
    controler: Any | None = None
    user: Any | None = None
    ID: Any | None = None
    
    def __post_init__(self):
        Auth = AuthHeader(self.req_data, self.scope)

        self.user = Auth.check_token()
        self.ID = Auth.has_permission()

@dataclass
class AppointmentsHeader(Header):
    def __post_init__(self):
        super().__post_init__()

        self.controler = AppointmentsControl(self.user)
        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")

@dataclass
class ServicesHeader(Header):
    def __post_init__(self):
        super().__post_init__()

        self.controler = ServicesControl(self.user)
        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")

@dataclass
class ClientsHeader(Header):
    def __post_init__(self):
        super().__post_init__()

        self.controler = ClientsServices(self.user)
        if not self.controler:
            raise AppError(logger_message="Erro ao gerar AppointmentsControl")
