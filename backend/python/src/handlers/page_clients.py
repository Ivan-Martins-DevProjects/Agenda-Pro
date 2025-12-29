import logging
import uuid

from src.models.header import AuthHeader
from src.validation import errors

logger = logging.getLogger(__name__)


def error_maps(e):
    error_list = {
        ValueError: (400, 'Formato Inválido'),
        PermissionError: (402, 'Permissão não encontrada'),
    }

    for errType, (status, message) in error_list.items():
        if isinstance(e, errType):
            return errors.CreateError(status, message)
    return errors.CreateError(500, 'Erro inesperado')

def set_clients_header_params(req_data, scope):
    try:
        header = AuthHeader()
        authorized = header.header_handler(req_data, scope)
        if isinstance(authorized, dict):
            return authorized

        controlers = header.header_client_services()
        return controlers
    except Exception as e:
        logger.error('Erro com a função set_clients_header_params', exc_info=True)
        return error_maps(e)

class ClientsHandler:
    def __init__(
        self,
        req_data,
        clientID = None,
        text = None
    ) -> None:
        self.req_data = req_data
        self.clientID = clientID
        self.text = text

    def list_contacts(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'read_contacts')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise ValueError

            offset = int(self.req_data.params.get('offset', 0))

            clients_list = clientsServices.get_all_clients(
                offset=offset,
                ID=AccessID
            )
            return clients_list
            
        except Exception as e:
            logger.error('Erro com a função list_contacts', exc_info=True)
            return error_maps(e)

    def get_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'read_contacts')
            if isinstance(controlers, dict):
                return controlers

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise ValueError

            CheckUserFromContact = clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )
            if isinstance(CheckUserFromContact, dict):
                return CheckUserFromContact

            response = clientsServices.get_unique_contact(
                contactId=self.clientID,
                UserID=AccessID
            )
            return response

        except Exception as e:
            logger.error('Erro com a função get_contact', exc_info=True)
            return error_maps(e)

           

    def insert_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'write_contacts')
            if isinstance(controlers, dict):
                return controlers

            clientsServices = controlers.clientsServices
            if not clientsServices:
                raise ValueError

            user = clientsServices.user
            if not user:
                raise ValueError

            body = self.req_data.body
            contact_data = {
                "userid": str(user.ID),
                "bussinesId": user.BussinesID,
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

            clientsServices.insert_new_contact(contact_data)

        except Exception as e:
            logger.error(f'Erro com a função insert_contact', exc_info=True)
            return error_maps(e)

    def update_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'write_contacts')
            if isinstance(controlers, dict):
                return controlers

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise ValueError
            
            user = clientsServices.user
            if not user:
                raise ValueError

            CheckUserFromContact = clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )
            if isinstance(CheckUserFromContact, dict):
                return CheckUserFromContact

            body = self.req_data.body
            data = {
                "userid": str(user.ID),
                "bussinesId": user.BussinesID,
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

            response = clientsServices.update_contact(self.clientID, data)
            return response

        except Exception as e:
            logger.error('Erro com a função update_contact', exc_info=True)
            return error_maps(e)

    def delete_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'delete_contact')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise ValueError

            CheckUserFromContact = clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )
            if isinstance(CheckUserFromContact, dict):
                return CheckUserFromContact

            response = clientsServices.delete_contact(self.clientID)
            return response
        except Exception as e:
            logger.error('Erro com a função delete_contact', exc_info=True)
            return error_maps(e)

    def search_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'read_contacts')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise ValueError

            response = clientsServices.search_contact(
                id=AccessID,
                text=self.text
            )
            return response

        except Exception as e:
            logger.error('Erro com a função search_contact', exc_info=True)
            return error_maps(e)
