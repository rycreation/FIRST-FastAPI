from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.get("/department-summary")
def department_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    departments = db.query(models.Department).all()

    result = []

    for dept in departments:
        result.append({"department": dept.name,"employees": len(dept.employees)})

    return result


@router.get("/",response_model=list[schemas.DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db)
):

    return db.query( models.Department).all()


@router.post("/",response_model=schemas.DepartmentResponse)
def create_department(department:schemas.DepartmentCreate,
                      db:Session=Depends(get_db),
                      current_user=Depends(get_current_user)):

    existing_department=db.query(models.Department).filter(models.Department.name==department.name).first()

    if existing_department:
        raise HTTPException(status_code=400,detail="Department already exists")

    new_department=models.Department(name=department.name)

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


@router.get("/{department_id}",response_model=schemas.DepartmentResponse)
def get_department(
    department_id:int,
    db:Session=Depends(get_db)
):
    department=db.query(models.Department).filter(models.Department.id==department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")

    return department

@router.put(
    "/{department_id}",
    response_model=schemas.DepartmentResponse
)
def update_department(
    department_id: int,
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    dept_query = db.query(models.Department).filter(models.Department.id == department_id)

    dept = dept_query.first()

    if not dept:
        raise HTTPException(status_code=404,detail="Department not found")

    dept_query.update({"name": department.name},synchronize_session=False)

    db.commit()

    return dept_query.first()


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    dept_query = db.query(models.Department).filter(models.Department.id == department_id)

    dept = dept_query.first()

    if not dept:
        raise HTTPException( status_code=404,detail="Department not found" )

    dept_query.delete( synchronize_session=False)

    db.commit()

    return  "Department deleted successfully"

