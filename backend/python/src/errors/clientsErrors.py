from .mainErrors import AppError
import logging

logger = logging.getLogger(__name__)

class ClientNotFound(AppError):
    default_code = 'CLIENT_NOT_FOUND'
    default_message = 'Contato não encontrado'
    default_logger_level = None
    default_logger_message = None
    default_status = 404

class DuplicateClientError(AppError):
    default_code = 'DUPLICATE_CLIENT_ERROR'
    default_message = 'Cliente já cadastrado'
    default_logger_level = None
    default_logger_message = None
    default_status = 409

class InaccessibleClient(AppError):
    default_code = 'INACCESSIBLE_CLIENT'
    default_message = 'Você não tem autorização para acessar esse clients'
    default_logger_level = None
    default_logger_message = None
    default_status = 409
