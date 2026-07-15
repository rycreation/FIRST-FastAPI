from fastapi import FastAPI,HTTPException,Query, Path,status
from model import Student
from datetime import datetime
from StudentRequest import Srequest
from studentResponse import studentResponse



app = FastAPI()


STUDENTS =[
    Student(1,"Tony", 42, "Python", True),
    Student(2,"Peter", 24, "nova", False),
    Student(3,"Steve", 89, "c+", True),
    Student(4,"Thor", 155, "Nothing", False),
    Student(5,"Bruse", 45, "java", True),
]

@app.get("/students/all",response_model=list[studentResponse])
async def get_all():
    return STUDENTS


@app.get("/students/get", response_model=list[studentResponse])
async def get_by_age(age:int=Query(ge=1,le=100)):
    result=[]
    for student in STUDENTS:
        if student.age== age:
          result.append(student)
    return result




def get_student_id(student):
    if len(STUDENTS)==0:
        student.id=1
    else:
        student.id=STUDENTS[-1].id+1
    return student

@app.post("/student/create",response_model=studentResponse,status_code=status.HTTP_201_CREATED)
async def create_student(student:Srequest):
    t = Student(**student.dict())
    STUDENTS.append(get_student_id(t))
    return t


@app.put("/studens/update", response_model=studentResponse,status_code=status.HTTP_201_CREATED)
async def update_student(student:Srequest):
    t= Student(**student.dict())
    not_found=True
    for index in range(len(STUDENTS)):
        if STUDENTS[index].id==t.id:
            STUDENTS[index]=t
            return t
        
    if not_found== True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")

@app.delete("/students/remove/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id:int = Path(get=1)):
    not_found = True
    for index in range(len(STUDENTS)):
        if STUDENTS[index].id == id:
            STUDENTS.pop(index)
            return 
    if not_found== True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")   
     