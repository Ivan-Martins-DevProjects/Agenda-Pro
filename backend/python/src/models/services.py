import logging
import uuid

from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

from src.errors.mainErrors import AppError, InvalidField
from src.internal import database

logger = logging.getLogger(__name__)
load_dotenv()

@dataclass
class Services():
    id: str
    userId: str
    bussinesId: str
    title: str
    price: int
    duration: int
    respName: str
    description: Optional[str] = None

    def __post_init__(self):
        if len(self.title) < 5:
            raise InvalidField(field='Título')

        if int(self.price) < 0:
            raise InvalidField(
                field='Preço'
            )

        if int(self.duration) < 0:
            raise InvalidField(
                message='Duração não pode ser menor que 0'
            )

        if self.description and len(self.description) < 10:
            raise InvalidField(
                message='Descrição não pode ter menos que 10 caracteres'
            )

class ServicesControl:
    def __init__(self, User) -> None:
        self.user = User
        self.repo = ServicesRepository()

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

        Services(**data)

        response = self.repo.insert_service(
            data=data
        )
        return response

    def delete_service(self, id):
        response = self.repo.delete_service(id)
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
        if not response:
            raise AppError(
                logger_message='Nenhuma resposta recebida da função insert_service_db'
            )
        return response

    def delete_service(self, id):
        response = database.delete_service(id)
        if not response:
            raise AppError(
                logger_message='Nenhuma resposta recebida da função DeleteContactDB'
            )
        return response

    def get_unique_service(self, id, AccessID, role):
        response = database.get_unique_service_db(
            serviceId=id,
            AccessID=AccessID,
            role=role
        )

        return response
        
