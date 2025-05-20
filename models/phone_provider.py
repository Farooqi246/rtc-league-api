from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
import uuid

class PhoneProvider(Base):
    __tablename__ = 'phone_providers'

    user_id = Column(String, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    phone_provider_id = Column(String, primary_key=True)
    auth_username = Column(String, nullable=True)
    authentication = Column(Boolean)
    created_at = Column(String, nullable=True)
    gateway_address = Column(String, nullable=True)
    gateway_netmask = Column(String, nullable=True)
    gateway_port = Column(String, nullable=True)
    gateway_sendOptionsPing = Column(Boolean, nullable=True)
    gateway_type = Column(String, nullable=True)
    password = Column(String, nullable=True)
    provider_name = Column(String, nullable=True)
    require_authIncoming = Column(Boolean, nullable=True)
    require_authOutgoing = Column(Boolean, nullable=True)
    status = Column(String, nullable=True)

    user = relationship("User", back_populates="phone_providers")