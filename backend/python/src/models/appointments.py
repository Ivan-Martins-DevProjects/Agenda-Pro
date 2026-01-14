from dataclasses import dataclass
import logging

from dotenv import load_dotenv

from src.errors.mainErrors import BadRequest
from src.internal import database


logger = logging.getLogger(__name__)
load_dotenv()

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

class AppointmentsControl:
    def __init__(self, User) -> None:
        self.user = User
        self.repo = AppointmentsRepository()

    def list_all_appointments(self, offset):
        appointments = self.repo.list_appointments (
            offset=offset,
            ID=self.user.true_id(),
            role=self.user.Role
        )
        return appointments

    def list_filter_appointments(self, offset, filter):
        allowed_status = {
            'pendente': 'status',
            'confirmado': 'status',
            'cancelado': 'status'
        }

        allowed_dates = {
            'hoje': ('day', 'date'),
            'semana': ('week', 'date'),
            'mes': ('month', 'date'),
        }

        if filter in allowed_status:
            internal_value = allowed_status[filter]
            appointments = self.repo.list_filter_appointments_repo(
                offset=offset,
                id=self.user.true_id(),
                field_type=internal_value,
                field=filter,
                role=self.user.Role
            )
            return appointments

        elif filter in allowed_dates:
            internal_field = allowed_dates[filter][0]
            internal_value = allowed_dates[filter][1]
            appointments = self.repo.list_filter_time_appointments_repo(
                offset=offset,
                id=self.user.true_id(),
                field_type=internal_field,
                field=internal_value,
                role=self.user.Role
            )
            return appointments

        else:
            raise BadRequest(field='Fitlro')

class AppointmentsRepository:
    def list_appointments(self, offset, ID, role):
        response = database.list_all_appointments_db(
            offset=offset,
            id=ID,
            role=role
        )
        return response

    def list_filter_appointments_repo(self, offset, id, field_type, field, role):
        response = database.list_filter_appointments_db(
            offset=offset,
            id=id,
            field_type=field_type,
            field=field,
            role=role
        )
        return response

    def list_filter_time_appointments_repo(self, offset, id, field_type, field, role):
        response = database.list_filter_time_appointments_db(
            offset=offset,
            id=id,
            field_type=field_type,
            field=field,
            role=role
        )
        return response

