from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


Base = declarative_base()

class UserClimbDiary(Base):
    __tablename__ = 'user_climb_diary'

    climbing_date = Column(String(8), primary_key=True)
    user_id = Column(String(255))
    diary_text = Column(Text, nullable=True)



class UserClimbDiaryModel(BaseModel):
    climbing_date: str
    user_id: str
    diary_text: str
    class Config:
        from_attributes = True
