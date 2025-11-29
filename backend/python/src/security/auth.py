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
        data = json.loads(payload)
        logger.error(f"Erro ao decodificar payload: {data['message']}")
        response = CreateResponse(payload)
        return response

    if payload['status'] == 'error':
        # Valida se o payload recebido foi inválido
        if payload['code'] == 401:
            return CreateError(401, 'Requisição não autorizada')
        
        # Registra um erro diferente para caso tenha recebido um token adulterado
        elif payload['code'] == 409:
            return CreateError(401,'Requisição não autorizada')

        # Resposta em caso de erro interno
        elif payload['code'] == 500:
            return payload

    return payload

