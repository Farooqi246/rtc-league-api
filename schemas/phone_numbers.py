from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PhoneNumberBase(BaseModel):
    user_id: str
    agent_id: Optional[str] = None
    auth_id: Optional[str] = None
    transfer_audioUrl: Optional[str] = None
    callTransfer: Optional[bool] = True
    transferNumber: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    password: Optional[str] = None
    status: Optional[str] = None
    trunkName: Optional[str] = None


class PhoneNumberCreate(PhoneNumberBase):
    phone_number: str


class PhoneNumberUpdate(BaseModel):
    agent_id: Optional[str] = None
    auth_id: Optional[str] = None
    transfer_audioUrl: Optional[str] = None
    callTransfer: Optional[bool] = None
    transferNumber: Optional[str] = None
    updated_at: Optional[datetime] = None
    password: Optional[str] = None
    status: Optional[str] = None
    trunkName: Optional[str] = None


class PhoneNumberOut(PhoneNumberBase):
    phone_number: str

    class Config:
        orm_mode = True
