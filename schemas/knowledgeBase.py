from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class KnowledgeBaseBase(BaseModel):
    name: str
    content: str
    created_at: str  # Ideally should be datetime
    uploaded_at: str  # Ideally should be datetime
    type: str
    size: str
    user_id: str

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseRead(KnowledgeBaseBase):
    bases_id: str

    class Config:
        orm_mode = True
