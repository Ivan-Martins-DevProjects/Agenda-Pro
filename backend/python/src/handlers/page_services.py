import logging

from dotenv import load_dotenv

from src.models import services
from src.models.header import AuthHeader
from src.security import jwt
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
        logger.error('Erro com a função set_service_header_params', exc_info=True)
        return error_maps(e)

def list_services(req_data):
    try:
        controlers = set_service_header_params(req_data, 'read_services')
        if isinstance(controlers, dict):
            return controlers
        elif not controlers:
            raise ValueError

        servicesControl = controlers.servicesControl
        AccessID = controlers.AccessID
        if not servicesControl:
            raise ValueError

        offset = int(req_data.params.get('offset', 0))

        services_list = servicesControl.list_all_services(
            offset=offset,
            ID=AccessID
        )
        return services_list
    except Exception as e:
        logger.error('Erro com a função list_services')
        return error_maps(e)
