from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size = 80,
    max_overflow=17,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
