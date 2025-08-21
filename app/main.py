import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import items, users
from app.database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Sample FastAPI App", version="1.0.0", lifespan=lifespan)

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Sample FastAPI App"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)