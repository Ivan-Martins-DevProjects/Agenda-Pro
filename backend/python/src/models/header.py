from src.models.clients import ClientsServices
from src.models.services import ServicesControl
from src.security import jwt
from src.validation import errors

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
            return errors.CreateError(401, 'Sessão não encontrada')

        check = jwt.AuthServices(token)
        user = check.Autenticar()
        if isinstance(user, dict):
            return user

        hasPermission = user.is_permitted(scope)
        if hasPermission is False:
            raise PermissionError
        elif isinstance(hasPermission, dict):
            return hasPermission

        self.AccessID = user.true_id()
        self.user = user

    def header_client_services(self):
        self.clientsServices = ClientsServices(self.user)
        return self

    def header_services_control(self):
        self.servicesControl = ServicesControl(self.user)
        return self
