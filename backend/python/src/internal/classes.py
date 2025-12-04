import logging

from src.validation import errors
from src.internal import database

logger = logging.getLogger(__name__)

# Classe responsável por criar e validar permissões do usuário
class User:
    def __init__(self, ID, BussinesID = "", Nome = "", Email = "", Instance = "", IsConnected = "", Role = ""):
        if Role == 'admin':
            self.ID = BussinesID
        else:
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
            return errors.CreateError(500, 'Internal server error')

        # Retorna se o usuário está autorizado ou não
        return check

    def GetAllClients(self):
        # Busca os clientes referentes a role do usuário no banco de dados
        clientes = database.GetClients(self.ID, self.Role)

        # Caso não tenha nenhum cliente informa ao FrontEnd
        if not clientes:
            response = errors.CreateResponse('No clients')
            return response

        # Caso haja formata a resposta de forma que o FrontEnd possa processar
        response = errors.CreateResponse(clientes)
        return response

    def GetUniqueContact(self, contactId):
        # Checa se o usuário tem permissão para essa operação
        check = self.Allowed('read_contacts')

        # Se check for False o usuário não tem permissão
        if check is False:
            return errors.CreateError(401, 'Usuário não autorizado')
        elif check['status'] == 'error':
            return check

        # Executa a função para buscar as informações do contato
        response = database.GetUniqueContact(contactId, self.ID, self.Role)

        # Em caso de erro interno registra o log
        if response['status'] == 'error' and response['status'] == 500:
            logger.error(f'Erro ao buscar contato: {response['message']}')
            return response

        # Retorna a resposta da função que pode ser um dict ou uma mensagem de erro
        return response

    def InsertNewContact(self, data):
        check = self.Allowed('write_contacts')

        if check is False:
            return errors.CreateError(401, 'Usuário não autorizado')
        elif check['status'] == 'error':
            return check

        response = database.InsertNewContactDB(data, self.Nome)
        if response['status'] == 'error':
            return response

        return response
        
