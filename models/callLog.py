from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from models import Base

class CallLog(Base):
    __tablename__ = 'call_logs'


    call_id = Column(String, primary_key=True)

    user_id = Column(String, ForeignKey('users.user_id',ondelete='CASCADE'), nullable=False, index=True)

    agent_id = Column(String, ForeignKey('agents.agent_id',ondelete='CASCADE'), nullable=False, index=True)

    json_call_key = Column(String, nullable=True, index=True)

    # --- Fields from the actual call log record ---
    agent_name = Column(String, nullable = True)
    
    call_recording_url = Column(Text, nullable=True) # Handles URLs or "No recording available"
    call_type = Column(String) # e.g., "Inbound"
    conversation_json_url = Column(Text, nullable=True) # Handles URLs or "No conversation data available"
    cost = Column(String, nullable=True) # e.g., "Free"
    
    date = Column(Date, nullable=False) # From 'date' field, e.g., "2025-04-07"
    
    duration = Column(String, nullable=True) # e.g., "00:00:00" or "00:01:23"
    end_time = Column(String, nullable=True)   
    start_time = Column(String, nullable=True) # e.g., "2025-04-07T00:00:00Z"

    reason = Column(String, nullable=True) # e.g., "Customer Inquiry"

    # --- Relationships (uncomment and adjust if User and Agent models are defined) ---
    user_profile = relationship("User", back_populates="call_logs")
    agent_profile = relationship("Agent", back_populates="call_logs")
    attendee_details = relationship("AttendeeDetail", back_populates="call_log", cascade="all, delete-orphan")
    conversation = relationship('Conversation', back_populates='call_log')
    __table_args__ = (
        UniqueConstraint('user_id', 'agent_id', name='uq_user_agent'),
    )

    def __repr__(self):
        return (f"<CallLog(id={self.call_id}, user_id='{self.user_id}', "
                f"agent_id='{self.agent_id}', "
                f"record_call_id='{self.call_id}')>")

