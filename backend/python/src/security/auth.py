import logging
from flask import request

from src.validation import CreateError
from src.validation.errors import CreateResponse

logger = logging.getLogger(__name__)

def ValidateJWT() :
# Verifica se há um token junto aos cookies
    token = request.headers.get('Authorization')
    if not token:
        # Gera Log de erro caso não encontre o token 
        logger.error("Requisição bloqueada por cookie inexistente!", exc_info=True)

        # Gera resposta de erro e a envia de volta ao FrontEnd
        return CreateError(401, "Requisição não autorizada")
    
    return CreateResponse(token)
