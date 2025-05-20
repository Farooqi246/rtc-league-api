from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
import uuid


class ConversationBase(BaseModel):
    call_id: str
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_json_url: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    json_upload_time: Optional[float] = None


class ConversationCreate(ConversationBase):
    conv_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class ConversationUpdate(BaseModel):
    call_id: Optional[str] = None
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_json_url: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    json_upload_time: Optional[float] = None


class ConversationResponse(ConversationBase):
    conv_id: str

    class Config:
        orm_mode = True
