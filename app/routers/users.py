from fastapi import APIRouter, HTTPException
from typing import List
from app.models import User
from app.database import get_database
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class UserCreate(BaseModel):
    name: str
    email: str
    age: int = None

class UserUpdate(BaseModel):
    name: str = None
    email: str = None
    age: int = None

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    user_dict = user_data.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    
    result = db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    
    return User(**user_dict)

@router.get("/", response_model=List[User])
async def get_users():
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    users = list(db.users.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return [User(**user) for user in users]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return User(**user)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_data: UserUpdate):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        update_data = user_data.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            result = db.users.update_one(
                {"_id": ObjectId(user_id)}, 
                {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="User not found")
        
        user = db.users.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return User(**user)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")