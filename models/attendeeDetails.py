from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID 
import uuid 
from models import Base

class AttendeeDetail(Base):
    __tablename__ = 'attendee_details'
    user_id = Column(String, ForeignKey('users.user_id',ondelete='CASCADE'), primary_key=True, index=True)
    call_id = Column(String, ForeignKey('call_logs.call_id',ondelete='CASCADE'), primary_key=True, index=True)

    company_name = Column(String, nullable=True) 
    email = Column(String, nullable=True)              
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)             
    timestamp = Column(DateTime, nullable=False)

    user_profile = relationship("User", back_populates="attendee_details")
    call_log = relationship("CallLog", back_populates="attendee_details")


    def __repr__(self):
        return f"<AttendeeDetail(user_id='{self.user_id}', call_id='{self.call_id}', name='{self.first_name} {self.last_name}')>"

