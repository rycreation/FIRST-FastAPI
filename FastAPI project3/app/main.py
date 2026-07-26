from fastapi import FastAPI

# Import models so SQLAlchemy registers the tables

from app import models
from app.database import Base, engine

#  routers

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.todo import router as todo_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Project03 Todo API",
    description="A complete FastAPI project with JWT Authentication and Todo CRUD",
    version="1.0.0",
)

# Root endpoint

@app.get("/")
def home():
    return {
        "message": "Welcome to FastAPI Todo API 🚀"
    }

# Register routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)