from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AttendeeDetailBase(BaseModel):
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timestamp: datetime


class AttendeeDetailCreate(AttendeeDetailBase):
    user_id: str
    call_id: str


class AttendeeDetailUpdate(BaseModel):
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AttendeeDetailResponse(AttendeeDetailBase):
    user_id: str
    call_id: str

    class Config:
        orm_mode = True
