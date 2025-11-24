from flask import Flask, jsonify, request
from flask_cors import CORS


from src.validation import *
from src.handlers import dashboard, clients
from src.security import jwt

# Setup para mensagens de Logs
SetupLogging()

app = Flask(__name__)

# Configuração de cors da aplicação
CORS(app, resources={
    r"/api/*": {"origins": ["http://0.0.0.0:7000"]}
})

logger = logging.getLogger(__name__)

@app.route("/api/dashboard", methods=['POST'])
def data():
    resultado = dashboard.main()

    return jsonify(resultado)

@app.route('api/clients', methods='GET')
def GetClients():

    # Verifica se há um token junto aos cookies
    token = request.cookies.get('Access_Key')
    if not token:
        # Gera Log de erro caso não encontre o token 
        logger.error("Requisição bloqueada por cookie inexistente!")

        # Gera resposta de erro e a envia de volta ao FrontEnd
        error = CreateError(401, "Requisição não autorizada")
        return error
    
    # Decodifica o token quando o encontra
    payload: Any = jwt.DecodeJWT(token)

    # Caso haja algum erro gera o log e retorna a resposta de erro já definida na função de decodificação
    if not isinstance(payload, dict):
        logger.error("Erro ao decodificar payload")
        return payload

    # Verificação extra para garantir a conformidade dos valores
    keys = payload.get('data')
    if not keys:
        logger.error('Erro com a extração de valores do jwt')
        error = CreateError(500, "Erro interno do servidor")
        return error

    # Captura o ID contido no token
    ID = clients.GetClients(keys.get('ID'))

    # Envia o ID do cliente para a função GetClients
    response = clients.GetClients(ID)

    # Retorna a resposta já tratada ba função
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
