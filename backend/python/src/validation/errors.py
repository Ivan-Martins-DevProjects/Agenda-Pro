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

    return dict


def CreateResponse(message, code):

    dict = {
        "status": "success",
        "code": code,
        "data": message
    }


    return dict
