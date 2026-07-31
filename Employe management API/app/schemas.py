from pydantic import BaseModel, EmailStr
from datetime import date


class CreateUser(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class DepartmentBase(BaseModel):
    name:str

class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes=True


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    salary: float
    hire_date: date
    status: bool = True
    department_id: int
    role_id: int


class EmployeeCreate(EmployeeBase):
    pass



class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    salary: float | None = None
    hire_date: date | None = None
    status: bool | None = None
    department_id: int | None = None
    role_id: int | None = None


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str