from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from models.billingDetails import BillingDetails
from database import get_db  # You need to create this get_db function using sessionmaker
from schemas.billingDetails import BillingDetailsCreate, BillingDetailsUpdate, BillingDetailsOut
import uuid

router = APIRouter(
    prefix="/billing",
    tags=["billing"],   
)

# --------------------------
# CREATE billing detail
# --------------------------
@router.post("/", response_model=BillingDetailsOut, status_code=status.HTTP_201_CREATED)
def create_billing_detail(billing: BillingDetailsCreate, db: Session = Depends(get_db)):
    # Ensure billing_id is set (it will be from schema default_factory)
    new_billing = BillingDetails(
        billing_id=billing.billing_id,
        user_id=billing.user_id,
        address_line1=billing.address_line1,
        city=billing.city,
        country=billing.country,
        state=billing.state,
        zip_code=billing.zip_code,
        card_holder_name=billing.card_holder_name,
        card_number_masked=billing.card_number_masked,
        expiry_date=billing.expiry_date,
        current_plan=billing.current_plan,
        minutes_used=billing.minutes_used,
    )
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)
    return new_billing


# --------------------------
# GET billing detail by ID
# --------------------------
@router.get("/{billing_id}", response_model=BillingDetailsOut)
def get_billing_detail(billing_id: str, db: Session = Depends(get_db)):
    billing = db.query(BillingDetails).filter(BillingDetails.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing detail not found")
    return billing


# --------------------------
# UPDATE billing detail
# --------------------------
@router.put("/{billing_id}", response_model=BillingDetailsOut)
def update_billing_detail(billing_id: str, billing_update: BillingDetailsUpdate, db: Session = Depends(get_db)):
    billing = db.query(BillingDetails).filter(BillingDetails.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing detail not found")

    # Update only provided fields
    update_data = billing_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(billing, key, value)

    db.commit()
    db.refresh(billing)
    return billing


# --------------------------
# DELETE billing detail
# --------------------------
@router.delete("/{billing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_billing_detail(billing_id: str, db: Session = Depends(get_db)):
    billing = db.query(BillingDetails).filter(BillingDetails.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing detail not found")

    db.delete(billing)
    db.commit()
    return

from typing import List

# --------------------------
# GET all billing details
# --------------------------
@router.get("/", response_model=List[BillingDetailsOut])
def get_all_billing_details(db: Session = Depends(get_db)):
    billings = db.query(BillingDetails).all()
    return billings
