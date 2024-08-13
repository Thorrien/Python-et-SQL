from app.view.views import View

class Controler:
    
    def __init__(self, user, userDAO):
        self.view = View()
        self.userDAO = userDAO
        self.user = user
        
    def run(self):
        self.view.logtrue(self.user)
        self.gestboucle()
        
    def gestboucle(self):
        choix = None
        while choix != "QUIT" : 
            choix = self.view.menuprincipalgestion(self.user)
            if choix == "US" : 
                choix = self.boucleUser()
            elif choix == "CL" :
                self.boucleClient()
            elif choix == "MO" :
                self.view.notautorized(self.user)
                
    def boucleUser(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                users = self.userDAO.get_all_user_with_role_name()
                choix = self.view.logutilisateurs(self.user, users)
                if choix == 'CR':
                    nom, email, mot_de_passe, role = self.view.createuserview()
                    self.userDAO.add_user(nom, email, mot_de_passe, int(role))
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
                        elif choix.startswith("RE "):
                            self.userDAO.update_pasword_user(affiche.id, new_data)
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
                        elif choix == "QUIT":
                            return choix
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
                        elif choix.startswith("RE "):
                            self.userDAO.update_pasword_user(affiche.id, new_data)
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
                        elif choix == "QUIT":
                            return choix
                        else: 
                            print("commande inconnue")
                elif choix.startswith("S"):
                    id = choix[1:]
                    self.userDAO.delete_user(id)
                elif choix == "QUIT":
                    return choix
        else : 
            self.view.notautorized(self.user)

    def boucleClient(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                companys = self.userDAO.get_all_company()
                choix = self.view.logclients(self.user, companys)
                if choix == 'CR':
                    compagny_name = self.view.createcompany(self.user)
                    self.userDAO.add_company(compagny_name, self.user.id)
                elif choix.startswith("A") :
                    id = choix[1:]
                    choix = None
                    while choix not in ['LIST', 'RET', 'QUIT', 'SUPPRIMER']:
                        company = self.userDAO.get_company(id)
                        contacts = self.userDAO.get_all_contact_by_company_id(id)
                        contrats = self.userDAO.get_all_contracts_by_company_id(id)
                        events = []
                        for contrat in contrats:
                            tempo = None
                            tempo = self.userDAO.get_event_for_contract(contrat.id)
                            for element in tempo : 
                                events.append(element)
                        choix = None
                        choix = self.view.totalViewCompagny(self.user, company, contacts, contrats, events)
                        if choix.startswith("A"):
                            id_contact = choix[1:]
                        else: 
                            new_data = choix[3:]

                        if choix == "CR":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                name, email, phone, signatory = self.view.createcontact(company, self.user)
                                self.userDAO.add_contact(company.id, name, email, phone, signatory)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix == 'RECUPERER':
                                self.userDAO.update_company(company.id, company.company_name, company.address,self.user.id)
                        elif choix == "SUPPRIMER":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.delete_company(company.id)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix.startswith("MN "):
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_company(company.id, new_data, company.address, company.user_id)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix.startswith("MA "):
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_company(company.id, company.company_name, new_data, company.user_id)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix.startswith("A"):
                            choix = None
                            while choix not in ['ENTR', 'RET', 'QUIT', 'SUPPRIMER']:
                                contact = self.userDAO.get_contact(id_contact)
                                choix = self.view.detailedContact(contact, company)
                                new_data = choix[3:]
                                print(new_data)
                                if choix == "SUPPRIMER":
                                    self.userDAO.delete_contact(id)
                                elif choix.startswith("NO "):
                                    self.userDAO.update_contact(contact.id, company.id, new_data, contact.email, contact.phone, contact.signatory)
                                elif choix.startswith("EM "):
                                    self.userDAO.update_contact(contact.id, company.id, contact.name, new_data, contact.phone, contact.signatory)
                                elif choix.startswith("TE "):
                                    self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, new_data, contact.signatory)
                                elif choix == "SI Oui":
                                    self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, contact.phone, 1)
                                elif choix == "SI Non":
                                    self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, contact.phone, 0)
                                elif choix == "QUIT":
                                    return choix
                                else: 
                                    print("commande inconnue")
                        elif choix == "QUIT":
                            return choix
                        else: 
                            print("commande inconnue")