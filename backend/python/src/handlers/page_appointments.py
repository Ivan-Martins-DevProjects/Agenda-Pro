from dataclasses import dataclass
from typing import Any
import logging

from dotenv import load_dotenv

from src.errors.mainErrors import AppError, BadRequest
from src.models.header import handle_header

logger = logging.getLogger(__name__)
load_dotenv()

@dataclass
class AppointmentsHandler:
    req_data: Any
    scope: str
    module: str
    controler: Any | None = None
    ID: Any | None = None

    def __post_init__(self):
        self.controler, self.ID = handle_header(self.req_data, self.scope, self.module)
        if not self.controler:
            raise AppError(logger_message='Erro ao extrair controlers de appointments')

class ListAppointments(AppointmentsHandler):
    def list_all_appointments(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        appointments_list = self.controler.list_all_appointments(offset)
        if not appointments_list:
            raise AppError(logger_message='Nenhum informação recebida de list_all_appointments')

        return appointments_list

    def list_filter_appointments(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        filter_value = self.req_data.params.get('value')
        if not filter_value:
            raise BadRequest(logger_message='Parâmetros incompletos')

        appointments_list = self.controler.list_filter_appointments(
            offset=offset,
            filter=filter_value
        )
        if not appointments_list:
            raise AppError(logger_message='Nenhum informação recebida de list_filter_appointments')

        return appointments_list

class GetUniqueAppointment(AppointmentsHandler):
     def get_unique_appointment(self):
         appointment_id = self.req_data.params.get('id')
         if not appointment_id:
             raise BadRequest(field='ID')

         response = self.controler.get_unique_appointment(appointment_id)
         if not response:
             raise AppError(logger_message='Nenhum informação recebida de get_unique_appointment')

         return response
