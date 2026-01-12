from dataclasses import dataclass
import logging

from dotenv import load_dotenv

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

class AppointmentsRepository:
    def list_appointments(self, offset, ID, role):
        response = database.list_all_appointments_db(
            offset=offset,
            id=ID,
            role=role
        )
        return response
