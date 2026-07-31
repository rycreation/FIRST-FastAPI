from fastapi import FastAPI
from app.database import engine
from app import models
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, student,course,enrollment,attendance


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Student Management API")


app.include_router(auth.router,prefix="/api/v1")
app.include_router(student.router,prefix="/api/v1") 
app.include_router(course.router,prefix="/api/v1")
app.include_router(enrollment.router,prefix="/api/v1")
app.include_router(attendance.router,prefix="/api/v1")

@app.get("/")
def home():
    return{
        "Student Management APi Runinng Successfully"
    }
