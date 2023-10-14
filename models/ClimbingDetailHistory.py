from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Json
from datetime import datetime

Base = declarative_base()

class ClimbingDetailHistory(Base):
    __tablename__ = 'climbing_detail_history'

    climbing_id = Column(String, primary_key=True)
    route_id = Column(String, primary_key=True)
    hold_id = Column(String, primary_key=True)
    tag_time = Column(DateTime)
    hold_seq = Column(Integer)

class ClimbingDetailHistoryModel(BaseModel):
    climbing_id: str
    route_id: str
    hold_id: str
    tag_time: str
    hold_seq: int

    class Config:
        from_attributes = True
      
    
