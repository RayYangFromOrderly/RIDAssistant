import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, DateTime

from .db import engine

Base = declarative_base()

Base.metadata.create_all(engine)


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    c_at = Column(DateTime, default=datetime.datetime.utcnow)
