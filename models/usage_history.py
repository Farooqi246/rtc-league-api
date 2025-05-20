from sqlalchemy import Column, String, DateTime, Interval, Numeric, ForeignKey
from datetime import datetime, timedelta
from models import Base
from sqlalchemy.orm import relationship

class UsageHistory(Base):
    __tablename__ = 'usage_history'

    usage_id = Column(String, primary_key=True)
    
    billing_id = Column(String, ForeignKey('billing_details.billing_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete='CASCADE'), nullable=False)

    billed_amount = Column(String, nullable=False)  # Decimal amount
    date = Column(String, nullable=False)  # Python datetime object
    minutes = Column(String, nullable=False)  # Python timedelta object
    total_cost = Column(String, nullable=False)

    user = relationship("User", back_populates="usage_histories")
    billing_details = relationship("BillingDetails", back_populates="usage_histories")
    agent = relationship("Agent", back_populates="usage_histories")


   