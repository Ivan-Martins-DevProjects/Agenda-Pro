from dataclasses import dataclass
from functools import cached_property
import logging
import os
from typing import Any
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.errors.mainErrors import AppError, BadRequest, HandleException
from src.internal.main_database import DatabasePool
from src.models.clients import User
from src.models.header import handle_header
from src.requests.request_builder import RequestBuilder
from src.handlers import page_clients, page_services, page_appointments
from src.validation.logging_conf import SetupLogging

# Setup para mensagens de Logs
SetupLogging()
logger = logging.getLogger(__name__)

DB_INFO = os.getenv('POSTGRES_URL', 'postgres')
db_pool = DatabasePool(conninfo=DB_INFO)

app = Flask(__name__)

# Configuração de cors da aplicação
CORS(app, resources={
    r"/api/*": {"origins": ["http://0.0.0.0:7000", "http://localhost:7000", "http://127.0.0.1:7000", "http://192.168.18.188:7000"]} })

logger = logging.getLogger(__name__)

def handle_main_errors(error):
    error = HandleException(error)
    data = error.generate_data()
    return jsonify(data or 'Erro interno do servidor'), error.status or 500

@dataclass
class RequestContext:
    req_data: Any
    scope: str
    module: str
    db_pool: DatabasePool

    @cached_property
    def controler(self) -> Any:
        return self._data[0]

    @cached_property
    def access_id(self) -> str:
        return self._data[1]

    @cached_property
    def user(self) -> User:
        return self._data[2]

    @cached_property
    def _data(self):
        controler, access_id, user = handle_header(
            req_data=self.req_data,
            scope=self.scope,
            module=self.module,
            db_pool=self.db_pool
        )
        if not controler:
            raise AppError(logger_message='Erro ao extrair controler de services')
        return controler, access_id, user

    def __post_init__(self):
        filter_modules = ['clients', 'services', 'appointments']
        if self.module.strip() not in filter_modules:
            raise BadRequest(logger_message='Módulo inválido')

        filter_scopes = [
            'read_contacts', 'write_contacts', 'delete_contact',
            'read_services', 'write_services', 'delete_services',
            'read_appointments', 'write_appointments', 'delete_appointments',
        ]
        if self.scope.strip() not in filter_scopes:
            raise BadRequest(logger_message='Scope inválido')

        if not self.db_pool:
            raise AppError(logger_message='Pool de conexões não inicializado')


@app.route('/api/clients', methods=['GET'])
def list_contacts_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.ListClients(context)
        if not handler:
            raise AppError('Erro ao gerar Handler')

        response = handler.list_all_clients()
        if not response:
            raise AppError('Erro ao capturar resposta da função get_clients')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)


# Rota responsável por coletar informações de um único contato
@app.route('/api/client', methods=['GET'])
def get_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.GetUniqueClient(context)
        if not handler:
            raise AppError('Erro ao gerar Handler')

        response = handler.get_unique_client()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

# Rota responsável pela criação de novos clientes
@app.route('/api/clients/create', methods=['POST'])
def create_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='write_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.InsertNewClient(context)
        if not handler:
            raise AppError(logger_message='Erro ao gerar Handler')

        response = handler.insert_client()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/clients', methods=['DELETE'])
def delete_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='delete_contact',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.DeleteClient(context)
        if not handler:
            raise AppError(logger_message='Erro ao gerar Handler')

        response = handler.delete_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')
        
        return jsonify(response), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/clients', methods=['PUT'])
def EditContactAPI():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='write_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.EditClient(context)
        if not handler:
            raise AppError(logger_message='Erro ao gerar Handler')

        response = handler.update_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/clients/search')
def search_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_clients.ListClients(context)
        if not handler:
            raise AppError(logger_message='Erro ao gerar Handler')

        response = handler.search_clients()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/services', methods=['GET'])
def list_services_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_services',
            module='services',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_services.ListServices(context)

        response = handler.list_all_services()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/services/create', methods=['POST'])
def create_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='write_services',
            module='services',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_services.InsertNewService(context)

        response = handler.insert_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/services/delete', methods=['DELETE'])
def delete_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.DeleteService(req_data, 'delete_services', 'services')

        response = handler.delete_service()
        if not response:
            raise AppError(
                message='Erro ao capturar resposta',
                logger_message='handler delete_service não retornou nenhuma resposta'
            )

        return '', 200

    except Exception as e:
        return handle_main_errors(e)


@app.route('/api/services/unique', methods=['GET']) 
def get_unique_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_contacts',
            module='clients',
            db_pool=db_pool
        )
        if not context:
            raise AppError(logger_message='Erro ao gerar RequestContext')

        handler = page_services.GetUniqueService(context)
        if not handler:
            raise AppError(logger_message='Erro ao gerar Handler')

        response = handler.get_unique_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/services/edit', methods=['PUT']) 
def edit_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_contacts',
            module='clients',
            db_pool=db_pool
        )
        handler = page_services.EditService(context)

        response = handler.edit_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/appointments', methods=['GET'])
def list_appointments():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_appointments',
            module='appointments',
            db_pool=db_pool
        )
        handler = page_appointments.ListAppointments(context)

        if not req_data.params.get('filterType'):
            response = handler.list_all_appointments()
        else:
            response = handler.list_filter_appointments()

        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/appointments/unique', methods=['GET'])
def get_unique_appointment():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_appointments',
            module='appointments',
            db_pool=db_pool
        )
        handler = page_appointments.GetUniqueAppointment(context)

        response = handler.get_unique_appointment()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/appointments', methods=['DELETE'])
def delete_appointment():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_appointments',
            module='appointments',
            db_pool=db_pool
        )
        handler = page_appointments.DeleteAppointment(context)

        response = handler.delete_appointment()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        return handle_main_errors(e)


@app.route('/api/appointments/update/status', methods=['PUT'])
def update_status_appointment():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_appointments',
            module='appointments',
            db_pool=db_pool
        )
        handler = page_appointments.UpdateAppointment(context)

        response = handler.update_status()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200
    except Exception as e:
        return handle_main_errors(e)

@app.route('/api/appointments/upda', methods=['PUT'])
def update_info_appointment():
    try:
        req_data = RequestBuilder.from_flask(request)
        context = RequestContext(
            req_data=req_data,
            scope='read_appointments',
            module='appointments',
            db_pool=db_pool
        )
        handler = page_appointments.UpdateAppointment(context)

        response = handler.update_status()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200
    except Exception as e:
        return handle_main_errors(e)
