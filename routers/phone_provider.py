from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.phone_provider import PhoneProvider  # SQLAlchemy model
from schemas.phone_provider import (
    PhoneProviderCreate,
    PhoneProviderUpdate,
    PhoneProviderResponse,
)
from database import get_db  # Your database session dependency

router = APIRouter(
    prefix="/phone_providers",
    tags=["Phone Providers"]
)

# CREATE
@router.post("/", response_model=PhoneProviderResponse, status_code=status.HTTP_201_CREATED)
def create_phone_provider(provider: PhoneProviderCreate, db: Session = Depends(get_db)):
    db_provider = db.query(PhoneProvider).filter_by(phone_provider_id=provider.phone_provider_id).first()
    if db_provider:
        raise HTTPException(status_code=400, detail="Phone Provider with this ID already exists.")
    
    new_provider = PhoneProvider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

# READ ALL
@router.get("/", response_model=List[PhoneProviderResponse])
def get_all_phone_providers(db: Session = Depends(get_db)):
    return db.query(PhoneProvider).all()

# READ ONE
@router.get("/{phone_provider_id}", response_model=PhoneProviderResponse)
def get_phone_provider(phone_provider_id: str, db: Session = Depends(get_db)):
    provider = db.query(PhoneProvider).filter_by(phone_provider_id=phone_provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Phone Provider not found")
    return provider

# UPDATE
@router.put("/{phone_provider_id}", response_model=PhoneProviderResponse)
def update_phone_provider(phone_provider_id: str, update_data: PhoneProviderUpdate, db: Session = Depends(get_db)):
    provider = db.query(PhoneProvider).filter_by(phone_provider_id=phone_provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Phone Provider not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

# DELETE
@router.delete("/{phone_provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phone_provider(phone_provider_id: str, db: Session = Depends(get_db)):
    provider = db.query(PhoneProvider).filter_by(phone_provider_id=phone_provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Phone Provider not found")

    db.delete(provider)
    db.commit()
    return None
