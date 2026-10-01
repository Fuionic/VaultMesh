import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

password = os.getenv("DATABASE_PASSWORD")
if not password:
    raise RuntimeError("Set DATABASE_PASSWORD in the .env file")

db_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/Vault"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    # Register the model before creating tables from Base.metadata.
    from model import transactionmodel  
    

    Base.metadata.create_all(bind=engine)
