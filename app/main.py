import uvicorn
from fastapi import FastAPI
from app.routers import items, users

app = FastAPI(title="Sample FastAPI App", version="1.0.0")

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Sample FastAPI App"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)