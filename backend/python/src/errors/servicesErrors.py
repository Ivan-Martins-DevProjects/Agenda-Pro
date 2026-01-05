from .mainErrors import AppError

class ServiceNotFound(AppError):
    code = 'SERVICE_NOT_FOUND'
    default_message = 'Serviço não encontrado'
    default_logger_level = None
    default_logger_message = None
    status = 404

class DuplicateServiceError(AppError):
    default_message = 'Serviço já cadastrado'
    default_logger_level = None
    default_logger_message = None

    code = 'DUPLICATE_SERVICE_ERROR'
    status = 409

