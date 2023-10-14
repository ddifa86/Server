from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel

Base = declarative_base()

class Crag(Base):
    __tablename__ = 'crag'

    crag_id = Column(String, primary_key=True)
    crag_name = Column(String)
    location = Column(String)
    phone_number = Column(String)
    score = Column(Float)
    avg_difficulty_level = Column(String)
    route_count = Column(Integer)    

class CragModel(BaseModel):
    crag_id: str
    crag_name: str
    location: str
    phone_number: str
    score: float
    avg_difficulty_level: str
    route_count: int    
    class Config:
        from_attributes = True
