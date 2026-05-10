from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextpilot.config import settings

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
