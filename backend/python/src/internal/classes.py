import logging

from src.validation import CreateResponse, CreateError
from src.internal import database

logger = logging.getLogger(__name__)

# Classe responsável por criar e validar permissões do usuário
class User:
    def __init__(self, ID, BussinesID = "", Nome = "", Email = "", Instance = "", IsConnected = "", Role = ""):
        self.ID = ID
        self.BussinesID = BussinesID
        self.Nome = Nome
        self.Email = Email
        self.Instance = Instance
        self.IsConnected = IsConnected
        self.Role = Role

    # Checa no banco de dados se o usuário tem permissão para realizar essa operação
    def Allowed(self, permission):
        check = database.CheckPermission(self.ID, permission)
        # Caso a função retorne None, isso significa que houve um erro
        if not check:
            logger.error('Erro ao checar permissões do usuário')
            return CreateError(500, 'Internal server error')
        elif check is False:
            return False

        # Caso o usuário esteja autorizado retorna True como validação
        return True

    def GetAllClients(self):
        # Busca os clientes referentes a role do usuário no banco de dados
        if self.Role == 'admin':
            clientes = database.GetClients(self.BussinesID, self.Role)
        elif self.Role == 'user':
            clientes = database.GetClients(self.ID, self.Role)
        else:
            logger.error('Role do cliente não definida')
            return CreateError(400, 'Role não encontrada')

        # Caso não tenha nenhum cliente informa ao FrontEnd
        if not clientes:
            response = CreateResponse('No clients')
            return response

        # Caso haja formata a resposta de forma que o FrontEnd possa processar
        response = CreateResponse(clientes)
        return response


