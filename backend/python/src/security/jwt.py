import logging
import jwt
import os

from dotenv import load_dotenv

from src.models.clients import User
from src.validation import errors
from src.internal import database

logger = logging.getLogger(__name__)
load_dotenv()

class AuthServices:
    def __init__(self, JWT) -> None:
        self.token = JWT
        self.secret = os.getenv("JWT_KEY")
        self.ErrorMap = {
            jwt.ExpiredSignatureError: (401, 'Sessão expirada'),
            jwt.InvalidSignatureError: (409, 'Erro ao verificar sessão'),
            jwt.InvalidTokenError: (401, 'Sessão inválida'),
            jwt.DecodeError: (401, 'Erro ao verificar sessão'),
            ValueError: (401, 'Sessão inválida'),
        }

    def JwtErrors(self, e):
        for errType, (status, message) in self.ErrorMap.items():
            if isinstance(e, errType):
                return errors.CreateError(status, message)

        return errors.CreateError(500, 'Erro ao autenticar')

    def Autenticar(self):
        if not self.secret:
            logger.error('Token JWT não encontrado')
            return errors.CreateError(401, 'Sessão não encontrada')

        try:
            payload = jwt.decode(
               self.token ,
                self.secret,
                algorithms=['HS256']
            )

            if not payload:
                logger.error('Erro ao decodificar payload')
                return errors.CreateError(401, 'Erro ao autenticar')

            ID = payload['ID']
            BussinesID = payload['BussinesID']
            Nome = payload['Nome']
            Instance = payload['Instance']
            IsConnected = payload['IsConnected']
            Role =  payload['Role']

            permissions = database.RequestPermissionsDB(ID)

            if permissions['status'] == 'error':
                return permissions

            Usuario = User(ID, BussinesID, Nome, Instance, IsConnected, Role, permissions['data'])
            return Usuario

        except Exception as e:
            logger.exception('Erro ao validar token JWT')
            return self.JwtErrors(e)

def DecodeJWT(token):
    secret = os.getenv("JWT_KEY")

    if not secret:
       error = errors.CreateError(500, "JWT Secret não encontrado") 
       return error

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=['HS256']
        )

        if not payload:
            error = errors.CreateError(500, "Erro ao decodificar JWT")
            return error

        return {
            'status': 'success',
            'data': payload
        }

    except jwt.ExpiredSignatureError as e:
        return errors.CreateError(401, str(e))

    except jwt.InvalidSignatureError as e:
        return errors.CreateError(409, str(e))

    except jwt.InvalidTokenError as e:
        return errors.CreateError(409, str(e))
