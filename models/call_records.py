
from models import Base
from sqlalchemy import Column, String, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship


class CallRecord(Base):
    __tablename__ = 'call_records'

    call_record_id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete="CASCADE"), unique=True)
    total_calls = Column(Integer)
    total_duration = Column(String)  # You can convert this to seconds or a `Time` object if needed

    agent = relationship('Agent', back_populates='call_record')