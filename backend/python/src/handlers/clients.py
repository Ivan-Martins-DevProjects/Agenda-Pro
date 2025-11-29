import logging

from src.security import auth
from src.validation import errors
from src.internal import classes

logger = logging.getLogger(__name__)

def TokenValidate():
# Valida e decodifica o token recebido
    payload = auth.ValidateJWT()
    if not payload or not isinstance(payload, dict):
        logger.error('Erro ao decodificar JWT')
        return errors.CreateError(500, 'Erro interno de servidor')

    elif payload['status'] == 'error':
        return payload
    
    # Verificação extra para garantir a conformidade dos valores
    data:dict = payload['data']
    if not data:
        logger.error('Erro com a extração de valores do jwt', exc_info=True)
        return errors.CreateError(500, "Erro interno do servidor")
    
    response = {
        'status': 'success',
        'data': data
    }

    return response


def ListClients():
    # valida o token e converte a estrutura em json
    response = TokenValidate()

    # Tratamento de erros em caso de problema com o token
    if response['status'] == 'error':
        if response['code'] == 401 or response['code'] == 500:
            return response
        elif response['code'] == 409:
            return errors.CreateError(401, 'Requisição não autorizada')


    # Parametrização dos valores recebidos pelo token
    data = response['data']
    id = data['ID']
    BussinesID = data['BussinesID']
    role = data['Role']

    # Cria o usuário com base no payload recebido
    user = classes.User(ID=id, BussinesID=BussinesID, Role=role)

    # Valida se o usuário tem permissão para essa tarefa
    check = user.Allowed('read_contacts')
    if check is False:
        return errors.CreateError(401, 'Usuário não autorizado')
    elif check['status'] == 'error':
        return check

    # Executa a função para receber a lista de clientes
    clientes = user.GetAllClients()
    return clientes


def GetContact(contactId):
    response = TokenValidate()

    if response['status'] == 'error':
        return response

    data = response['data']
    id = data['ID']
    BussinesID = data['BussinesID']
    role = data['Role']

    # Cria o usuário com base no payload recebido
    user = classes.User(ID=id, BussinesID=BussinesID, Role=role)
    response = user.GetUniqueContact(contactId)

    return response

