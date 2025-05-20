from pydantic import BaseModel, HttpUrl, constr, Field
from typing import Optional
from datetime import date

class CallLogBase(BaseModel):
    call_id: str
    user_id: str
    agent_id: str
    json_call_key: Optional[str] = None

    agent_name: Optional[str] = None

    call_recording_url: Optional[str] = None
    call_type: Optional[str] = None
    conversation_json_url: Optional[str] = None
    cost: Optional[str] = None

    date: date

    duration: Optional[str]
    end_time: Optional[str]
    start_time: Optional[str]

    reason: Optional[str]

class CallLogCreate(CallLogBase):
    pass

class CallLogUpdate(BaseModel):
    agent_name: Optional[str]
    call_recording_url: Optional[str]
    call_type: Optional[str]
    conversation_json_url: Optional[str]
    cost: Optional[str] = None
    json_call_key: Optional[str] = None
    duration: Optional[str] = None
    end_time: Optional[str] = None
    start_time: Optional[str] = None

    reason: Optional[str] = None

class CallLogInDBBase(CallLogBase):
    call_id: str

    class Config:
        orm_mode = True

class CallLogRead(CallLogInDBBase):
    pass
