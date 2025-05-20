from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.conversation import Conversation as ConversationModel  # your SQLAlchemy model
from schemas.conversation import ConversationCreate, ConversationUpdate, ConversationResponse  # your Pydantic schema
from database import get_db  # your DB session dependency

router = APIRouter(prefix="/conversations", tags=["Conversations"])


#====================== Create Conversation ======================
@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = ConversationModel(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation



#====================== Get All Conversations ======================
@router.get("/", response_model=List[ConversationResponse])
def get_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ConversationModel).offset(skip).limit(limit).all()


#====================== Get Conversation by ID ======================
@router.get("/{conv_id}", response_model=ConversationResponse)
def get_conversation(conv_id: str, db: Session = Depends(get_db)):
    conversation = db.query(ConversationModel).filter(ConversationModel.conv_id == conv_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


#====================== Update Conversation ======================
@router.put("/{conv_id}", response_model=ConversationResponse)
def update_conversation(conv_id: str, update_data: ConversationUpdate, db: Session = Depends(get_db)):
    conversation = db.query(ConversationModel).filter(ConversationModel.conv_id == conv_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(conversation, key, value)

    db.commit()
    db.refresh(conversation)
    return conversation


#====================== Delete Conversation ======================
@router.delete("/{conv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conv_id: str, db: Session = Depends(get_db)):
    conversation = db.query(ConversationModel).filter(ConversationModel.conv_id == conv_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conversation)
    db.commit()
