from pydantic import BaseModel, Field
from typing import Optional
import uuid


class BillingDetailsBase(BaseModel):
    user_id: str
    address_line1: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    card_holder_name: Optional[str] = None
    card_number_masked: Optional[str] = None
    expiry_date: Optional[str] = None
    current_plan: Optional[str] = None
    minutes_used: Optional[int] = None


class BillingDetailsCreate(BillingDetailsBase):
    billing_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class BillingDetailsUpdate(BaseModel):
    address_line1: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    card_holder_name: Optional[str] = None
    card_number_masked: Optional[str] = None
    expiry_date: Optional[str] = None
    current_plan: Optional[str] = None
    minutes_used: Optional[int] = None


class BillingDetailsOut(BillingDetailsBase):
    billing_id: str

    class Config:
        orm_mode = True
