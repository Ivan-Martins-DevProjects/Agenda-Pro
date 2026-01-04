import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.internal import database
from src.errors.mainErrors import AppError, NullableField, handle_exception
from src.requests.request_builder import RequestBuilder
from src.handlers import dashboard, page_clients, page_services
from src.validation.logging_conf import SetupLogging

# Setup para mensagens de Logs
SetupLogging()
logger = logging.getLogger(__name__)

# Criação do pool de conexões
database.CreatePool()

app = Flask(__name__)

# Configuração de cors da aplicação
CORS(app, resources={
    r"/api/*": {"origins": ["http://0.0.0.0:7000", "http://localhost:7000", "http://127.0.0.1:7000"]}
})

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
        if not req_data:
            raise AppError('Erro ao capturar req_data')

        handler = page_clients.ClientsHandler(
            req_data=req_data
        )
        if not handler:
            raise AppError('Erro ao gerar Handler')

        response = handler.list_contacts()
        if not response:
            raise AppError('Erro ao capturar resposta da função get_clients')

        return jsonify(response.get('data')), 200

    except Exception as e:
        response = handle_exception(e)
        logger.debug(response['status'])
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)


# Rota responsável por coletar informações de um único contato
@app.route('/api/client/<id>/info', methods=['GET'])
def get_contact_api(id):
    if not id:
        raise NullableField('id')

    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ClientsHandler(
            req_data=req_data,
            clientID=id
        )
        response = handler.get_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200

    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

# Rota responsável pela criação de novos clientes
@app.route('/api/clients/create', methods=['POST'])
def create_contact_api():
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ClientsHandler(
            req_data=req_data
        )
        response = handler.insert_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

@app.route('/api/clients/delete/<id>', methods=['DELETE'])
def delete_contact_api(id):
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ClientsHandler(
            req_data=req_data,
            clientID=id
        )
        response = handler.delete_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')
        
        return jsonify(response.get('data')), 200
    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

@app.route('/api/clients/update/<id>', methods=['PUT'])
def EditContactAPI(id):
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_clients.ClientsHandler(
            req_data=req_data,
            clientID=id
        )
        response = handler.update_contact()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200

    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

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
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

@app.route('/api/services', methods=['GET'])
def list_services_api():
    try:
        req_data = RequestBuilder.from_flask(request)

        handler = page_services.ServicesHandler(req_data)
        response = handler.list_services()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

@app.route('/api/services/create', methods=['POST'])
def create_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.ServicesHandler(req_data)

        response = handler.insert_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)

@app.route('/api/services/unique', methods=['GET']) 
def get_unique_service_api():
    try:
        req_data = RequestBuilder.from_flask(request)
        handler = page_services.ServicesHandler(req_data)

        response = handler.get_unique_service()
        if not response:
            raise AppError(logger_message='Erro ao capturar resposta do handler')

        return jsonify(response.get('data')), 200
    except Exception as e:
        response = handle_exception(e)
        return jsonify(response.get('error', 'Erro interno do servidor')), response.get('status', 500)
