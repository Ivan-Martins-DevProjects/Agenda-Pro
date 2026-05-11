import logging
from src.errors.mainErrors import AppError
from src.models.header_handler import AppointmentsHeader, ClientsHeader, ServicesHeader
from src.security import jwt

from src.errors.authErrors import UnauthorizedSession, UserNotPermited
logger = logging.getLogger(__name__)

def handle_header(req_data, scope, module, db_pool):
    modules = {
        'clients': lambda: ClientsHeader(req_data, scope, db_pool),
        'services': lambda: ServicesHeader(req_data, scope, db_pool),
        'appointments': lambda: AppointmentsHeader(req_data, scope, db_pool),
    }

    services = None
    for module_name, services_factory in modules.items():
        if module == module_name:
            services = services_factory()

    if not services:
        raise AppError(logger_message='Módulo não encontrado')

    controler = services.controler
    if not controler:
        raise AppError(logger_message="Erro ao definir Controlers")

    return controler, services.access_id, services.user

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
