import json

# Função para criação de erros padronizados
def CreateError(code, message):
    dict = {
        "code": code,
        "message": message
    }

    response = json.dumps(dict)
    
    return response

# Função para criação de logs padronizados
def PrintError(archive, line, message):
   return print(f'Error:{message}\nArchive:{archive} | Line:{line}')
