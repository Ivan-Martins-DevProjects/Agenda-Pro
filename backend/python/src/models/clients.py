import logging

from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from src.errors.authErrors import UserNotPermited
from src.errors.mainErrors import InvalidField
from src.internal import database
from src.validation.checkTypes import isNumber

logger = logging.getLogger(__name__)
load_dotenv()

class ServiceLayer:
    def set_response(self, data):
        if data['status'] == 'error':
            logger.error(data['message'])
            return data

        return data

    def validate_user(self, contactID, userID, role):
        response = database.GetUniqueContact(contactID, userID, role)
        return response


class ClientsRepository:
    def ListClients(self, offset, ID, Role):
        # Busca os clientes referentes a role do usuário no banco de dados
        try:
            clientes = database.GetClients(ID, Role, offset)
            return clientes

        except Exception:
            raise

    def GetContact(self, ClientID, ID, Role):
        try:
            response = database.GetUniqueContact(
                contactId=ClientID,
                id=ID,
                role=Role
            )

            return response
        except Exception:
            raise

    def NewContact(self, data):
        try:
            response = database.InsertNewContactDB(data)
            return response
        except Exception:
            raise

    def UpdateContact(self, ContactID, data):
        try:
            response = database.UpdateContactDB(ContactID, data)
            return response
        except Exception:
            raise

    def DeleteContact(self, id):
        try:
            response = database.DeleteContactDB(id)
            return response
        except Exception:
            raise

    def SearchContact(self, id, text, role):
        try:
            response = database.SearchContactDB(
                id=id,
                text=text,
                role=role
            )
            return response
        except Exception:
            raise

    def InsertNewContact(self, data):
        try:
            response = database.InsertNewContactDB(data)
            return response
        except Exception:
            raise


class Clients(BaseModel):
    userid: str
    contactID: Optional[str] = None
    nome: str
    email: Optional[EmailStr] = None
    telefone: str
    cpf: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[int] = 0
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    gasto: Optional[int] = 0
    visitas: Optional[int] = 0
    obs: Optional[str] = None

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
    BussinesID: str
    Nome: str
    Instance: Optional[str] = None
    IsConnected: Optional[str] = None
    Role: Optional[str] = None
    Permissions: Optional[dict] = None
    
    def true_id(self):
        if self.Role == 'admin':
            return self.BussinesID
        else:
            return self.ID

    def is_permitted(self, scope):
        if scope not in self.Permissions:
            raise UserNotPermited()

        return True

class ClientsServices:
    def __init__(self, User) -> None:
        self.user = User
        self.repo = ClientsRepository()
        self.services = ServiceLayer()

    def grant_access(self, scope):
        try:
            ID = self.user.true_id()
            self.user.is_permitted(scope)

            return ID
        except Exception:
            raise

    def validate_user_from_contact(self, contactID, ID):
        try:
            self.repo.GetContact(
                ClientID=contactID,
                ID=ID,
                Role=self.user.Role
            )

            return True
        except Exception:
            raise

    def insert_new_contact(self, data):
        try:
            Clients(**data)
            response = self.repo.InsertNewContact(data)
            return response
        except Exception:
            raise

    def get_all_clients(self, offset, ID):
        try:
            clients = self.repo.ListClients(
                offset=offset * 10,
                ID=ID,
                Role=self.user.Role
            )
            return {
                'data': clients
            }

        except Exception:
            raise


    def get_unique_contact(self, contactId, UserID):
        try:
            response = self.repo.GetContact(
                ClientID=contactId,
                ID=UserID,
                Role=self.user.Role
            )
            return response
        except Exception:
            raise

    def update_contact(self, contactID, data):
        try:
            Clients(**data)
            response = self.repo.UpdateContact(
                ContactID=contactID,
                data=data
            )
            return response

        except Exception:
            raise

    def delete_contact(self, contactID):
        try:
            response = self.repo.DeleteContact(id=contactID)
            return response
        except Exception:
            raise

    def search_contact(self,id, text):
        try:
            response = self.repo.SearchContact(
                id=id,
                text=text,
                role=self.user.Role
            )
            return response
        except Exception:
            raise
