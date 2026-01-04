import logging
import uuid

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
        services = self.repo.list_services(
            offset=offset * 10,
            ID=ID,
            Role=self.user.Role
        )
        return services

    def insert_new_service(self, data):
        data['userId'] = self.user.ID
        data['bussinesId'] = self.user.BussinesID
        data['respName'] = self.user.Nome
        data['id'] = uuid.uuid4()

        response = self.repo.insert_service(
            data=data
        )
        return response

    def get_unique_service(self, serviceId, AccessID):
        response = self.repo.get_unique_service(
            id=serviceId,
            AccessID=AccessID,
            role=self.user.Role
        )
        return response

class ServicesRepository:
    def list_services(self, offset, ID, Role):
        response = database.list_services_db(
            offset=offset,
            id=ID,
            role=Role
        )
        return response

    def insert_service(self, data):
        response = database.insert_service_db(
            data
        )

        return response

    def get_unique_service(self, id, AccessID, role):
        response = database.get_unique_service_db(
            serviceId=id,
            AccessID=AccessID,
            role=role
        )

        return response
        
