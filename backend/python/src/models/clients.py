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
        clientes = database.GetClients(ID, Role, offset)
        return clientes


    def GetContact(self, ClientID, ID, Role):
        response = database.GetUniqueContact(
            contactId=ClientID,
            id=ID,
            role=Role
        )

        return response

    def NewContact(self, data):
        response = database.InsertNewContactDB(data)
        return response

    def UpdateContact(self, ContactID, data):
        response = database.UpdateContactDB(ContactID, data)
        return response

    def DeleteContact(self, id):
        response = database.DeleteContactDB(id)
        return response

    def SearchContact(self, id, text, role):
        response = database.SearchContactDB(
            id=id,
            text=text,
            role=role
        )
        return response

    def InsertNewContact(self, data):
        response = database.InsertNewContactDB(data)
        return response


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

    def validate_user_from_contact(self, contactID, ID):
        self.repo.GetContact(
            ClientID=contactID,
            ID=ID,
            Role=self.user.Role
        )

        return True

    def insert_new_contact(self, data):
        Clients(**data)
        response = self.repo.InsertNewContact(data)
        return response

    def get_all_clients(self, offset, ID):
        clients = self.repo.ListClients(
            offset=offset * 10,
            ID=ID,
            Role=self.user.Role
        )
        return {
            'data': clients
        }

    def get_unique_contact(self, contactId, UserID):
        response = self.repo.GetContact(
            ClientID=contactId,
            ID=UserID,
            Role=self.user.Role
        )
        return response

    def update_contact(self, contactID, data):
        Clients(**data)
        response = self.repo.UpdateContact(
            ContactID=contactID,
            data=data
        )
        return response

    def delete_contact(self, contactID):
        response = self.repo.DeleteContact(id=contactID)
        return response

    def search_contact(self,id, text):
        response = self.repo.SearchContact(
            id=id,
            text=text,
            role=self.user.Role
        )
        return response
