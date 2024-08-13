from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, inspect
from app.models.models import User, Base, Role, Company, Event, Contact, Contract
from app.utils import config


class UserDAO:
    def __init__(self):
        self.engine = create_engine(
            f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}',
            echo=False
        )
        self.base = Base
        self.base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def tables(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        print("Tables dans la database:")
        for table in tables:
            print(table)
            print(" ")
            tableentiere = self.metadata.tables[table]
            print("########DETAIL###########")
            for column in tableentiere.columns:
                print(f"  - Column: {column.name}, Type: {column.type}")
            print(" ")
            print(" ")
            
    def get_all_users(self):
        session = self.Session()
        try:
            users = session.query(User).all()
            return users
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
    
    def get_all_user_with_role_name(self):
        session = self.Session()
        try:
            users_with_roles = session.query(User, Role).join(Role).all()
            result = [
                {
                    'user_id': user.id,
                    'user_name': user.nom,
                    'user_email': user.email,
                    'role_id': role.id,
                    'role_name': role.role
                }
                for user, role in users_with_roles
            ]
            result_sorted = sorted(result, key=lambda x: x['user_name'])
            return result_sorted
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()

    def get_user(self, user_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_user_by_email(self, email: str):
        session = self.Session()
        try:
            user = session.query(User).filter(User.email == email).one_or_none()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
                
    def get_user_by_role(self, role_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.role_id == role_id).all()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def add_user(self, name: str, email: str, password: str, role_id: int):
        session = self.Session()
        try:
            new_user = User(
                nom=name, 
                email=email, 
                role_id=role_id
                )
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_pasword_user(self, user_id: int, password: str ):
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                user.set_password(password)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_user(self, user_id: int, name: str, email: str, role_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                user.nom = name
                user.email = email
                user.role_id = role_id
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def delete_user(self, user_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                session.delete(user)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def add_role(self, role: str):
        session = self.Session()
        try:
            new_role = Role(role=role)
            session.add(new_role)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_role(self, role_id: int):
        session = self.Session()
        try:
            role = session.query(Role).filter(Role.id == role_id).one_or_none()
            return role
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_roles(self):
        session = self.Session()
        try:
            roles = session.query(Role).all()
            return roles
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def update_role(self, role_id: int, role: str):
        session = self.Session()
        try:
            role_obj = session.query(Role).filter(Role.id == role_id).one_or_none()
            if role_obj:
                role_obj.role = role
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def delete_role(self, role_id: int):
        session = self.Session()
        try:
            role = session.query(Role).filter(Role.id == role_id).one_or_none()
            if role:
                session.delete(role)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()


    def add_company(self, name: str, user_id: int, adress: str ):
        session = self.Session()
        try:
            new_company = Company(
                company_name=name,
                adress = adress, 
                user_id=user_id
                )
            session.add(new_company)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_company(self, id: int, name: str, address: str, user_id: int ):
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.id == id).one_or_none()
            if company:
                company.company_name = name
                company.address = address
                company.user_id = user_id
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def delete_company(self, company_id: int):
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.id == company_id).one_or_none()
            if company:
                session.delete(company)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_company(self):
        session = self.Session()
        try:
            companys = session.query(Company).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
    
    def get_all_company_without_user(self):
        session = self.Session()
        try:
            companys = session.query(Company).filter(Company.user_id == None).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_company(self, id: int):
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.id == id).one_or_none()
            return company
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
                
    def get_user_by_user_id(self, user_id: int):
        session = self.Session()
        try:
            companys = session.query(Company).filter(Company.user_id == user_id).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def add_event(self, event_date_start, event_date_end, location: str, id_user: int, attendees: int, notes=None):
        session = self.Session()
        try:
            new_event = Event(
                event_date_start=event_date_start,
                event_date_end=event_date_end,
                location=location,
                id_user=id_user,
                attendees=attendees,
                notes=notes
            )
            session.add(new_event)
            session.commit()
            print(f"Event added with ID: {new_event.id}")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_event(self, id: int):
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == id).one_or_none()
            return event
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_events_by_user_id(self, user_id):
        session = self.Session()
        try:
            events = session.query(Event).filter(Event.id_user == user_id).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_all_events_without_user(self):
        session = self.Session()
        try:
            events = session.query(Event).filter(Event.id_user == None).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
            
    def get_all_events(self):
        session = self.Session()
        try:
            events = session.query(Event).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def update_event(self, id: int, event_date_start, event_date_end, location: str, id_user: int, attendees: int, notes):
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == id).one_or_none()
            if event:
                event.event_date_start = event_date_start,
                event.event_date_end = event_date_end,
                event.location = location,
                event.id_user = id_user,
                event.attendees = attendees,
                event.notes = notes,
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def delete_event(self, event_id: int):
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == event_id).one_or_none()
            if event:
                session.delete(event)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def add_contact(self, compagny_id: int, name: str, email: str, phone: str, signatory=False):
        session = self.Session()
        try:
            new_contact = Contact(
                compagny_id=compagny_id,
                name=name,
                email=email,
                phone=phone,
                signatory=signatory,
            )
            session.add(new_contact)
            session.commit()
            print(f"Contact added with ID: {new_contact.id}")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_contact(self, id: int, compagny_id: int, name: str, email: str, phone: str, signatory):
        session = self.Session()
        try:
            contact = session.query(Contact).filter(Contact.id == id).one_or_none()
            if contact:
                contact.compagny_id = compagny_id
                contact.name = name
                contact.email = email
                contact.phone = phone
                contact.signatory = signatory
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def delete_contact(self, contact_id: int):
        session = self.Session()
        try:
            contact = session.query(Contact).filter(Contact.id == contact_id).one_or_none()
            if contact:
                session.delete(contact)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_contact(self, id: int):
        session = self.Session()
        try:
            contact = session.query(Contact).filter(Contact.id == id).one_or_none()
            return contact
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contact_by_company_id(self, id):
        session = self.Session()
        try:
            contacts = session.query(Contact).filter(Contact.compagny_id == id).all()
            return contacts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contact(self):
        session = self.Session()
        try:
            contacts = session.query(Contact).all()
            return contacts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contacts_by_user_id(self, user_id: int):
        session = self.Session()
        try:
            contacts = (
                session.query(Contact)
                .join(Company)
                .filter(Company.user_id == user_id)
                .all()
            )
            return contacts
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return []
        finally:
            session.close()
            
    def delete_contract(self, contract_id: int):
        session = self.Session()
        try:
            contract = session.query(Contract).filter(Contract.id == contract_id).one_or_none()
            if contract:
                session.delete(contract)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_contract(self, contract_id: int):
        session = self.Session()
        try:
            contact = session.query(Contract).filter(Contract.id == contract_id).one_or_none()
            return contact
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            

    def get_all_contract(self):
        session = self.Session()
        try:
            contracts = session.query(Contract).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contracts_by_user_id(self, user_id: int):
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(Contract.user_id == user_id).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_all_contracts_by_company_id(self, compagny_id : int):
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(Contract.compagny_id == compagny_id).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_all_my_contracts_sign(self, user_id : int):
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(Contract.user_id == user_id, Contract.sign == True).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
            
    def get_all_contracts_without_user(self):
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(Contract.user_id == None).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()
    
    def get_all_contracts_without_full_paiement(self, user_id : int):
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(Contract.user_id == user_id, Contract.current_amont < Contract.total_amont).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def add_contract(self, compagny_id: int, user_id: int, total_amont: float, current_amont: float, sign=False):
        session = self.Session()
        try:
            contract = Contract(
                compagny_id=compagny_id,
                user_id=user_id,
                total_amont=total_amont,
                current_amont=current_amont,
                sign=sign
            )
            session.add(contract)
            session.commit()
            print(f"Event added with ID: {contract.id}")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_contract(self, id: int, compagny_id: int, user_id: int, total_amont: float, current_amont: float, sign=False):
        session = self.Session()
        try:
            contract = session.query(Contract).filter(Contract.id == id).one_or_none()
            if contract:
                contract.compagny_id = compagny_id
                contract.user_id = user_id
                contract.total_amont = total_amont
                contract.current_amont = current_amont
                contract.sign = sign
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def add_event_contract(self, event_id: int, contract_id: str):
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == event_id).one_or_none()
            contract = session.query(Contract).filter(Contract.id == contract_id).one_or_none()
            
            if event and contract:
                event.contracts.append(contract)
                session.commit()
                print(f"Event {event_id} successfully linked with contract {contract_id}")
            else:
                if not event:
                    print(f"Event with ID {event_id} not found.")
                if not contract:
                    print(f"Contract with ID {contract_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
    
    def modify_event_contract(self, event_id: int, old_contract_id: str, new_contract_id: str):
        session = self.Session()
        try:
            # Rechercher l'événement et les contrats
            event = session.query(Event).filter(Event.id == event_id).one_or_none()
            old_contract = session.query(Contract).filter(Contract.id == old_contract_id).one_or_none()
            new_contract = session.query(Contract).filter(Contract.id == new_contract_id).one_or_none()
            
            if event and old_contract and new_contract:
                # Remplacer l'ancien contrat par le nouveau
                if old_contract in event.contracts:
                    event.contracts.remove(old_contract)
                    event.contracts.append(new_contract)
                    session.commit()
                    print(f"Contract {old_contract_id} replaced with {new_contract_id} for event {event_id}")
                else:
                    print(f"Contract {old_contract_id} is not associated with event {event_id}")
            else:
                if not event:
                    print(f"Event with ID {event_id} not found.")
                if not old_contract:
                    print(f"Old contract with ID {old_contract_id} not found.")
                if not new_contract:
                    print(f"New contract with ID {new_contract_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
    
    def delete_event_contract(self, event_id: int, contract_id: str):
        session = self.Session()
        try:
            # Rechercher l'événement et le contrat
            event = session.query(Event).filter(Event.id == event_id).one_or_none()
            contract = session.query(Contract).filter(Contract.id == contract_id).one_or_none()
            
            if event and contract:
                # Supprimer l'association
                if contract in event.contracts:
                    event.contracts.remove(contract)
                    session.commit()
                    print(f"Contract {contract_id} removed from event {event_id}")
                else:
                    print(f"Contract {contract_id} is not associated with event {event_id}")
            else:
                if not event:
                    print(f"Event with ID {event_id} not found.")
                if not contract:
                    print(f"Contract with ID {contract_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_contract_for_event(self, event_id: int):
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == event_id).one_or_none()
            
            if event:
                return event.contracts
            else:
                print(f"Event with ID {event_id} not found.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()
            
    def get_event_for_contract(self, contract_id: str):
        session = self.Session()
        try:
            contract = session.query(Contract).filter(Contract.id == contract_id).one_or_none()
            
            if contract:
                return contract.events
            else:
                print(f"Contract with ID {contract_id} not found.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()
            
    def get_company_events(self, company_id: int):
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.id == company_id).one_or_none()
            
            if company:
                events = []
                for contract in company.contracts:
                    events.extend(contract.events)
                return events
            else:
                print(f"Company with ID {company_id} not found.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()