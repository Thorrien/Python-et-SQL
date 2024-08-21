from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, inspect
from app.models.models import User, event_contract, Base, Role
from app.models.models import Company, Event, Contact, Contract, Text
from app.utils import config
import sentry_sdk

class UserDAO:
    def __init__(self):
        self.engine = create_engine(
            f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@'
            f'{config.DB_HOST}/{config.DB_NAME}',
            echo=False
        )
        self.base = Base
        self.base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def tables(self):
        """
        Affiche les tables présentes dans la base de données ainsi que les détails de chaque colonne 
        pour chaque table, y compris le nom et le type de colonne.
        """
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
        """
        Récupère et retourne tous les utilisateurs de la base de données.
        """
        session = self.Session()
        try:
            users = session.query(User).all()
            return users
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_user_with_role_name(self):
        """
        Récupère et retourne tous les utilisateurs de la 
        base de données avec le role détaillé.
        """
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
        """
        Récupère et retourne un utilisateur de la base de données en fonction de son ID.

        Entrées:
        - user_id (int): L'ID de l'utilisateur à récupérer.

        """
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_user_by_email(self, email: str):
        """
        Récupère et retourne un utilisateur de la base de données en fonction de son email.

        Entrées:
        - email (str): L'email de l'utilisateur à récupérer.
        
        """
        session = self.Session()
        try:
            user = session.query(User).filter(
                User.email == email
                ).one_or_none()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_user_by_role(self, role_id: int):
        """
        Récupère et retourne tous les utilisateurs de la base de données ayant un rôle spécifique.

        Entrées:
        - role_id (int): L'ID du rôle pour lequel récupérer les utilisateurs.

        """
        session = self.Session()
        try:
            user = session.query(User).filter(User.role_id == role_id).all()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def add_user(self, name: str, email: str, password: str, role_id: int):
        """
        Ajoute un nouvel utilisateur à la base de 
        données avec les informations fournies.

        Entrées:
        - name (str): Le nom de l'utilisateur.
        - email (str): L'email de l'utilisateur.
        - password (str): Le mot de passe de l'utilisateur.
        - role_id (int): L'ID du rôle attribué à l'utilisateur.
        """
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
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("action", "create")
                scope.set_tag("collaborator_name", name)
            sentry_sdk.capture_message(f"Collaborateur Créé : Nom={name}, Email={email}")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
        
    def update_pasword_user(self, user_id: int, password: str):
        """
        Met à jour le mot de passe d'un utilisateur spécifique dans la base de données.

        Entrées:
        - user_id (int): L'ID de l'utilisateur dont le mot de passe doit être mis à jour.
        - password (str): Le nouveau mot de passe à attribuer à l'utilisateur.
        """
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
        """
        Met à jour les informations d'un utilisateur spécifique dans la base de données.

        Entrées:
        - user_id (int): L'ID de l'utilisateur à mettre à jour.
        - name (str): Le nouveau nom de l'utilisateur.
        - email (str): Le nouvel email de l'utilisateur.
        - role_id (int): Le nouvel ID de rôle attribué à l'utilisateur.
        """
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                user.nom = name
                user.email = email
                user.role_id = role_id
                session.commit()
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag("action", "update")
                    scope.set_tag("collaborator_name", name)
                sentry_sdk.capture_message(f"Collaborateur modifié : Nom={user.nom}, Email={user.email}")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def delete_user(self, user_id: int):
        """
        Supprime un utilisateur spécifique de la base de données.

        Entrées:
        - user_id (int): L'ID de l'utilisateur à supprimer.
        """
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                session.delete(user)
                session.commit()
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag("action", "delete")
                    scope.set_tag("collaborator_name", user.nom)
                sentry_sdk.capture_message(f"Collaborateur supprimé : Nom={user.nom}, Email={user.email}")

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_roles(self):
        """
        Récupère et retourne tous les rôles de la base de données.
        """
        session = self.Session()
        try:
            roles = session.query(Role).all()
            return roles
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def add_company(self, name: str, user_id: int, address: str):
        """
        Ajoute une nouvelle entreprise à la base de données avec les informations fournies.

        Entrées:
        - name (str): Le nom de l'entreprise.
        - user_id (int): L'ID de l'utilisateur associé à l'entreprise.
        - address (str): L'adresse de l'entreprise.
        """    
        session = self.Session()
        try:
            new_company = Company(
                company_name=name,
                address=address,
                user_id=user_id
                )
            session.add(new_company)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_company(self, id: int, name: str, address: str, user_id: int):
        """
        Met à jour les informations d'une entreprise spécifique dans la base de données.

        Entrées:
        - id (int): L'ID de l'entreprise à mettre à jour.
        - name (str): Le nouveau nom de l'entreprise.
        - address (str): La nouvelle adresse de l'entreprise.
        - user_id (int): Le nouvel ID de l'utilisateur associé à l'entreprise.
        """
        session = self.Session()
        try:
            company = session.query(Company).filter(
                Company.id == id
                ).one_or_none()
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
        """
        Supprime une entreprise spécifique de la base de données.

        Entrées:
        - company_id (int): L'ID de l'entreprise à supprimer.
        """
        session = self.Session()
        try:
            company = session.query(Company).filter(
                Company.id == company_id
                ).one_or_none()
            if company:
                session.delete(company)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_company(self):
        """
        Récupère et retourne toutes les entreprises de la base de données.
        """
        session = self.Session()
        try:
            companys = session.query(Company).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_company_without_user(self):
        """
        Récupère et retourne toutes les entreprises de la base de données qui ne sont associées à aucun utilisateur.
        """
        session = self.Session()
        try:
            companys = session.query(Company).filter(
                Company.user_id == None).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_company(self, id: int):
        """
        Récupère et retourne une entreprise spécifique de la base de données en fonction de son ID.

        Entrées:
        - id (int): L'ID de l'entreprise à récupérer.
        """
        session = self.Session()
        try:
            company = session.query(Company).filter(
                Company.id == id
                ).one_or_none()
            return company
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_company_by_user_id(self, user_id: int):
        """
        Récupère et retourne toutes les entreprises associées à un utilisateur spécifique dans la base de données.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les entreprises.
        """
        session = self.Session()
        try:
            companys = session.query(Company).filter(
                Company.user_id == user_id
                ).all()
            return companys
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def add_event(self, event_date_start, event_date_end, location: str,
                  id_user: int, attendees: int, notes=None):
        """
        Ajoute un nouvel événement à la base de données avec 
        les informations fournies.

        Entrées:
        - event_date_start: La date et l'heure de début de l'événement.
        - event_date_end: La date et l'heure de fin de l'événement.
        - location (str): Le lieu de l'événement.
        - id_user (int): L'ID de l'utilisateur associé à l'événement.
        - attendees (int): Le nombre de participants à l'événement.
        - notes (str, optionnel): Notes supplémentaires sur l'événement.

        Retourne:
        - int: L'ID de l'événement ajouté.

        """
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
            return new_event.id
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_event(self, id: int):
        """
        Récupère et retourne un événement spécifique de la base
        de données en fonction de son ID.

        Entrées:
        - id (int): L'ID de l'événement à récupérer.

        """
        session = self.Session()
        try:
            event = session.query(Event).filter(Event.id == id).one_or_none()
            return event
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_events_by_user_id(self, user_id):
        """
        Récupère et retourne tous les événements associés à un utilisateur spécifique.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les événements.

        """
        session = self.Session()
        try:
            events = session.query(Event).filter(
                Event.id_user == user_id
                ).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_events_without_user(self):
        """
        Récupère et retourne tous les événements non associés à un utilisateur.

        Gère les exceptions potentielles et ferme la session après l'opération.
        """
        session = self.Session()
        try:
            events = session.query(Event).filter(Event.id_user == None).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_events(self):
        """
        Récupère et retourne tous les événements de la base de données.

        Gère les exceptions potentielles et ferme la session après l'opération.
        """
        session = self.Session()
        try:
            events = session.query(Event).all()
            return events
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def update_event(self, id: int, event_date_start, event_date_end,
                     location: str, id_user: int, attendees: int, notes):
        """
        Met à jour les informations d'un événement spécifique dans la base de données.

        Entrées:
        - id (int): L'ID de l'événement à mettre à jour.
        - event_date_start: La nouvelle date et heure de début de l'événement.
        - event_date_end: La nouvelle date et heure de fin de l'événement.
        - location (str): Le nouveau lieu de l'événement.
        - id_user (int): Le nouvel ID de l'utilisateur associé à l'événement.
        - attendees (int): Le nouveau nombre de participants.
        - notes: Les nouvelles notes sur l'événement.
        """

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
        """
        Supprime un événement spécifique de la base de données.

        Entrées:
        - event_id (int): L'ID de l'événement à supprimer.

        """
        session = self.Session()
        try:
            event = session.query(Event).filter(
                Event.id == event_id
                ).one_or_none()
            if event:
                session.delete(event)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def add_contact(self, compagny_id: int, name: str,
                    email: str, phone: str, signatory=False):
        """
        Ajoute un nouveau contact à la base de données avec les informations fournies.

        Entrées:
        - compagny_id (int): L'ID de l'entreprise associée au contact.
        - name (str): Le nom du contact.
        - email (str): L'email du contact.
        - phone (str): Le numéro de téléphone du contact.
        - signatory (bool, optionnel): Indique si le contact est signataire.

        """
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

    def update_contact(self, id: int, compagny_id: int,
                       name: str, email: str, phone: str, signatory):
        """
        Met à jour les informations d'un contact spécifique dans la base de données.

        Entrées:
        - id (int): L'ID du contact à mettre à jour.
        - compagny_id (int): Le nouvel ID de l'entreprise associée au contact.
        - name (str): Le nouveau nom du contact.
        - email (str): Le nouvel email du contact.
        - phone (str): Le nouveau numéro de téléphone du contact.
        - signatory: Met à jour le statut de signataire du contact.
        """
        session = self.Session()
        try:
            contact = session.query(Contact).filter(
                Contact.id == id
                ).one_or_none()
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
        """
        Supprime un contact spécifique de la base de données.

        Entrées:
        - contact_id (int): L'ID du contact à supprimer.
        """
        session = self.Session()
        try:
            contact = session.query(Contact).filter(
                Contact.id == contact_id
                ).one_or_none()
            if contact:
                session.delete(contact)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_contact(self, id: int):
        """
        Récupère et retourne un contact spécifique de la base de données en fonction de son ID.

        Entrées:
        - id (int): L'ID du contact à récupérer.
        """

        session = self.Session()
        try:
            contact = session.query(Contact).filter(
                Contact.id == id
                ).one_or_none()
            return contact
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contact_by_company_id(self, id):
        """
        Récupère et retourne tous les contacts associés à une entreprise spécifique dans la base de données.

        Entrées:
        - id (int): L'ID de l'entreprise pour laquelle récupérer les contacts.
        """
        session = self.Session()
        try:
            contacts = session.query(Contact).filter(
                Contact.compagny_id == id
                ).all()
            return contacts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contact(self):
        """
        Récupère et retourne tous les contacts de la base de données.

        Gère les exceptions potentielles et ferme la session après l'opération.
        """
        session = self.Session()
        try:
            contacts = session.query(Contact).all()
            return contacts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contacts_by_user_id(self, user_id: int):
        """
        Récupère et retourne tous les contacts associés aux entreprises d'un utilisateur spécifique.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les contacts.

        """
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
        """
        Supprime un contrat spécifique de la base de données.

        Entrées:
        - contract_id (int): L'ID du contrat à supprimer.
        """
        session = self.Session()
        try:
            contract = session.query(Contract).filter(
                Contract.id == contract_id
                ).one_or_none()
            if contract:
                session.delete(contract)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def get_contract(self, contract_id: int):
        """
        Récupère et retourne un contrat spécifique de la base de données en fonction de son ID.

        Entrées:
        - contract_id (int): L'ID du contrat à récupérer.
        """
        session = self.Session()
        try:
            contact = session.query(Contract).filter(
                Contract.id == contract_id
                ).one_or_none()
            return contact
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contract(self):
        """
        Récupère et retourne tous les contrats de la base de données.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contracts_by_user_id(self, user_id: int):
        """
        Récupère et retourne tous les contrats associés à un utilisateur spécifique dans la base de données.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les contrats.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(
                Contract.user_id == user_id
                ).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contracts_by_company_id(self, compagny_id: int):
        """
        Récupère et retourne tous les contrats associés à une entreprise spécifique dans la base de données.

        Entrées:
        - compagny_id (int): L'ID de l'entreprise pour laquelle récupérer les contrats.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(
                Contract.compagny_id == compagny_id
                ).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_my_contracts_sign(self, user_id: int):
        """
        Récupère et retourne tous les contrats signés associés à un utilisateur spécifique.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les contrats signés.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(
                Contract.user_id == user_id, Contract.sign == 1).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contracts_without_user(self):
        """
        Récupère et retourne tous les contrats qui ne sont associés à aucun utilisateur.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(
                Contract.user_id == None
                ).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def get_all_contracts_without_full_paiement(self, user_id: int):
        """
        Récupère et retourne tous les contrats associés à un utilisateur spécifique 
        dont le paiement total n'a pas été effectué.

        Entrées:
        - user_id (int): L'ID de l'utilisateur pour lequel récupérer les contrats non payés en totalité.
        """
        session = self.Session()
        try:
            contracts = session.query(Contract).filter(
                Contract.user_id == user_id,
                Contract.current_amont < Contract.total_amont).all()
            return contracts
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def add_contract(self, compagny_id: int, user_id: int, total_amont: float,
                     current_amont: float, sign=False):
        """
        Ajoute un nouveau contrat à la base de données avec les informations fournies.

        Entrées:
        - compagny_id (int): L'ID de l'entreprise associée au contrat.
        - user_id (int): L'ID de l'utilisateur associé au contrat.
        - total_amont (float): Le montant total du contrat.
        - current_amont (float): Le montant actuel payé pour le contrat.
        - sign (bool, optionnel): Indique si le contrat est signé.
        """
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

    def update_contract(self, id: int, compagny_id: int, user_id: int,
                        total_amont: float, current_amont: float, sign=False):
        """
        Met à jour les informations d'un contrat spécifique dans la base de données.

        Entrées:
        - id (int): L'ID du contrat à mettre à jour.
        - compagny_id (int): Le nouvel ID de l'entreprise associée au contrat.
        - user_id (int): Le nouvel ID de l'utilisateur associé au contrat.
        - total_amont (float): Le nouveau montant total du contrat.
        - current_amont (float): Le nouveau montant actuel payé pour le contrat.
        - sign (bool, optionnel): Met à jour le statut de signature du contrat.
        """
        session = self.Session()
        try:
            contract = session.query(Contract).filter(
                Contract.id == id
                ).one_or_none()
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
        """
        Associe un contrat spécifique à un événement dans la base de données.

        Entrées:
        - event_id (int): L'ID de l'événement auquel associer le contrat.
        - contract_id (str): L'ID du contrat à associer à l'événement.

        """
        session = self.Session()
        try:
            event = session.query(Event).filter(
                Event.id == event_id
                ).one_or_none()
            contract = session.query(Contract).filter(
                Contract.id == contract_id
                ).one_or_none()

            if event and contract:
                event.contracts.append(contract)
                session.commit()
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

    def get_event_contract(self, event_id: int, contract_id: str):
        """
        Récupère et retourne un événement et un contrat spécifiques si le contrat est associé à l'événement.

        Entrées:
        - event_id (int): L'ID de l'événement à vérifier.
        - contract_id (str): L'ID du contrat à vérifier.

        Retourne:
        - tuple: Un tuple contenant l'événement et le contrat s'ils sont associés, sinon (None, None).
        """
        session = self.Session()
        try:
            event = session.query(Event).filter(
                Event.id == event_id
            ).one_or_none()

            contract = session.query(Contract).filter(
                Contract.id == contract_id
            ).one_or_none()

            if event and contract:
                if contract in event.contracts:
                    return event, contract
                else:
                    print(f"Contract with ID {contract_id} is not linked to Event with ID {event_id}.")
                    return None, None
            else:
                if not event:
                    print(f"Event with ID {event_id} not found.")
                if not contract:
                    print(f"Contract with ID {contract_id} not found.")
                return None, None
        except Exception as e:
            print(f"Error: {e}")
            return None, None
        finally:
            session.close()


    def modify_event_contract(self, event_id: int,
                              old_contract_id: str,
                              new_contract_id: str):
        """
        Modifie l'association d'un contrat pour un événement en remplaçant un ancien contrat par un nouveau.

        Entrées:
        - event_id (int): L'ID de l'événement dont le contrat doit être modifié.
        - old_contract_id (str): L'ID de l'ancien contrat à retirer de l'événement.
        - new_contract_id (str): L'ID du nouveau contrat à ajouter à l'événement.
        """
        session = self.Session()
        try:

            event = session.query(Event).filter(
                Event.id == event_id
                ).one_or_none()
            old_contract = session.query(Contract).filter(
                Contract.id == old_contract_id
                ).one_or_none()
            new_contract = session.query(Contract).filter(
                Contract.id == new_contract_id
                ).one_or_none()

            if event and old_contract and new_contract:

                if old_contract in event.contracts:
                    event.contracts.remove(old_contract)
                    event.contracts.append(new_contract)
                    session.commit()
                else:
                    print(f"Contract {old_contract_id} / {event_id}")
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
        """
        Supprime l'association d'un contrat spécifique d'un événement.

        Entrées:
        - event_id (int): L'ID de l'événement dont le contrat doit être dissocié.
        - contract_id (str): L'ID du contrat à retirer de l'événement.
        """
        session = self.Session()
        try:

            event = session.query(Event).filter(
                Event.id == event_id
                ).one_or_none()
            contract = session.query(Contract).filter(
                Contract.id == contract_id
                ).one_or_none()

            if event and contract:

                if contract in event.contracts:
                    event.contracts.remove(contract)
                    session.commit()
                else:
                    print(f"Contract {contract_id} / {event_id}")
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
        """
        Récupère et retourne tous les contrats associés à un événement spécifique.

        Entrées:
        - event_id (int): L'ID de l'événement pour lequel récupérer les contrats.

        Retourne:
        - list: Une liste de contrats associés à l'événement.
        """
        session = self.Session()
        try:
            event = session.query(Event).filter(
                Event.id == event_id
                ).one_or_none()

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
        """
        Récupère et retourne tous les événements associés à un contrat spécifique.

        Entrées:
        - contract_id (str): L'ID du contrat pour lequel récupérer les événements.

        Retourne:
        - list: Une liste d'événements associés au contrat.
        """
        session = self.Session()
        try:
            contract = session.query(Contract).filter(
                Contract.id == contract_id
                ).one_or_none()

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
        """
        Récupère et retourne tous les événements associés à une entreprise spécifique via ses contrats.

        Entrées:
        - company_id (int): L'ID de l'entreprise pour laquelle récupérer les événements.

        Retourne:
        - list: Une liste d'événements associés aux contrats de l'entreprise.
        """
        session = self.Session()
        try:
            company = session.query(Company).filter(
                Company.id == company_id
                ).one_or_none()

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

    def get_all_event_details_with_company(self):
        """
        Récupère et retourne les détails de tous les événements avec les informations associées aux contrats 
        et aux entreprises.

        Retourne:
        - list: Une liste de dictionnaires contenant les détails des événements, contrats, et entreprises associés.
        """
        session = self.Session()
        try:
            results = session.query(
                Event.id.label('event_id'),
                Event.event_date_start,
                Event.event_date_end,
                Event.location,
                Event.attendees,
                Event.id_user,
                Event.notes,
                Contract.id.label('contract_id'),
                Contract.total_amont,
                Contract.current_amont,
                Company.id.label('company_id'),
                Company.company_name,
                Company.address
            ).join(event_contract, Event.id == event_contract.c.event_id) \
             .join(Contract, event_contract.c.contract_id == Contract.id) \
             .join(Company, Contract.compagny_id == Company.id) \
             .all()

            event_details_list = []
            for result in results:
                event_details_list.append({
                    "event_id": result.event_id,
                    "event_date_start": result.event_date_start,
                    "event_date_end": result.event_date_end,
                    "location": result.location,
                    "attendees": result.attendees,
                    "id_user": result.id_user,
                    "notes": result.notes,
                    "contract_id": result.contract_id,
                    "total_amont": result.total_amont,
                    "current_amont": result.current_amont,
                    "company_id": result.company_id,
                    "company_name": result.company_name,
                    "address": result.address
                })

            return event_details_list
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()

    def get_text(self, id: int):
        """
        Récupère et retourne un texte spécifique de la base de données en fonction de son ID.

        Entrées:
        - id (int): L'ID du texte à récupérer.
        """
        session = self.Session()
        try:
            text = session.query(Text).filter(Text.id == id).one_or_none()
            return text
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

    def update_text(self, id: int, text: str):
        """
        Met à jour le contenu d'un texte spécifique dans la base de données.

        Entrées:
        - id (int): L'ID du texte à mettre à jour.
        - text (str): Le nouveau contenu du texte.
        """
        session = self.Session()
        try:
            texte = session.query(Text).filter(Text.id == id).one_or_none()
            if texte:
                texte.id = id
                texte.data = text
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
