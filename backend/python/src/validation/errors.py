import json
import logging

logger = logging.getLogger(__name__)

# Função para criação de erros padronizados
def CreateError(code, message):

    if not isinstance(code, int):
        code = int(code)

    if not isinstance(message, str):
        message = str(message)

    dict = {
        "status": "error",
        "code": code,
        "message": message
    }

    response = json.dumps(dict)
    
    return response


def CreateResponse(message):

    dict = {
        "status": "success",
        "data": message
    }

    response = json.dumps(dict)

    return response
