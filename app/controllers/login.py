from app.view.views import View
from app.view.loginview import Loginview
from app.dao.userdao import UserDAO
from app.controllers.control import Controler
import sentry_sdk

class Login:

    def __init__(self):
        self.view = View()
        self.loginview = Loginview()
        self.userdao = UserDAO()

    def login(self):
        self.view.ascii()
        email, password = self.loginview.log()
        user = self.userdao.get_user_by_email(email)

        if user:
            if user.verify_password(password):
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag("action", "connexion")
                    scope.set_tag("collaborator_name", email)
                sentry_sdk.capture_message(f"Collaborateur connecté : Nom={user.nom}, Email={email}")
                self.loginview.logtrue()
                controler = Controler(user, self.userdao)
                controler.run()

            else:
                self.loginview.logfalse()
                exit()
        else:
            print("Email inconnu")
            exit()
