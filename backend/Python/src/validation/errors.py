import json

# Função para criação de erros padronizados
def CreateError(code, message):
    dict = {
        "code": code,
        "message": message
    }

    response = json.dumps(dict)
    
    return response

