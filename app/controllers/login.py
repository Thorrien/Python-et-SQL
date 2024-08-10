from app.view.views import View
from app.view.loginview import Loginview
from app.dao.userdao import UserDAO
from app.controllers.control import Controler


class Login:
    
    def __init__(self):
        self.view = View()
        self.loginview = Loginview()
        self.userdao = UserDAO()

    def login(self):
        self.view.ascii()
        
        ################A ENLEVER
        user = self.userdao.get_user_by_email('eric.bariller.48@gmail.com')
        controler = Controler(user, self.userdao)
        controler.run()

        
        ################A ENLEVER
        #email, password = self.loginview.log()
        #user = self.userdao.get_user_by_email(email)
        
        #if user:
        #    if user.verify_password(password):
        #        print("connexion Autorisée")
        #        controler = Controler(user, self.userdao)
        #        controler.run()
        #    else:
        #        print("Mot de passe incorrect")
        #        exit()
        #else:
        #    print("Email inconnu")
        #    exit()
