from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
# Assuming you have routers for all entities created in the 'routers' directory
from database import create_db_tables, get_db
# Import the users router
from routers import users, phone_numbers,phone_provider, agents, callLog, attendeeDetails, billingDetails, usage_history, call_records, conversation_router, custom_tools, knowledgeBase
from auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user
)
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

class TokenRequest(BaseModel):
    email: EmailStr
    password: str

# Get environment variables
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(
    title="RTC League API",
    description="API for managing RTC League data entities",
    version="0.1.0",
    docs_url="/docs",  # Always enable Swagger
    redoc_url="/redoc",  # Always enable ReDoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
# @app.on_event("startup")
# async def startup_event():
#     create_db_tables()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RTC League API"}

@app.post("/token")
async def login_for_access_token(
    request: TokenRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(request.email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Include users router without authentication for user creation
app.include_router(users.router)

# Include all other routers with authentication
app.include_router(agents.router, dependencies=[Depends(get_current_active_user)])
app.include_router(callLog.router, dependencies=[Depends(get_current_active_user)])
app.include_router(attendeeDetails.router, dependencies=[Depends(get_current_active_user)])
app.include_router(billingDetails.router, dependencies=[Depends(get_current_active_user)])
app.include_router(usage_history.router, dependencies=[Depends(get_current_active_user)])
app.include_router(call_records.router, dependencies=[Depends(get_current_active_user)])
app.include_router(conversation_router.router, dependencies=[Depends(get_current_active_user)])
app.include_router(custom_tools.router, dependencies=[Depends(get_current_active_user)])
app.include_router(knowledgeBase.router, dependencies=[Depends(get_current_active_user)])
app.include_router(phone_numbers.router, dependencies=[Depends(get_current_active_user)])
app.include_router(phone_provider.router, dependencies=[Depends(get_current_active_user)])

# WSGI entrypoint for PythonAnywhere
from uvicorn.middleware.wsgi import WSGIMiddleware
application = WSGIMiddleware(app)
