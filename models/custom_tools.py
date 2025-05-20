from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import Base
import uuid



class CustomTool(Base):
    __tablename__ = 'custom_tools'

    custom_tool_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String)
    parameters = Column(Text)  # storing JSON as string
    speakAfterExecution = Column(Boolean, default=False)
    speakAfterPrompt = Column(Text)
    speakDuringExecution = Column(Boolean, default=False)
    speakDuringPrompt = Column(Text)
    status = Column(String)
    createdAt = Column(String)
    updatedAt = Column(String)

    user_id = Column(String, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="custom_tools")