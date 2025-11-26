from flask import Flask, jsonify
from flask_cors import CORS


from src.internal import database
from src.security import auth
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
    # Valida e decodifica o token recebido
    payload = auth.ValidateJWT()
    if not payload or not isinstance(payload, dict):
        return CreateError(500, 'Erro interno do servidor')

    # Verificação extra para garantir a conformidade dos valores
    data = payload['data']
    keys = data['ID']
    if not keys:
        logger.error('Erro com a extração de valores do jwt', exc_info=True)
        error = CreateError(500, "Erro interno do servidor")
        return error

    # Utiliza o id do token para verificar os clientes associados ao usuário
    response = clients.GetListClients(keys)
    if not response:
        return CreateError(500, 'Erro interno do servidor')

    # Retorna a resposta já codificada como json
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8585, debug=True)
