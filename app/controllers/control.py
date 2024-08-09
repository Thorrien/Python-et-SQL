from app.view.views import View
from app.dao.userdao import UserDAO

from time import sleep


class Controler:
    
    def __init__(self, user, userDAO):
        self.view = View()
        self.userDAO = userDAO
        self.user = user
        
    def run(self):
        if self.user.authorisation('Sale'):
            print("menu admin")
        else : 
            print('accès refusé')