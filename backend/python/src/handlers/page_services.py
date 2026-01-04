import logging

from dotenv import load_dotenv

from src.models.header import AuthHeader
from ..errors.mainErrors import AppError, BadRequest



logger = logging.getLogger(__name__)
load_dotenv()

def set_service_header_params(req_data, scope):
    try:
        header = AuthHeader()
        header.header_handler(req_data, scope)
        
        controlers = header.header_services_control()
        return controlers

    except Exception:
        raise

class ServicesHandler:
    def __init__(self, req_data) -> None:
        self.req_data = req_data

    def list_services(self):
        try:
            controlers = set_service_header_params(self.req_data, 'read_services')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers')

            servicesControl = controlers.servicesControl
            AccessID = controlers.AccessID
            if not servicesControl:
                raise AppError(logger_message='Erro ao extrair instância servicesControl de controlers')

            offset = int(self.req_data.params.get('offset'))
            if offset < 0:
                raise BadRequest(logger_message='Offset Inválido')
            services_list = servicesControl.list_all_services(
                offset=offset,
                ID=AccessID
            )
            if not services_list:
                raise AppError(logger_message='Nenhum informação recebida de list_all_services')

            return services_list
        except Exception:
            raise

    def insert_service(self):
        try:
            controlers = set_service_header_params(self.req_data, 'write_services')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers', status=500)

            servicesControl = controlers.servicesControl
            if not servicesControl:
                raise AppError(logger_message='Erro ao extrair instância servicesControl de controlers', status=500)

            data = self.req_data.body
            if not data:
                raise BadRequest(
                    field='Payload',
                    logger_message='Payload incorreto ou vazio'
                 )

            insert = servicesControl.insert_new_service(data)
            if not insert:
                raise AppError(logger_message='Nenhuma informação recebida da função insert_new_service', status=500)

            return insert

        except Exception:
            raise

    def get_unique_service(self):
        try:
            controlers = set_service_header_params(self.req_data, 'read_services')
            if not controlers:
                raise AppError(logger_message='Erro ao definir controlers', status=500)

            servicesControl = controlers.servicesControl
            AccessID = controlers.AccessID
            if not servicesControl:
                raise AppError(logger_message='Erro ao extrair instância servicesControl de controlers', status=500)

            id = self.req_data.params.get('id')
            if not id:
                raise BadRequest(
                    field='id',
                    logger_message='Parâmetro ID não encontrado'
                )

            response = servicesControl.get_unique_service(
                serviceId=id,
                AccessID=AccessID
            )
            if not response:
                raise AppError(logger_message='Nenhum informação recebida de get_unique_service')
            return response
            
        except Exception:
            raise
