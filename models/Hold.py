from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Hold(Base):
    __tablename__ = 'hold'

    crag = Column(String, primary_key=True)
    hold_id = Column(Integer, Sequence('hold_id_sequence'), primary_key=True, autoincrement=True)
    tag_id = Column(String, index=True)
    hold_type = Column(String)
    hold_size = Column(String)
    hold_shape = Column(String)
    hold_color = Column(String)

    def __repr__(self):
        return f"Hold(crag='{self.crag}', hold_id={self.hold_id}, tag_id='{self.tag_id}', hold_type='{self.hold_type}', hold_size='{self.hold_size}', hold_shape='{self.hold_shape}', hold_color='{self.hold_color}')"
    

class HoldModel(BaseModel):
    crag: str
   # hold_id: int
    tag_id: str
    hold_type: str
    hold_size: str
    hold_shape: str
    hold_color: str
    class Config:
        from_attributes = True
    
