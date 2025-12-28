import logging
import jwt
import os

from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, field_validator

from src.validation import errors
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

    def services_errors(self, e):
        error_list = {
            ValidationError: (400, 'Requisição inválida')
        }

        for errType, (status, message) in error_list.items():
            if isinstance(e, errType):
                return errors.CreateError(status, message)

        return errors.CreateError(500, 'Erro inesperado do servidro')


class AuthServices:
    def __init__(self, JWT) -> None:
        self.token = JWT
        self.secret = os.getenv("JWT_KEY")
        self.ErrorMap = {
            jwt.ExpiredSignatureError: (401, 'Sessão expirada'),
            jwt.InvalidSignatureError: (409, 'Erro ao verificar sessão'),
            jwt.InvalidTokenError: (401, 'Sessão inválida'),
            jwt.DecodeError: (401, 'Erro ao verificar sessão'),
            ValueError: (401, 'Sessão inválida'),
        }

    def JwtErrors(self, e):
        for errType, (status, message) in self.ErrorMap.items():
            if isinstance(e, errType):
                return errors.CreateError(status, message)

        return errors.CreateError(500, 'Erro ao autenticar')

    def Autenticar(self):
        if not self.secret:
            logger.error('Token JWT não encontrado')
            return errors.CreateError(401, 'Sessão não encontrada')

        try:
            payload = jwt.decode(
               self.token ,
                self.secret,
                algorithms=['HS256']
            )

            if not payload:
                logger.error('Erro ao decodificar payload')
                return errors.CreateError(401, 'Erro ao autenticar')

            ID = payload['ID']
            BussinesID = payload['BussinesID']
            Nome = payload['Nome']
            Instance = payload['Instance']
            IsConnected = payload['IsConnected']
            Role =  payload['Role']

            permissions = database.RequestPermissionsDB(ID)

            if permissions['status'] == 'error':
                return permissions

            Usuario = User(ID, BussinesID, Nome, Instance, IsConnected, Role, permissions['data'])
            return Usuario

        except Exception as e:
            logger.exception('Erro ao validar token JWT')
            return self.JwtErrors(e)

class ClientsRepository:
    def ListClients(self, offset, ID, Role):
        # Busca os clientes referentes a role do usuário no banco de dados
        clientes = database.GetClients(ID, Role, offset)

        return clientes

    def GetContact(self, ClientID, ID, Role):
        response = database.GetUniqueContact(
            contactId= ClientID,
            id= ID,
            role= Role
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
            raise ValueError('Telefone Inválido')
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
    Permissions: Optional[str] = None
    
    def set_scope(self, scope):
        if scope not in self.Permissions:
            return errors.CreateError(401, 'Usuário não autorizado')
        return None

    def true_id(self):
        if self.Role == 'admin':
            return self.BussinesID
        else:
            return self.ID

    def is_permitted(self, scope):
        if scope not in self.Permissions:
            return errors.CreateError(409, 'Usuário não autorizado')

        return True

class UserServices:
    def __init__(self, User) -> None:
        self.user = User
        self.repo = ClientsRepository()
        self.services = ServiceLayer()

    def grant_access(self, scope):
        ID = self.user.true_id(self.user)
        checkScope = self.user.set_scope(scope)
        if checkScope is not None:
            return checkScope

        return ID

    def validate_user_from_contact(self, contactID, ID):
        response = self.repo.GetContact(
            ClientID=contactID,
            ID=ID,
            Role=self.user.Role
        )
        if response['status'] == 'error':
            return response

        return True

    def insert_new_contact(self, data):
        try:
            Clients(**data)
            response = self.repo.InsertNewContact(data)
        except Exception as e:
            logger.error('Payload da função insert_new_contact mal formatado', exc_info=True)
            return self.services.services_errors(e)

        response = self.repo.InsertNewContact(data)
        return response

    def get_all_clients(self, offset, ID):
        clients = self.repo.ListClients(
            offset=offset * 10,
            ID=ID,
            Role=self.user.Role
        )
        return errors.CreateResponse(clients, 200)

    def get_unique_contact(self, contactId, UserID):
        response = self.repo.GetContact(
            ClientID=contactId,
            ID=UserID,
            Role=self.user.Role
        )
        return response

    def update_contact(self, contactID, data):
        try:
            Clients(**data)
        except Exception as e:
            logger.error('erro ao validar body recebido na função update_contact', exc_info=True)
            return self.services.services_errors(e)

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
