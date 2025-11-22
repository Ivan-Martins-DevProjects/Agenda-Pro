from src.validation import checkTypes, errors

class User:
    def __init__(self, id:str) -> None:
            self.id = id

    def AddContact(self, name:str, number:int, email:str):
        # Checagem de tipos
        if checkTypes.isStr(name) or checkTypes.isStr(email) == False:
            return errors.CreateError(401, "Formato inválido")
        
        if checkTypes.isInt(number) == False:
            return errors.CreateError(401, "Formato inválido")
