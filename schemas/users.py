from pydantic import BaseModel

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: str
    # is_active: bool

    class Config:
        orm_mode = True 