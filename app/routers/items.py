from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import Item
from app.database import get_database
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

@router.post("/", response_model=Item)
async def create_item(item_data: ItemCreate):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    item_dict = item_data.model_dump()
    item_dict["created_at"] = datetime.utcnow()
    item_dict["updated_at"] = datetime.utcnow()
    
    result = db.items.insert_one(item_dict)
    item_dict["_id"] = str(result.inserted_id)
    
    return Item(**item_dict)

@router.get("/", response_model=List[Item])
async def get_items():
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    items = list(db.items.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return [Item(**item) for item in items]

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: str):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        item = db.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item["_id"] = str(item["_id"])
        return Item(**item)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: str, item_data: ItemUpdate):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        update_data = item_data.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            result = db.items.update_one(
                {"_id": ObjectId(item_id)}, 
                {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Item not found")
        
        item = db.items.find_one({"_id": ObjectId(item_id)})
        item["_id"] = str(item["_id"])
        return Item(**item)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    db = get_database()
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        result = db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")