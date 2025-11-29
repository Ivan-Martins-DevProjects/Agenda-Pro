import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.wrappers import ResponseStream


from src.internal import database
from src.validation import *
from src.handlers import dashboard, clients

# Setup para mensagens de Logs
SetupLogging()

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
def GetClients():
    contactId = request.args.get('id')
    if contactId:
        response = clients.GetContact(contactId)
        if response['status'] == 'error':
            return jsonify(response), response['code']

        return jsonify(response)

    if request.method == 'GET':
        response = clients.ListClients()
        if response['status'] == 'error':
            return jsonify(response), response['code']

        return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8585, debug=True)
