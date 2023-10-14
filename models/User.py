from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(255), primary_key=True)
    password = Column(String(20))
    name = Column(String(100))    
    email = Column(String(100))
    role = Column(String(20))

class UserModel(BaseModel):
    class Config:
        from_attributes = True
    user_id: str
    password: str
    name: str
    email: str
    role: str
