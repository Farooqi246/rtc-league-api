from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from models import Base
from sqlalchemy.orm import relationship

import uuid


class BillingDetails(Base):
    __tablename__ = 'billing_details'

    billing_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), index=True, nullable=False)

    address_line1 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True) # Renamed 'zip' to 'zip_code' to avoid conflict with Python's built-in zip
    card_holder_name = Column(String, nullable=True)
    card_number_masked = Column(String, nullable=True) # Storing only a masked version or last 4 digits is recommended
    expiry_date = Column(String, nullable=True) # Consider storing as Date type if appropriate for your DB
    current_plan = Column(String, nullable=True)
    minutes_used = Column(Integer, nullable=True)


    user_profile = relationship("User", back_populates="billing_details")
    usage_histories = relationship('UsageHistory', back_populates='billing_details',cascade="all, delete-orphan")


    def __repr__(self):
        return f"<BillingDetails(billing_id='{self.billing_id}', user_id='{self.user_id}', current_plan='{self.current_plan}')>"

