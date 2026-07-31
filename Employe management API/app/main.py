from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth, employee,department,role

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")

app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(role.router)

@app.get("/")
def home():
    return "Employee Management API is running"
