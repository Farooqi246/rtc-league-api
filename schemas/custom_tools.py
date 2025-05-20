from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class CustomToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    parameters: Optional[str] = None  # Consider using `dict` if you're dealing with actual JSON
    speakAfterExecution: Optional[bool] = False
    speakAfterPrompt: Optional[str] = None
    speakDuringExecution: Optional[bool] = False
    speakDuringPrompt: Optional[str] = None
    status: Optional[str] = None
    createdAt: Optional[str] = None  # Consider using datetime if you store datetime strings
    updatedAt: Optional[str] = None
    user_id: str


class CustomToolCreate(CustomToolBase):
    custom_tool_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))


class CustomToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    parameters: Optional[str] = None
    speakAfterExecution: Optional[bool] = None
    speakAfterPrompt: Optional[str] = None
    speakDuringExecution: Optional[bool] = None
    speakDuringPrompt: Optional[str] = None
    status: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    user_id: Optional[str] = None


class CustomToolRead(CustomToolBase):
    custom_tool_id: str

    class Config:
        orm_mode = True
