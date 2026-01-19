from dataclasses import dataclass
from typing import Any
import logging
import uuid

from src.errors.mainErrors import AppError, BadRequest
from src.models.header import handle_header

logger = logging.getLogger(__name__)

@dataclass
class ClientsHandler:
    req_data: Any
    scope: str
    module: str
    client: Any | None = None
    controler: Any | None = None
    user: Any | None = None
    ID: Any | None = None

    def __post_init__(self):
        self.controler, self.ID = handle_header(self.req_data, self.scope, self.module)
        if not self.controler:
            raise AppError(logger_message='Erro ao extrair controlers de services')

        self.user = self.controler.user

class ListClients(ClientsHandler):
    def list_all_clients(self):
        offset = int(self.req_data.params.get('offset', 0))

        clients_list = self.controler.get_all_clients(
            offset=offset,
            ID=self.ID
        )
        return clients_list

    def get_unique_client(self):
        client_id = self.req_data.params.get('id')
        self.controler.validate_user_from_contact(
            contactID=client_id,
            ID=self.ID
        )

        response = self.controler.get_unique_contact(
            contactId=client_id,
            UserID=self.ID
        )
        return response

class InsertNewClient(ClientsHandler):
    def insert_contact(self):
        body = self.req_data.body
        user = self.user

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

        response = self.controler.insert_new_contact(contact_data)
        return response

class EditClient(ClientsHandler):
    def update_contact(self):
        client_id = self.req_data.params.get('id')
        if not client_id:
            raise BadRequest(field='Contato')

        self.controler.validate_user_from_contact(
            contactID=client_id,
            ID=self.ID
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

        response = self.controler.update_contact(client_id, data)
        return response

class DeleteClient(ClientsHandler):
    def delete_contact(self):
        client_id = self.req_data.params.get('id')
        if not client_id:
            raise BadRequest(field='Contato')
        self.controler.validate_user_from_contact(
            contactID=client_id,
            ID=self.ID
        )

        response = self.controler.delete_contact(client_id)
        return response
