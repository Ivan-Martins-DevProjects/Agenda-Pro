import logging

from dotenv import load_dotenv

from src.errors.mainErrors import AppError, BadRequest
from src.models.header import AuthHeader


logger = logging.getLogger(__name__)
load_dotenv()

def set_appointments_header_params(req_data, scope):
    header = AuthHeader()
    header.header_handler(req_data, scope)

    controlers = header.header_appointments_control()
    return controlers

class AppointmentsHandler:
    def __init__(self,  req_data):
        self.req_data = req_data

    def list_appointments(self):
        controlers = set_appointments_header_params(self.req_data, 'read_appointments')
        if not controlers:
            raise AppError(logger_message='Erro ao definir controlers')

        appointmentsControl = controlers.appointmentsControl
        if not appointmentsControl:
            raise AppError(logger_message='Erro ao extrair instância servicesControl de controlers')

        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        appointments_list = appointmentsControl.list_all_appointments(offset)
        if not appointments_list:
            raise AppError(logger_message='Nenhum informação recebida de list_all_services')

        return appointments_list
