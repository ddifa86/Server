from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)    
    role = Column(String)
    crew = Column(String)    
    leadlevel = Column(Float)    

class UserModel(BaseModel):
    class Config:
        from_attributes = True
    user_id: str
    password: str
    name: str
    role: str
    crew: str
    leadlevel: float
