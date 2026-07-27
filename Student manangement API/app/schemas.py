from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional



class UserLogin(BaseModel):
    email: EmailStr
    password: str

#User Schemas
class UserBase(BaseModel):
    username: str
    email:EmailStr

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id:int

    class Config:
        from_attributes=True



#Student Schemas

class StudentBase(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    phone:Optional[str]=None
    age:Optional[int]=None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = None


class StudentResponse(StudentBase):
    id:int

    class Config:
        from_attributes=True


#Course schemas

class CourseBase(BaseModel):
    course_name: str
    course_code: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_name:Optional[str]=None
    course_code:Optional[str]=None


class CourseResponse(CourseBase):
    id:int

    class Config:
        from_attributes=True


#enrollment schemas

class EnrollmentBase(BaseModel):
    student_id: int
    course_id:int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
         from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: str


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    date: Optional[date] = None
    status: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

