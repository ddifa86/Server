from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Route(Base):
    __tablename__ = 'route'

    crag_id = Column(String, primary_key=True)
    route_id = Column(String, primary_key=True)
    route_name = Column(String)
    difficulty_level = Column(String)
    technical_score = Column(Float)
    physical_score = Column(Float)
    route_complexity_score = Column(Float)
    additional_score = Column(Float)
    start_hold_id = Column(String)
    end_hold_id = Column(String)
    hold_count = Column(Integer)    
    
class RouteModel(BaseModel):
    crag_id: str
    route_id: str
    route_name: str
    #difficulty_level: str
    #technical_score: float
    #physical_score: float
    #route_complexity_score: float
    #additional_score: float
    start_hold_id: str
    end_hold_id: str
    hold_count: int    
    class Config:
        from_attributes = True