from pydantic import BaseModel, Field
from typing import Optional
import uuid


class CallRecordBase(BaseModel):
    agent_id: str
    total_calls: Optional[int] = None
    total_duration: Optional[str] = None  # You could use time duration format if needed


class CallRecordCreate(CallRecordBase):
    call_record_id: str = Field(default_factory=lambda: str(uuid.uuid4())) 


class CallRecordUpdate(BaseModel):
    total_calls: Optional[int] = None
    total_duration: Optional[str] = None


class CallRecordRead(CallRecordBase):
    call_record_id: str

    class Config:
        orm_mode = True
