from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, inspect
from app.models.models import User, Base, Role, Company, Event, Contact
from app.utils import config


class UserDAO:
    def __init__(self):
        self.engine = create_engine(
            f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}',
            echo=True
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

    def update_user(self, user_id: int, name: str, email: str, password: str, role_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                user.nom = name
                user.email = email
                user.set_password(password)
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


    def add_company(self, name: str, user_id: int ):
        session = self.Session()
        try:
            new_company = Company(
                compagny_name=name, 
                user_id=user_id
                )
            session.add(new_company)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_company(self, id: int, name: str, user_id: int ):
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.id == id).one_or_none()
            if company:
                company.compagny_name = name
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