from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, inspect
from app.models.models import User, Base, Role
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
            
    def get_all_users_name(self):
        session = self.Session()
        try:
            names = session.query(User.nom).all()
            return [name[0] for name in names]
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
            
    def add_user(self, name: str, email: str, password: str, role_id: int):
        session = self.Session()
        try:
            new_user = User(nom=name, email=email, role_id=role_id)
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