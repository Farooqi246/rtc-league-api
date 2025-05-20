from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PhoneProviderBase(BaseModel):
    user_id: str
    auth_username: Optional[str] = None
    authentication: Optional[bool] = None
    created_at: Optional[str] = None  # If you want to convert to datetime, change this to Optional[datetime]
    gateway_address: Optional[str] = None
    gateway_netmask: Optional[str] = None
    gateway_port: Optional[str] = None
    gateway_sendOptionsPing: Optional[bool] = None
    gateway_type: Optional[str] = None
    password: Optional[str] = None
    provider_name: Optional[str] = None
    require_authIncoming: Optional[bool] = None
    require_authOutgoing: Optional[bool] = None
    status: Optional[str] = None

class PhoneProviderCreate(PhoneProviderBase):
    phone_provider_id: str

class PhoneProviderUpdate(BaseModel):
    auth_username: Optional[str] = None
    authentication: Optional[bool] = None
    created_at: Optional[str] = None
    gateway_address: Optional[str] = None
    gateway_netmask: Optional[str] = None
    gateway_port: Optional[str] = None
    gateway_sendOptionsPing: Optional[bool] = None
    gateway_type: Optional[str] = None
    password: Optional[str] = None
    provider_name: Optional[str] = None
    require_authIncoming: Optional[bool] = None
    require_authOutgoing: Optional[bool] = None
    status: Optional[str] = None

class PhoneProviderResponse(PhoneProviderBase):
    phone_provider_id: str

    class Config:
        orm_mode = True
