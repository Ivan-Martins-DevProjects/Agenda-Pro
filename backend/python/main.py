import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.internal import database
from src.errors.mainErrors import AppError, NullableField, HandleException
from src.requests.request_builder import RequestBuilder
from src.handlers import page_clients, page_services, page_appointments
from src.validation.logging_conf import SetupLogging

# Setup para mensagens de Logs
SetupLogging()
logger = logging.getLogger(__name__)

# Criação do pool de conexões
database.CreatePool()

app = Flask(__name__)

# Configuração de cors da aplicação
CORS(app, resources={
    r"/api/*": {"origins": ["http://0.0.0.0:7000", "http://localhost:7000", "http://127.0.0.1:7000"]} })

logger = logging.getLogger(__name__)

# @app.route("/api/dashboard", methods=['POST'])
# def data():
#     resultado = dashboard.main()
#
#     return jsonify(resultado)

@app.route('/api/clients', methods=['GET'])
def list_contacts_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_clients.ListClients(req_data, 'read_contacts', 'clients')
        if not handler:
            raise AppError('Erro ao gerar Handler')

        response = handler.list_all_clients()
        if not response:
            raise AppError('Erro ao capturar resposta da função get_clients')

        return jsonify(response.get('data')), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status


# Rota responsável por coletar informações de um único contato
@app.route('/api/client', methods=['GET'])
def get_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ListClients(req_data, 'read_contacts', 'clients')
        response = handler.get_unique_client()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

# Rota responsável pela criação de novos clientes
@app.route('/api/clients/create', methods=['POST'])
def create_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_clients.InsertNewClient(req_data, 'write_contacts', 'clients')

        response = handler.insert_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/clients', methods=['DELETE'])
def delete_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.DeleteClient(req_data, 'delete_contact', 'clients')
        response = handler.delete_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')
        
        return jsonify(response), 200
    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/clients', methods=['PUT'])
def EditContactAPI():
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.EditClient(req_data, 'write_contacts', 'clients')
        response = handler.update_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/clients/search/<text>')
def search_contact_api(text):
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ClientsHandler(
            req_data=req_data,
            text=text
        )
        response = handler.search_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/services', methods=['GET'])
def list_services_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.ListServices(req_data, 'read_services', 'services')

        response = handler.list_services()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/services/create', methods=['POST'])
def create_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.InsertNewService(req_data, 'write_services', 'services')

        response = handler.insert_service()
        if not response:
            raise AppError(
                message='Erro ao capturar resposta do handler',
                logger_message='Erro ao capturar resposta do handler'
            )

        return jsonify(response.get('data')), 200
    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

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
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status


@app.route('/api/services/unique', methods=['GET']) 
def get_unique_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.GetUniqueService(req_data, 'read_services', 'services')

        response = handler.get_unique_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/services/edit', methods=['PUT']) 
def edit_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.EditService(req_data, 'write_services', 'services')

        response = handler.edit_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/appointments', methods=['GET'])
def list_appointments():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_appointments.ListAppointments(req_data, 'read_appointments', 'appointments')

        if not req_data.params.get('filterType'):
            response = handler.list_all_appointments()
        else:
            response = handler.list_filter_appointments()

        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status

@app.route('/api/appointments/unique', methods=['GET'])
def get_unique_appointment():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_appointments.GetUniqueAppointment(req_data, 'read_appointments', 'appointments')

        response = handler.get_unique_appointment()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response), 200

    except Exception as e:
        error = HandleException(e)
        data = error.generate_data()
        return jsonify(data), error.status
