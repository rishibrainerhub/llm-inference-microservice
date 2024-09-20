from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = os.environ["DATABASE_URL"]


# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
