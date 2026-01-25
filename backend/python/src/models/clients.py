import logging

from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel, EmailStr, field_validator

from src.errors.authErrors import UserNotPermited
from src.errors.clientsErrors import InaccessibleClient
from src.errors.mainErrors import AppError, InvalidField
from src.internal import database
from src.internal import clients_database as database
from src.internal.main_database import DatabasePool
from src.validation.checkTypes import isNumber

logger = logging.getLogger(__name__)
load_dotenv()


@dataclass
class ClientsControl:
    db_pool: DatabasePool
    role: str
    access_id: str 

    def __post_init__(self):
        if not self.db_pool:
            raise AppError(logger_message='Pool de conexões não inicializado')
        if not self.role:
            raise AppError(logger_message='Role não recebida')

    @property
    def params(self) -> tuple:
        return self.role, self.db_pool

class ClientsRepository(ClientsControl):
    def validate_user_from_contact(self, contactID):
        repo = database.GetContact(
            params=self.params
        )
        response = repo.get_unique_contact_db(
            contactId=contactID,
            id=self.access_id
        )
        if not response:
            raise InaccessibleClient()
        return True

    def list_all_clients_repo(self, offset):
        repo = database.ListClientsRepository(
            params=self.params
        )
        response = repo.get_clients_db(
            id=self.access_id,
            offset=offset
        )
        return response

    def search_clients_repo(self, text):
        repo = database.ListClientsRepository(
            params=self.params
        )
        response = repo.search_clients_db(
            user_id=self.access_id,
            text=text
        )
        return response

    def get_unique_contact_repo(self, client_id):
        repo = database.GetContact(
            params=self.params
        )
        response = repo.get_unique_contact_db(
            contactId=client_id,
            id=self.access_id
        )
        return response

    def insert_new_contact_repo(self, data):
        repo = database.InsertContact(
            params=self.params
        )
        response = repo.insert_new_contact_db(
            data=data
        )
        return response

    def update_contact_repo(self, client_id, data):
        repo = database.SetContact(
            params=self.params
        )
        response = repo.update_contact_db(
            id=client_id,
            body=data
        )
        return response

    def delete_contact_repo(self, client_id):
        repo = database.SetContact(
            params=self.params
        )
        response = repo.delete_contact_db(
            client_id=client_id
        )
        return response


class Clients(BaseModel):
    cpf: str | None = None
    nome: str
    userid: str
    telefone: str
    contactID: str | None = None
    email: EmailStr | None = None

    rua: str | None = None
    numero: int | None = 0
    bairro: str | None = None
    cidade: str | None = None

    gasto: int | None = 0
    visitas: int | None = 0

    obs: str | None = None

    @field_validator('telefone')
    @classmethod
    def check_telefone(cls, value):
        if isNumber(value) is False:
            raise InvalidField(field='Telefone')
        return value

# Classe responsável por criar e validar permissões do usuário
@dataclass
class User:
    ID: str
    Nome: str
    BussinesID: str
    Role: Any | None = None
    Instance: str | None = None
    IsConnected: str | None = None
    Permissions: dict | None = None
    
    def true_id(self):
        if self.Role == 'admin':
            return self.BussinesID
        else:
            return self.ID

    def is_permitted(self, scope):
        if scope not in self.Permissions:
            raise UserNotPermited()

        return True
