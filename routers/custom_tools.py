from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.custom_tools import CustomTool
from schemas.custom_tools import CustomToolCreate, CustomToolRead, CustomToolUpdate
from database import get_db  # You must have a get_db dependency

import uuid

router = APIRouter(prefix="/custom_tools", tags=["Custom Tools"])

# Get all custom tools
@router.get("/", response_model=List[CustomToolRead])
def get_custom_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tools = db.query(CustomTool).offset(skip).limit(limit).all()
    return tools

# Get a custom tool by ID
@router.get("/{tool_id}", response_model=CustomToolRead)
def get_custom_tool(tool_id: str, db: Session = Depends(get_db)):
    tool = db.query(CustomTool).filter(CustomTool.custom_tool_id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Custom tool not found")
    return tool

# Create a new custom tool
@router.post("/", response_model=CustomToolRead, status_code=status.HTTP_201_CREATED)
def create_custom_tool(tool: CustomToolCreate, db: Session = Depends(get_db)):
    db_tool = CustomTool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

# Update an existing custom tool
@router.put("/{tool_id}", response_model=CustomToolRead)
def update_custom_tool(tool_id: str, tool_update: CustomToolUpdate, db: Session = Depends(get_db)):
    db_tool = db.query(CustomTool).filter(CustomTool.custom_tool_id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Custom tool not found")

    for field, value in tool_update.dict(exclude_unset=True).items():
        setattr(db_tool, field, value)

    db.commit()
    db.refresh(db_tool)
    return db_tool

# Delete a custom tool
@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_custom_tool(tool_id: str, db: Session = Depends(get_db)):
    db_tool = db.query(CustomTool).filter(CustomTool.custom_tool_id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Custom tool not found")

    db.delete(db_tool)
    db.commit()
