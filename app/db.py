from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

PASS = os.getenv("PASSWORD")


SLQALCHEMY_DB_URL = f"""postgresql://postgres:{PASS}@localhost/fastApi"""
engine = create_engine(SLQALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
