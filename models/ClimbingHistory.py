from sqlalchemy import Column, String, Integer, Float, Boolean,DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class ClimbingHistory(Base):
    __tablename__ = 'climbing_history'

    climbing_id = Column(String, primary_key=True)
    route_id = Column(String)
    user_id = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    climbing_date = Column(String)
    climbing_time = Column(Float)
    progress = Column(Float)
    completion_status = Column(Boolean)

class ClimbingHistoryModel(BaseModel):
    climbing_id: str
    route_id: str
    user_id: str
    start_time: str
    end_time: str
    climbing_date: str
    climbing_time: float
    progress: float
    completion_status: bool

    class Config:
        from_attributes = True
