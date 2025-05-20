from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.call_records import CallRecord
from schemas.call_records import CallRecordCreate, CallRecordRead, CallRecordUpdate

router = APIRouter(
    prefix="/call_records",
    tags=["Call Records"]
)

# Create a new call record
@router.post("/", response_model=CallRecordRead)
def create_call_record(data: CallRecordCreate, db: Session = Depends(get_db)):
    db_record = CallRecord(**data.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# Get a call record by ID
@router.get("/{call_record_id}", response_model=CallRecordRead)
def get_call_record(call_record_id: str, db: Session = Depends(get_db)):
    db_record = db.query(CallRecord).filter(CallRecord.call_record_id == call_record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Call record not found")
    return db_record

# Get all call records
@router.get("/", response_model=List[CallRecordRead])
def get_all_call_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CallRecord).offset(skip).limit(limit).all()

# Update a call record
@router.put("/{call_record_id}", response_model=CallRecordRead)
def update_call_record(call_record_id: str, update_data: CallRecordUpdate, db: Session = Depends(get_db)):
    db_record = db.query(CallRecord).filter(CallRecord.call_record_id == call_record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Call record not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record

# Delete a call record
@router.delete("/{call_record_id}", response_model=CallRecordRead)
def delete_call_record(call_record_id: str, db: Session = Depends(get_db)):
    db_record = db.query(CallRecord).filter(CallRecord.call_record_id == call_record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Call record not found")
    db.delete(db_record)
    db.commit()
    return db_record
