from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
import uuid

class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    user_id = Column(String, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete='CASCADE'), nullable=True)
    auth_id = Column(String, nullable=True)
    transfer_audioUrl = Column(Text, nullable=True)
    callTransfer = Column(Boolean, default=True)
    transferNumber = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    phone_number = Column(String, primary_key=True)
    password = Column(String, nullable=True)
    status = Column(String, nullable=True)
    trunkName = Column(String, nullable=True)


    user = relationship("User", back_populates="phone_numbers")
