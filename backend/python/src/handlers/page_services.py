import logging

from dotenv import load_dotenv

from src.models.header import AuthHeader
from src.validation import errors


logger = logging.getLogger(__name__)
load_dotenv()

def error_maps(e):
    errors_list = {
        ValueError: (400, 'Formato Inválido'),
        PermissionError: (402, 'Permissão não encontrada'),
    }

    for errType, (status, message) in errors_list.items():
        if isinstance(e, errType):
            return errors.CreateError(status, message)

        return errors.CreateError(500, 'Erro inesperado')

def set_service_header_params(req_data, scope):
    try:
        header = AuthHeader()
        authorized = header.header_handler(req_data, scope)
        if isinstance(authorized, dict):
            return authorized
        
        controlers = header.header_services_control()
        return controlers

    except Exception as e:
        logger.exception('Erro com a função set_service_header_params')
        return error_maps(e)

class ServicesHandler:
    def __init__(self, req_data) -> None:
        self.req_data = req_data

    def list_services(self):
        try:
            controlers = set_service_header_params(self.req_data, 'read_services')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            servicesControl = controlers.servicesControl
            AccessID = controlers.AccessID
            if not servicesControl:
                raise ValueError

            offset = int(self.req_data.params.get('offset', 0))

            services_list = servicesControl.list_all_services(
                offset=offset,
                ID=AccessID
            )
            return services_list
        except Exception as e:
            logger.exception('Erro com a função list_services')
            return error_maps(e)

    def insert_service(self):
        try:
            controlers = set_service_header_params(self.req_data, 'write_services')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            servicesControl = controlers.servicesControl
            if not servicesControl:
                raise ValueError

            data = self.req_data.body
            if not data:
                raise ValueError

            insert = servicesControl.insert_new_service(data)
            if not insert:
                raise ValueError

            return insert

        except Exception as e:
            logger.exception('Erro com a função insert_service')
            return error_maps(e)

    def get_unique_service(self):
        try:
            controlers = set_service_header_params(self.req_data, 'read_services')
            if isinstance(controlers, dict):
                return controlers
            elif not controlers:
                raise ValueError

            servicesControl = controlers.servicesControl
            AccessID = controlers.AccessID
            if not servicesControl:
                raise ValueError

            id = self.req_data.params.get('id')
            if not id:
                raise ValueError

            response = servicesControl.get_unique_service(
                serviceId=id,
                AccessID=AccessID
            )
            return response
            
        except Exception as e:
            logger.exception('Erro com a função get_unique_service')
            return error_maps(e)
