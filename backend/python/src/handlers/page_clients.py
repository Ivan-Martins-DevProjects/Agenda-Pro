import logging
import uuid

from src.errors.mainErrors import AppError, BadRequest
from src.models.request import ControlHandler

logger = logging.getLogger(__name__)

class ListClients(ControlHandler):
    def list_all_clients(self):
        offset = int(self.req_data.params.get('offset', 0))

        clients_list = self.controler.list_all_clients_repo(
            offset=offset
        )
        return clients_list

    def search_clients(self):
        text = self.req_data.params.get('text')

        clients = self.controler.search_clients_repo(
            text=text
        )
        return clients

class GetUniqueClient(ControlHandler):
    def get_unique_client(self):
        client_id = self.req_data.params.get('id')
        self.controler.validate_user_from_contact(
            contactID=client_id
        )

        response = self.controler.get_unique_contact_repo(
            client_id=client_id
        )
        return response

class InsertNewClient(ControlHandler):
    def insert_client(self):
        body = self.req_data.body
        user = self.user

        contact_data = {
            "userid": str(user.ID),
            "respName": user.Nome,
            "bussinesId": user.BussinesID,
            "contactID": str(uuid.uuid4()),
            "status": "ativo",
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

        response = self.controler.insert_new_contact_repo(contact_data)
        return response

class EditClient(ControlHandler):
    def update_contact(self):
        client_id = self.req_data.params.get('id')
        if not client_id:
            raise BadRequest(field='Contato')

        self.controler.validate_user_from_contact(
            contactID=client_id
        )

        body = self.req_data.body
        user = self.user
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

        response = self.controler.update_contact_repo(client_id, data)
        return response

class DeleteClient(ControlHandler):
    def delete_contact(self):
        client_id = self.req_data.params.get('id')
        if not client_id:
            raise BadRequest(field='ID do Contato')

        self.controler.validate_user_from_contact(
            contactID=client_id
        )

        response = self.controler.delete_contact_repo(client_id)
        return response
