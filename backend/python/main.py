import logging
from flask import Flask, jsonify
from flask_cors import CORS

from src.internal import database
from src.validation import *
from src.handlers import dashboard, clients

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
def GetContactsAPI():
    response = clients.ListClients()
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    if response['status'] == 'error':
        return jsonify(response), response['code']

    return jsonify(response), 200

# Rota responsável por coletar informações de um único contato
@app.route('/api/client/<id>/info', methods=['GET'])
def GetContactAPI(id):
    if id:
        response = clients.GetContact(id)
        if not response:
            return CreateError(500, 'Erro interno do servidor')
        if response['status'] == 'error':
            return jsonify(response), response['code']

        return jsonify(response), 200
    
    logger.error('ID do contato, recebido na query, vazio')
    return CreateError(401, 'ID do contato não enviado')

# Rota responsável pela criação de novos clientes
@app.route('/api/clients/create', methods=['POST'])
def CreateContactAPI():
    response = clients.InsertContact()
    if not response:
        return CreateError(500, 'Erro interno do servidor')
    if response['status'] == 'error':
        return jsonify(response), response['code']

    return jsonify(response), 200

@app.route('/api/clients/delete/<id>', methods=['DELETE'])
def EditContactAPI(id):
    response = clients.DeleteContact(id)
    if not response:
        return CreateError(500, 'Erro interno do servidor')
    
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8585, debug=True)
