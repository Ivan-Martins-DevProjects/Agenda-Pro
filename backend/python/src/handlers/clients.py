import logging
import uuid

from flask import request
from pydantic import ValidationError

from src.security import auth
from src.validation import errors
from src.internal import classes

logger = logging.getLogger(__name__)

def HeaderHandler(scope):
    CheckJWT = auth.ValidateJWT()
    if CheckJWT['status'] == 'error':
        return errors.CreateError(401, 'Sessão não encontrada')

    token = CheckJWT['data']
    check = classes.AuthServices(token)

    user = check.Autenticar()
    if isinstance(user, dict):
        return user

    hasPermission = user.is_permitted(scope)
    if isinstance(hasPermission, dict):
        return hasPermission

    userServices = classes.UserServices(user)
    AccessID = user.true_id()

    data = {
        'userServices': userServices,
        'AccessID': AccessID
    }

    return {
        'status': 'success',
        'data': data
    }

def ListClients():
    AuthHeader = HeaderHandler('read_contacts')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']
    AccessID = AuthHeader['data']['AccessID']

    
    paramOffset = request.args.get('offset', default=0, type=int)
    offset = (paramOffset - 1) * 10

    # Executa a função para receber a lista de clientes
    clients = userServices.get_all_clients(
        offset=offset,
        ID=AccessID
    )
    return clients


def GetContact(contactId):
    AuthHeader = HeaderHandler('read_contacts')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']
    AccessID = AuthHeader['data']['AccessID']

    CheckUserFromContact = userServices.validate_user_from_contact(
        contactID=contactId,
        ID=AccessID
    )
    if isinstance(CheckUserFromContact, dict):
        return CheckUserFromContact

    response = userServices.get_unique_contact(
        contactId=contactId,
        UserID=AccessID
    )
    return response


def InsertContact():
    AuthHeader = HeaderHandler('write_contacts')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']

    body = request.get_json()
    contact_data = {
        "userid": str(userServices.user.ID),
        "bussinesId": userServices.user.BussinesID,
        "contactID": str(uuid.uuid4()),
        "nome": body.get('nome'),
        "email": body.get('email'),
        "telefone": body.get('telefone'),
        "obs": body.get('obs'),
        "cpf": body.get('cpf'),
        "rua": body.get('rua'),
        "numero": body.get('numero'),
        "bairro": body.get('bairro'),
        "cidade": body.get('cidade'),
        "gasto": body.get('gasto'),
        "visitas": body.get('visitas'),
    }

    try:
        validated_client = classes.Clients(**contact_data)
    except ValidationError as e:
        return errors.CreateError(404, e)
    
    data = validated_client.model_dump()
    data['bussinesId'] = userServices.user.BussinesID
    data['respName'] = userServices.user.Nome
    
    response = userServices.insert_new_contact(data)
    return response

def UpdateContact(id):
    AuthHeader = HeaderHandler('write_contacts')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']
    AccessID = AuthHeader['data']['AccessID']

    CheckUserFromContact = userServices.validate_user_from_contact(
        contactID=id,
        ID=AccessID
    )
    if isinstance(CheckUserFromContact, dict):
        return CheckUserFromContact

    body = request.get_json()
    
    response = userServices.update_contact(id, body)
    return response


def DeleteContact(id):
    AuthHeader = HeaderHandler('delete_contact')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']
    AccessID = AuthHeader['data']['AccessID']

    CheckUserFromContact = userServices.validate_user_from_contact(
        contactID=id,
        ID=AccessID
    )
    if isinstance(CheckUserFromContact, dict):
        return CheckUserFromContact
    response = userServices.delete_contact(id)
    return response

def SearchContact(text):
    AuthHeader = HeaderHandler('read_contacts')
    if AuthHeader['status'] == 'error':
        return AuthHeader

    userServices = AuthHeader['data']['userServices']
    AccessID = AuthHeader['data']['AccessID']

    response = userServices.search_contact(
        id=AccessID,
        text=text
    )
    return response

