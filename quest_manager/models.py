from core.models import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

class Quest(BaseModel):
    __tablename__ = 'quest'
    name = Column(String)
    description = Column(String)

class QuestSeries(BaseModel):
    __tablename__ = 'quest_series'
    name = Column(String)
    description = Column(String)
