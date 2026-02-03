from dataclasses import dataclass
import logging

from dotenv import load_dotenv

from src.errors.mainErrors import AppError, BadRequest
from src.internal import appointments_database as database
from src.internal.main_database import DatabasePool


logger = logging.getLogger(__name__)
load_dotenv()

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
    id: str
    service: str
    clientId: str
    userId: str
    date: str
    time_begin: str
    time_end: str
    status: str

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
