# routers/knowledge_base.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from models.knowledgeBases import KnowledgeBase
from database import get_db
from schemas.knowledgeBase import KnowledgeBaseCreate, KnowledgeBaseRead

router = APIRouter(prefix="/knowledge_base", tags=["Knowledge Base"])

# CREATE
@router.post("/", response_model=KnowledgeBaseRead)
def create_knowledge_base(kb: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    kb_id = str(uuid.uuid4())
    db_kb = KnowledgeBase(bases_id=kb_id, **kb.dict())
    db.add(db_kb)
    db.commit()
    db.refresh(db_kb)
    return db_kb

# READ ALL
@router.get("/", response_model=list[KnowledgeBaseRead])
def get_all_knowledge_bases(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).all()

# READ ONE
@router.get("/{bases_id}", response_model=KnowledgeBaseRead)
def get_knowledge_base(bases_id: str, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.bases_id == bases_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    return kb

# UPDATE
@router.put("/{bases_id}", response_model=KnowledgeBaseRead)
def update_knowledge_base(bases_id: str, kb_update: KnowledgeBaseCreate, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.bases_id == bases_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    for key, value in kb_update.dict().items():
        setattr(kb, key, value)
    db.commit()
    db.refresh(kb)
    return kb

# DELETE
@router.delete("/{bases_id}")
def delete_knowledge_base(bases_id: str, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.bases_id == bases_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    db.delete(kb)
    db.commit()
    return {"detail": "Knowledge base deleted successfully"}
