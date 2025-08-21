from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_users():
    return [{"user_id": 1, "username": "user1"}, {"user_id": 2, "username": "user2"}]


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "username": f"user{user_id}"}


@router.post("/")
async def create_user(username: str):
    return {"message": f"User '{username}' created successfully"}