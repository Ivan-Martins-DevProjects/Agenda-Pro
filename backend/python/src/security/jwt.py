import logging
import jwt
import os

from dotenv import load_dotenv

from src.models.clients import User
from src.errors.authErrors import UnauthorizedSession, jwtErrors
from src.internal import database

logger = logging.getLogger(__name__)
load_dotenv()

class AuthServices:
    def __init__(self, JWT) -> None:
        self.token = JWT
        self.secret = os.getenv("JWT_KEY")

    def Autenticar(self):
        if not self.secret:
            raise UnauthorizedSession(message='Sessão não encontrada')
        try:
            payload = jwt.decode(
               self.token ,
                self.secret,
                algorithms=['HS256']
            )
            if not payload:
                raise UnauthorizedSession(message='Sessão não encontrada')

            ID = payload['ID']
            BussinesID = payload['BussinesID']
            Nome = payload['Nome']
            Instance = payload['Instance']
            IsConnected = payload['IsConnected']
            Role =  payload['Role']

            permissions = database.RequestPermissionsDB(ID)

            Usuario = User(ID, BussinesID, Nome, Instance, IsConnected, Role, permissions)
            return Usuario

        except Exception as e:
            raise jwtErrors(e)
