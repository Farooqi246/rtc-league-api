from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from models.phone_numbers import PhoneNumber
from schemas.phone_numbers import PhoneNumberCreate, PhoneNumberUpdate, PhoneNumberOut
from database import get_db  # Adjust the import based on your project structure

router = APIRouter(prefix="/phone_numbers", tags=["Phone Numbers"])

# Create phone number
@router.post("/", response_model=PhoneNumberOut, status_code=status.HTTP_201_CREATED)
def create_phone_number(phone_number: PhoneNumberCreate, db: Session = Depends(get_db)):
    db_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == phone_number.phone_number).first()
    if db_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    new_phone = PhoneNumber(**phone_number.dict())
    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)
    return new_phone

# Get all phone numbers
@router.get("/", response_model=List[PhoneNumberOut])
def get_all_phone_numbers(db: Session = Depends(get_db)):
    return db.query(PhoneNumber).all()

# Get a phone number by ID
@router.get("/{phone_number}", response_model=PhoneNumberOut)
def get_phone_number(phone_number: str, db: Session = Depends(get_db)):
    db_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == phone_number).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return db_phone

# Update phone number
@router.put("/{phone_number}", response_model=PhoneNumberOut)
def update_phone_number(phone_number: str, update_data: PhoneNumberUpdate, db: Session = Depends(get_db)):
    db_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == phone_number).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone number not found")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_phone, key, value)
    
    db.commit()
    db.refresh(db_phone)
    return db_phone

# Delete phone number
@router.delete("/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phone_number(phone_number: str, db: Session = Depends(get_db)):
    db_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == phone_number).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone number not found")
    
    db.delete(db_phone)
    db.commit()
    return None
