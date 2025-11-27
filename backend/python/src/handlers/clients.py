import logging
import json

from src.security import auth
from src.validation import CreateError
from src.internal import classes

logger = logging.getLogger(__name__)

def TokenValidate():
# Valida e decodifica o token recebido
    payload = auth.ValidateJWT()
    if not payload or not isinstance(payload, dict):
        logger.error('Erro ao decodificar JWT')
        return CreateError(500, 'Erro interno de servidor')
    
    # Verificação extra para garantir a conformidade dos valores
    data:dict = payload['data']
    if not data:
        logger.error('Erro com a extração de valores do jwt', exc_info=True)
        error = CreateError(500, "Erro interno do servidor")
        return error
    
    dictionary = {
        'status': 'success',
        'data': data
    }
    response = json.dumps(dictionary)

    return response




def ListClients():
    # valida o token e converte a estrutura em json
    response = TokenValidate()
    responseJson = json.loads(response)

    if responseJson['status'] == 'error':
        return responseJson

    data = responseJson['data']
    id = data['ID']
    BussinesID = data['BussinesID']
    role = data['Role']

    # Cria o usuário com base no payload recebido
    user = classes.User(ID=id, BussinesID=BussinesID, Role=role)

    # Valida se o usuário tem permissão para essa tarefa
    check = user.Allowed('read_contacts')
    if check is False:
        return CreateError(401, 'Usuário não autorizado')

    # Executa a função para receber a lista de clientes
    clientes = user.GetAllClients()
    return clientes



def GetContact(contactId):
    response = TokenValidate()
    responseJson = json.loads(response)

    if responseJson['status'] == 'error':
        return responseJson

    data = responseJson['data']
    id = data['ID']
    BussinesID = data['BussinesID']
    role = data['Role']

    # Cria o usuário com base no payload recebido
    user = classes.User(ID=id, BussinesID=BussinesID, Role=role)

