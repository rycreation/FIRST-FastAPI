from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)




@router.get("/count")
def employee_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    total = db.query( models.Employee).count()

    return {"total_employees": total}



@router.post("/",response_model=schemas.EmployeeResponse)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_employee = models.Employee(**employee.model_dump())

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.get( "/",response_model=list[schemas.EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    role_id: Optional[int] = None,
    status: Optional[bool] = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(models.Employee)

    if search:
        query = query.filter(models.Employee.first_name.contains(search))

    if department_id:
        query = query.filter(models.Employee.department_id == department_id)

    if role_id:
        query = query.filter(models.Employee.role_id == role_id)

    if status is not None:
        query = query.filter(models.Employee.status == status)

    employees = query.offset((page - 1) * limit).limit(limit).all()

    return employees


@router.get( "/{employee_id}",response_model=schemas.EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    employee = db.query(models.Employee ).filter( models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException( status_code=404, detail="Employee not found" )

    return employee

@router.put( "/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: int,
    updated_employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    employee_query = db.query( models.Employee).filter(models.Employee.id == employee_id)

    employee = employee_query.first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_query.update(
        updated_employee.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return employee_query.first()


@router.delete( "/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    employee_query = db.query( models.Employee).filter(models.Employee.id == employee_id)

    employee = employee_query.first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_query.delete(synchronize_session=False)

    db.commit()

    return  "Employee deleted successfully"




