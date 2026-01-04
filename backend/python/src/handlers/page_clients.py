import logging
import uuid


from src.errors.mainErrors import AppError
from src.models.header import AuthHeader

logger = logging.getLogger(__name__)


def set_clients_header_params(req_data, scope):
    try:
        header = AuthHeader()
        header.header_handler(req_data, scope)
        
        controlers = header.header_client_services()
        return controlers

    except Exception:
        raise

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
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')

            offset = int(self.req_data.params.get('offset', 0))

            clients_list = clientsServices.get_all_clients(
                offset=offset,
                ID=AccessID
            )
            return clients_list
            
        except Exception:
            raise

    def get_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'read_contacts')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')

            clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )

            response = clientsServices.get_unique_contact(
                contactId=self.clientID,
                UserID=AccessID
            )
            return response

        except Exception:
            raise
           

    def insert_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'write_contacts')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')

            user = clientsServices.user
            if not user:
                raise AppError(logger_message='Erro ao extrair instância user de clientsServices')

            body = self.req_data.body
            contact_data = {
                "userid": str(user.ID),
                "respName": user.Nome,
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

            response = clientsServices.insert_new_contact(contact_data)
            return response

        except Exception:
            raise

    def update_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'write_contacts')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')
            
            user = clientsServices.user
            if not user:
                raise AppError(logger_message='Erro ao extrair instância user de clientsServices')

            clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )

            body = self.req_data.body
            data = {
                "userid": str(user.ID),
                "bussinesId": user.BussinesID,
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

        except Exception:
            raise

    def delete_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'delete_contact')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')

            clientsServices.validate_user_from_contact(
                contactID=self.clientID,
                ID=AccessID
            )

            response = clientsServices.delete_contact(self.clientID)
            return response

        except Exception:
            raise

    def search_contact(self):
        try:
            controlers = set_clients_header_params(self.req_data, 'read_contacts')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            clientsServices = controlers.clientsServices
            AccessID = controlers.AccessID
            if not clientsServices:
                raise AppError(logger_message='Erro ao extrair instância clientsServices de controlers')

            response = clientsServices.search_contact(
                id=AccessID,
                text=self.text
            )
            return response

        except Exception:
            raise
