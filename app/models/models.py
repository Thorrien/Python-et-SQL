from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from argon2 import PasswordHasher
import argon2.exceptions

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mot_de_passe = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role_id={self.role_id})>"
    
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