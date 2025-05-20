from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from models import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    conv_id = Column(String, primary_key=True)
    call_id = Column(String, ForeignKey('call_logs.call_id', ondelete='CASCADE'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete='CASCADE'), nullable=True)
    user_id = Column(String, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)

    conversation_json_url = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)
    json_upload_time = Column(Float)

    call_log = relationship('CallLog', back_populates='conversation')
    agent = relationship('Agent', back_populates='conversations')
    user = relationship('User', back_populates='conversations')