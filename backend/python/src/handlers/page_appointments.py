import logging

from src.errors.mainErrors import AppError, BadRequest
from src.models.request import ControlHandler

logger = logging.getLogger(__name__)

class ListAppointments(ControlHandler):
    def list_all_appointments(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        appointments_list = self.controler.list_all_appointments_repo(offset) 
        if not appointments_list:
            raise AppError(logger_message='Nenhum informação recebida de list_all_appointments')

        return appointments_list

    def list_filter_appointments(self):
        offset = int(self.req_data.params.get('offset'))
        if offset < 0:
            raise BadRequest(logger_message='Offset Inválido')

        filter_value = self.req_data.params.get('value')
        if not filter_value:
            raise BadRequest(message='Parâmetros incompletos')

        filter_type = self.req_data.params.get('filterType')
        if not filter_type:
            raise BadRequest(message='Parâmetros incompletos')

        appointments_list = None

        if filter_type == 'status':
            appointments_list = self.controler.list_filter_appointments_repo(
                offset=offset,
                field_type=filter_type,
                field=filter_value
            )
        elif filter_type == 'date':
            filter = {
                'hoje': 'day',
                'semana': 'week',
                'mes': 'month'
            }
            for k, v in filter.items():
                if k == filter_value:
                    appointments_list = self.controler.list_filter_time_appointments_repo(
                        offset=offset,
                        date_value=v
                    )
        else:
            raise BadRequest(message='Tipo de Filtro Inválido')

        if not appointments_list:
            raise AppError(logger_message='Nenhum informação recebida de list_filter_appointments')

        return appointments_list

class GetUniqueAppointment(ControlHandler):
     def get_unique_appointment(self):
         appointment_id = self.req_data.params.get('id')
         if not appointment_id:
             raise BadRequest(field='ID')

         response = self.controler.get_unique_appointment_repo(appointment_id)
         if not response:
             raise AppError(logger_message='Nenhum informação recebida de get_unique_appointment')

         return response

class DeleteAppointment(ControlHandler):
    def delete_appointment(self):
        appointment_id = self.req_data.params.get('id')
        if not appointment_id:
            raise BadRequest(field='ID')

        response = self.controler.delete_appointment_repo(
            appointment_id=appointment_id,
        )
        return response

class UpdateAppointment(ControlHandler):
    def update_status(self):
        appointment_id = self.req_data.params.get('id')
        status = self.req_data.params.get('status')
        if not appointment_id or not status:
            raise BadRequest(field='ID')

        response = self.controler.update_appointment_status_repo(
            appointment_id=appointment_id,
            status=status
        )
        return response
