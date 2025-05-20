from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional


class UsageHistoryBase(BaseModel):
    billing_id: str
    user_id: str
    agent_id: str
    billed_amount: str
    date: str
    minutes: str
    total_cost: str


class UsageHistoryCreate(UsageHistoryBase):
    usage_id: str


class UsageHistoryUpdate(BaseModel):
    billed_amount: Optional[str] = None
    date: Optional[str] = None
    minutes: Optional[str] = None
    total_cost: Optional[str] = None


class UsageHistoryRead(UsageHistoryBase):
    usage_id: str

    class Config:
        orm_mode = True
