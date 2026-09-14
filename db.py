from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

sessionLocal = sessionmaker(
    bind=engine
)

def get_db():
    db = sessionLocal
    try:
        yield db

    finally:
        db.close()


