from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, TIMESTAMP, Date, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from argon2 import PasswordHasher
import argon2.exceptions
from sqlalchemy.sql import func

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.role})>"
    

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mot_de_passe = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    companies = relationship("Company", back_populates="user")
    events = relationship("Event", back_populates="user")
    
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.nom}, email={self.email}, role_id={self.role_id})>"
    
    def set_password(self, password):
        ph = PasswordHasher()
        self.mot_de_passe = ph.hash(password)

    def verify_password(self, password):
        ph = PasswordHasher()
        try:
            return ph.verify(self.mot_de_passe, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def authorisation(self, level):
        if level == 'Admin' : 
            return self.role_id == 1
        elif level == 'Gestion':
            return self.role_id == 2
        elif level == 'Sale':
            return self.role_id == 3
        elif level == 'Support':
            return self.role_id == 4
        else:
            print("Niveau d'authorisation inconnu => refusé")
            return False


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    company_name = Column(String(255), nullable=False)
    creation_date = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    update_date = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="companies") 
    contacts = relationship("Contact", back_populates="compagny")

    def __repr__(self):
        return (f"<Company(id={self.id}, compagny_name={self.compagny_name}, update_date={self.update_date})>")


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_date_start = Column(Date, nullable=False)
    event_date_end = Column(Date, nullable=False)
    location = Column(Text, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id'), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="events")

    def __repr__(self):
        return (f"<Event(id={self.id}, event_date_start={self.event_date_start}, "
                f"event_date_end={self.event_date_end}, location={self.location}, "
                f"id_user={self.id_user}, attendees={self.attendees}, notes={self.notes})>")


class Contact(Base):
    __tablename__ = 'client_contact'

    id = Column(Integer, primary_key=True, autoincrement=True)
    compagny_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    creation_date = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    update_date = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    signatory = Column(Boolean, default=False, nullable=True)

    compagny = relationship("Company", back_populates="contacts")

    def __repr__(self):
        return (f"<Contact(id={self.id}, compagny_id={self.compagny_id}, name={self.name}, "
                f"email={self.email}, phone={self.phone}, creation_date={self.creation_date}, "
                f"update_date={self.update_date}, signatory={self.signatory})>")