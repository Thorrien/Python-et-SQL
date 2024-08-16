from app.view.views import View
from datetime import datetime
class Controler:
    
    def __init__(self, user, userDAO):
        self.view = View()
        self.userDAO = userDAO
        self.user = user
        
    def run(self):
        text = self.userDAO.get_text(1)
        self.view.logtrue(self.user, text.data)
        self.gestboucle()
        
    def gestboucle(self):
        choix = None
        while choix != "QUIT":
            choix = self.view.menuprincipalgestion(self.user)
            match choix:
                case "US":
                    choix = self.boucleUser()
                case "CL":
                    self.boucleClient()
                case "CO":
                    self.boucleContracts()
                case "EV":
                    self.boucleEvents()
                case "MO":
                    if self.user.authorisation("Gestion"):
                        data = self.view.getText(self.user)
                        self.userDAO.update_text(1, data)
                    else:
                        self.view.notautorized(self.user)
                case "SU":
                    if self.user.authorisation("Gestion"):
                        self.boucleAttributions()
                    else:
                        self.view.notautorized(self.user)
    
    def boucleAttributions(self):   
        choix = None
        while choix not in ['RET', 'QUIT']:
            companys = self.userDAO.get_all_company_without_user()
            events = self.userDAO.get_all_events_without_user()
            choix = self.view.logWithoutUser(self.user, events, companys)
            if choix.startswith("AE"):
                id = choix[2:]
                event = self.userDAO.get_event(id)
                users = self.userDAO.get_user_by_role(4)
                user_id = self.view.chooseUser( users)
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, user_id, event.attendees, event.notes)
                return 'LIST'
            elif choix.startswith("AC"):
                id = choix[2:]
                company = self.userDAO.get_company(id)
                users = self.userDAO.get_user_by_role(3)
                user_id = self.view.chooseUser( users)
                self.userDAO.update_company(company.id, company.company_name, company.address, user_id )
                return 'LIST'
            else: 
                return 'LIST'

    def boucleUser(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                users = self.userDAO.get_all_user_with_role_name()
                choix = self.view.logutilisateurs(self.user, users)
                self.main_choice(choix)
        else:
            self.view.notautorized(self.user)

    def main_choice(self, choix):
        match choix:
            case 'CR':
                self.create_user()
            case _ if choix.startswith("A"):
                id = c[1:]
                self.handle_user_modification(id)
            case _ if choix.startswith("M"):
                id = c[1:]
                self.handle_user_modification(id)
            case _ if choix.startswith("S"):
                id = c[1:]
                self.userDAO.delete_user(id)
            case "QUIT":
                return choix

    def create_user(self):
        nom, email, mot_de_passe, role = self.view.createuserview()
        self.userDAO.add_user(nom, email, mot_de_passe, int(role))

    def handle_user_modification(self, id):
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT', 'SUPPRIMER']:
            affiche = self.userDAO.get_user(id)
            choix = self.view.soloUserView(self.user, affiche)
            new_data = choix[3:]
            match choix:
                case "SUPPRIMER":
                    self.userDAO.delete_user(affiche.id)
                case _ if choix.startswith("NO "):
                    self.userDAO.update_user(affiche.id, new_data, affiche.email, affiche.role_id)
                case _ if choix.startswith("RE "):
                    self.userDAO.update_pasword_user(affiche.id, new_data)
                case _ if choix.startswith("EM "):
                    self.userDAO.update_user(affiche.id, affiche.nom, new_data, affiche.role_id)
                case "SE AD":
                    self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 1)
                case "SE VE":
                    self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 3)
                case "SE GE":
                    self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 2)
                case "SE SU":
                    self.userDAO.update_user(affiche.id, affiche.nom, affiche.email, 4)
                case "QUIT":
                    return choix
                case _:
                    print("commande inconnue")
        
    
    def boucleClient(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                companys = self.userDAO.get_all_company()
                choix = self.view.logclients(self.user, companys)
                self.client_main_choice(choix)
        else:
            self.view.notautorized(self.user)

    def client_main_choice(self, choix):
        match choix:
            case 'CR':
                self.create_company()
            case _ if choix.startswith("A"):
                id = choix[1:]
                self.handle_company_modification(id)
            case "QUIT":
                return choix

    def create_company(self):
        compagny_name = self.view.createcompany(self.user)
        self.userDAO.add_company(compagny_name, self.user.id)

    def handle_company_modification(self, id):
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT', 'SUPPRIMER']:
            company = self.userDAO.get_company(id)
            contacts = self.userDAO.get_all_contact_by_company_id(id)
            choix = self.view.totalViewCompagny(self.user, company, contacts)
            self.process_company_modification_choice(choix, company, contacts)

    def process_company_modification_choice(self, choix, company, contacts):
        match choix:
            case 'CR':
                self.create_contact(company)
            case 'RECUPERER':
                self.recover_company(company)
            case 'SUPPRIMER':
                self.delete_company(company)
            case _ if choix.startswith("MN "):
                new_data = choix[3:]
                self.update_company_name(company, new_data)
            case _ if choix.startswith("MA "):
                new_data = choix[3:]
                self.update_company_address(company, new_data)
            case _ if choix.startswith("A"):
                id_contact = choix[1:]
                self.handle_contact_modification(id_contact, company)
            case "QUIT":
                return choix
            case _:
                print("commande inconnue")

    def create_contact(self, company):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            name, email, phone, signatory = self.view.createcontact(company, self.user)
            self.userDAO.add_contact(company.id, name, email, phone, signatory)
        else:
            self.view.notautorized(self.user)

    def recover_company(self, company):
        self.userDAO.update_company(company.id, company.company_name, company.address, self.user.id)

    def delete_company(self, company):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            self.userDAO.delete_company(company.id)
        else:
            self.view.notautorized(self.user)

    def update_company_name(self, company, new_data):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            self.userDAO.update_company(company.id, new_data, company.address, company.user_id)
        else:
            self.view.notautorized(self.user)

    def update_company_address(self, company, new_data):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            self.userDAO.update_company(company.id, company.company_name, new_data, company.user_id)
        else:
            self.view.notautorized(self.user)

    def handle_contact_modification(self, id_contact, company):
        choix = None
        while choix not in ['ENTR', 'RET', 'QUIT', 'SUPPRIMER']:
            contact = self.userDAO.get_contact(id_contact)
            choix = self.view.detailedContact(contact, company)
            self.process_contact_modification_choice(choix, contact, company)

    def process_contact_modification_choice(self, choix, contact, company):
        new_data = choix[3:]
        print(new_data)
        
        match choix:
            case "SUPPRIMER":
                self.userDAO.delete_contact(contact.id)
            case _ if choix.startswith("NO "):
                self.userDAO.update_contact(contact.id, company.id, new_data, contact.email, contact.phone, contact.signatory)
            case _ if choix.startswith("EM "):
                self.userDAO.update_contact(contact.id, company.id, contact.name, new_data, contact.phone, contact.signatory)
            case _ if choix.startswith("TE "):
                self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, new_data, contact.signatory)
            case "SI Oui":
                self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, contact.phone, 1)
            case "SI Non":
                self.userDAO.update_contact(contact.id, company.id, contact.name, contact.email, contact.phone, 0)
            case "QUIT":
                return choix
            case _:
                print("commande inconnue")
                            
    def boucleContracts(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                contrats = self.userDAO.get_all_contract()
                supports = self.userDAO.get_user_by_role(4)
                choix = self.view.logcontracts(self.user, contrats, self.userDAO)
                self.handle_main_choice(choix, contrats, supports)

    def handle_main_choice(self, choix, contrats, supports):
        match choix:
            case _ if choix.startswith("CR"):
                self.create_contract(choix)

            case _ if choix.startswith("A"):
                self.view_contract(choix, contrats, supports)

            case _ if choix.startswith("E"):
                self.view_company(choix)

            case _ if choix.startswith("S"):
                self.delete_contract(choix, contrats)

            case "QUIT":
                return choix

    def create_contract(self, choix):
        id = choix[2:]
        company = self.userDAO.get_company(id)
        total_amont, current_amont, sign = self.view.createcontract(self.user, company)
        sign_flag = 1 if sign else 0
        self.userDAO.add_contract(company.id, self.user.id, total_amont, current_amont, sign_flag)

    def view_contract(self, choix, contrats, supports):
        id = int(choix[1:])
        contrat = contrats[id]
        contratId = contrat.id
        choix = None
        while choix not in ['RET', 'QUIT']:
            contrat = self.userDAO.get_contract(contratId)
            company = self.userDAO.get_company(contrat.compagny_id)
            events = self.userDAO.get_event_for_contract(contrat.id)
            choix = self.view.contractview(self.user, company, contrat, events, self.userDAO)
            self.contract_choice(choix, contrat, company, events, supports)

    def contract_choice(self, choix, contrat, company, events, supports):
        match choix:
            case _ if choix.startswith("A"):
                self.view_event(choix)

            case "CR":
                self.create_event(company, contrat, supports)

            case "SUPPRIMER":
                self.delete_contract_if_authorized(contrat, company)

            case _ if choix.startswith("MT "):
                self.update_contract_total(choix, contrat, company)

            case _ if choix.startswith("MV "):
                self.update_contract_current(choix, contrat, company)

            case "MS SI":
                self.update_contract_sign(contrat, company, sign=1)

            case "MS NS":
                self.update_contract_sign(contrat, company, sign=0)

            case "QUIT" | "RET":
                return choix

    def view_event(self, choix):
        id_event = choix[1:]
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT']:
            event = self.userDAO.get_event(id_event)
            choix = self.view.eventview(self.user, event, self.userDAO)
            self.event_choice(choix, event)

    def event_choice(self, choix, event):
        new_data = choix[3:]
        match choix:
            case "SUPPRIMER":
                self.userDAO.delete_event(event.id)
                return 'LIST'
            case "RET" | "QUIT":
                return choix
            case _ if choix.startswith("MS"):
                self.userDAO.update_event(event.id, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.event_date_end, event.location, event.id_user, event.attendees, event.notes)
            case _ if choix.startswith("ME"):
                self.userDAO.update_event(event.id, event.event_date_start, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.location, event.id_user, event.attendees, event.notes)
            case _ if choix.startswith("ML"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, new_data, event.id_user, event.attendees, event.notes)
            case _ if choix.startswith("MA"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, new_data, event.notes)
            case _ if choix.startswith("MN"):
                self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, event.attendees, new_data)

    def create_event(self, company, contrat, supports):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            event_date_start, event_date_end, location, support_id, attendees, notes = self.view.createevent(company, self.user, supports)
            eventid = self.userDAO.add_event(event_date_start, event_date_end, location, support_id, attendees, notes)
            self.userDAO.add_event_contract(eventid, contrat.id)
        else:
            self.view.notautorized(self.user)

    def delete_contract_if_authorized(self, contrat, company):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            self.userDAO.delete_contract(contrat.id)
        else:
            self.view.notautorized(self.user)

    def update_contract_total(self, choix, contrat, company):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            new_total = float(choix[3:])
            self.userDAO.update_contract(contrat.id, company.id, self.user.id, new_total, contrat.current_amont, contrat.sign)
        else:
            self.view.notautorized(self.user)

    def update_contract_current(self, choix, contrat, company):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            new_current = float(choix[3:])
            self.userDAO.update_contract(contrat.id, company.id, self.user.id, contrat.total_amont, new_current, contrat.sign)
        else:
            self.view.notautorized(self.user)

    def update_contract_sign(self, contrat, company, sign):
        if self.user.authorisation('Sale') and self.user.id == company.user_id:
            self.userDAO.update_contract(contrat.id, company.id, self.user.id, contrat.total_amont, contrat.current_amont, sign)
        else:
            self.view.notautorized(self.user)

    def view_company(self, choix):
        id = choix[1:]
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT']:
            company = self.userDAO.get_company(id)
            contacts = self.userDAO.get_all_contact_by_company_id(id)
            choix = self.view.LiteViewCompagny(self.user, company, contacts)

    def delete_contract(self, choix, contrats):
        id = int(choix[1:])
        contrat = contrats[id]
        self.userDAO.delete_contract(contrat.id)
                
    def boucleEvents(self):
        if self.user.authorisation('Admin') or self.user.authorisation('Gestion') or self.user.authorisation('Sale') or self.user.authorisation('Support'):
            choix = None
            while choix not in ['RET', 'QUIT']:
                events = self.userDAO.get_all_event_details_with_company()
                choix = self.display_events_based_on_role(events)
                self.handle_events_choice(choix, events)

    def display_events_based_on_role(self, events):
        if self.user.authorisation('Support'):
            return self.view.myMensualEvents(self.user, events)
        else:
            return self.view.TotalEvents(self.user, events)

    def handle_events_choice(self, choix, events):
        match choix:
            case "TO":
                self.handle_total_events_choice(events)
            case "TT":
                self.handle_total_events_choice(events)
            case _ if choix.startswith("A"):
                self.boucleSoloEvents(choix)
            case _:
                return choix

    def handle_total_events_choice(self, events):
        choix = None
        while choix not in ['RET', 'QUIT']:
            choix = self.view.myTotalEvents(self.user, events)
            if choix.startswith("A"):
                self.boucleSoloEvents(choix)
            elif choix == "TT":
                self.handle_tt_events_choice(events)
            else:
                return choix

    def handle_tt_events_choice(self, events):
        choix = None
        while choix not in ['RET', 'QUIT']:
            choix = self.view.TotalEvents(self.user, events)
            if choix.startswith("A"):
                self.boucleSoloEvents(choix)
            else:
                return choix

    def boucleSoloEvents(self, choix):
        id_event = choix[1:]
        choix = None
        while choix not in ['LIST', 'RET', 'QUIT']:
            event = self.userDAO.get_event(id_event)
            choix = self.view.eventview(self.user, event, self.userDAO)
            new_data = choix[3:]

            match choix:
                case "SUPPRIMER":
                    self.userDAO.delete_event(event.id)
                    return 'LIST'
                case "RET" | "QUIT":
                    return choix
                case _ if choix.startswith("MS"):
                    self.userDAO.update_event(event.id, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.event_date_end, event.location, event.id_user, event.attendees, event.notes)
                case _ if choix.startswith("ME"):
                    self.userDAO.update_event(event.id, event.event_date_start, datetime.strptime(new_data, "%d/%m/%Y %H:%M"), event.location, event.id_user, event.attendees, event.notes)
                case _ if choix.startswith("ML"):
                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, new_data, event.id_user, event.attendees, event.notes)
                case _ if choix.startswith("MA"):
                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, new_data, event.notes)
                case _ if choix.startswith("MN"):
                    self.userDAO.update_event(event.id, event.event_date_start, event.event_date_end, event.location, event.id_user, event.attendees, new_data)
                case _:
                    return choix