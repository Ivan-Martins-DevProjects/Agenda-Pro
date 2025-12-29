import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.internal import database
from src.models import services
from src.requests.request_builder import RequestBuilder
from src.validation import *
from src.handlers import dashboard, page_clients, page_services

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

@app.route("/api/dashboard", methods=['POST'])
def data():
    resultado = dashboard.main()

    return jsonify(resultado)

@app.route('/api/clients', methods=['GET'])
def list_contacts_api():
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data
    )
    response = handler.list_contacts()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    return jsonify(response), response['code']

# Rota responsável por coletar informações de um único contato
@app.route('/api/client/<id>/info', methods=['GET'])
def get_contact_api(id):
    if not id:
        return CreateError(400, 'ID do cliente ausente')
    
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data,
        clientID=id
    )
    response = handler.get_contact()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    return jsonify(response), response['code']

# Rota responsável pela criação de novos clientes
@app.route('/api/clients/create', methods=['POST'])
def create_contact_api():
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data
    )
    response = handler.insert_contact()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    return jsonify(response), response['code']

@app.route('/api/clients/delete/<id>', methods=['DELETE'])
def delete_contact_api(id):
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data,
        clientID=id
    )
    response = handler.delete_contact()
    if not response:
        return CreateError(500, 'Erro interno do servidor')
    
    return jsonify(response), response['code']

@app.route('/api/clients/update/<id>', methods=['PUT'])
def EditContactAPI(id):
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data,
        clientID=id
    )
    response = handler.update_contact()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    return jsonify(response), response['code']

@app.route('/api/clients/search/<text>')
def search_contact_api(text):
    req_data = RequestBuilder.from_flask(request)

    handler = page_clients.ClientsHandler(
        req_data=req_data,
        text=text
    )
    response = handler.search_contact()
    if not response:
        CreateError(500, 'Erro interno do servidor')

    return jsonify(response), 200

@app.route('/api/services', methods=['GET'])
def list_services_api():
    req_data = RequestBuilder.from_flask(request)

    handler = page_services.ServicesHandler(req_data)
    response = handler.list_services()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    return jsonify(response), response['code']
