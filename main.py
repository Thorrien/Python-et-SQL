from sqlalchemy import create_engine, Column, Integer, String, inspect, MetaData

from sqlalchemy.orm import sessionmaker, declarative_base
from utils import config

engine = create_engine(f'mysql+mysqldb://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
metadata.reflect(bind=engine)

inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables in the database:")
for table in tables:
    print(table)
    print(" ")
    tableentiere = metadata.tables[table]
    print("########DETAIL###########")
    for column in tableentiere.columns:
        print(f"  - Column: {column.name}, Type: {column.type}")
    print(" ")
    print(" ")
