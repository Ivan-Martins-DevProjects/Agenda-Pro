import logging
from src.validation import CreateResponse, CreateError
from src.internal import database

logger = logging.getLogger(__name__)

def GetListClients(id):
    if not isinstance(id, str):
        id = str(id)

    clientes = database.GetClients(id)
    if not clientes:
        data = CreateResponse('No clients')
        return data

    response = CreateResponse(clientes)
    return response


