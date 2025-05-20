from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
import uuid

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    bases_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
    uploaded_at = Column(String, nullable=False)
    type = Column(String, nullable=False)
    size = Column(String, nullable=False)

    user_id = Column(String, ForeignKey('users.user_id',ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="knowledge_bases")
