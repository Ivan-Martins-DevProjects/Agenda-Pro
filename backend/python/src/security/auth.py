import logging

from src.validation import CreateError

logger = logging.getLogger(__name__)

class Authentication:
    @staticmethod
    def CheckJWT(request_data):
        token = request_data.headers.get('Authorization')
        if not token:
            logger.info('Sessão não encontrada')
            return CreateError(401, 'Sessão não encontrada')

        return token
