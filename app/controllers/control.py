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
        test = self.userDAO.get_company_events(3)
        print(test)