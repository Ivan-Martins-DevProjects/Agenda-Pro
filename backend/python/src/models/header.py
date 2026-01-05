import logging
from src.errors.mainErrors import AppError
from src.models.clients import ClientsServices
from src.models.services import ServicesControl
from src.security import jwt

from src.errors.authErrors import UnauthorizedSession, UserNotPermited
logger = logging.getLogger(__name__)

class AuthHeader:
    def __init__(
        self,
        user = None,
        clientsServices = None,
        servicesControl = None,
        AccessID = None
    ):
        self.user = user
        self.clientsServices = clientsServices
        self.servicesControl = servicesControl
        self.AccessID = AccessID

    def header_handler(self, req_data, scope):
        try:
            token = req_data.headers.get('Authorization')
            if not token:
                raise UnauthorizedSession('Sessão não encontrada')

            check = jwt.AuthServices(token)
            user = check.Autenticar()
            if not user:
                raise AppError(logger_message='Erro ao criar classe User')

            hasPermission = user.is_permitted(scope)
            if hasPermission is False:
                raise UserNotPermited()

            self.AccessID = user.true_id()
            self.user = user

        except Exception:
            raise

    def header_client_services(self):
        self.clientsServices = ClientsServices(self.user)
        return self

    def header_services_control(self):
        self.servicesControl = ServicesControl(self.user)
        return self
