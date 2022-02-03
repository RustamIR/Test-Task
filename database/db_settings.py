import os

from sqlalchemy import create_engine, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

load_dotenv()

SERVER_POSTGRES_CONNECTION = os.getenv("SERVER_POSTGRES_CONNECTION", 'sqlite:///db.sqlite3')
engine = create_engine(SERVER_POSTGRES_CONNECTION, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

metadata.create_all(engine)
Base = declarative_base()