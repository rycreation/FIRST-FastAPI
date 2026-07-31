from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/", response_model=schemas.AttendanceResponse)
def mark_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    student = db.query(models.Student).filter(models.Student.id == attendance.student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing = db.query(models.Attendance).filter(
        models.Attendance.student_id == attendance.student_id,
        models.Attendance.date == attendance.date).first()

    if existing:
        raise HTTPException( status_code=400,detail="Attendance already marked for this date")

    new_attendance = models.Attendance(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance



@router.get("/", response_model=list[schemas.AttendanceResponse])
def get_attendance(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return db.query(models.Attendance).all()


@router.get("/{attendance_id}", response_model=schemas.AttendanceResponse)
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()

    if not attendance:
        raise HTTPException( status_code=404,detail="Attendance record not found")

    return attendance



@router.put("/{attendance_id}", response_model=schemas.AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: schemas.AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    db_attendance = db.query(models.Attendance).filter( models.Attendance.id == attendance_id).first()

    if not db_attendance:
        raise HTTPException(status_code=404,detail="Attendance record not found")

    update_data = attendance.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_attendance, key, value)

    db.commit()
    db.refresh(db_attendance)

    return db_attendance


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()

    if not attendance:
        raise HTTPException(status_code=404,detail="Attendance record not found")

    db.delete(attendance)
    db.commit()

    return "Attendance deleted successfully"
