from app.view.views import View
from datetime import datetime
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
            elif choix == "CO" :
                self.boucleContracts()
            elif choix == "EV":
                self.boucleEvents()
            elif choix == "MO":
                pass
            elif choix == "SU":
                pass
                
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
                        choix = None
                        choix = self.view.totalViewCompagny(self.user, company, contacts)
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
                            
    def boucleContracts(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                contrats = self.userDAO.get_all_contract()
                supports = self.userDAO.get_user_by_role(4)
                choix = self.view.logcontracts(self.user, contrats, self.userDAO)
                if choix.startswith("CR"):
                    id = choix[2:]
                    company = self.userDAO.get_company(id)
                    total_amont, current_amont, sign = self.view.createcontract(self.user, company)
                    if sign is True: 
                        self.userDAO.add_contract(company.id, self.user.id, total_amont, current_amont, 1)
                    else : 
                        self.userDAO.add_contract(company.id, self.user.id, total_amont, current_amont, 0)

                if choix.startswith("A"):
                    id = int(choix[1:])
                    choix = None
                    contrat = contrats[id]
                    contratId = contrat.id
                    while choix not in ['RET', 'QUIT']:
                        contrat = self.userDAO.get_contract(contratId)
                        company = self.userDAO.get_company(contrat.compagny_id)
                        events = self.userDAO.get_event_for_contract(contrat.id)
                        choix = self.view.contractview(self.user, company, contrat, events, self.userDAO)
                        if choix.startswith("A"):
                            id_event = choix[1:]
                            choix = None
                            while choix not in ['LIST', 'RET', 'QUIT']:
                                event = self.userDAO.get_event(id_event)
                                choix = self.view.eventview(self.user, event, self.userDAO)
                                new_data = choix[3:]
                                if choix == "SUPPRIMER" :
                                    pass
                                elif choix == "RET" or choix == "QUIT":
                                    return choix
                                elif choix.startswith("MS"):
                                    self.userDAO.update_event(event.id, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.event_date_end, event.location, event.id_user, event.attendees, event.notes)
                                elif choix.startswith("ME"):
                                    self.userDAO.update_event(event.id, event.event_date_start, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.location, event.id_user, event.attendees, event.notes)
                                elif choix.startswith("ML"):
                                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, new_data, event.id_user, event.attendees, event.notes)
                                elif choix.startswith("MA"):
                                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, new_data, event.notes)
                                elif choix.startswith("MN"):
                                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, event.attendees, new_data)
                        else: 
                            new_data = choix[3:]
                        if choix == "CR":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                event_date_start, event_date_end, location, support_id, attendees, notes = self.view.createevent(company, self.user, supports)
                                eventid = self.userDAO.add_event(event_date_start, event_date_end, location, support_id, attendees, notes)
                                self.userDAO.add_event_contract(eventid, contrat.id)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix == "SUPPRIMER":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.delete_contract(contrat.id)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix.startswith("MT "):
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_contract(contrat.id, company.id, self.user.id, float(new_data), contrat.current_amont, contrat.sign)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix.startswith("MV "):
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_contract(contrat.id, company.id, self.user.id, contrat.total_amont, float(new_data), contrat.sign)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix == "MS SI":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_contract(contrat.id, company.id, self.user.id, contrat.total_amont, contrat.current_amont, 1)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix == "MS NS":
                            if self.user.authorisation('Sale') and self.user.id == company.user_id :
                                self.userDAO.update_contract(contrat.id, company.id, self.user.id, contrat.total_amont, contrat.current_amont, 0)
                            else: 
                                self.view.notautorized(self.user)
                        elif choix == "QUIT":
                            return choix
                        elif choix == "RET":
                            return choix
                elif choix.startswith("E") :
                    id = choix[1:]
                    choix = None
                    while choix not in ['LIST', 'RET', 'QUIT']:
                        company = self.userDAO.get_company(id)
                        contacts = self.userDAO.get_all_contact_by_company_id(id)
                        choix = None
                        choix = self.view.LiteViewCompagny(self.user, company, contacts)
                elif choix.startswith("S") :
                    id = int(choix[1:])
                    choix = None
                    contrat = contrats[id]
                    contratId = contrat.id
                    self.userDAO.delete_contract(contratId)
                elif choix == "QUIT":
                    return choix
                
    def boucleEvents(self):
        events = self.userDAO.get_all_event_details_with_company()
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                if self.user.authorisation('Support'):
                    choix = self.view.myMensualEvents(self.user, events)
                else:
                    choix = self.view.TotalEvents(self.user, events)
                if choix == "TO":
                    while choix not in ['RET', 'QUIT']:
                        choix = None
                        choix = self.view.myTotalEvents(self.user, events)
                        if choix.startswith("A"):
                            choix = self.boucleSoloEvents(choix)
                        elif choix == "TT":
                            while choix not in ['RET', 'QUIT']:
                                choix = None
                                choix = self.view.TotalEvents(self.user, events)
                                if choix.startswith("A"):
                                    choix = self.boucleSoloEvents(choix)
                                else: 
                                    return choix
                elif choix == "TT":
                    while choix not in ['RET', 'QUIT']:
                        choix = None
                        choix = self.view.TotalEvents(self.user, events)
                        if choix.startswith("A"):
                            choix = self.boucleSoloEvents(choix)
                        else: 
                            return choix
                elif choix.startswith("A"):
                    choix = self.boucleSoloEvents(choix)
                else: 
                    return choix

    def boucleSoloEvents(self, choix):
        id_event = choix[1:]
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT']:
            event = self.userDAO.get_event(id_event)
            choix = self.view.eventview(self.user, event, self.userDAO)
            new_data = choix[3:]
            if choix == "SUPPRIMER" :
                pass
            elif choix == "RET" or choix == "QUIT":
                return choix
            elif choix.startswith("MS"):
                self.userDAO.update_event(event.id, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.event_date_end, event.location, event.id_user, event.attendees, event.notes)
            elif choix.startswith("ME"):
                self.userDAO.update_event(event.id, event.event_date_start, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.location, event.id_user, event.attendees, event.notes)
            elif choix.startswith("ML"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, new_data, event.id_user, event.attendees, event.notes)
            elif choix.startswith("MA"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, new_data, event.notes)
            elif choix.startswith("MN"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, event.attendees, new_data)
            else: 
                return choix