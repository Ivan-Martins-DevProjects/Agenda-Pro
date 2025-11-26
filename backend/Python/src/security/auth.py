import logging
from flask import request

from src.validation import CreateError, CreateResponse
from src.security import jwt

logger = logging.getLogger(__name__)

def ValidateJWT() :
# Verifica se há um token junto aos cookies
    token = request.headers.get('Authorization')
    if not token:
        # Gera Log de erro caso não encontre o token 
        logger.error("Requisição bloqueada por cookie inexistente!", exc_info=True)

        # Gera resposta de erro e a envia de volta ao FrontEnd
        error = CreateError(401, "Requisição não autorizada")
        return error
    
    # Decodifica o token quando o encontra
    payload = jwt.DecodeJWT(token)

    # Caso haja algum erro gera o log e retorna a resposta de erro já definida na função de decodificação
    if not isinstance(payload, dict):
        logger.error("Erro ao decodificar payload", exc_info=True)
        response = CreateResponse(payload)
        return response

    return payload

