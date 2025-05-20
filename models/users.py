from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from models.agents import Agent
from models import Base


class User(Base):
    __tablename__ = 'users'

    # The user ID from the JSON keys will be the primary key
    user_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True, nullable=False)
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String) # Note: Passwords should be hashed in a real application
    role = Column(String)


    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    call_logs = relationship("CallLog", back_populates="user_profile", cascade="all, delete-orphan")
    billing_details = relationship("BillingDetails", back_populates="user_profile", cascade="all, delete-orphan")
    usage_histories = relationship('UsageHistory', back_populates='user', foreign_keys='UsageHistory.user_id', cascade="all, delete-orphan")
    attendee_details = relationship("AttendeeDetail", back_populates="user_profile", cascade="all, delete-orphan")
    conversations = relationship('Conversation', back_populates='user')
    custom_tools = relationship("CustomTool", back_populates="user")
    knowledge_bases = relationship("KnowledgeBase", back_populates="user", cascade="all, delete-orphan")
    phone_numbers = relationship("PhoneNumber", back_populates="user", cascade="all, delete-orphan")
    phone_providers = relationship("PhoneProvider", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', email='{self.email}', role='{self.role}')>"

