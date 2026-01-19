import logging
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv

from src.errors.mainErrors import AppError, BadRequest
from src.models.header import handle_header

logger = logging.getLogger(__name__)
load_dotenv()

@dataclass
class ServicesHandler:
    req_data: Any
    scope: str
    module: str
    controler: Any | None = None
    ID: Any | None = None

    def __post_init__(self):
        self.controler, self.ID = handle_header(self.req_data, self.scope, self.module)
        if not self.controler:
            raise AppError(logger_message='Erro ao extrair controlers de services')

class ListServices(ServicesHandler):
    def list_services(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        services_list = self.controler.list_all_services_control(
            offset=offset,
            ID=self.ID
        )
        if not services_list:
            raise AppError(logger_message='Nenhum informação recebida de list_all_services')

        return services_list

class GetUniqueService(ServicesHandler):
    def get_unique_service(self):
        id = self.req_data.params.get('id')
        if not id:
            raise BadRequest(
                field='id',
                logger_message='Parâmetro ID não encontrado'
            )

        response = self.controler.get_unique_service_control(
            serviceId=id,
            AccessID=self.ID
        )
        if not response:
            raise AppError(logger_message='Nenhum informação recebida de get_unique_service')
        return response

class InsertNewService(ServicesHandler):
    def insert_service(self):
        data = self.req_data.body
        if not data:
            raise BadRequest(
                field='Payload',
                logger_message='Payload incorreto ou vazio'
             )

        insert = self.controler.insert_new_service_control(data)
        if not insert:
            raise AppError(logger_message='Nenhuma informação recebida da função insert_new_service', status=500)

        return insert

class DeleteService(ServicesHandler):
    def delete_service(self):
        id = self.req_data.params.get('id')
        if not id:
            raise BadRequest(
                field='ID',
                logger_message='Service ID não encontrado'
            )

        delete = self.controler.delete_service_control(id)
        return delete

class EditService(ServicesHandler):
    def edit_service(self):
        id = self.req_data.params.get('id')
        if not id:
            raise BadRequest(
                field='id',
                logger_message='Parâmetro ID não encontrado'
            )

        body = self.req_data.body
        if not body:
            raise BadRequest(
                field='Payload',
                logger_message=f'Payload incorreto ou vazio: {body}'
            )

        response = self.controler.edit_service_control(
            serviceId=id,
            data=body
        )
        if not response:
            raise AppError(logger_message='Nenhum informação recebida de get_unique_service')

        return response

