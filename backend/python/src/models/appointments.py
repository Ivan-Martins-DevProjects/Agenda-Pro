from dataclasses import dataclass
from datetime import datetime
import logging
import re
import json

from typing import Any

from src.errors.appointmentErrors import AppointmentPastDate
from src.errors.mainErrors import AppError, BadRequest
from src.internal import appointments_database as database
from src.internal.main_database import DatabasePool


logger = logging.getLogger(__name__)

@dataclass
class AppointmentsControl:
    db_pool: DatabasePool
    role: str
    access_id: str 

    def __post_init__(self):
        if not self.db_pool:
            raise AppError(logger_message='Pool de conexões não inicializado')
        if not self.role:
            raise AppError(logger_message='Role não recebida')

    @property
    def params(self) -> tuple:
        return self.role, self.db_pool

@dataclass
class Appointments:
    id: Any
    userId: str
    clientId: str
    date: Any
    hour: Any
    status: str
    businessId: str
    clientName: str
    userName: str
    price: Any
    description: str
    duration: Any
    services: Any

    def __post_init__(self):
        if len(self.services) <= 0:
            raise BadRequest(message='Nenhum serviço fornecido')

        # Validar se não foi recebido uma data no passado
        format = "%d/%m/%Y %H:%M"
        appointmentDate = datetime.strptime(f'{self.date} {self.hour}', format)
        now = datetime.now()
        if appointmentDate < now:
            raise AppointmentPastDate

        # Converte string data em formato date
        self.date = datetime.strptime(self.date, '%d/%m/%Y')

        # Converte string de hour para formato hour
        self.hour = datetime.strptime(self.hour, '%H:%M').time()

        # Remove caracteres de preço
        self.price = int(self.price.replace("R$", "").split(",")[0].strip()) * 100

        # Remove qualquer caractere que não seja número
        self.duration = int(re.sub(r'[a-zA-Z]', '', self.duration))

        self.services = json.dumps(self.services)



class AppointmentsRepository(AppointmentsControl):
    def list_all_appointments_repo(self, offset):
        repo = database.ListAppointmentsRepository(
            params=self.params
        )
        response = repo.list_all_appointments_db(
            offset=offset,
            id=self.access_id,
        )
        return response

    def list_filter_appointments_repo(self, offset, field_type, field):
        repo = database.ListAppointmentsRepository(
            params=self.params
        )
        response = repo.list_filter_appointments_db(
            offset=offset,
            id=self.access_id,
            field_type=field_type,
            field=field,
        )
        return response

    def insert_new_appointment_repo(self, appointment: Appointments):
        repo = database.ListAppointmentsRepository(
            params=self.params
        )
        repo.check_if_appointment_already_exists(appointment.date, appointment.hour)

        repo = database.InsertNewAppointmentRepository(
            params=self.params
        )
        response = repo.insert_new_appointment_db(
            appointment=appointment
        )
        return response

    def list_filter_time_appointments_repo(self, offset, date_value):
        repo = database.ListAppointmentsRepository(
            params=self.params
        )
        response = repo.list_filter_time_appointments_db(
            offset=offset,
            id=self.access_id,
            date_value=date_value
        )
        return response

    def get_unique_appointment_repo(self, appointment_id):
        repo = database.GetUniqueAppointmentRepository(
            params=self.params
        )
        response = repo.get_unique_appointment_db(
            appointment_id=appointment_id,
            user_id=self.access_id,
        )
        return response

    def delete_appointment_repo(self, appointment_id):
        repo = database.DeleteAppointmentRepository(
            params=self.params
        )
        response = repo.delete_appointment_db(
            appointment_id=appointment_id,
            id=self.access_id,
        )
        return response
    
    def update_appointment_status_repo(self, appointment_id, status):
        repo = database.UpdateAppointmentRepository(
            params=self.params
        )
        response = repo.update_appointment_status_db(
            appointment_id=appointment_id,
            status=status,
            id=self.access_id,
        )
        return response

    def update_appointment_info_repo(self, data, appointment_id):
        repo = database.UpdateAppointmentRepository(
            params=self.params
        )
        response = repo.update_appointment_info_db(
            data=data,
            appointment_id=appointment_id
        )
        return response
