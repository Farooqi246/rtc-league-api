from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from passlib.context import CryptContext

import models.users
import schemas.users
from database import get_db
from auth import get_current_active_user, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_user_by_email(db: Session, email: str):
    return db.query(models.users.User).filter(models.users.User.email == email).first()

def get_user(db: Session, user_id: str):
    return db.query(models.users.User).filter(models.users.User.user_id == user_id).first()

@router.post("/", response_model=schemas.users.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.users.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)

    db_user = models.users.User(
        user_id=str(uuid.uuid4()),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=schemas.users.User)
async def read_users_me(current_user: models.users.User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[schemas.users.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.users.User = Depends(get_current_active_user)
):
    users = db.query(models.users.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.users.User)
def read_user(
    user_id: str, 
    db: Session = Depends(get_db),
    current_user: models.users.User = Depends(get_current_active_user)
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.users.User)
def update_user(
    user_id: str, 
    user_update: schemas.users.UserBase, 
    db: Session = Depends(get_db),
    current_user: models.users.User = Depends(get_current_active_user)
):
    # Check if the user exists
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Don't allow updating email if it's already taken by another user
    if user_update.email and user_update.email != db_user.email:
        existing_user = get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=schemas.users.User)
def delete_user(
    user_id: str, 
    db: Session = Depends(get_db),
    current_user: models.users.User = Depends(get_current_active_user)
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user