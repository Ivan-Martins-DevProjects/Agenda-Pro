import logging

from dotenv import load_dotenv
from pydantic import BaseModel

from src.internal import database

logger = logging.getLogger(__name__)
load_dotenv()

class Services(BaseModel):
    id: str
    userID: str
    bussinesID: str
    nome: str
    description: str
    price: int
    duration: int

class ServicesControl:
    def __init__(self, User) -> None:
        self.user = User
        self.repo = ServicesRepository()

    def grant_access(self, scope):
        ID = self.user.true_id()
        checkScope = self.user.set_scope(scope)
        if checkScope is not None:
            return checkScope

        return ID

    def list_all_services(self, offset, ID):
        logger.debug(f'Offset: {offset}')
        services = self.repo.list_services(
            offset=offset * 10,
            ID=ID,
            Role=self.user.Role
        )
        return services

class ServicesRepository:
    def list_services(self, offset, ID, Role):
        response = database.list_services_db(
            offset=offset,
            id=ID,
            role=Role
        )
        return response
