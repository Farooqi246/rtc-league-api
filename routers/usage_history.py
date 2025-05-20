from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.usage_history import UsageHistory
from schemas.usageHistory import UsageHistoryCreate, UsageHistoryRead, UsageHistoryUpdate

router = APIRouter(
    prefix="/usage_history",
    tags=["Usage History"]
)

# Create a new usage history entry
@router.post("/", response_model=UsageHistoryRead)
def create_usage_history(data: UsageHistoryCreate, db: Session = Depends(get_db)):
    db_usage = UsageHistory(**data.dict())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage

# Get a usage history by ID
@router.get("/{usage_id}", response_model=UsageHistoryRead)
def get_usage_history(usage_id: str, db: Session = Depends(get_db)):
    db_usage = db.query(UsageHistory).filter(UsageHistory.usage_id == usage_id).first()
    if not db_usage:
        raise HTTPException(status_code=404, detail="Usage history not found")
    return db_usage

# Get all usage histories
@router.get("/", response_model=List[UsageHistoryRead])
def get_all_usage_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(UsageHistory).offset(skip).limit(limit).all()

# Update a usage history
@router.put("/{usage_id}", response_model=UsageHistoryRead)
def update_usage_history(usage_id: str, update_data: UsageHistoryUpdate, db: Session = Depends(get_db)):
    db_usage = db.query(UsageHistory).filter(UsageHistory.usage_id == usage_id).first()
    if not db_usage:
        raise HTTPException(status_code=404, detail="Usage history not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_usage, key, value)
    db.commit()
    db.refresh(db_usage)
    return db_usage

# Delete a usage history
@router.delete("/{usage_id}", response_model=UsageHistoryRead)
def delete_usage_history(usage_id: str, db: Session = Depends(get_db)):
    db_usage = db.query(UsageHistory).filter(UsageHistory.usage_id == usage_id).first()
    if not db_usage:
        raise HTTPException(status_code=404, detail="Usage history not found")
    db.delete(db_usage)
    db.commit()
    return db_usage
