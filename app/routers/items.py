from fastapi import APIRouter
from typing import Optional

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_items():
    return [{"item_id": 1, "name": "Item 1"}, {"item_id": 2, "name": "Item 2"}]


@router.get("/{item_id}")
async def get_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@router.post("/")
async def create_item(name: str):
    return {"message": f"Item '{name}' created successfully"}