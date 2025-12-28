import logging
import uuid

from flask import request
from pydantic import ValidationError

from src.requests import request_data
from src.security import auth
from src.validation import errors
from src.models import clients

logger = logging.getLogger(__name__)


def error_maps(e):
    error_list = {
        ValueError: (400, 'Erro com a requisição'),
    }

    for errType, (status, message) in error_list.items():
        if isinstance(e, errType):
            return errors.CreateError(status, message)
    return errors.CreateError(500, 'Erro inesperado')

class AuthHeader:
    def __init__(self, userServices = None, AccessID = None) -> None:
        self.UserServices = userServices
        self.AccessID = AccessID

    @classmethod
    def HeaderHandler(cls, req_data, scope):
        token = req_data.headers.get('Authorization')
        if not token:
            error = errors.CreateError(401, 'Sessão não encontrada')
            raise ValueError

        check = clients.AuthServices(token)
        user = check.Autenticar()
        if isinstance(user, dict):
            return user

        hasPermission = user.is_permitted(scope)
        if hasPermission is False:
            raise PermissionError('Usuário não autorizado')
        elif isinstance(hasPermission, dict):
            raise PermissionError(hasPermission['message'])

        userServices = clients.UserServices(user)
        AccessID = user.true_id()
        return cls(userServices, AccessID)


def list_contacts(req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'read_contacts')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        AccessID = authorized.AccessID
        if not userServices:
            raise ValueError

        offset = int(req_data.params.get('offset', 0))

        clients_list = userServices.get_all_clients(
            offset=offset,
            ID=AccessID
        )
        return clients_list
        
    except Exception as e:
        logger.error('Erro com a função list_contacts', exc_info=True)
        return error_maps(e)

def get_contact(contactId, req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'read_contacts')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        AccessID = authorized.AccessID
        if not userServices:
            raise ValueError

        CheckUserFromContact = userServices.validate_user_from_contact(
            contactID=contactId,
            ID=AccessID
        )
        if isinstance(CheckUserFromContact, dict):
            return CheckUserFromContact

        response = userServices.get_unique_contact(
            contactId=contactId,
            UserID=AccessID
        )
        return response

    except Exception as e:
        logger.error('Erro com a função get_contact', exc_info=True)
        return error_maps(e)

       

def insert_contact(req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'write_contacts')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        if not userServices:
            raise ValueError

        body = req_data.body
        contact_data = {
            "userid": str(userServices.user.ID),
            "bussinesId": userServices.user.BussinesID,
            "contactID": str(uuid.uuid4()),
            "nome": body.get('nome'),
            "email": body.get('email'),
            "telefone": body.get('telefone'),
            "obs": body.get('obs'),
            "cpf": body.get('cpf'),
            "rua": body.get('rua'),
            "numero": body.get('numero'),
            "bairro": body.get('bairro'),
            "cidade": body.get('cidade'),
            "gasto": body.get('gasto'),
            "visitas": body.get('visitas'),
        }

        userServices.insert_new_contact(contact_data)

    except Exception as e:
        logger.error(f'Erro com a função insert_contact', exc_info=True)
        return error_maps(e)

def update_contact(id, req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'write_contacts')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        AccessID = authorized.AccessID
        if not userServices:
            raise ValueError

        CheckUserFromContact = userServices.validate_user_from_contact(
            contactID=id,
            ID=AccessID
        )
        if isinstance(CheckUserFromContact, dict):
            return CheckUserFromContact

        body = req_data.body
        data = {
            "userid": str(userServices.user.ID),
            "bussinesId": userServices.user.BussinesID,
            "contactID": str(uuid.uuid4()),
            "nome": body.get('nome'),
            "email": body.get('email'),
            "telefone": body.get('telefone'),
            "obs": body.get('obs'),
            "cpf": body.get('cpf'),
            "rua": body.get('rua'),
            "numero": body.get('numero'),
            "bairro": body.get('bairro'),
            "cidade": body.get('cidade'),
            "gasto": body.get('gasto'),
            "visitas": body.get('visitas'),
        }

        response = userServices.update_contact(id, data)
        return response

    except Exception as e:
        logger.error('Erro com a função update_contact', exc_info=True)
        return error_maps(e)

def delete_contact(id, req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'delete_contact')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        AccessID = authorized.AccessID
        if not userServices:
            raise ValueError

        CheckUserFromContact = userServices.validate_user_from_contact(
            contactID=id,
            ID=AccessID
        )
        if isinstance(CheckUserFromContact, dict):
            return CheckUserFromContact

        response = userServices.delete_contact(id)
        return response
    except Exception as e:
        logger.error('Erro com a função delete_contact', exc_info=True)
        return error_maps(e)

def search_contact(text, req_data):
    try:
        authorized = AuthHeader.HeaderHandler(req_data, 'read_contacts')
        if isinstance(authorized, dict):
            return authorized

        userServices = authorized.UserServices
        AccessID = authorized.AccessID
        if not userServices:
            raise ValueError

        response = userServices.search_contact(
            id=AccessID,
            text=text
        )
        return response

    except Exception as e:
        logger.error('Erro com a função search_contact', exc_info=True)
        return error_maps(e)
