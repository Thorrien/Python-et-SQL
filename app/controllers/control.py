from app.view.views import View
from app.dao.userdao import UserDAO
from datetime import date

from time import sleep


class Controler:
    
    def __init__(self, user, userDAO):
        self.view = View()
        self.userDAO = userDAO
        self.user = user
        
    def run(self):
        self.view.logtrue(self.user)
        if self.user.authorisation("Admin"):
            self.gestboucle()
        elif self.user.authorisation("Gestion"):
            self.gestboucle()
        elif self.user.authorisation("Sale"):
            print('Sale')
        elif self.user.authorisation("Support"):
            print('Support')
        
    def gestboucle(self):
        choix = None
        while choix != "QUIT" : 
            choix = self.view.menuprincipalgestion(self.user)
            if choix == "US" : 
                choix = None
                while choix not in ['RET', 'QUIT']:
                    users = self.userDAO.get_all_user_with_role_name()
                    choix = self.view.logutilisateurs(self.user, users)
                    if choix == 'CR':
                        pass
                    elif choix.startswith("A"):
                        id = choix[1:]
                        choix = None
                        while choix not in ['LIST', 'RET', 'QUIT', 'SUPPRIMER']:
                            affiche = self.userDAO.get_user(id)
                            choix = self.view.soloUserView(self.user, affiche)
                            new_data = choix[3:]
                            print(new_data)
                            if choix == "SUPPRIMER":
                                self.userDAO.delete_user(id)
                            elif choix.startswith("NO "):
                                self.userDAO.update_user(affiche.id, new_data, affiche.email, affiche.role_id)
                            elif choix.startswith("EM "):
                                self.userDAO.update_user(affiche.id, affiche.nom, new_data, affiche.role_id)
                            elif choix == "SE AD":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 1)
                            elif choix == "SE VE":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 3)
                            elif choix == "SE GE":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 2)
                            elif choix == "SE SU":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 4)
                            else: 
                                print("commande inconnue")    
                    elif choix.startswith("M"):
                        id = choix[1:]
                        choix = None
                        while choix not in ['LIST', 'RET', 'QUIT', 'SUPPRIMER']:
                            affiche = self.userDAO.get_user(id)
                            choix = self.view.soloUserView(self.user, affiche)
                            new_data = choix[3:]
                            print(new_data)
                            if choix == "SUPPRIMER":
                                self.userDAO.delete_user(id)
                            elif choix.startswith("NO "):
                                self.userDAO.update_user(affiche.id, new_data, affiche.email, affiche.role_id)
                            elif choix.startswith("EM "):
                                self.userDAO.update_user(affiche.id, affiche.nom, new_data, affiche.role_id)
                            elif choix == "SE AD":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 1)
                            elif choix == "SE VE":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 3)
                            elif choix == "SE GE":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 2)
                            elif choix == "SE SU":
                                self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 4)
                            else: 
                                print("commande inconnue")
                    elif choix.startswith("S"):
                        id = choix[1:]
                        self.userDAO.delete_user(id)

