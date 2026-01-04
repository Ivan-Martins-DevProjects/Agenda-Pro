from .mainErrors import AppError

class ServiceNotFound(AppError):
    code = 'SERVICE_NOT_FOUND'
    message = 'Serviço não encontrado'
    default_logger_level = None
    default_logger_message = None
    status = 404

class DuplicateServiceError(AppError):
    code = 'DUPLICATE_SERVICE_ERROR'
    message = 'Serviço já cadastrado'
    default_logger_level = None
    default_logger_message = None
    status = 409
