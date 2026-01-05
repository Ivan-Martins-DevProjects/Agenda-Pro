from .mainErrors import AppError
import logging

logger = logging.getLogger(__name__)

class ClientNotFound(AppError):
    code = 'CLIENT_NOT_FOUND'
    default_message = 'Contato não encontrado'
    default_logger_level = None
    default_logger_message = None
    status = 404

class DuplicateClientError(AppError):
    code = 'DUPLICATE_CLIENT_ERROR'
    default_message = 'Cliente já cadastrado'
    default_logger_level = None
    default_logger_message = None
    status = 409
