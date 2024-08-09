import getpass

class Loginview:
    def __init__(self):
        pass

    def log(self):
        print('\n\n------------------------------------------------------------')
        print('-----------------------------Loggin--------------------------')
        print('Quel est votre Identifiant ? ')
        username = None
        username = input('email : ')
        password = getpass.getpass("Mot de passe: ")
        return username, password