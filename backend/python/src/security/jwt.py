import jwt
import os
from dotenv import load_dotenv

from src.validation import CreateError

load_dotenv()

def DecodeJWT(token):
    secret = os.getenv("JWT_KEY")

    if not secret:
       error = CreateError(500, "JWT Secret não encontrado") 
       return error

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=['HS256']
        )

        if not payload:
            error = CreateError(500, "Erro ao decodificar JWT")
            return error

        return {
            'status': 'success',
            'data': payload
        }

    except jwt.ExpiredSignatureError as e:
        return CreateError(401, str(e))

    except jwt.InvalidSignatureError as e:
        return CreateError(409, str(e))

    except jwt.InvalidTokenError as e:
        return CreateError(409, str(e))
