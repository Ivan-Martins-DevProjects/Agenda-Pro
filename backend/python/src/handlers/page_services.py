import logging
import uuid
from dotenv import load_dotenv

from src.errors.mainErrors import AppError, BadRequest
from src.models.request import ControlHandler
from src.models.services import Services

logger = logging.getLogger(__name__)
load_dotenv()

class ListServices(ControlHandler):
    def list_all_services(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')
        services_list = self.controler.list_all_services_repo(
            offset=offset,
        )
        if not services_list:
            raise AppError(logger_message='Nenhum informação recebida de list_all_services')

        return services_list

class GetUniqueService(ControlHandler):
    def get_unique_service(self):
        id = self.req_data.params.get('id')
        if not id:
            raise BadRequest(field='ID')
        response = self.controler.get_unique_service_repo(
            serviceId=id,
        )
        if not response:
            raise AppError(logger_message='Nenhum informação recebida de get_unique_service')
        return response

class InsertNewService(ControlHandler):
    def insert_service(self):
        data = self.req_data.body
        if not data:
            raise BadRequest(field='Payload')

        data['userId'] = self.user.ID
        data['bussinesId'] = self.user.BussinesID
        data['respName'] = self.user.Nome
        data['id'] = uuid.uuid4()

        service = Services(**data)
        insert = self.controler.insert_new_service_control(service)
        if not insert:
            raise AppError(logger_message='Nenhuma informação recebida da função insert_new_service', status=500)

        return insert

class InsertNewServicebak(ControlHandler):
    def insert_service(self):
        data = self.req_data.body
        if not data:
            raise BadRequest(
                field='Payload',
                logger_message='Payload incorreto ou vazio'
             )

        insert = self.controler.insert_new_service_repo(data)
        if not insert:
            raise AppError(logger_message='Nenhuma informação recebida da função insert_new_service', status=500)

        return insert

class DeleteService(ControlHandler):
    def delete_service(self):
        id = self.req_data.params.get('id')
        if not id:
            raise BadRequest(
                field='ID',
                logger_message='Service ID não encontrado'
            )

        delete = self.controler.delete_service_control(id)
        return delete

class EditService(ControlHandler):
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

