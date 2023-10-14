from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class RouteHold(Base):
    __tablename__ = 'route_hold'

    crag_id = Column(String, primary_key=True)
    route_id = Column(String, primary_key=True)
    hold_id = Column(String, primary_key=True)
    hold_seq = Column(Integer)


class RouteHoldModel(BaseModel):
    crag_id: str
    route_id: str
    hold_id: str
    hold_seq: int

    class Config:
        from_attributes = True