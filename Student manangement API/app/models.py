from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


#---------User Table-----

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100), unique=True,nullable=True)
    email=Column(String(150),unique=True,nullable=False)
    password=Column(String(255),nullable=False)

#--------Student Table------
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String(100),nullable=False)
    last_name=Column(String(100), nullable=False)
    email=Column(String(150),unique=True,nullable=False)
    phone=Column(String(20))
    age=Column(Integer)
    enrollments = relationship(
    "Enrollment",    # ✅ Correct
    back_populates="student",
    cascade="all, delete"
)
    attendance = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete"
    )


#=--------course Table------
class Course(Base):
    __tablename__="courses"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), nullable=False)
    course_code = Column(String(20), unique=True)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete"
    )
   
# Enrollment Table

class Enrollment(Base):
    __tablename__="enrollments"
    id=Column(Integer,primary_key=True)
    student_id=Column(Integer,ForeignKey("students.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))
    student=relationship("Student",back_populates="enrollments")
    course=relationship("Course",back_populates="enrollments")

# Attendance Table

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    status = Column(String(20))

    student = relationship(
        "Student",
        back_populates="attendance"
    )