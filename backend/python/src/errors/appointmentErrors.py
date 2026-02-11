from .mainErrors import AppError

class AppointmentAlreadyExists(AppError):
    default_code = 'APPOINTMENT_ALREADY_EXISTS'
    default_message = 'Agendamento já cadastrado nesse horário'
    default_logger_message = None
    default_logger_level = None
    status = 409

class AppointmentPastDate(AppError):
    default_code = 'DATE_IN_PAST'
    default_message = 'Data inválida'
    default_logger_message = None
    default_logger_level = None
    status = 409
