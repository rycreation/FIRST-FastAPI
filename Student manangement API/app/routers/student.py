from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc

from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

#create Student
@router.post("/",response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db:Session=Depends(get_db),
    current_user: models.User=Depends(get_current_user)
):
    existing_student = db.query(models.Student).filter(
        models.Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student email already exists"
        )

    new_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        phone=student.phone,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

from fastapi import Query
from sqlalchemy import or_, asc, desc


# Get All Students

@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    age: int | None = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Student)

    # Search
    if search:
        query = query.filter(
            or_(
                models.Student.first_name.ilike(f"%{search}%"),
                models.Student.last_name.ilike(f"%{search}%"),
                models.Student.email.ilike(f"%{search}%")
            )
        )

    # Filter
    if age:
        query = query.filter(
            models.Student.age == age
        )

    # Sorting
    allowed_fields = {
        "id": models.Student.id,
        "first_name": models.Student.first_name,
        "last_name": models.Student.last_name,
        "age": models.Student.age,
        "email": models.Student.email
    }

    sort_column = allowed_fields.get(sort_by, models.Student.id)

    if order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    students = query.offset(skip).limit(limit).all()

    return students


# Get Student By ID
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# Update Student
@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student


# Delete Student=>
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return  "Student deleted successfully"
    