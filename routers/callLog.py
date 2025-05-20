from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.callLog import CallLog  # Your SQLAlchemy model
from schemas.callLog import CallLogCreate, CallLogRead, CallLogUpdate  # Your Pydantic schemas
from database import get_db  # Session dependency

router = APIRouter(
    prefix="/call_logs",
    tags=["Call Logs"]
)

# --- Create ---
@router.post("/", response_model=CallLogRead, status_code=status.HTTP_201_CREATED)
def create_call_log(call_log: CallLogCreate, db: Session = Depends(get_db)):
    db_call_log = CallLog(**call_log.dict())
    db.add(db_call_log)
    try:
        db.commit()
        db.refresh(db_call_log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create: {e}")
    return db_call_log

# --- Read all ---
@router.get("/", response_model=List[CallLogRead])
def read_call_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CallLog).offset(skip).limit(limit).all()

# --- Read by ID ---
@router.get("/{call_id}", response_model=CallLogRead)
def read_call_log(call_id: str, db: Session = Depends(get_db)):
    call_log = db.query(CallLog).filter(CallLog.call_id == call_id).first()
    if not call_log:
        raise HTTPException(status_code=404, detail="Call log not found")
    return call_log

# --- Update ---
@router.put("/{call_id}", response_model=CallLogRead)
def update_call_log(call_id: str, call_log_update: CallLogUpdate, db: Session = Depends(get_db)):
    call_log = db.query(CallLog).filter(CallLog.call_id == call_id).first()
    if not call_log:
        raise HTTPException(status_code=404, detail="Call log not found")

    for var, value in call_log_update.dict(exclude_unset=True).items():
        setattr(call_log, var, value)
    
    try:
        db.commit()
        db.refresh(call_log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update: {e}")
    
    return call_log

# --- Delete ---
@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_call_log(call_id: str, db: Session = Depends(get_db)):
    call_log = db.query(CallLog).filter(CallLog.call_id == call_id).first()
    if not call_log:
        raise HTTPException(status_code=404, detail="Call log not found")
    try:
        db.delete(call_log)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete: {e}")
    return
