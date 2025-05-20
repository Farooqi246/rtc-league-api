from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db  # Assuming you have a get_db dependency
from models.attendeeDetails import AttendeeDetail
from schemas.attendeeDetails import AttendeeDetailCreate, AttendeeDetailUpdate, AttendeeDetailResponse

router = APIRouter(
    prefix="/attendee_details",
    tags=["Attendee Details"]
)

# Create Attendee Detail
@router.post("/", response_model=AttendeeDetailResponse, status_code=status.HTTP_201_CREATED)
def create_attendee_detail(attendee: AttendeeDetailCreate, db: Session = Depends(get_db)):
    db_attendee = db.query(AttendeeDetail).filter(
        AttendeeDetail.user_id == attendee.user_id,
        AttendeeDetail.call_id == attendee.call_id
    ).first()
    if db_attendee:
        raise HTTPException(status_code=400, detail="Attendee detail already exists for this user and call.")

    new_attendee = AttendeeDetail(**attendee.dict())
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee


@router.get("/", response_model=list[AttendeeDetailResponse])
def get_all_attendee_details(db: Session = Depends(get_db)):
    attendees = db.query(AttendeeDetail).all()
    return attendees

# Get Attendee Detail by user_id and call_id
@router.get("/{user_id}/{call_id}", response_model=AttendeeDetailResponse)
def get_attendee_detail(user_id: str, call_id: str, db: Session = Depends(get_db)):
    attendee = db.query(AttendeeDetail).filter(
        AttendeeDetail.user_id == user_id,
        AttendeeDetail.call_id == call_id
    ).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee detail not found.")
    return attendee

# Update Attendee Detail
@router.put("/{user_id}/{call_id}", response_model=AttendeeDetailResponse)
def update_attendee_detail(user_id: str, call_id: str, updates: AttendeeDetailUpdate, db: Session = Depends(get_db)):
    attendee = db.query(AttendeeDetail).filter(
        AttendeeDetail.user_id == user_id,
        AttendeeDetail.call_id == call_id
    ).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee detail not found.")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(attendee, key, value)

    db.commit()
    db.refresh(attendee)
    return attendee

# Delete Attendee Detail
@router.delete("/{user_id}/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendee_detail(user_id: str, call_id: str, db: Session = Depends(get_db)):
    attendee = db.query(AttendeeDetail).filter(
        AttendeeDetail.user_id == user_id,
        AttendeeDetail.call_id == call_id
    ).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee detail not found.")
    
    db.delete(attendee)
    db.commit()
    return
