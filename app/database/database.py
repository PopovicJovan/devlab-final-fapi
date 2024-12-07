from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()
settings = Settings()
engine = create_engine(settings.db_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


database = Annotated[Session, Depends(get_db)]
