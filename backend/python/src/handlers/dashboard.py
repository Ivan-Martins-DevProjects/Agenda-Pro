# import logging
#
# from src.validation import *
#
# logger = logging.getLogger(__name__)
#
# class User:
#     def __init__(self, id:str) -> None:
#             self.id = id
#
#     def AddContact(self, name:str, number:str, email:str):
#         # Checagem de tipos
#         if checkTypes.isName(name) == False:
#             return errors.CreateError(401, "Formato inválido")
#
#         if checkTypes.isEmail(email) == False:
#             return errors.CreateError(401, "Formato inválido")
#
#         if checkTypes.isNumber(number) == False:
#             return errors.CreateError(401, "Formato inválido")
#
# def main():
#     return {
#         "status": "sucesso"
#     }
