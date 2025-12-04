import logging
import uuid

from flask import request

from src.security import auth
from src.validation import errors
from src.internal import classes
from src.validation.checkTypes import isEmail, isName, isNumber

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


def InsertContact():
    response = TokenValidate()
    if response['status'] == 'error':
        return response

    data = response['data']
    id = data['ID']
    BussinesID = data['BussinesID']
    nome = data['Nome']
    role = data['Role']

    # Cria o usuário com base no payload recebido
    user = classes.User(ID=id, BussinesID=BussinesID, Role=role)

    body = request.get_json()

    clientId = uuid.uuid4()
    chaves = [
        'userid', 'bussinesId', 'clientId', 'nome', 'email', 'telefone',
        'obs', 'cpf', 'rua', 'numero', 'bairro', 'cidade', 'respName'
    ]

    data = {
        "userid" : id,
        "bussinesId" : BussinesID,
        "clientID" : str(clientId),
    }

    for chave in chaves:
        valor = body.get(chave) or ''
        if chave == 'numero':
            valor = body.get(chave) or 0

        elif chave == 'email':
            resp = isEmail(body.get(chave))
            if resp is False:
                return errors.CreateError(401, 'Email Inválido')
            valor = body.get(chave)

        elif chave == 'nome':
            resp = isName(body.get(chave))
            if resp is False:
                return errors.CreateError(401, 'Formato de Nome inválido')
            valor = body.get(chave)

        elif chave == 'telefone':
            resp = isNumber(body.get(chave))
            if resp is False:
                return errors.CreateError(401, 'Número de telefone inválido')
            valor = body.get(chave)

        elif chave == 'respName':
            valor = nome
        data[chave] = valor

    insert = user.InsertNewContact(data)
    if insert['status'] == 'error':
        return insert

    return insert

def DeleteContact(id):
    response = TokenValidate()
    if response['status'] == 'error':
        return response

    data = response['data']
    userId = data['ID']
    BussinesID = data['BussinesID']
    role = data['Role']

    user = classes.User(ID=userId, BussinesID=BussinesID, Role=role)
    response = user.DeleteContact(id)
    if not response:
        logger.error('Função DeleteContact não retornou nada')
        return errors.CreateError(500, 'Erro interno do servidor')

    return response

