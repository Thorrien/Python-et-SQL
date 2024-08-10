import getpass
from app.controllers.security import validate_email

class Loginview:
    def __init__(self):
        pass

    def log(self):
        print('\n\n------------------------------------------------------------')
        print('-----------------------------Loggin--------------------------')
        print('Quel est votre Identifiant ? ')
        username = None
        username = input('email : ')
        if validate_email(username):
            password = getpass.getpass("Mot de passe: ")
            return username, password
        else:
            print("format d'email invalide")
            exit()